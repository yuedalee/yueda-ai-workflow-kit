# 本地商品内容与发货工作台｜顶层设计

> Status：Design Draft v0.1  
> Repo：`yueda-ai-workflow-kit`  
> 适用对象：一人公司、软件/插件卖家、虚拟商品卖家、内容型电商卖家  
> 核心目标：用最低成本，把商品内容生产、教程视频处理、发货话术与发货记录做成一个可复用的本地工作台。

---

## 1. 一句话结论

这个系统不是“全自动电商机器人”，也不是“AI Agent 大杂烩”。

它应该被设计成：

```text
本地商品资料库
→ 商品图/详情页模板化生成
→ 教程视频半自动成片
→ 发货内容半自动生成
→ 人工确认后复制/上传/发送
→ 自动记录日志，防漏发、防重复发货
```

核心判断：

> 先做“本地确定性生产线”，再做“平台自动化”；先做“半自动可控”，再做“全自动”；先做“能直接交付文件”，再谈 Agent 和工作流。

---

## 2. 为什么不直接做大而全自动化？

当前最大风险不是“做不出来”，而是：

```text
功能看起来很多
但输出文件不能直接用
平台自动化不稳定
错误无法追踪
依赖第三方订阅
最终维护成本高于人工成本
```

所以 V1 必须坚持四个边界：

1. **本地优先**：核心流程必须在本地可运行，不把 SaaS 订阅作为必需条件。
2. **标准文件输出**：最终必须输出 PNG、MP4、HTML、TXT、CSV、SQLite 记录，而不是只在界面里看起来完成。
3. **人工确认**：涉及发布商品、发送买家消息、发货、改价、售后承诺的动作，V1 不做全自动执行。
4. **可验收**：每个模块都必须有输入、输出、日志和失败提示。

---

## 3. V1 系统范围

V1 只做三条生产线。

### 3.1 商品图与详情页生产线

输入：

```text
product.yaml
logo.png
商品图 / 软件截图 / 插件截图
卖点文案
平台尺寸要求
```

输出：

```text
output/images/main_800x800_01.png
output/images/main_800x800_02.png
output/images/carousel_01.png
output/images/carousel_02.png
output/images/carousel_03.png
output/detail/detail.html
output/detail/detail_750_long.png
output/video/cover_9x16.png
```

第一阶段不要追求 AI 神图，而是先做稳定模板：

```text
产品图 / 软件截图
+ 大标题
+ 副标题
+ 3 个核心卖点
+ 服务承诺
+ 售后说明
+ 平台尺寸输出
```

---

### 3.2 教程视频半自动成片生产线

输入：

```text
录屏视频
product.yaml
logo.png
封面标题
片头 / 片尾模板
```

输出：

```text
output/video/tutorial_16x9.mp4
output/video/tutorial_9x16.mp4
output/video/subtitle.srt
output/video/cover.png
```

V1 不追求复杂动画。核心是：

1. 自动剪掉明显静音和长停顿；
2. 自动生成字幕文件；
3. 可烧录字幕；
4. 输出横版和竖版；
5. 自动生成封面；
6. 允许人工修改字幕后重新渲染。

---

### 3.3 半自动发货生产线

输入：

```text
从拼多多 / 淘宝 / 闲鱼复制出来的订单文本
商品资料
卡密池 / 激活码 / 下载链接 / 教程链接
```

输出：

```text
output/delivery/message.txt
output/delivery/install_guide.txt
output/delivery/faq.txt
SQLite 发货记录
CSV 发货记录
```

V1 不自动登录平台、不自动绕过验证码、不自动私信买家。它只做：

```text
粘贴订单文本
→ 自动识别订单号、买家、商品、规格
→ 匹配 SKU
→ 取出一条可用卡密或发货内容
→ 生成发货话术
→ 人工一键复制发送
→ 自动记录发货日志
→ 重复订单提醒
```

---

## 4. V1 不做什么

以下内容不进入 V1：

```text
自动登录拼多多 / 淘宝 / 闲鱼
绕过验证码、风控、滑块、短信验证
自动发布商品
自动改价
自动批量私信
自动催评
刷单、刷评、刷曝光
必须付费 API 才能跑通的功能
复杂多 Agent 编排
n8n / Dify / Chatwoot 作为必需依赖
ComfyUI 作为商品主图第一核心
```

这些不是永远不能做，而是不能作为第一阶段主线。

---

## 5. 推荐技术栈

最低成本 V1：

