from pathlib import Path
from urllib.request import urlretrieve

MODEL_DIR = Path('models')
MODEL_DIR.mkdir(exist_ok=True)

FILES = [
    (
        'https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm',
        MODEL_DIR / 'deepspeech-0.9.3-models.pbmm',
    ),
    (
        'https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer',
        MODEL_DIR / 'deepspeech-0.9.3-models.scorer',
    ),
]


def download(url: str, target: Path) -> None:
    if target.exists():
        print(f'[skip] {target} already exists')
        return
    print(f'[download] {url}')
    print(f'[target] {target}')
    urlretrieve(url, target)
    print(f'[ok] {target}')


if __name__ == '__main__':
    for url, target in FILES:
        download(url, target)
    print('DeepSpeech model files are ready.')
    print('Coqui TTS model will be downloaded automatically on first run.')
