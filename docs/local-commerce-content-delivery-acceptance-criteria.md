# 本地商品内容与发货工作台｜验收标准

> Status：Acceptance Criteria v0.1  
> 用途：防止 Codex 或开发者只“做出来”，但交付物不能用。  
> 核心原则：验收标准必须围绕真实交付物，而不是围绕功能清单。

---

## 1. 总体验收结论

这个项目只有满足以下条件，才算 V1 可用：

```text
输入一个商品资料包
→ 生成可上传的商品图片和详情页
→ 处理一条教程录屏
→ 生成可复制的发货话术
→ 记录发货日志并防止重复发货
→ 全流程不依赖必须付费订阅
```

不是“界面能打开”就算完成。  
不是“功能菜单很多”就算完成。  
不是“Codex 说完成了”就算完成。

---

## 2. 最终交付物验收

### 2.1 一个合格商品输出包

每个商品至少要生成：

```text
output/
├── images/
│   ├── main_800x800_01.png
│   ├── main_800x800_02.png
│   ├── carousel_01.png
│   ├── carousel_02.png
│   ├── carousel_03.png
│   └── cover_9x16.png
├── detail/
│   ├── detail.html
│   └── detail_750_long.png
├── video/
│   ├── tutorial_16x9.mp4
│   ├── tutorial_9x16.mp4
│   ├── subtitle.srt
│   └── cover.png
└── delivery/
    ├── message.txt
    ├── install_guide.txt
    └── faq.txt
```

### 验收标准

1. 文件真实存在；
2. 文件命名稳定；
3. 文件能打开；
4. 图片尺寸符合平台常用要求；
5. 视频能正常播放；
6. 发货文案能直接复制给买家；
7. 重新生成不会破坏旧日志。

---

## 3. 商品资料验收

### 必须支持

```bash
python -m local_commerce_workbench validate products/demo-plugin-001
```

### 必须检查

1. `product.yaml` 是否存在；
2. 必填字段是否完整；
3. 素材路径是否存在；
4. 价格、平台、功能列表是否格式正确；
5. 发货链接、教程链接是否存在；
6. 商品 ID 是否可用于目录和文件名。

### 失败标准

以下情况必须失败，不能静默通过：

```text
缺少商品名称
缺少发货内容
素材路径不存在
features 为空
商品 ID 含非法字符
product.yaml 格式错误
```

---

## 4. 图片和详情页验收

### 命令

```bash
python -m local_commerce_workbench generate-images products/demo-plugin-001
python -m local_commerce_workbench generate-detail products/demo-plugin-001
```

### 主图验收

1. 至少生成 2 张 800x800 主图；
2. 至少生成 3 张轮播图；
3. 主标题不溢出；
4. 产品图不变形；
5. 卖点文字不重复；
6. 输出图片大小合理；
7. 图片可直接上传。

### 详情页验收

1. 生成 `detail.html`；
2. 生成 `detail_750_long.png`；
3. 详情长图宽度为 750px；
4. 至少包含痛点、解决方案、功能、使用步骤、发货说明、售后 FAQ；
5. 不出现空白模块或模板占位符。

---

## 5. 视频处理验收

### 命令

```bash
python -m local_commerce_workbench process-video products/demo-plugin-001
```

### 必须输出

```text
tutorial_16x9.mp4
tutorial_9x16.mp4
subtitle.srt
cover.png
```

### 验收标准

1. 3-5 分钟录屏可以完成处理；
2. 明显长静音能被剪掉；
3. 字幕文件可手动编辑；
4. 烧录字幕后视频能播放；
5. 竖版视频主体内容不被裁掉；
6. 失败时能定位到 FFmpeg、auto-editor、faster-whisper 中的具体步骤。

---

## 6. 发货助手验收

### 命令

```bash
python -m local_commerce_workbench deliver --order-text "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
```

### 必须输出

```text
output/delivery/message.txt
data/delivery_logs.csv
```

### 验收标准

1. 能识别订单号；
2. 能识别商品名或规格；
3. 能匹配正确 SKU；
4. 能生成发货话术；
5. 能消耗一条未使用卡密；
6. 能记录发货日志；
7. 同一订单再次输入时提示重复；
8. 卡密不足时不生成错误发货内容；
9. 找不到商品时进入人工确认状态。

---

## 7. 成本验收

V1 必须满足：

```text
无 OpenAI API 必需依赖
无 Claude API 必需依赖
无 Midjourney 必需依赖
无 Runway 必需依赖
无 n8n Cloud 必需依赖
无 Dify Cloud 必需依赖
无 CapCut API 必需依赖
无第三方平台账号登录作为核心流程前置条件
```

允许存在可选扩展，但不能影响本地核心流程。

---

## 8. 稳定性验收

### 必须有日志

每次运行必须记录：

```text
运行时间
商品 ID
命令名称
输入路径
输出路径
成功 / 失败状态
错误原因
```

### 必须可重复

同一个商品资料包重复运行时：

1. 输出目录结构不变；
2. 文件命名不乱；
3. 发货日志不丢失；
4. 卡密不会重复发；
5. 错误可以复现和定位。

---

## 9. 人工确认验收

V1 必须保留人工确认环节。

以下动作不允许默认全自动：

```text
发布商品
改价格
发送买家消息
确认发货
删除订单记录
批量操作平台页面
```

系统可以生成内容、辅助填写、复制话术，但最终动作由人确认。

---

## 10. Codex 交付验收模板

每次 Codex 完成任务后，必须按照这个格式报告：

```text
本次完成：

修改文件：

运行命令：

验收方式：

已通过测试：

当前限制：

下一步建议：
```

没有运行命令和验收方式的交付，不算完成。

---

## 11. 一票否决项

出现以下任一情况，判定为不可用：

1. 只能在开发者机器上跑；
2. 必须购买订阅才能完成核心流程；
3. 没有输出标准文件；
4. 没有错误日志；
5. 自动消耗卡密但不记录；
6. 重复订单重复发货；
7. 生成图片不可上传；
8. 视频不能播放；
9. 平台自动化绕过验证码或风控；
10. 界面好看但 CLI 不可用。

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
