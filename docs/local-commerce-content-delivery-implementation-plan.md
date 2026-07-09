# 本地商品内容与发货工作台｜落地路线

> Status：Implementation Plan v0.1  
> 目标：把“顶层设计”拆成 Codex 可以逐步执行、人工可以逐步验收的任务。  
> 原则：每一步都必须产生可检查、可运行、可交付的结果。

---

## 1. 总体落地顺序

不要从“大系统”开始。

正确顺序：

```text
01 商品资料标准化
→ 02 输出目录与日志
→ 03 商品图/详情页生成
→ 04 半自动发货
→ 05 教程视频处理
→ 06 简单本地界面
→ 07 平台辅助自动化
```

原因：

1. 商品资料是所有模块的共同输入；
2. 输出文件和日志决定系统是否能用于生产；
3. 商品图和发货助手最容易先产生价值；
4. 视频处理对依赖要求更高，放在中后段；
5. 平台自动化最容易踩坑，必须最后做。

---

## 2. 阶段 0：项目骨架

### 目标

建立一个能被 Codex 稳定维护的本地 Python 项目。

### 必须产出

```text
README.md
pyproject.toml
src/local_commerce_workbench/
tests/
products/demo-plugin-001/product.yaml
```

### 命令要求

至少支持：

```bash
python -m local_commerce_workbench --help
python -m local_commerce_workbench validate products/demo-plugin-001
```

### 验收标准

1. 本地能安装依赖；
2. `--help` 能显示命令；
3. demo 商品能通过基础校验；
4. 错误时不能直接崩溃，必须输出可读错误。

---

## 3. 阶段 1：商品资料标准化

### 目标

把所有商品都变成结构化资料，而不是散落的文字、图片和链接。

### 输入

```text
product.yaml
raw/logo.png
raw/product.png
raw/screenshots/
```

### 必填字段

```yaml
id:
name:
platforms:
price:
target_user:
main_pain:
core_value:
features:
delivery_type:
assets:
delivery:
after_sale:
```

### 必须实现

1. 读取 `product.yaml`；
2. 校验必填字段；
3. 校验素材路径是否存在；
4. 输出标准化商品对象；
5. 给出缺失字段清单。

### 验收标准

1. 缺字段时明确提示字段名；
2. 素材不存在时明确提示路径；
3. 合格商品能进入下一阶段；
4. 不允许静默跳过错误。

---

## 4. 阶段 2：输出目录与日志

### 目标

先把交付物和日志结构固定下来。

### 输出目录

```text
output/
├── images/
├── detail/
├── video/
└── delivery/
```

### 日志文件

```text
logs/run.log
data/delivery_logs.csv
data/app.db
```

### 必须实现

1. 自动创建输出目录；
2. 每次生成记录时间、商品 ID、命令、输出文件；
3. 失败时记录错误原因；
4. 支持导出发货日志 CSV。

### 验收标准

1. 任意命令执行后都有日志；
2. 文件生成路径明确；
3. 失败后能定位问题；
4. 重新运行不会覆盖重要历史记录。

---

## 5. 阶段 3：商品主图和轮播图生成

### 目标

先不用复杂 AI 作图，用模板稳定生成能上传的商品图片。

### 输入

```text
product.yaml
logo.png
product.png 或 screenshots
```

### 输出

```text
output/images/main_800x800_01.png
output/images/main_800x800_02.png
output/images/carousel_01.png
output/images/carousel_02.png
output/images/carousel_03.png
output/video/cover_9x16.png
```

### 推荐实现

1. Jinja2 生成 HTML 模板；
2. Playwright 截图；
3. Pillow 压缩、裁剪、尺寸检查；
4. 所有字体本地化，不依赖在线字体；
5. 文案过长时自动换行或缩小字号。

### 验收标准

1. 图片尺寸正确；
2. 文字不溢出；
3. 图片不拉伸变形；
4. 每张图卖点不同；
5. 输出文件可直接上传到平台。

