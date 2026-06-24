# Voice Hermes Bridge 交接台账

## 1. 项目目标

把用户现有的 Hermes / 飞书 AI 助理改造成“类贾维斯语音交互入口”：

```text
用户直接说话
→ 本地语音识别成文字
→ 自动发送给 Hermes / 飞书机器人
→ 获取 Hermes 的文字回复
→ 本地文字转语音
→ 扬声器播报
```

目标不是重做 Hermes，而是在 Hermes 外面加一层本地语音桥。

---

## 2. 当前仓库位置

仓库：`yuedalee/yueda-ai-workflow-kit`

当前新增目录：

```text
voice-hermes-bridge/
  README.md
  HANDOFF.md
  requirements.txt
  .env.example
  .gitignore
  download_models.py
  voice_bridge.py
```

---

## 3. 当前已完成内容

### 3.1 已写入仓库的功能骨架

已经完成：

1. DeepSpeech 语音转文字骨架。
2. Coqui TTS 文字转语音骨架。
3. DeepSpeech 模型下载脚本。
4. `.env.example` 配置模板。
5. `voice_bridge.py` 主程序骨架。
6. README 说明文档。

### 3.2 当前主流程

`voice_bridge.py` 当前设计流程：

```text
record_wav()
→ speech_to_text()
→ ask_hermes() 或 send_to_feishu()
→ text_to_speech()
→ speak()
```

---

## 4. 需要 Codex 重点处理的问题

### 问题 A：确认 Hermes 的真实接入方式

当前 `.env.example` 中假设 Hermes 有本地 HTTP 接口：

```env
HERMES_API_URL=http://127.0.0.1:8000/chat
```

但这只是占位地址。Codex 需要检查用户本机 Hermes 的真实接口。

需要确认：

1. Hermes 是否暴露 HTTP API？
2. 真实端口是多少？
3. 请求字段是 `message`、`text`、`query`，还是其他？
4. 返回字段是 `reply`、`answer`、`content`，还是其他？
5. 是否需要 API Key / Token？

如果 Hermes 没有 HTTP API，只能通过飞书机器人中转，则需要走问题 B。

---

### 问题 B：如果只能走飞书，需要补飞书事件回调

当前代码只能把用户语音识别结果通过飞书 webhook 发出去。

但飞书 webhook 只能“发消息”，不能自动拿到 Hermes 的回复。

要实现完整闭环，必须增加：

```text
飞书事件订阅 / 消息回调
→ 捕获 Hermes 在飞书群里的回复
→ 把回复文本交给 Coqui TTS 播报
```

Codex 需要判断当前用户的飞书机器人架构：

1. Sherry 是自建应用，还是群机器人？
2. 是否有事件订阅地址？
3. 本机是否有公网地址，还是需要内网穿透？
4. 如果没有公网地址，可考虑 Cloudflare Tunnel / frp / ngrok。

推荐优先级：

```text
优先方案：语音桥直接调用 Hermes HTTP API
备选方案：语音桥 → 飞书 webhook → 飞书事件回调 → TTS
```

---

### 问题 C：DeepSpeech 中文识别效果可能不够用

当前用户前面指定的是：

- STT：DeepSpeech
- TTS：Coqui TTS

所以本仓库按这个要求建了骨架。

但需要明确：DeepSpeech 官方模型主要是英文，中文识别效果不适合正式使用。

Codex 需要评估是否替换为更适合中文的开源 STT：

1. FunASR：更适合中文，阿里开源，中文普通话识别较稳。
2. faster-whisper：部署成熟，但中文也可用，模型较大。
3. Vosk 中文模型：轻量，但准确率一般。

建议：

```text
第一阶段：保留 DeepSpeech 骨架，跑通工程链路。
第二阶段：新增 FunASR 后端，作为中文正式方案。
```

注意：如果更换 STT，不要破坏当前 DeepSpeech 文件；建议做成可配置：

