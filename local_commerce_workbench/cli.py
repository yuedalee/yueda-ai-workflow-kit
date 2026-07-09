from __future__ import annotations

import argparse
import csv
import html
import importlib.util
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageDraw, ImageFont

PRODUCT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")
ORDER_ID_PATTERNS = [re.compile(r"订单号[：:\s]*([A-Za-z0-9_-]{4,})"), re.compile(r"\b(\d{6,})\b")]
BUYER_PATTERN = re.compile(r"买家[：:\s]*([^\s，,]+)")
SPEC_PATTERN = re.compile(r"规格[：:\s]*([^\s，,]+)")
REQUIRED_FIELDS = ["id", "name", "platforms", "price", "target_user", "main_pain", "core_value", "features", "delivery", "after_sale"]
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


class WorkbenchError(Exception):
    """Expected operational error with a human-readable message."""


@dataclass(frozen=True)
class ProductPackage:
    product_dir: Path
    data: dict[str, Any]

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def name(self) -> str:
        return str(self.data["name"])

    @property
    def output_dir(self) -> Path:
        return self.product_dir / "output"


@dataclass(frozen=True)
class ParsedOrder:
    order_id: str
    buyer: str | None
    spec: str | None
    raw_text: str


def load_product(product_dir: str | Path) -> ProductPackage:
    product_dir = Path(product_dir)
    product_file = product_dir / "product.yaml"
    if not product_file.exists():
        raise WorkbenchError(f"缺少商品资料文件：{product_file}")
    try:
        data = yaml.safe_load(product_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise WorkbenchError(f"product.yaml 格式错误：{exc}") from exc
    if not isinstance(data, dict):
        raise WorkbenchError("product.yaml 顶层必须是对象/字典")
    return ProductPackage(product_dir, data)


def validate_product(product_dir: str | Path, *, strict_assets: bool = True) -> ProductPackage:
    package = load_product(product_dir)
    data = package.data
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, ""):
            errors.append(f"缺少必填字段：{field}")
    if data.get("id") and not PRODUCT_ID_RE.match(str(data["id"])):
        errors.append("商品 id 只能使用小写字母、数字、短横线、下划线，长度 3-64")
    if not isinstance(data.get("platforms"), list) or not data.get("platforms"):
        errors.append("platforms 必须是非空列表")
    if not isinstance(data.get("features"), list) or not data.get("features"):
        errors.append("features 必须是非空列表")
    try:
        if float(data.get("price", 0)) < 0:
            errors.append("price 不能为负数")
    except (TypeError, ValueError):
        errors.append("price 必须是数字")
    delivery = data.get("delivery")
    if not isinstance(delivery, dict):
        errors.append("delivery 必须是对象")
    else:
        for field in ["type", "download_url", "install_guide_url"]:
            if not delivery.get(field):
                errors.append(f"delivery 缺少字段：{field}")
    if not isinstance(data.get("after_sale"), list) or not data.get("after_sale"):
        errors.append("after_sale 必须是非空列表")
    if strict_assets:
        assets = data.get("assets", {}) or {}
        if not isinstance(assets, dict):
            errors.append("assets 必须是对象")
        else:
            for key in ["logo", "cover", "product_image"]:
                rel = assets.get(key)
                if rel and not (package.product_dir / str(rel)).exists():
                    errors.append(f"素材文件不存在：assets.{key} -> {rel}")
            screenshots_dir = assets.get("screenshots_dir")
            if screenshots_dir and not (package.product_dir / str(screenshots_dir)).exists():
                errors.append(f"截图目录不存在：assets.screenshots_dir -> {screenshots_dir}")
    if errors:
        raise WorkbenchError("\n".join(errors))
    return package


def ensure_output_dirs(package: ProductPackage) -> dict[str, Path]:
    dirs = {}
    for name in ["images", "detail", "video", "delivery", "logs"]:
        path = package.output_dir / name
        path.mkdir(parents=True, exist_ok=True)
        dirs[name] = path
    return dirs