---

## 6. 阶段 4：详情页生成

### 目标

生成 750px 宽商品详情长图，同时保留 HTML 方便修改。

### 输出

```text
output/detail/detail.html
output/detail/detail_750_long.png
```

### 模块建议

```text
01 首屏卖点
02 用户痛点
03 解决方案
04 功能列表
05 使用步骤
06 发货说明
07 售后 FAQ
08 风险和边界说明
```

### 验收标准

1. 长图宽度为 750px；
2. 模块顺序稳定；
3. 文字可读；
4. 不出现空模块；
5. 修改 product.yaml 后可重新生成。

---

## 7. 阶段 5：半自动发货助手

### 目标

先做“订单识别 + 发货内容生成 + 日志记录”，不做自动发消息。

### 输入

```text
从平台复制的订单文本
product.yaml
card_pool.csv
```

### 输出

```text
output/delivery/message.txt
data/delivery_logs.csv
```

### 必须实现

1. 识别订单号；
2. 识别商品名或规格；
3. 匹配 SKU；
4. 取一条可用卡密；
5. 生成发货话术；
6. 记录发货日志；
7. 重复订单提醒。

### 卡密池格式

```csv
sku,code,status,used_order_id,used_at
standard,ABCD-EFGH-1234,unused,,
standard,EFGH-IJKL-5678,unused,,
```

### 验收标准

1. 同一订单不能重复消耗卡密；
2. 找不到商品时不生成发货；
3. 卡密不足时明确提醒；
4. 生成内容必须可一键复制；
5. 发货日志可导出。

---

## 8. 阶段 6：教程视频处理

### 目标

把录屏视频处理成横版教程、竖版教程、字幕文件和封面图。

### 输入

```text
raw/recording.mp4
product.yaml
logo.png
```

### 输出

```text
output/video/tutorial_16x9.mp4
output/video/tutorial_9x16.mp4
output/video/subtitle.srt
output/video/cover.png
```

### 推荐流程

```text
FFmpeg 检查视频信息
→ auto-editor 剪静音
→ faster-whisper 生成字幕
→ 人工可修改 SRT
→ FFmpeg 烧录字幕
→ 输出 16:9 和 9:16
→ 生成封面
```

### 验收标准

1. 输入一条 3-5 分钟录屏能生成视频；
2. 字幕时间基本对齐；
3. 能保留可编辑 SRT；
4. 竖版视频主体内容不被裁掉；
5. 处理失败时能看到是哪一步失败。

---

## 9. 阶段 7：简单本地界面

### 目标

让非程序员也能操作，但界面只包住已经跑通的 CLI。

### 页面

```text
商品管理
商品图生成
详情页生成
视频处理
发货助手
日志查看
```

### 验收标准

1. 每个按钮都对应一个已验证 CLI 命令；
2. 界面不隐藏错误；
3. 可以打开输出文件夹；
4. 可以复制发货话术；
5. 不要求登录任何第三方平台。

---

## 10. 阶段 8：平台辅助自动化

### 目标

仅在 V1 稳定后，再考虑 Playwright 半自动操作平台页面。

### 允许做

```text
自动打开后台页面
自动截图
自动填入草稿字段
自动复制商品标题和详情
人工确认后发布
```

### 不允许做

```text
绕过验证码
自动批量私信
自动点击最终付款/发布/发货确认
规避风控
刷单刷评
```

### 验收标准

平台辅助自动化必须可关闭，不能影响本地核心流程。

---

## 11. Codex 执行原则

给 Codex 的任务必须小而具体。

错误写法：

```text
帮我做一个电商自动化系统。
```

正确写法：

```text
实现 product.yaml 读取和校验。
要求：缺失字段要报错；素材不存在要报错；通过后输出标准化 JSON；添加测试；给出运行命令和验收方式。
```

每个任务必须交付：

```text
完成了什么
修改了哪些文件
如何运行
如何验收
通过了哪些测试
当前限制和风险
```

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
