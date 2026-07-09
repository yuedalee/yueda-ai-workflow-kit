# 本地商品内容与发货工作台 V1｜实现状态

> Status：V0.1 bootstrap completed  
> 目标：把前期顶层设计推进到可运行工程骨架，方便 Codex 后续按任务继续实现，而不是只停留在文档层。

---

## 1. 本次推进范围

V0.1 只做低风险、本地确定性能力：

```text
商品资料校验
→ 商品主图/轮播图基础生成
→ 详情页 HTML 与 750px 长图生成
→ 安装说明、FAQ、标题建议生成
→ 订单文本解析
→ 卡密池消耗
→ 发货话术生成
→ 发货日志与重复订单检测
```

不做平台自动登录、自动发布商品、自动发送买家消息、绕过验证码或风控。

---

## 2. 新增工程文件

```text
pyproject.toml
local_commerce_workbench/
  __init__.py
  __main__.py
  cli.py
products/demo-plugin-001/
  product.yaml
  data/demo_codes.csv
tests/test_local_commerce_workbench.py
.github/workflows/local-workbench-ci.yml
```

---

## 3. 本地运行命令

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

python -m local_commerce_workbench doctor
python -m local_commerce_workbench validate products/demo-plugin-001
python -m local_commerce_workbench generate-images products/demo-plugin-001
python -m local_commerce_workbench generate-detail products/demo-plugin-001
python -m local_commerce_workbench generate-copy products/demo-plugin-001
python -m local_commerce_workbench deliver --order-text "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
pytest
```

---

## 4. 当前验收口径

V0.1 暂时只认以下交付物：

1. CLI 能启动；
2. demo 商品能通过校验；
3. 能生成 PNG 商品图；
4. 能生成详情页 HTML 与长图；
5. 能生成发货说明、FAQ、标题建议；
6. 能从订单文本识别订单号、买家、规格；
7. 能消耗一条 demo 卡密；
8. 能记录 `data/delivery_logs.csv`；
9. 同一订单再次输入会判定为重复；
10. 测试能通过。

---

## 5. 下一步建议

下一步不要扩张到平台自动化，先继续补强 V1 内核：

1. 把 `cli.py` 拆分为 `product.py`、`render.py`、`delivery.py`、`video.py`；
2. 加入 `process-video` 命令，只负责 FFmpeg 检测、录屏转码、横竖版输出；
3. 增加 `products/_template/product.yaml`，方便复制创建新商品；
4. 增加 `make demo` 或 `justfile`，降低本地启动成本；
5. 增加真实商品素材的私有目录说明，明确不要把真实卡密和订单提交到公开仓库。
