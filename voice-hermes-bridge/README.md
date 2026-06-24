# Voice Hermes Bridge

把本地语音交互接到 Hermes / 飞书机器人：

- 语音转文字：DeepSpeech
- 文字转语音：Coqui TTS
- 目标效果：你直接说话 → 本地识别成文字 → 发给 Hermes / 飞书机器人 → 收到文字回复 → 本地语音播报

> 注意：GitHub 仓库不适合直接存放大型模型权重文件。本目录提供下载脚本和运行代码，模型会下载到本地 `models/` 目录，并已通过 `.gitignore` 排除。

## 目录结构

```text
voice-hermes-bridge/
  README.md
  requirements.txt
  .env.example
  .gitignore
  download_models.py
  voice_bridge.py
```

## 安装

建议使用 Python 3.9 或 3.10。DeepSpeech 对高版本 Python 支持不稳定。

```bash
cd voice-hermes-bridge
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 下载模型

```bash
python download_models.py
```

默认会下载：

- DeepSpeech 英文模型：`deepspeech-0.9.3-models.pbmm`
- DeepSpeech scorer：`deepspeech-0.9.3-models.scorer`

中文语音识别后续建议替换为中文 STT 模型；本版先按你前面指定的 DeepSpeech + Coqui TTS 建立骨架。

## 配置

复制配置模板：

```bash
copy .env.example .env
```

然后填写：

```env
HERMES_API_URL=http://127.0.0.1:8000/chat
FEISHU_WEBHOOK_URL=
TTS_MODEL_NAME=tts_models/zh-CN/baker/tacotron2-DDC-GST
```

两种发送方式：

1. 有 Hermes 本地 HTTP 接口：优先填 `HERMES_API_URL`。
2. 只有飞书机器人入口：填 `FEISHU_WEBHOOK_URL`，把识别出的文字发到飞书群里。

## 运行

```bash
python voice_bridge.py
```

当前骨架流程：

1. 录音。
2. DeepSpeech 转文字。
3. 把文字发给 Hermes 或飞书。
4. 将返回文本用 Coqui TTS 合成语音。
5. 通过扬声器播放。

## 重要边界

- DeepSpeech 官方模型主要是英文，中文效果不理想。
- Coqui TTS 可以选中文模型，但第一次运行会自动下载模型。
- 如果 Hermes 只通过飞书群回复文字，而没有 HTTP 返回接口，就需要额外接飞书事件回调或消息监听，才能把 Hermes 的回复自动抓回来播报。
- 最稳的闭环方案是：本地语音桥直接调用 Hermes HTTP API，而不是绕飞书聊天窗口。

## 后续建议

第一版先跑通：

```text
语音输入 → STT → Hermes HTTP API → TTS → 扬声器
```

如果必须走飞书：

```text
语音输入 → STT → 飞书 webhook 发消息 → 飞书事件回调捕获 Hermes 回复 → TTS → 扬声器
```
