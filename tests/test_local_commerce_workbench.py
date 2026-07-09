from __future__ import annotations

import csv
from pathlib import Path

from local_commerce_workbench.cli import deliver, generate_detail, generate_images, parse_order_text, validate_product


def _make_product(tmp_path: Path) -> Path:
    product_dir = tmp_path / "products" / "demo-plugin-001"
    (product_dir / "data").mkdir(parents=True)
    (product_dir / "product.yaml").write_text(
        """
id: demo-plugin-001
name: 拼多多虚拟商品半自动发货助手
platforms: [拼多多, 淘宝, 闲鱼]
price: 49
target_user: 一人公司
main_pain: 手动发货慢，容易重复发货。
core_value: 半自动生成发货话术并记录日志。
features:
  - 识别订单号
  - 生成发货话术
  - 记录发货日志
delivery:
  type: 网盘链接 + 激活码
  download_url: https://example.com/download
  install_guide_url: https://example.com/tutorial
  code_pool_file: data/codes.csv
after_sale:
  - question: 打不开怎么办？
    answer: 请先查看教程。
assets: {}
""".strip(),
        encoding="utf-8",
    )
    (product_dir / "data" / "codes.csv").write_text("code,status,order_id,used_at\nCODE-001,unused,,\nCODE-002,unused,,\n", encoding="utf-8")
    return product_dir


def test_validate_product(tmp_path: Path) -> None:
    product_dir = _make_product(tmp_path)
    package = validate_product(product_dir)
    assert package.id == "demo-plugin-001"


def test_generate_images_and_detail(tmp_path: Path) -> None:
    product_dir = _make_product(tmp_path)
    image_paths = generate_images(product_dir)
    detail_paths = generate_detail(product_dir)
    assert (product_dir / "output" / "images" / "main_800x800_01.png").exists()
    assert len(image_paths) >= 6
    assert (product_dir / "output" / "detail" / "detail_750_long.png").exists()
    assert len(detail_paths) == 2


def test_parse_order_text() -> None:
    order = parse_order_text("订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三")
    assert order.order_id == "123456"
    assert order.buyer == "张三"
    assert order.spec == "标准版"


def test_deliver_consumes_code_and_detects_duplicate(tmp_path: Path, monkeypatch) -> None:
    product_dir = _make_product(tmp_path)
    monkeypatch.chdir(tmp_path)
    text = "订单号：123456 商品：拼多多虚拟商品半自动发货助手 规格：标准版 买家：张三"
    status, message_path, log_path, code = deliver(text, product_dir)
    assert status == "sent_pending_manual_copy"
    assert code == "CODE-001"
    assert message_path and message_path.exists()
    duplicate_status, _, _, _ = deliver(text, product_dir)
    assert duplicate_status == "duplicate"
    with log_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["order_id"] == "123456"
    assert rows[0]["code"] == "CODE-001"
    assert rows[1]["status"] == "duplicate"