```env
STT_ENGINE=deepspeech
# 或
STT_ENGINE=funasr
```

---

### 问题 D：TTS 需要验证中文模型是否可用

当前 `.env.example` 里写的是：

```env
TTS_MODEL_NAME=tts_models/zh-CN/baker/tacotron2-DDC-GST
```

Codex 需要验证：

1. 当前 Coqui TTS 版本是否还能正常下载该中文模型。
2. Windows 环境是否能正常播放生成 wav。
3. 是否存在依赖冲突。
4. 中文发音是否自然。

如果 Coqui TTS 不稳定，可备选：

1. Edge-TTS：中文效果好，但依赖微软在线服务，不是纯离线。
2. ChatTTS：中文自然，但部署复杂度更高。
3. Piper：轻量，但中文声音资源需确认。

用户当前要求是开源优先，所以先验证 Coqui TTS。

---

## 5. 本地部署步骤草案

在 Windows 电脑上执行：

```bash
cd voice-hermes-bridge
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python download_models.py
copy .env.example .env
python voice_bridge.py
```

如果报错，优先检查：

1. Python 版本，建议 3.9 或 3.10。
2. DeepSpeech 是否支持当前 Python。
3. `sounddevice` 是否能识别麦克风。
4. 扬声器是否能播放 wav。
5. Hermes API 地址是否正确。

---

## 6. Codex 下一步执行清单

### 第一阶段：跑通最小闭环

目标：不追求完美识别，先跑通语音输入和语音输出。

- [ ] 拉取仓库最新代码。
- [ ] 进入 `voice-hermes-bridge/`。
- [ ] 创建虚拟环境。
- [ ] 安装依赖。
- [ ] 修复依赖版本冲突。
- [ ] 执行 `python download_models.py`。
- [ ] 执行 `python voice_bridge.py`。
- [ ] 确认麦克风能录音。
- [ ] 确认 STT 能输出文字。
- [ ] 确认 TTS 能生成语音。
- [ ] 确认扬声器能播报。

验收标准：

```text
用户说一句话，程序能录音、识别、生成回复文本，并播报出来。
```

即使先不用 Hermes，能完成本地“语音 → 文字 → 测试回复 → 语音”也算第一阶段通过。

---

### 第二阶段：接 Hermes

- [ ] 找到 Hermes 当前本地服务入口。
- [ ] 确认 Hermes HTTP API 路由。
- [ ] 修改 `.env` 中的 `HERMES_API_URL`。
- [ ] 调整 `ask_hermes()` 的请求字段和返回字段。
- [ ] 增加错误日志。
- [ ] 增加超时处理。
- [ ] 增加失败后的语音提示。

验收标准：

```text
用户说话 → Hermes 收到文字 → Hermes 返回结果 → 本机语音播报 Hermes 回复。
```

---

### 第三阶段：如果必须走飞书

只有在 Hermes 没有本地 HTTP API 时执行。

- [ ] 确认飞书机器人类型。
- [ ] 确认是否能配置事件订阅。
- [ ] 新建本地 FastAPI 服务作为飞书事件回调入口。
- [ ] 配置内网穿透。
- [ ] 捕获 Hermes 回复消息。
- [ ] 过滤掉用户自己发出的消息，避免自我循环。
- [ ] 将 Hermes 回复送入 TTS。

验收标准：

```text
用户说话 → 语音桥发到飞书 → Hermes 在飞书回复 → 本地收到回调 → 扬声器播报。
```

---

### 第四阶段：中文正式化

- [ ] 评估 DeepSpeech 中文识别是否可接受。
- [ ] 如果不行，新增 FunASR STT 后端。
- [ ] 增加 `STT_ENGINE` 配置项。
- [ ] 保留 DeepSpeech，不要删除。
- [ ] 增加中文唤醒词或快捷键启动录音。
- [ ] 增加连续对话模式。

