# Codex 构建任务书｜本地商品内容与发货工作台 V1

> Status：Codex Task Spec v0.1  
> 用途：把系统拆成可由 Codex 逐步实现、逐步验收的任务，防止一次性生成一个“能跑但不能用”的大杂烩。  
> 核心约束：低成本、本地运行、标准文件输出、人工确认、可测试、可追踪。

---

## 1. 总任务

请构建一个本地运行的 Python 工具：`local-commerce-workbench`。

它用于帮助一人公司或软件/插件卖家完成：

1. 商品资料标准化；
2. 商品主图、轮播图、详情页生成；
3. 教程录屏处理和字幕生成；
4. 虚拟商品/软件/插件半自动发货；
5. 发货日志和重复订单检测。

---

## 2. 不可违反的约束

### 2.1 成本约束

不得把任何付费服务作为 V1 必需依赖。

禁止默认依赖：

```text
OpenAI API
Claude API
Midjourney
Runway
CapCut API
飞书/企业微信付费能力
n8n Cloud
Dify Cloud
任何必须订阅才能跑通的 SaaS
```

### 2.2 平台风险约束

V1 不做：

```text
自动登录拼多多 / 淘宝 / 闲鱼
绕过验证码 / 滑块 / 短信验证
自动发布商品
自动发买家消息
自动改价格
自动催评
刷单刷评刷曝光
```

### 2.3 交付物约束

每个模块必须输出标准文件。

允许输出：

```text
PNG
MP4
SRT
HTML
TXT
CSV
SQLite
JSON
YAML
```

不允许只做一个看起来完成但没有可用文件的界面。

---

## 3. 推荐技术栈

```text
Python 3.11+
SQLite
YAML
Jinja2
Playwright Python
Pillow
FFmpeg
auto-editor
faster-whisper
Streamlit 或 FastAPI（后期）
pytest
```

V1 优先 CLI，界面后置。

---

## 4. 任务拆解

### Task 01：项目骨架和 CLI

#### 目标

创建可运行项目骨架。

#### 要求

1. 创建 `pyproject.toml`；
2. 创建 `src/local_commerce_workbench/`；
3. 创建 CLI 入口；
4. 支持 `--help`；
5. 添加 demo 商品目录。

#### 验收命令

```bash
python -m local_commerce_workbench --help
```

#### 完成标准

1. 命令可运行；
2. 没有依赖付费服务；
3. README 说明如何安装和运行。

---

### Task 02：商品资料 Schema、读取、校验

#### 目标

读取并校验 `product.yaml`。

#### 输入

```text
products/demo-plugin-001/product.yaml
```

#### 要求

1. 校验必填字段；
2. 校验素材路径；
3. 输出标准化 JSON；
4. 缺字段时返回清楚错误；
5. 添加单元测试。

#### 验收命令

```bash
python -m local_commerce_workbench validate products/demo-plugin-001
pytest tests/test_product_schema.py
```

#### 完成标准

1. 合格商品通过；
2. 缺字段商品失败；
3. 素材路径错误商品失败；
4. 错误信息可读。

---

### Task 03：输出目录和日志系统

#### 目标

创建稳定输出目录和日志。

#### 要求

1. 自动创建 `output/images`、`output/detail`、`output/video`、`output/delivery`；
2. 记录运行日志；
3. 记录生成文件；
4. 失败时记录错误原因。

#### 验收命令

```bash
python -m local_commerce_workbench init-output products/demo-plugin-001
```

#### 完成标准

1. 输出目录完整；
2. 日志文件存在；
3. 重复运行不会破坏已有发货记录。

---

### Task 04：商品主图和轮播图生成

#### 目标

基于模板生成平台可用商品图。

#### 要求

1. 生成至少 2 张 800x800 主图；
2. 生成至少 3 张轮播图；
3. 生成 9:16 封面图；
4. 支持中文字体；
5. 文案自动换行；
6. 图片尺寸校验。

#### 推荐实现

```text
Jinja2 HTML 模板
→ Playwright 截图
→ Pillow 尺寸校验和压缩
```

#### 验收命令

```bash
python -m local_commerce_workbench generate-images products/demo-plugin-001
```

#### 完成标准

1. 输出文件真实存在；
2. 尺寸正确；
3. 文字不溢出；
4. 产品图不变形；
5. 不依赖在线字体。

---

### Task 05：详情页 HTML 和长图生成

#### 目标

生成商品详情页 HTML 和 750px 长图。

#### 要求

1. 生成 `detail.html`；
2. 生成 `detail_750_long.png`；
3. 模块包含痛点、解决方案、功能、步骤、发货说明、FAQ；
4. 不出现空模块；
5. 支持重新生成。