def append_run_log(package: ProductPackage, command: str, status: str, message: str = "") -> Path:
    log_file = ensure_output_dirs(package)["logs"] / "run_log.csv"
    is_new = not log_file.exists()
    if is_new:
        log_file.write_text("time,product_id,command,status,message\n", encoding="utf-8")
    clean_message = message.replace("\n", " ").replace(",", "；")
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')},{package.id},{command},{status},{clean_message}\n")
    return log_file


def _font(size: int) -> ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines = []
    for raw in str(text).splitlines() or [""]:
        buf = ""
        for char in raw:
            candidate = buf + char
            box = draw.textbbox((0, 0), candidate, font=font)
            if box[2] - box[0] <= max_width or not buf:
                buf = candidate
            else:
                lines.append(buf)
                buf = char
        if buf:
            lines.append(buf)
    return lines


def _draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, max_width: int, fill=(25, 25, 25), gap: int = 10) -> int:
    x, y = xy
    for line in _wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        box = draw.textbbox((x, y), line, font=font)
        y += box[3] - box[1] + gap
    return y


def _save_card(path: Path, size: tuple[int, int], title: str, subtitle: str, bullets: list[str], footer: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, (248, 248, 246))
    draw = ImageDraw.Draw(img)
    width, height = size
    draw.rounded_rectangle((40, 40, width - 40, 170), radius=24, fill=(32, 32, 32))
    draw.text((70, 78), "悦达智科 本地工作台", font=_font(28), fill=(255, 255, 255))
    y = 220
    y = _draw_text(draw, (60, y), title, _font(54 if width >= 800 else 42), width - 120, fill=(10, 10, 10), gap=14) + 20
    y = _draw_text(draw, (60, y), subtitle, _font(28), width - 120, fill=(70, 70, 70), gap=10) + 28
    box_bottom = min(height - 110, y + 300)
    draw.rounded_rectangle((50, y, width - 50, box_bottom), radius=22, fill=(255, 255, 255), outline=(225, 225, 225))
    bullet_y = y + 30
    for bullet in bullets[:5]:
        bullet_y = _draw_text(draw, (80, bullet_y), f"• {bullet}", _font(30), width - 160, fill=(30, 30, 30), gap=6) + 8
    draw.text((60, height - 70), footer, font=_font(24), fill=(90, 90, 90))
    img.save(path, quality=95)


def generate_images(product_dir: str | Path) -> list[Path]:
    package = validate_product(product_dir)
    dirs = ensure_output_dirs(package)
    d = package.data
    features = [str(x) for x in d.get("features", [])]
    specs = [
        ("main_800x800_01.png", (800, 800), d["name"], d["core_value"], features[:3], "适合：" + str(d["target_user"])),
        ("main_800x800_02.png", (800, 800), "解决痛点", d["main_pain"], features[:4], "半自动可控 · 本地运行 · 防漏发"),
        ("carousel_01.png", (800, 800), "核心功能", d["name"], features[:4], "标准化资料 → 标准化输出"),
        ("carousel_02.png", (800, 800), "适用场景", str(d["target_user"]), features[:4], "降低重复劳动，保留人工确认"),
        ("carousel_03.png", (800, 800), "发货说明", str(d.get("delivery", {}).get("type", "虚拟商品发货")), ["下载链接", "安装教程", "售后 FAQ", "重复订单检测"], "下单后按说明完成交付"),
        ("cover_9x16.png", (1080, 1920), d["name"], d["core_value"], features[:5], "教程 / 宣传 / 商品图统一生产"),
    ]
    paths = []
    for filename, size, title, subtitle, bullets, footer in specs:
        path = dirs["images"] / filename
        _save_card(path, size, str(title), str(subtitle), [str(x) for x in bullets], str(footer))
        paths.append(path)
    append_run_log(package, "generate-images", "success", f"generated {len(paths)} images")
    return paths


def _faq_items(package: ProductPackage) -> list[tuple[str, str]]:
    items = []
    for item in package.data.get("after_sale", []):
        if isinstance(item, dict):
            items.append((str(item.get("question", "常见问题")), str(item.get("answer", "请联系人工处理。"))))
        else:
            items.append((str(item), "请先按安装教程操作；仍无法解决时再联系人工处理。"))
    return items


