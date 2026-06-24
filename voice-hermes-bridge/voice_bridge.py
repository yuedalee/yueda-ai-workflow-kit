import json
import os
import tempfile
import wave
from pathlib import Path
from typing import Optional

import deepspeech
import numpy as np
import requests
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from playsound import playsound
from TTS.api import TTS

load_dotenv()

DEEPSPEECH_MODEL = os.getenv('DEEPSPEECH_MODEL', 'models/deepspeech-0.9.3-models.pbmm')
DEEPSPEECH_SCORER = os.getenv('DEEPSPEECH_SCORER', 'models/deepspeech-0.9.3-models.scorer')
HERMES_API_URL = os.getenv('HERMES_API_URL', '').strip()
FEISHU_WEBHOOK_URL = os.getenv('FEISHU_WEBHOOK_URL', '').strip()
TTS_MODEL_NAME = os.getenv('TTS_MODEL_NAME', 'tts_models/zh-CN/baker/tacotron2-DDC-GST')
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', '5'))
SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', '16000'))


def record_wav(seconds: int = RECORD_SECONDS, sample_rate: int = SAMPLE_RATE) -> Path:
    print(f'开始录音：{seconds} 秒')
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    wav_path = output_dir / 'input.wav'

    with wave.open(str(wav_path), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    print(f'录音完成：{wav_path}')
    return wav_path


def speech_to_text(wav_path: Path) -> str:
    model_path = Path(DEEPSPEECH_MODEL)
    scorer_path = Path(DEEPSPEECH_SCORER)
    if not model_path.exists() or not scorer_path.exists():
        raise FileNotFoundError('DeepSpeech 模型文件不存在，请先运行 python download_models.py')

    model = deepspeech.Model(str(model_path))
    model.enableExternalScorer(str(scorer_path))

    audio, rate = sf.read(str(wav_path), dtype='int16')
    if rate != SAMPLE_RATE:
        raise ValueError(f'采样率必须是 {SAMPLE_RATE}，当前是 {rate}')

    if len(audio.shape) > 1:
        audio = audio[:, 0]

    text = model.stt(audio)
    return text.strip()


def ask_hermes(text: str) -> str:
    if not HERMES_API_URL:
        return ''

    payload_candidates = [
        {'message': text},
        {'text': text},
        {'query': text},
    ]

    last_error: Optional[Exception] = None
    for payload in payload_candidates:
        try:
            resp = requests.post(HERMES_API_URL, json=payload, timeout=90)
            if resp.status_code >= 400:
                continue
            data = resp.json()
            for key in ['reply', 'answer', 'text', 'message', 'content']:
                if key in data and isinstance(data[key], str):
                    return data[key]
            return json.dumps(data, ensure_ascii=False)
        except Exception as exc:
            last_error = exc

    if last_error:
        raise RuntimeError(f'Hermes API 调用失败：{last_error}')
    raise RuntimeError('Hermes API 没有返回可识别的内容')


def send_to_feishu(text: str) -> None:
    if not FEISHU_WEBHOOK_URL:
        raise RuntimeError('没有配置 FEISHU_WEBHOOK_URL')

    payload = {
        'msg_type': 'text',
        'content': {'text': text},
    }
    resp = requests.post(FEISHU_WEBHOOK_URL, json=payload, timeout=30)
    resp.raise_for_status()
    print('已发送到飞书。')


def text_to_speech(text: str) -> Path:
    if not text.strip():
        raise ValueError('没有可播报的文字')

    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    wav_path = output_dir / 'reply.wav'

    tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=False)
    tts.tts_to_file(text=text, file_path=str(wav_path))
    return wav_path


def speak(text: str) -> None:
    wav_path = text_to_speech(text)
    print(f'开始播报：{wav_path}')
    playsound(str(wav_path))


def main() -> None:
    wav_path = record_wav()
    user_text = speech_to_text(wav_path)
    print(f'识别结果：{user_text}')

    if not user_text:
        print('没有识别到有效文字。')
        return

    reply = ''
    if HERMES_API_URL:
        reply = ask_hermes(user_text)
        print(f'Hermes 回复：{reply}')
    elif FEISHU_WEBHOOK_URL:
        send_to_feishu(user_text)
        reply = '已把你的语音内容发送到飞书。注意：要自动播报 Hermes 回复，需要接入飞书事件回调。'
    else:
        reply = '没有配置 Hermes API 或飞书 webhook，无法发送。'

    speak(reply)


if __name__ == '__main__':
    main()