建议交互形态：

```text
按住快捷键说话 → 松开后自动发送 → 自动播报
```

比 24 小时一直监听更稳定，也更保护隐私。

后续再升级为：

```text
唤醒词：Sherry / 小雪 / 助理
→ 开始录音
→ 自动交互
```

---

## 7. 风险与注意事项

### 7.1 不要把大模型文件提交进 GitHub

模型文件应放本地：

```text
voice-hermes-bridge/models/
```

不要提交：

```text
*.pbmm
*.scorer
*.pth
*.onnx
*.bin
*.safetensors
```

### 7.2 不要把密钥写进仓库

`.env` 不要提交。

飞书 webhook、Hermes Token、API Key 都只能放本地 `.env`。

### 7.3 不要一开始就做 24 小时监听

第一版优先做：

```text
手动启动 / 快捷键录音 / 固定录音 5 秒
```

24 小时监听涉及：

1. 唤醒词误触发。
2. 隐私风险。
3. 麦克风占用。
4. 长时间运行稳定性。
5. 日志和缓存清理。

等最小闭环稳定后再做。

---

## 8. 建议最终产品形态

第一版：命令行工具。

```bash
python voice_bridge.py
```

第二版：桌面托盘程序。

功能：

1. 开机自启。
2. 托盘常驻。
3. 快捷键说话。
4. 自动播报。
5. 日志窗口。
6. 一键切换 STT/TTS。

第三版：真正的家庭/办公室语音助手。

功能：

1. 唤醒词。
2. 连续对话。
3. 自动调用 Hermes 工具。
4. 接入电脑文件、日程、飞书、企业微信。
5. 本地隐私策略。
6. 失败时自动降级到文字模式。

---

## 9. 给 Codex 的执行提示词

请直接复制下面这段给 Codex：

```text
你现在接手 yuedalee/yueda-ai-workflow-kit 仓库里的 voice-hermes-bridge 项目。目标是把用户的 Hermes / 飞书 AI 助理改造成可以语音输入、语音播报的本地语音桥。

请先阅读：
1. voice-hermes-bridge/README.md
2. voice-hermes-bridge/HANDOFF.md
3. voice-hermes-bridge/voice_bridge.py
4. voice-hermes-bridge/.env.example

你的任务按阶段完成：

第一阶段：先在 Windows 本机跑通最小闭环。即使暂时不接 Hermes，也要做到：录音 → STT → 测试回复文本 → TTS → 扬声器播报。修复所有依赖、Python 版本、音频设备、播放问题。

第二阶段：检查本机 Hermes 是否有 HTTP API。如果有，确认真实接口地址、请求字段、返回字段，然后修改 voice_bridge.py 和 .env，使流程变成：用户说话 → Hermes 收到 → Hermes 回复 → 本机语音播报。

第三阶段：如果 Hermes 没有 HTTP API，只能走飞书，则补飞书事件回调方案。注意：飞书 webhook 只能发消息，不能拿回复。要自动播报 Hermes 回复，必须通过飞书事件订阅捕获 Hermes 的回复消息。

第四阶段：评估 DeepSpeech 中文识别效果。如果中文效果不可用，请新增 FunASR 作为中文 STT 后端，并通过 STT_ENGINE 配置切换。不要删除 DeepSpeech 骨架。

约束：
1. 不要把模型权重、大音频、.env、密钥提交到 GitHub。
2. 不要一开始做 24 小时监听，先做快捷键或固定时长录音。
3. 所有改动要写清楚 README。
4. 每完成一个阶段，提交一次 commit，并说明测试结果。
```

---

## 10. 当前结论

这个项目现在不是“完全完成”，而是已经完成了可交接的工程骨架。

Codex 接下来要做的是：

```text
本机调试依赖
→ 确认 Hermes 接口
→ 跑通完整闭环
→ 再优化中文识别和长期运行体验
```