def generate_detail(product_dir: str | Path) -> list[Path]:
    package = validate_product(product_dir)
    dirs = ensure_output_dirs(package)
    d = package.data
    delivery = d.get("delivery", {})
    features = [str(x) for x in d.get("features", [])]
    html_path = dirs["detail"] / "detail.html"
    png_path = dirs["detail"] / "detail_750_long.png"
    features_html = "".join(f"<li>{html.escape(f)}</li>" for f in features)
    faq_html = "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in _faq_items(package))
    html_path.write_text(f"""<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><title>{html.escape(str(d['name']))}</title><style>body{{margin:0;background:#f6f6f4;font-family:-apple-system,BlinkMacSystemFont,'Microsoft YaHei',sans-serif;color:#1f1f1f}}.page{{width:750px;margin:0 auto;background:#fff}}.hero{{padding:56px 48px;background:#202020;color:#fff}}h1{{font-size:44px;line-height:1.2}}h2{{font-size:32px;margin-top:42px}}p,li{{font-size:24px;line-height:1.7}}.section{{padding:20px 48px 36px;border-bottom:1px solid #eee}}</style></head><body><main class=\"page\"><section class=\"hero\"><h1>{html.escape(str(d['name']))}</h1><p>{html.escape(str(d['core_value']))}</p></section><section class=\"section\"><h2>适合谁</h2><p>{html.escape(str(d['target_user']))}</p></section><section class=\"section\"><h2>正在解决的痛点</h2><p>{html.escape(str(d['main_pain']))}</p></section><section class=\"section\"><h2>核心功能</h2><ul>{features_html}</ul></section><section class=\"section\"><h2>发货说明</h2><p>{html.escape(str(delivery.get('type', '')))}</p></section><section class=\"section\"><h2>售后 FAQ</h2>{faq_html}</section></main></body></html>""", encoding="utf-8")
    width, margin = 750, 42
    sections = [(str(d["name"]), str(d["core_value"])), ("适合谁", str(d["target_user"])), ("痛点", str(d["main_pain"])), ("核心功能", "\n".join(f"• {f}" for f in features)), ("发货说明", f"发货类型：{delivery.get('type','')}\n下载链接：{delivery.get('download_url','')}\n安装教程：{delivery.get('install_guide_url','')}"), ("售后 FAQ", "\n".join(f"Q：{q}\nA：{a}" for q, a in _faq_items(package)))]
    dummy = Image.new("RGB", (width, 10))
    draw = ImageDraw.Draw(dummy)
    title_font, body_font = _font(34), _font(24)
    blocks = []
    height = margin
    for title, body in sections:
        lines = _wrap(draw, body, body_font, width - margin * 2)
        block_h = 60 + len(lines) * 42 + 46
        blocks.append((title, lines, block_h))
        height += block_h
    img = Image.new("RGB", (width, max(1200, height + margin)), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    y = margin
    for title, lines, block_h in blocks:
        draw.rounded_rectangle((24, y - 10, width - 24, y + block_h - 18), radius=22, fill=(248, 248, 246), outline=(230, 230, 230))
        draw.text((margin, y + 12), title, font=title_font, fill=(25, 25, 25))
        ty = y + 72
        for line in lines:
            draw.text((margin, ty), line, font=body_font, fill=(55, 55, 55))
            ty += 42
        y += block_h
    img.save(png_path, quality=95)
    append_run_log(package, "generate-detail", "success", "generated detail html and long image")
    return [html_path, png_path]


def generate_copy(product_dir: str | Path) -> list[Path]:
    package = validate_product(product_dir)
    dirs = ensure_output_dirs(package)
    d = package.data
    delivery = d.get("delivery", {})
    install = f"# 安装与使用说明｜{d['name']}\n\n1. 下载文件：{delivery.get('download_url','')}\n2. 打开教程：{delivery.get('install_guide_url','')}\n3. 按教程完成安装、配置和首次运行。\n4. 如遇到问题，请先看 FAQ，再联系人工。\n"
    faq = [f"# 售后 FAQ｜{d['name']}", ""]
    for q, a in _faq_items(package):
        faq.extend([f"## {q}", a, ""])
    titles = [f"{d['name']}｜{d['core_value']}", f"适合{d['target_user']}的{d['name']}", f"解决：{d['main_pain']}"]
    outputs = {"install_guide.txt": install, "faq.txt": "\n".join(faq), "titles.txt": "\n".join(titles) + "\n"}
    paths = []
    for filename, content in outputs.items():
        path = dirs["delivery"] / filename
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    append_run_log(package, "generate-copy", "success", f"generated {len(paths)} copy files")
    return paths


def parse_order_text(text: str) -> ParsedOrder:
    order_id = None
    for pattern in ORDER_ID_PATTERNS:
        match = pattern.search(text)
        if match:
            order_id = match.group(1)
            break
    if not order_id:
        raise WorkbenchError("无法识别订单号，请检查订单文本是否包含：订单号：xxxx")
    buyer = BUYER_PATTERN.search(text)
    spec = SPEC_PATTERN.search(text)
    return ParsedOrder(order_id, buyer.group(1) if buyer else None, spec.group(1) if spec else None, text)


def find_product_for_order(order_text: str, products_root: str | Path = "products") -> Path:
    root = Path(products_root)
    candidates = [p for p in root.iterdir() if p.is_dir() and (p / "product.yaml").exists()] if root.exists() else []
    matches = []
    for candidate in candidates:
        try:
            package = validate_product(candidate)
        except Exception:
            continue
        if package.id in order_text or package.name in order_text:
            matches.append(candidate)
    if len(matches) == 1:
        return matches[0]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise WorkbenchError("没有找到 products/*/product.yaml 商品目录")
    raise WorkbenchError("无法唯一匹配商品，请使用 --product-dir 指定商品目录")


def _delivery_log_path() -> Path:
    path = Path("data") / "delivery_logs.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _existing_orders(log_path: Path) -> set[str]:
    if not log_path.exists():
        return set()
    with log_path.open("r", encoding="utf-8", newline="") as f:
        return {row.get("order_id", "") for row in csv.DictReader(f) if row.get("order_id")}


def _append_delivery_log(log_path: Path, package: ProductPackage, order: ParsedOrder, status: str, code: str | None, reason: str) -> None:
    is_new = not log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as f:
        fieldnames = ["time", "order_id", "buyer", "product_id", "product_name", "spec", "status", "code", "reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        writer.writerow({"time": datetime.now().isoformat(timespec="seconds"), "order_id": order.order_id, "buyer": order.buyer or "", "product_id": package.id, "product_name": package.name, "spec": order.spec or "", "status": status, "code": code or "", "reason": reason})


def _consume_code(package: ProductPackage, order: ParsedOrder) -> str | None:
    rel = package.data.get("delivery", {}).get("code_pool_file")
    if not rel:
        return None
    code_file = package.product_dir / str(rel)
    if not code_file.exists():
        raise WorkbenchError(f"卡密池不存在：{code_file}")
    with code_file.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise WorkbenchError("卡密池为空")
    fieldnames = list(rows[0].keys())
    for col in ["code", "status", "order_id", "used_at"]:
        if col not in fieldnames:
            fieldnames.append(col)
    selected = None
    for row in rows:
        row.setdefault("status", "unused")
        if row.get("status") == "unused":
            selected = row
            break
    if selected is None:
        raise WorkbenchError("卡密不足：没有 unused 状态的卡密")
    selected["status"] = "used"
    selected["order_id"] = order.order_id
    selected["used_at"] = datetime.now().isoformat(timespec="seconds")
    with code_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return selected.get("code")


def deliver(order_text: str, product_dir: str | Path | None = None) -> tuple[str, Path | None, Path, str | None]:
    order = parse_order_text(order_text)
    product_path = Path(product_dir) if product_dir else find_product_for_order(order_text)
    package = validate_product(product_path)
    ensure_output_dirs(package)
    generate_copy(product_path)
    log_path = _delivery_log_path()
    if order.order_id in _existing_orders(log_path):
        _append_delivery_log(log_path, package, order, "duplicate", None, "duplicate_order")
        append_run_log(package, "deliver", "duplicate", "duplicate_order")
        return "duplicate", None, log_path, None
    code = _consume_code(package, order)
    d = package.data
    delivery_info = d.get("delivery", {})
    buyer = order.buyer or "您好"
    code_block = f"\n激活码/卡密：{code}\n" if code else ""
    message = f"""{buyer}，您好，您购买的【{d['name']}】已为您整理好发货内容：

下载链接：
{delivery_info.get('download_url', '')}

安装教程：
{delivery_info.get('install_guide_url', '')}
{code_block}
使用建议：
1. 请先完整查看安装教程，再进行安装或配置。
2. 如果系统提示风险或打不开，请先看教程中的常见问题部分。
3. 如果仍无法解决，请把报错截图、订单号、电脑系统版本发给我，我再协助处理。

订单号：{order.order_id}
商品规格：{order.spec or '默认规格'}
"""
    message_path = package.output_dir / "delivery" / "message.txt"
    message_path.write_text(message, encoding="utf-8")
    _append_delivery_log(log_path, package, order, "sent_pending_manual_copy", code, "message_generated")
    append_run_log(package, "deliver", "success", "delivery message generated; manual copy required")
    return "sent_pending_manual_copy", message_path, log_path, code


def doctor_text() -> str:
    lines = ["Local Commerce Workbench Doctor", ""]
    lines.append(f"- python: ok ({sys.version.split()[0]})")
    for pkg in ["yaml", "PIL"]:
        lines.append(f"- {pkg}: {'ok' if importlib.util.find_spec(pkg) else 'missing'} (required)")
    for cmd in ["ffmpeg", "auto-editor"]:
        lines.append(f"- {cmd}: {'ok' if shutil.which(cmd) else 'missing'} (optional for video pipeline)")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="local-commerce-workbench")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="检查本地依赖状态").set_defaults(func=lambda a: print(doctor_text()) or 0)
    p = sub.add_parser("validate", help="校验商品资料包")
    p.add_argument("product_dir")
    p.set_defaults(func=lambda a: print(f"OK: {validate_product(a.product_dir).id}｜{validate_product(a.product_dir).name}") or 0)
    p = sub.add_parser("generate-images", help="生成商品主图、轮播图和竖版封面")
    p.add_argument("product_dir")
    p.set_defaults(func=lambda a: _print_paths(generate_images(a.product_dir)))
    p = sub.add_parser("generate-detail", help="生成详情页 HTML 和 750px 长图")
    p.add_argument("product_dir")
    p.set_defaults(func=lambda a: _print_paths(generate_detail(a.product_dir)))
    p = sub.add_parser("generate-copy", help="生成安装说明、FAQ 和标题建议")
    p.add_argument("product_dir")
    p.set_defaults(func=lambda a: _print_paths(generate_copy(a.product_dir)))
    p = sub.add_parser("deliver", help="根据订单文本生成半自动发货话术并记录日志")
    p.add_argument("--order-text", required=True)
    p.add_argument("--product-dir", default=None)
    p.set_defaults(func=_cmd_deliver)
    return parser


def _print_paths(paths: list[Path]) -> int:
    for path in paths:
        print(path.as_posix())
    return 0


def _cmd_deliver(args: argparse.Namespace) -> int:
    status, message_path, log_path, code = deliver(args.order_text, args.product_dir)
    print(f"status: {status}")
    if code:
        print(f"code: {code}")
    if message_path:
        print(f"message: {message_path.as_posix()}")
    print(f"log: {log_path.as_posix()}")
    return 0 if status != "duplicate" else 2


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except WorkbenchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"UNEXPECTED_ERROR: {exc}", file=sys.stderr)
        return 1