#### 验收命令

```bash
python -m local_commerce_workbench generate-detail products/demo-plugin-001
```

#### 完成标准

1. HTML 能打开；
2. 长图宽度 750px；
3. 内容来自 product.yaml；
4. 没有模板占位符残留。

---

### Task 06：订单文本解析

#### 目标

从复制文本中识别订单信息。

#### 输入示例

```text
订单号：123456
买家：张三
商品：拼多多虚拟商品半自动发货助手
规格：标准版
```

#### 要求

1. 识别订单号；
2. 识别买家；
3. 识别商品名；
4. 识别规格；
5. 匹配商品 SKU；
6. 解析失败时进入人工确认状态。

#### 验收命令

```bash
python -m local_commerce_workbench parse-order --text "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
```

#### 完成标准

1. 能输出结构化 JSON；
2. 无订单号时失败；
3. 找不到商品时不继续发货。

---

### Task 07：发货话术生成和发货日志

#### 目标

生成可复制发货话术，并记录日志。

#### 要求

1. 根据商品资料生成 `message.txt`；
2. 写入 `delivery_logs.csv`；
3. 同一订单重复输入时提示已发货；
4. 不自动发送平台消息。

#### 验收命令

```bash
python -m local_commerce_workbench deliver --order-text "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
```

#### 完成标准

1. 发货话术可复制；
2. 日志有订单号、商品、发货时间；
3. 重复订单不会重复发货。

---

### Task 08：卡密池管理

#### 目标

支持卡密/激活码/兑换码发一个少一个。

#### 输入

```csv
sku,code,status,used_order_id,used_at
standard,ABCD-EFGH-1234,unused,,
standard,EFGH-IJKL-5678,unused,,
```

#### 要求

1. 根据 SKU 取未使用卡密；
2. 标记卡密已使用；
3. 记录订单号和时间；
4. 卡密不足时阻止发货；
5. 重复订单不重复消耗卡密。

#### 验收命令

```bash
python -m local_commerce_workbench deliver --order-text "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
```

#### 完成标准

1. 卡密状态正确变化；
2. 同一订单不重复消耗；
3. 卡密不足有明确提示。

---

### Task 09：视频信息检查

#### 目标

先检查视频，再处理视频。

#### 要求

1. 用 FFmpeg / ffprobe 读取视频信息；
2. 检查文件是否存在；
3. 检查时长、分辨率、音轨；
4. 输出视频信息 JSON；
5. 错误可读。

#### 验收命令

```bash
python -m local_commerce_workbench inspect-video products/demo-plugin-001
```

#### 完成标准

1. 有效视频通过；
2. 无音轨视频给出提醒；
3. 文件不存在时失败。

---

### Task 10：剪静音、字幕、导出视频

#### 目标

处理教程录屏。

#### 要求

1. 调用 auto-editor 剪静音；
2. 调用 faster-whisper 生成 SRT；
3. 保留可编辑字幕文件；
4. 调用 FFmpeg 输出 16:9；
5. 调用 FFmpeg 输出 9:16；
6. 生成封面图。

#### 验收命令

```bash
python -m local_commerce_workbench process-video products/demo-plugin-001
```

#### 完成标准

1. 输出 MP4 可播放；
2. SRT 存在；
3. 日志记录每一步；
4. 任一步失败能看到失败原因。

---

### Task 11：简单本地界面

#### 目标

用 Streamlit 或 FastAPI 包装已完成 CLI。

#### 页面

```text
商品管理
图片生成
详情页生成
视频处理
发货助手
日志查看
```

#### 要求

1. 每个按钮调用已有 CLI 或函数；
2. 显示输出文件路径；
3. 显示错误信息；
4. 发货话术可复制；
5. 不强制使用平台账号。

#### 完成标准

1. 非程序员可操作核心流程；
2. 不隐藏错误；
3. 不破坏 CLI 可用性。

---

## 5. 每次 Codex 交付必须回复的格式

```text
本次完成：

修改文件：

运行命令：

验收方式：

已通过测试：

当前限制：

下一步建议：
```

没有“运行命令”和“验收方式”，不得合并。

---

## 6. V1 完成定义

V1 完成必须同时满足：

1. 一个 demo 商品能跑完整流程；
2. 图片、详情页、视频、发货文案都有标准文件输出；
3. 发货日志可查；
4. 重复订单不会重复发货；
5. 核心流程不依赖付费订阅；
6. 每个核心模块有测试或可重复验收命令；
7. README 说明普通用户如何运行。

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