```text
Python
SQLite
YAML
Jinja2
FastAPI 或 Streamlit
Pillow
Playwright
FFmpeg
auto-editor
faster-whisper
rembg（可选）
```

原则：

1. 能本地跑；
2. 免费或开源；
3. 输出标准文件；
4. 不绑定特定平台账号；
5. 容易被 Codex 分阶段实现；
6. 出错可以查日志。

---

## 6. 标准目录结构

建议最终项目结构：

```text
local-commerce-workbench/
├── README.md
├── pyproject.toml
├── data/
│   ├── app.db
│   ├── card_pool.csv
│   └── delivery_logs.csv
├── products/
│   └── demo-plugin-001/
│       ├── product.yaml
│       ├── raw/
│       │   ├── logo.png
│       │   ├── product.png
│       │   ├── recording.mp4
│       │   └── screenshots/
│       └── output/
│           ├── images/
│           ├── detail/
│           ├── video/
│           └── delivery/
├── templates/
│   ├── images/
│   ├── detail/
│   ├── delivery/
│   └── video/
├── src/
│   └── local_commerce_workbench/
│       ├── cli.py
│       ├── config.py
│       ├── product_schema.py
│       ├── image_generator.py
│       ├── detail_generator.py
│       ├── video_processor.py
│       ├── order_parser.py
│       ├── delivery_manager.py
│       ├── card_pool.py
│       └── ui.py
└── tests/
```

---

## 7. 商品资料标准

每个商品必须维护一个 `product.yaml`。

示例：

```yaml
id: demo-plugin-001
name: 拼多多虚拟商品半自动发货助手
platforms:
  - 拼多多
  - 淘宝
  - 闲鱼
price: 49
target_user: 卖软件、插件、教程、资料包的小商家
main_pain: 手动发货慢、容易漏发、重复发货、售后解释重复
core_value: 自动生成发货话术、记录发货状态，降低漏发和重复发货
features:
  - 订单文本复制后自动识别
  - 自动匹配商品 SKU
  - 自动生成发货话术
  - 自动记录发货日志
  - 重复订单提醒
delivery_type: 网盘链接 + 安装教程 + 激活码
assets:
  logo: raw/logo.png
  product_image: raw/product.png
  recording: raw/recording.mp4
  screenshots_dir: raw/screenshots
delivery:
  download_url: https://example.com/download
  tutorial_url: https://example.com/tutorial
  faq_url: https://example.com/faq
after_sale:
  - 安装失败怎么办
  - 链接打不开怎么办
  - 激活码无效怎么办
```

---

## 8. 质量标准

V1 是否有用，不看功能数量，只看交付质量。

必须满足：

1. 输入一个商品资料包，能生成完整输出目录；
2. 主图、轮播图、详情长图能直接上传；
3. 教程视频能生成横版和竖版；
4. 发货话术能一键复制；
5. 卡密发一个少一个；
6. 同一订单再次输入会提醒重复；
7. 每一步都有日志；
8. 出错时能看到失败原因；
9. 核心流程不依赖付费订阅；
10. 人工修改资料后可以一键重新生成。

---

## 9. 最小验收场景

准备一个 demo 商品：

```text
products/demo-plugin-001/product.yaml
products/demo-plugin-001/raw/logo.png
products/demo-plugin-001/raw/product.png
products/demo-plugin-001/raw/recording.mp4
```

运行：

```bash
python -m local_commerce_workbench validate products/demo-plugin-001
python -m local_commerce_workbench generate-images products/demo-plugin-001
python -m local_commerce_workbench generate-detail products/demo-plugin-001
python -m local_commerce_workbench process-video products/demo-plugin-001
python -m local_commerce_workbench deliver --order-text "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
```

验收：

```text
生成图片不少于 5 张
生成详情页 HTML 和 750px 长图
生成 16:9 与 9:16 视频
生成 SRT 字幕
生成发货 message.txt
delivery_logs.csv 出现订单记录
重复输入同一订单号时提示已发货
```

---

## 10. 后续扩展顺序

V1 稳定后再做：

1. 浏览器半自动填表；
2. 多平台素材尺寸适配；
3. ComfyUI 背景图生成；
4. Remotion 宣传短视频模板；
5. n8n 编排已经稳定的流程；
6. Dify / Chatwoot 做售后知识库；
7. 官方 API 对接；
8. 平台消息聚合。

扩展原则：

> 任何新功能都不能破坏 V1 的本地可用、标准文件输出、人工确认和日志追踪。

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
