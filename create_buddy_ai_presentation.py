# -*- coding: utf-8 -*-
"""
Generator cho bộ Slide PowerPoint (13 trang) đồ án BUDDY AI
Phong cách: Pikbest AI Artificial Intelligence Introduction Business Technology Work PPT Template (#211210)
Tone màu: Deep Cyber Navy (#070B19), Dark Tech Slate (#0F172A / #131F3A),
          Electric Cyan (#00E5FF), Neon Royal Blue (#3B82F6), Vibrant Violet (#8B5CF6),
          Emerald Accent (#10B981), Amber Highlight (#F59E0B), Crisp White (#FFFFFF).
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent
ROLLBACK_DIR = ROOT / "_buddy_rollback"
OUT_DIR = ROOT / "output"
BG_DIR = OUT_DIR / "ppt_assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)
BG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# BẢNG MÀU PIKBEST AI TECH (#211210 STYLE)
# ---------------------------------------------------------------------------
C_BG_DEEP = RGBColor(7, 11, 25)        # #070B19 - Nền chính Cyber Navy đậm
C_CARD_BG = RGBColor(16, 26, 50)       # #101A32 - Nền card công nghệ
C_CARD_ALT = RGBColor(21, 34, 64)      # #152240 - Nền card phụ / nổi bật
C_CARD_DARK = RGBColor(10, 16, 34)     # #0A1022 - Nền hộp code / công thức
C_CYAN = RGBColor(0, 229, 255)         # #00E5FF - Điểm nhấn AI Cyan phát sáng
C_BLUE = RGBColor(59, 130, 246)        # #3B82F6 - Xanh công nghệ
C_PURPLE = RGBColor(139, 92, 246)      # #8B5CF6 - Tím Neural / Deep Learning
C_EMERALD = RGBColor(16, 185, 129)     # #10B981 - Xanh lá hiệu suất / PASS
C_AMBER = RGBColor(245, 158, 11)       # #F59E0B - Cam vàng cảnh báo / điểm nhấn
C_ROSE = RGBColor(244, 63, 94)         # #F43F5E - Đỏ hồng
C_WHITE = RGBColor(255, 255, 255)      # #FFFFFF - Chữ tiêu đề chính
C_TEXT = RGBColor(226, 232, 240)       # #E2E8F0 - Chữ nội dung sáng
C_MUTED = RGBColor(148, 163, 184)      # #94A3B8 - Chữ phụ / chú thích
C_BORDER = RGBColor(36, 62, 115)       # #243E73 - Viền card tiêu chuẩn

FONT_MAIN = "Segoe UI"
FONT_MONO = "Consolas"


# ---------------------------------------------------------------------------
# 1. TẠO HÌNH NỀN CÔNG NGHỆ AI (PIKBEST FUTURISTIC HUD & CIRCUIT BACKGROUND)
# ---------------------------------------------------------------------------
def generate_tech_backgrounds():
    """Vẽ 2 hình nền 1920x1080 chuẩn Pikbest AI Tech (Cover & Content Slide)."""
    w, h = 1920, 1080

    # --- A. Nền trang bìa (Cover Background) ---
    cover = Image.new("RGBA", (w, h), (6, 10, 24, 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    # Quầng sáng Cyan góc phải & Tím góc trái dưới
    gdraw.ellipse((1050, -100, 2050, 900), fill=(0, 195, 255, 65))
    gdraw.ellipse((1180, 120, 1850, 790), fill=(59, 130, 246, 55))
    gdraw.ellipse((-250, 450, 650, 1350), fill=(124, 58, 237, 50))
    gdraw.ellipse((350, -250, 1050, 350), fill=(0, 229, 255, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=95))
    cover = Image.alpha_composite(cover, glow)

    cdraw = ImageDraw.Draw(cover)
    # Lưới chấm công nghệ (Tech Dot Grid)
    for x in range(60, w, 60):
        for y in range(60, h, 60):
            cdraw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(56, 189, 248, 32))

    # Vòng tròn HUD công nghệ bên phải (sau lưng Robot 3D)
    cx, cy = 1440, 490
    for r, col, width in [
        (340, (0, 229, 255, 45), 2),
        (285, (59, 130, 246, 70), 3),
        (230, (139, 92, 246, 55), 2),
        (175, (0, 229, 255, 35), 1),
    ]:
        cdraw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=width)

    # Các đường mạch điện tử (Circuit Lines) & Node phát sáng
    circuit_paths = [
        [(0, 140), (260, 140), (310, 90), (680, 90)],
        [(0, 960), (420, 960), (470, 910), (920, 910)],
        [(1120, 980), (1650, 980), (1710, 920), (1920, 920)],
        [(1350, 70), (1740, 70), (1790, 120), (1920, 120)],
    ]
    for path in circuit_paths:
        cdraw.line(path, fill=(0, 229, 255, 70), width=2)
        ex, ey = path[-1]
        cdraw.ellipse((ex - 5, ey - 5, ex + 5, ey + 5), fill=(0, 229, 255, 160))

    # Khung góc HUD (Corner Brackets)
    b_col = (0, 229, 255, 150)
    cdraw.line([(36, 90), (36, 36), (110, 36)], fill=b_col, width=3)
    cdraw.line([(w - 110, 36), (w - 36, 36), (w - 36, 90)], fill=b_col, width=3)
    cdraw.line([(36, h - 90), (36, h - 36), (110, h - 36)], fill=b_col, width=3)
    cdraw.line([(w - 110, h - 36), (w - 36, h - 36), (w - 36, h - 90)], fill=b_col, width=3)

    cover_path = BG_DIR / "bg_cover_pikbest.png"
    cover.convert("RGB").save(cover_path, quality=95)

    # --- B. Nền trang nội dung (Content Slide Background) ---
    content = Image.new("RGBA", (w, h), (7, 11, 25, 255))
    cglow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cgdraw = ImageDraw.Draw(cglow)
    cgdraw.ellipse((1350, -250, 2100, 500), fill=(0, 195, 255, 38))
    cgdraw.ellipse((-250, 600, 550, 1300), fill=(99, 102, 241, 32))
    cglow = cglow.filter(ImageFilter.GaussianBlur(radius=100))
    content = Image.alpha_composite(content, cglow)

    draw = ImageDraw.Draw(content)
    # Lưới mảnh hiện đại
    for x in range(0, w, 96):
        draw.line([(x, 0), (x, h)], fill=(30, 58, 138, 18), width=1)
    for y in range(0, h, 96):
        draw.line([(0, y), (w, y)], fill=(30, 58, 138, 18), width=1)

    # Thanh HUD trang trí trên cùng & dưới cùng
    draw.line([(60, 112), (1860, 112)], fill=(30, 64, 175, 90), width=1)
    draw.line([(60, 112), (380, 112)], fill=(0, 229, 255, 190), width=3)
    draw.line([(60, 1028), (1860, 1028)], fill=(30, 64, 175, 80), width=1)
    draw.line([(1650, 1028), (1860, 1028)], fill=(0, 229, 255, 160), width=2)

    # Góc HUD mảnh
    draw.line([(28, 65), (28, 24), (75, 24)], fill=(0, 229, 255, 110), width=2)
    draw.line([(w - 75, 24), (w - 28, 24), (w - 28, 65)], fill=(0, 229, 255, 110), width=2)

    content_path = BG_DIR / "bg_content_pikbest.png"
    content.convert("RGB").save(content_path, quality=95)
    return cover_path, content_path


# ---------------------------------------------------------------------------
# 2. CÁC HÀM TIỆN ÍCH VẼ SLIDE CHUẨN DESIGN SYSTEM
# ---------------------------------------------------------------------------
def set_slide_bg(slide, bg_path: Path):
    slide.shapes.add_picture(str(bg_path), Inches(0), Inches(0), Inches(13.333), Inches(7.5))


def add_textbox(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    text: str = "",
    font_size: float = 14,
    color: RGBColor = C_TEXT,
    bold: bool = False,
    italic: bool = False,
    font_name: str = FONT_MAIN,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    line_spacing: float = 1.15,
):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    return box


def add_card(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    fill_color: RGBColor = C_CARD_BG,
    border_color: RGBColor = C_BORDER,
    border_pt: float = 1.2,
    shape_type=MSO_SHAPE.ROUNDED_RECTANGLE,
    accent_top_color: RGBColor = None,
    accent_left_color: RGBColor = None,
):
    shape = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE and len(shape.adjustments) > 0:
        shape.adjustments[0] = 0.035

    if accent_top_color:
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left + 0.08), Inches(top), Inches(width - 0.16), Inches(0.055)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_top_color
        bar.line.fill.background()

    if accent_left_color:
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top + 0.08), Inches(0.065), Inches(height - 0.16)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_left_color
        bar.line.fill.background()

    return shape


def add_pill(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    text: str,
    fill_color: RGBColor = C_BLUE,
    text_color: RGBColor = C_WHITE,
    border_color: RGBColor = None,
    font_size: float = 10.5,
    bold: bool = True,
):
    pill = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    pill.fill.solid()
    pill.fill.fore_color.rgb = fill_color
    if border_color:
        pill.line.color.rgb = border_color
        pill.line.width = Pt(1.0)
    else:
        pill.line.fill.background()
    if len(pill.adjustments) > 0:
        pill.adjustments[0] = 0.5
    tf = pill.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_MAIN
    r.font.size = Pt(font_size)
    r.font.color.rgb = text_color
    r.font.bold = bold
    return pill


def add_bullet_list(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    items: list,
    font_size: float = 12.5,
    space_after: float = 6,
    bullet_color: RGBColor = C_CYAN,
    title_color: RGBColor = C_WHITE,
    body_color: RGBColor = C_TEXT,
):
    """
    items: danh sách tuple (bold_prefix, regular_text) hoặc chuỗi đơn.
    """
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)

    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.line_spacing = 1.15

        r_bul = p.add_run()
        r_bul.text = "▸ "
        r_bul.font.name = FONT_MAIN
        r_bul.font.size = Pt(font_size)
        r_bul.font.bold = True
        r_bul.font.color.rgb = bullet_color

        if isinstance(item, (tuple, list)):
            head, body = item[0], item[1]
            if head:
                r_head = p.add_run()
                r_head.text = head + (" " if body else "")
                r_head.font.name = FONT_MAIN
                r_head.font.size = Pt(font_size)
                r_head.font.bold = True
                r_head.font.color.rgb = title_color
            if body:
                r_body = p.add_run()
                r_body.text = body
                r_body.font.name = FONT_MAIN
                r_body.font.size = Pt(font_size)
                r_body.font.bold = False
                r_body.font.color.rgb = body_color
        else:
            r_body = p.add_run()
            r_body.text = str(item)
            r_body.font.name = FONT_MAIN
            r_body.font.size = Pt(font_size)
            r_body.font.color.rgb = body_color
    return box


def add_header_and_footer(
    slide,
    bg_path: Path,
    slide_num: int,
    total_slides: int,
    section_tag: str,
    title: str,
    subtitle: str = "",
    notes: str = "",
):
    set_slide_bg(slide, bg_path)

    # Tag phân mục kiểu Pikbest AI
    add_pill(
        slide,
        left=0.42,
        top=0.22,
        width=2.95,
        height=0.28,
        text=section_tag,
        fill_color=RGBColor(14, 34, 68),
        text_color=C_CYAN,
        border_color=C_CYAN,
        font_size=9.5,
        bold=True,
    )

    # Badge số thứ tự góc phải trên
    add_pill(
        slide,
        left=11.75,
        top=0.22,
        width=1.15,
        height=0.28,
        text=f"SLIDE {slide_num:02d}/{total_slides:02d}",
        fill_color=RGBColor(18, 30, 58),
        text_color=C_MUTED,
        border_color=C_BORDER,
        font_size=9.5,
        bold=True,
    )

    # Tiêu đề trang
    add_textbox(
        slide,
        left=0.42,
        top=0.52,
        width=9.2,
        height=0.45,
        text=title,
        font_size=22,
        color=C_WHITE,
        bold=True,
    )

    # Phụ đề ngắn bên phải hoặc ngay dưới
    if subtitle:
        add_textbox(
            slide,
            left=7.15,
            top=0.22,
            width=4.45,
            height=0.28,
            text=subtitle,
            font_size=10,
            color=C_MUTED,
            italic=True,
            align=PP_ALIGN.RIGHT,
            valign=MSO_ANCHOR.MIDDLE,
        )

    # Footer công nghệ
    add_textbox(
        slide,
        left=0.42,
        top=7.16,
        width=7.5,
        height=0.25,
        text="BUDDY AI ECOSYSTEM  |  ĐỒ ÁN TRỢ LÝ AI ĐỒNG HÀNH, ĐIỀU KHIỂN THIẾT BỊ & TỰ ĐỘNG HÓA LẬP TRÌNH",
        font_size=8.5,
        color=C_MUTED,
    )
    add_textbox(
        slide,
        left=9.5,
        top=7.16,
        width=3.4,
        height=0.25,
        text=f"AI TECHNOLOGY REPORT • PAGE {slide_num:02d}",
        font_size=8.5,
        color=C_CYAN,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )

    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def safe_add_image(slide, rel_path: str, left: float, top: float, width: float = None, height: float = None):
    img_path = ROLLBACK_DIR / rel_path
    if not img_path.exists():
        return None
    with Image.open(img_path) as im:
        iw, ih = im.size
    aspect = iw / ih
    if width and height:
        # Căn vừa khung (contain) không làm méo ảnh
        box_aspect = width / height
        if aspect > box_aspect:
            w = width
            h = width / aspect
            left_adj = left
            top_adj = top + (height - h) / 2
        else:
            h = height
            w = height * aspect
            left_adj = left + (width - w) / 2
            top_adj = top
        return slide.shapes.add_picture(str(img_path), Inches(left_adj), Inches(top_adj), Inches(w), Inches(h))
    elif width:
        return slide.shapes.add_picture(str(img_path), Inches(left), Inches(top), width=Inches(width))
    elif height:
        return slide.shapes.add_picture(str(img_path), Inches(left), Inches(top), height=Inches(height))
    return None


# ---------------------------------------------------------------------------
# 3. XÂY DỰNG 13 SLIDE NỘI DUNG CHI TIẾT
# ---------------------------------------------------------------------------
def build_presentation():
    cover_bg, content_bg = generate_tech_backgrounds()
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    total_slides = 13

    # =========================================================================
    # SLIDE 01: TRANG BÌA (COVER SLIDE - PIKBEST AI STYLE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, cover_bg)

    add_pill(
        s1, 0.72, 0.75, 4.15, 0.36,
        "ARTIFICIAL INTELLIGENCE  •  CAPSTONE PROJECT 2026",
        fill_color=RGBColor(14, 34, 68), text_color=C_CYAN, border_color=C_CYAN, font_size=10.5
    )

    add_textbox(
        s1, 0.72, 1.32, 7.6, 1.85,
        text="HỆ SINH THÁI TRỢ LÝ AI\nĐỒNG HÀNH & ĐIỀU KHIỂN\nTHIẾT BỊ — BUDDY AI",
        font_size=36, color=C_WHITE, bold=True, line_spacing=1.08
    )

    add_textbox(
        s1, 0.72, 3.35, 7.3, 0.85,
        text="Kiến trúc Đa phương thức (Voice · Vision · Desktop Control · Agentic Coding)\nTối ưu hóa Thuật toán NLU/ASR Tiếng Việt & Runtime Nhẹ cho Máy tính Cá nhân",
        font_size=15, color=C_CYAN, bold=True, line_spacing=1.25
    )

    # 4 thẻ thông số nổi bật ở trang bìa
    cover_pills = [
        ("01 // KIẾN TRÚC", "Web Lite + Electron Robot + OpenClaw", C_CYAN),
        ("02 // THUẬT TOÁN", "CRF-Viterbi NLU · LoRA ASR · AST Edit", C_BLUE),
        ("03 // HIỆU SUẤT", "95.54% Intent · 181/181 Unit Suites", C_EMERALD),
        ("04 // TỐI ƯU HÓA", "JS Bundle ~315KB · Lệnh nhanh <600ms", C_PURPLE),
    ]
    for idx, (tag, desc, col) in enumerate(cover_pills):
        col_idx = idx % 2
        row_idx = idx // 2
        cx = 0.72 + col_idx * 3.72
        cy = 4.42 + row_idx * 1.05
        add_card(s1, cx, cy, 3.55, 0.90, fill_color=C_CARD_BG, border_color=col, border_pt=1.3, accent_left_color=col)
        add_textbox(s1, cx + 0.16, cy + 0.10, 3.25, 0.28, tag, font_size=10, color=col, bold=True)
        add_textbox(s1, cx + 0.16, cy + 0.40, 3.25, 0.42, desc, font_size=12, color=C_WHITE, bold=True)

    # Khung Robot 3D bên phải
    add_card(
        s1, 8.55, 0.95, 4.15, 5.55,
        fill_color=RGBColor(12, 22, 46), border_color=C_CYAN, border_pt=1.5, accent_top_color=C_CYAN
    )
    safe_add_image(s1, "public/images/buddy-robot-3d-v2.png", 8.75, 1.15, 3.75, 4.35)
    add_textbox(
        s1, 8.70, 5.55, 3.85, 0.35,
        "BUDDY 3D DESKTOP COMPANION", font_size=13, color=C_CYAN, bold=True, align=PP_ALIGN.CENTER
    )
    add_textbox(
        s1, 8.70, 5.88, 3.85, 0.50,
        "Qwen3-VL · PhoWhisper · Devstral-24B\nWindows Desktop & Web Workspace",
        font_size=10.5, color=C_MUTED, align=PP_ALIGN.CENTER
    )

    add_textbox(
        s1, 0.72, 6.78, 11.9, 0.35,
        "BÁO CÁO KỸ THUẬT ĐỒ ÁN: GIỚI THIỆU  •  CHỨC NĂNG  •  THUẬT TOÁN  •  HIỆU SUẤT  •  TỐI ƯU HÓA   |   SLIDE 01/13",
        font_size=10, color=C_MUTED, bold=True
    )
    s1.notes_slide.notes_text_frame.text = (
        "Xin chào Hội đồng và các bạn. Hôm nay mình xin trình bày đồ án Hệ sinh thái Trợ lý AI Đồng hành "
        "và Điều khiển Thiết bị — Buddy AI. Bài trình bày gồm 13 trang, đi sâu vào 5 trụ cột: Giới thiệu bài toán, "
        "Hệ thống chức năng đa không gian, Các thuật toán cốt lõi (NLU, ASR, Retrieval, Agentic Coding), "
        "Số liệu đánh giá hiệu suất thực nghiệm và Các kỹ thuật tối ưu hóa hệ thống."
    )

    # =========================================================================
    # SLIDE 02: MỤC LỤC & CẤU TRÚC BÁO CÁO (AGENDA - 5 PILLARS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s2, content_bg, 2, total_slides,
        "00 // STRUCTURE & AGENDA",
        "Cấu Trúc Nội Dung Đồ Án (5 Trụ Cột Kỹ Thuật)",
        "Bố cục 13 trang chuyên sâu: Giới thiệu · Chức năng · Thuật toán · Hiệu suất · Tối ưu",
        "Slide 2 trình bày lộ trình 5 phần chính của báo cáo kỹ thuật đồ án Buddy AI."
    )

    agenda_items = [
        (
            "01", "GIỚI THIỆU & KIẾN TRÚC HỆ THỐNG", "Slides 03 – 04", C_CYAN,
            [
                ("Bối cảnh & Động lực:", "Giải quyết sự phân mảnh công cụ học tập, làm việc và điều khiển máy tính."),
                ("Kiến trúc Đa tầng:", "Kết hợp Web Workspace (Node Lite/Next.js), Electron Robot nổi và AI Gateway."),
            ]
        ),
        (
            "02", "HỆ THỐNG CHỨC NĂNG ĐA KHÔNG GIAN", "Slides 05 – 07", C_BLUE,
            [
                ("Buddy Study & Life:", "Quản lý tài liệu, hỏi đáp trích nguồn, Quiz điền từ, lịch Pomodoro, thu chi VND."),
                ("Desktop Bot & Buddy Coder:", "Robot giọng nói/camera, điều khiển ứng dụng Windows & Agent lập trình tự sửa lỗi."),
            ]
        ),
        (
            "03", "THUẬT TOÁN CỐT LÕI (AI / NLU / AGENT)", "Slides 08 – 10", C_PURPLE,
            [
                ("Xử lý Tiếng Việt (SLU/ASR):", "LinearSVC + Context-CRF, giải mã Viterbi ràng buộc BIO, Ensemble V7 & BamiBERT."),
                ("Retrieval & Code Edit Engine:", "Tìm kiếm từ khóa không dấu, lập lịch deadline, khớp sửa code 3 tầng & vòng lặp Verify."),
            ]
        ),
        (
            "04", "ĐÁNH GIÁ HIỆU SUẤT & THỰC NGHIỆM", "Slides 11 – 12", C_EMERALD,
            [
                ("Benchmark Mô hình AI:", "So sánh thực nghiệm trên 12.979 câu train / 1.345 câu dev VN-SLU & 244 mẫu audio."),
                ("Kiểm thử Hệ thống (QA):", "181/181 file unit test PASS, độ trễ điều khiển Windows 236–598ms, Coder Tier-1 Live PASS."),
            ]
        ),
        (
            "05", "KỸ THUẬT TỐI ƯU HÓA & ĐỊNH HƯỚNG", "Slide 13", C_AMBER,
            [
                ("Tối ưu Tài nguyên & Độ trễ:", "Node Lite (~315KB JS), Fast-path routing, LoRA 96 tensors, nén ngữ cảnh cửa sổ trượt 85%."),
                ("An toàn & Lộ trình:", "Shadow Git checkpoint khôi phục từng byte, Quota reservation/refund & hướng mở rộng."),
            ]
        ),
    ]

    for i, (num, heading, sl_range, col, bullets) in enumerate(agenda_items):
        y = 1.15 + i * 1.14
        add_card(s2, 0.42, y, 12.48, 1.02, fill_color=C_CARD_BG, border_color=col, border_pt=1.2, accent_left_color=col)
        add_pill(s2, 0.62, y + 0.22, 0.85, 0.56, num, fill_color=col, text_color=C_BG_DEEP, font_size=18, bold=True)
        add_textbox(s2, 1.62, y + 0.14, 4.2, 0.36, heading, font_size=14.5, color=C_WHITE, bold=True)
        add_pill(s2, 1.62, y + 0.54, 1.55, 0.30, sl_range, fill_color=C_CARD_ALT, text_color=col, border_color=col, font_size=9.5)
        add_bullet_list(s2, 5.85, y + 0.12, 6.9, 0.82, bullets, font_size=11.5, space_after=3, bullet_color=col)

    # =========================================================================
    # SLIDE 03: GIỚI THIỆU TỔNG QUAN & BÀI TOÁN ĐẶT RA (INTRODUCTION)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s3, content_bg, 3, total_slides,
        "01 // INTRODUCTION & VISION",
        "Giới Thiệu Đồ Án: Bài Toán Thực Tiễn & Định Vị Giải Pháp Buddy AI",
        "Trợ lý AI đồng hành đa phương thức cho sinh viên & người dùng máy tính Windows",
        "Slide 3 giới thiệu bài toán thực tế, các hạn chế của công cụ rời rạc và tầm nhìn của hệ thống Buddy AI."
    )

    # Cột trái: 3 thách thức thực tế
    add_card(s3, 0.42, 1.15, 4.15, 5.82, fill_color=C_CARD_BG, border_color=C_AMBER, accent_top_color=C_AMBER)
    add_textbox(s3, 0.62, 1.32, 3.75, 0.38, "1. BÀI TOÁN & THÁCH THỨC HIỆN TẠI", font_size=14.5, color=C_AMBER, bold=True)
    add_bullet_list(
        s3, 0.62, 1.78, 3.78, 5.0,
        [
            ("Phân mảnh không gian làm việc:", "Tài liệu PDF/DOCX, lịch học, ghi chú, quản lý chi tiêu và công cụ lập trình nằm rời rạc ở nhiều ứng dụng khác nhau."),
            ("Khoảng cách từ Hỏi–Đáp đến Hành động:", "Các chatbot thuần văn bản không thể trực tiếp mở ứng dụng Windows, kiểm tra thư mục hay chạy kiểm thử mã nguồn trên máy."),
            ("Rào cản Tiếng Việt & Giọng nói:", "Nhận dạng lệnh giọng nói tiếng Việt pha thuật ngữ tiếng Anh (tên bài hát, thư mục, lệnh kỹ thuật) dễ sai lệch thực thể."),
            ("Giới hạn Phần cứng Cá nhân:", "Máy tính sinh viên phổ biến chỉ có 8 GB RAM / GPU 4 GB, đòi hỏi kiến trúc cực nhẹ thay vì phụ thuộc hoàn toàn vào đám mây đắt đỏ."),
            ("Rủi ro Quyền riêng tư & Bảo mật:", "Cấp quyền camera, microphone hoặc điều khiển máy cho AI nếu thiếu cơ chế kiểm soát sẽ gây nguy cơ lộ dữ liệu và thực thi lệnh nguy hiểm."),
        ],
        font_size=11.8, space_after=8, bullet_color=C_AMBER
    )

    # Cột giữa: Định vị Giải pháp Buddy AI
    add_card(s3, 4.72, 1.15, 4.45, 5.82, fill_color=C_CARD_ALT, border_color=C_CYAN, accent_top_color=C_CYAN)
    add_textbox(s3, 4.92, 1.32, 4.05, 0.38, "2. ĐỊNH VỊ GIẢI PHÁP: BUDDY AI ECOSYSTEM", font_size=14.5, color=C_CYAN, bold=True)
    add_textbox(
        s3, 4.92, 1.75, 4.05, 0.72,
        "“Biến tài liệu, deadline và yêu cầu bằng giọng nói thành hành động có thể kiểm chứng ngay trên Web và Desktop Windows.”",
        font_size=12, color=C_WHITE, bold=True, italic=True
    )
    add_bullet_list(
        s3, 4.92, 2.52, 4.05, 4.3,
        [
            ("Web Workspace + Robot Nổi (Electron):", "Kết hợp không gian học tập toàn diện trên trình duyệt với Robot 3D luôn nổi trên màn hình Windows."),
            ("Đa phương thức (Voice + Vision + Text):", "Nghe tiếng Việt qua PhoWhisper, suy luận ngôn ngữ–thị giác với Qwen3-VL và phản hồi giọng đọc Piper TTS tự nhiên."),
            ("Điều khiển Thiết bị Có Kiểm soát:", "Thực thi công cụ mở ứng dụng, trình duyệt, tìm kiếm YouTube, đọc thư mục với cơ chế cấp quyền theo tài khoản."),
            ("Tích hợp Không gian Lập trình (Buddy Coder):", "Hỗ trợ duyệt dự án, phân tích AST, tự động vá lỗi và chạy kiểm thử an toàn với mô hình Devstral-24B."),
        ],
        font_size=11.8, space_after=8, bullet_color=C_CYAN
    )

    # Cột phải: Hình ảnh trực quan từ dự án
    add_card(s3, 9.32, 1.15, 3.58, 5.82, fill_color=C_CARD_BG, border_color=C_BLUE, accent_top_color=C_BLUE)
    add_textbox(s3, 9.48, 1.32, 3.25, 0.35, "3. GIAO DIỆN & NHÂN VẬT ĐỒNG HÀNH", font_size=13.5, color=C_BLUE, bold=True)
    safe_add_image(s3, "artifacts/intro-ai.png", 9.48, 1.75, 3.26, 2.15)
    safe_add_image(s3, "public/images/buddy-tutor-3d.png", 9.85, 4.02, 2.50, 2.15)
    add_textbox(
        s3, 9.48, 6.22, 3.26, 0.65,
        "Trải nghiệm Intro Học tập × AI (Canvas/CSS 7.6s) & Mascot 3D tương tác theo chuyển động chuột.",
        font_size=10.5, color=C_MUTED, align=PP_ALIGN.CENTER
    )

    # =========================================================================
    # SLIDE 04: KIẾN TRÚC TỔNG THỂ HỆ THỐNG (SYSTEM ARCHITECTURE)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s4, content_bg, 4, total_slides,
        "01 // SYSTEM ARCHITECTURE",
        "Kiến Trúc Tổng Thể Đa Tầng & Luồng Xử Lý Dữ Liệu (End-to-End)",
        "Thiết kế Modular kết hợp Local-First Runtime với AI/Voice Gateway chuyên biệt",
        "Slide 4 mô tả kiến trúc 4 tầng của hệ thống Buddy từ giao diện người dùng, cổng điều phối bảo mật đến lưu trữ và suy luận AI."
    )

    layers = [
        (
            "TẦNG 1: GIAO DIỆN & TƯƠNG TÁC ĐA KÊNH (CLIENT & INTERACTION LAYER)",
            C_CYAN,
            [
                ("Buddy Web Workspace", "React 19 + TypeScript (Node Lite / Next.js), phím tắt Ctrl+K, giao diện học tập & quản trị."),
                ("Electron Desktop Robot", "Cửa sổ trong suốt luôn nổi (Always-on-top), khay hệ thống (Ctrl+Alt+B), đồng bộ Web Locks."),
                ("Buddy Coder & WebViews", "IDE thu gọn trên trình duyệt & tối đa 6 tab WebContentsView cô lập trong Electron."),
            ]
        ),
        (
            "TẦNG 2: ĐIỀU PHỐI, BẢO MẬT & THỰC THI CÔNG CỤ (ORCHESTRATION & SECURITY GATE)",
            C_BLUE,
            [
                ("Authenticated API & OpenClaw", "Xác thực scrypt+salt, cookie HttpOnly, chống CSRF origin, giới hạn tốc độ (Rate Limit)."),
                ("AI Security & Safety Gate", "Quét Prompt Injection bằng Protect AI DeBERTa-v3 & phân loại an toàn Qwen3Guard 0.6B."),
                ("Action Planner & Executor", "Bộ định tuyến lệnh nhanh (Fast-path), kiểm tra quyền thư mục, chạy npm script cô lập."),
            ]
        ),
        (
            "TẦNG 3: DỮ LIỆU, TRẠNG THÁI & KHÔI PHỤC (PERSISTENCE & STATE MANAGEMENT)",
            C_PURPLE,
            [
                ("Dual Database Adapter", "SQLite (Node built-in local) & PostgreSQL (Neon Cloud) dùng chung schema tham số hóa."),
                ("Quota & Billing Engine", "Cơ chế giữ chỗ/hoàn trả hạn mức (Reservation/Refund 1M token), tích hợp webhook payOS."),
                ("Shadow Git Checkpoints", "Nhánh Git ẩn độc lập lưu ảnh chụp mã nguồn trước mỗi lần sửa, khôi phục chính xác từng byte."),
            ]
        ),
        (
            "TẦNG 4: HẠ TẦNG MÔ HÌNH AI, GIỌNG NÓI & THỊ GIÁC (MULTIMODAL AI INFERENCE LAYER)",
            C_EMERALD,
            [
                ("Ngôn ngữ & Thị giác (LLM/VLM)", "Qwen3-1.7B (llama.cpp Vulkan/Ollama), Qwen3-VL 4B/9B & Devstral-Small-2 24B (Modal Gateway)."),
                ("Nhận dạng Tiếng nói (ASR/STT)", "PhoWhisper & Qwen3-ASR 1.7B tinh chỉnh LoRA + Bộ phân tích NLU Context-CRF / Viterbi."),
                ("Tổng hợp Giọng đọc & Camera", "Piper TTS tiếng Việt cục bộ / SpeechSynthesis + Xử lý tín hiệu khuôn mặt tại máy client."),
            ]
        ),
    ]

    for idx, (l_title, col, subcards) in enumerate(layers):
        y = 1.12 + idx * 1.48
        add_card(s4, 0.42, y, 12.48, 1.36, fill_color=C_CARD_BG, border_color=col, border_pt=1.2, accent_left_color=col)
        add_textbox(s4, 0.62, y + 0.06, 12.1, 0.28, l_title, font_size=11.5, color=col, bold=True)
        for j, (sc_title, sc_desc) in enumerate(subcards):
            sx = 0.62 + j * 4.06
            sy = y + 0.36
            add_card(s4, sx, sy, 3.92, 0.90, fill_color=C_CARD_ALT, border_color=C_BORDER, border_pt=0.8)
            add_textbox(s4, sx + 0.12, sy + 0.06, 3.68, 0.26, sc_title, font_size=11.5, color=C_WHITE, bold=True)
            add_textbox(s4, sx + 0.12, sy + 0.34, 3.68, 0.50, sc_desc, font_size=10.2, color=C_TEXT)

    # =========================================================================
    # SLIDE 05: CHỨC NĂNG (1) - KHÔNG GIAN HỌC TẬP & CÁ NHÂN HÓA
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s5, content_bg, 5, total_slides,
        "02 // CORE FEATURES: STUDY & WORKSPACE",
        "Chức Năng (1): Không Gian Học Tập Thông Minh & Quản Lý Cá Nhân",
        "Chu trình khép kín: Tài liệu → Hỏi đáp có trích dẫn → Luyện Quiz → Lập lịch ôn → Theo dõi tiến độ",
        "Slide 5 trình bày chi tiết 6 phân hệ chức năng trong không gian học tập và sinh hoạt dành cho sinh viên."
    )

    study_features = [
        ("1. Thư Viện Tài Liệu & Trích Xuất", C_CYAN,
         "Hỗ trợ tải lên PDF có lớp văn bản (parser PDF.js v2.0.550 với Uint8Array), DOCX, TXT, MD, CSV (tối đa 10 MB / 250.000 ký tự). Đọc toàn văn, lọc/sắp xếp và tải bản text trích xuất."),
        ("2. Hỏi Đáp AI Kèm Nguồn Kiểm Chứng", C_BLUE,
         "Trò chuyện trực tiếp trên tài liệu đã tải. AI kết hợp 12 tin nhắn gần nhất, trí nhớ, lịch học và đoạn trích khớp từ khóa; chỉ gắn nhãn trích dẫn khi có đoạn nguồn thực sự."),
        ("3. Luyện Tập Quiz Điền Từ Chủ Động", C_PURPLE,
         "Tự động sinh câu hỏi điền khuyết từ câu gốc của tài liệu. Ẩn đáp án trên API trước khi nộp bài, chặn chấm lặp, lưu lịch sử điểm số và giải thích chi tiết từng câu."),
        ("4. Lịch Học, Planner & Pomodoro", C_EMERALD,
         "Quản lý công việc theo môn học/trạng thái (đang làm, quá hạn, hoàn thành). Tự động chia phiên ôn tập theo hạn chót, đồng hồ Pomodoro 50/5 phút và xuất tệp chuẩn .ICS."),
        ("5. Quản Lý Thu Chi Cá Nhân (VND)", C_AMBER,
         "Ghi nhận các khoản thu/chi theo danh mục, kiểm tra số tiền hợp lệ, thống kê tổng tháng và biểu đồ tỷ trọng chi tiêu. AI không tự ý tạo giao dịch tài chính nếu chưa xác nhận."),
        ("6. Trí Nhớ Ngữ Cảnh & Kết Nối Google", C_CYAN,
         "Người dùng chủ động lưu/xóa mục tiêu học tập vào bộ nhớ AI. Hỗ trợ Google Calendar/Gmail OAuth để xem lịch, thêm sự kiện và tạo email nháp sau bước duyệt."),
    ]

    for idx, (ftitle, col, fdesc) in enumerate(study_features):
        r = idx // 2
        c = idx % 2
        fx = 0.42 + c * 3.88
        fy = 1.15 + r * 1.94
        add_card(s5, fx, fy, 3.74, 1.80, fill_color=C_CARD_BG, border_color=col, accent_top_color=col)
        add_textbox(s5, fx + 0.14, fy + 0.12, 3.46, 0.32, ftitle, font_size=12.5, color=col, bold=True)
        add_textbox(s5, fx + 0.14, fy + 0.48, 3.46, 1.22, fdesc, font_size=10.8, color=C_TEXT, line_spacing=1.18)

    # Khung ảnh chụp màn hình thực tế bên phải
    add_card(s5, 8.22, 1.15, 4.68, 5.68, fill_color=C_CARD_ALT, border_color=C_CYAN, accent_top_color=C_CYAN)
    add_textbox(s5, 8.38, 1.28, 4.36, 0.32, "GIAO DIỆN AGENT WORKSPACE THỰC TẾ", font_size=12.5, color=C_CYAN, bold=True)
    safe_add_image(s5, "artifacts/agent-overview.png", 8.36, 1.68, 4.40, 3.10)
    add_bullet_list(
        s5, 8.38, 4.90, 4.36, 1.80,
        [
            ("Tìm kiếm nhanh (Ctrl+K):", "Mở công cụ hoặc chuyển thẳng câu hỏi vào luồng hội thoại."),
            ("Quy trình 5 bước:", "Ôn thi, sắp xếp tuần, cân bằng thu chi với checklist trực quan."),
            ("Tương thích đa thiết bị:", "Giao diện đáp ứng (Responsive) trên cả màn hình máy tính và di động."),
        ],
        font_size=10.8, space_after=4, bullet_color=C_CYAN
    )

    # =========================================================================
    # SLIDE 06: CHỨC NĂNG (2) - ROBOT DESKTOP, GIỌNG NÓI & ĐIỀU KHIỂN MÁY
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s6, content_bg, 6, total_slides,
        "02 // CORE FEATURES: DESKTOP ROBOT & MULTIMODAL",
        "Chức Năng (2): Robot Desktop Nổi, Giọng Nói Tiếng Việt & Điều Khiển Máy",
        "Đồng hành liên tục ngoài trình duyệt với Electron, PhoWhisper STT, Piper TTS & Qwen3-VL",
        "Slide 6 mô tả khả năng của Robot nổi trên Windows, luồng hội thoại giọng nói, thị giác camera và điều khiển ứng dụng."
    )

    # Cột trái: Ảnh chụp Robot Desktop & Thông số tương tác
    add_card(s6, 0.42, 1.15, 4.55, 5.75, fill_color=C_CARD_BG, border_color=C_CYAN, accent_top_color=C_CYAN)
    add_textbox(s6, 0.58, 1.28, 4.22, 0.34, "ROBOT ELECTRON NỔI TRÊN WINDOWS", font_size=13, color=C_CYAN, bold=True)
    safe_add_image(s6, "artifacts/robot-interactive-dashboard.png", 0.58, 1.68, 4.22, 2.75)
    add_bullet_list(
        s6, 0.58, 4.52, 4.22, 2.25,
        [
            ("Cửa sổ trong suốt luôn nổi:", "Hoạt động độc lập ngay cả khi đóng trình duyệt; phím nóng Ctrl+Alt+B gọi nhanh từ khay hệ thống."),
            ("Đồng bộ chống trùng lặp:", "Tự động ẩn robot trên web khi bản Desktop đang chạy; quản lý phiên bằng Web Locks."),
            ("Chuyển động 3D mượt mà:", "Tương tác nghiêng theo con trỏ chuột bằng requestAnimationFrame & biến CSS; tôn trọng prefers-reduced-motion."),
        ],
        font_size=10.8, space_after=5, bullet_color=C_CYAN
    )

    # Cột phải: 3 khối chức năng chuyên sâu
    desktop_blocks = [
        (
            "1. Hội Thoại Giọng Nói Tiếng Việt Theo Lượt (Voice Pipeline)",
            C_BLUE,
            [
                ("Luồng xử lý khép kín:", "Thu âm MediaRecorder → Nhận dạng PhoWhisper / Qwen3-ASR → Suy luận AI → Đọc phản hồi bằng Piper TTS / SpeechSynthesis rồi tự động mở lượt nghe tiếp theo."),
                ("Kiểm soát chủ động:", "Hỗ trợ bấm mic để ngắt lời (barge-in thủ công), chế độ “Nói rồi sửa lời trước khi gửi” khi gặp tên bài hát tiếng Anh hoặc từ chuyên ngành."),
            ]
        ),
        (
            "2. Quan Sát Qua Camera Cục Bộ & Nhắc Học Thông Minh",
            C_PURPLE,
            [
                ("Xử lý tín hiệu khuôn mặt tại máy:", "Nhận diện sự hiện diện, hướng nhìn, nét cười, mắt nhắm lâu hoặc ngáp lặp lại ngay trên thiết bị mà không tải video nền lên máy chủ."),
                ("Phân tích hình ảnh theo yêu cầu:", "Tính năng “Chụp ảnh / Xem màn hình để hỏi Buddy” gửi ảnh đã duyệt tới mô hình thị giác Qwen3-VL 4B và không lưu ngầm vào lịch sử."),
                ("Đồng hành & Nhắc nghỉ (25/50/90 phút):", "Đếm thời gian hoạt động thực tế, tự động hoãn lời nhắc trong giờ yên lặng (22:00–07:00) hoặc khi người dùng đang nói."),
            ]
        ),
        (
            "3. Thực Thi Lệnh Điều Khiển Máy Tính Có Kiểm Soát (Desktop Control)",
            C_EMERALD,
            [
                ("Danh mục công cụ được cấp quyền:", "Mở ứng dụng (Chrome, Edge, VS Code, Calculator, Notepad, Explorer, Paint, Office), mở URL/tìm kiếm YouTube, đọc & tóm tắt thư mục, tạo ghi chú."),
                ("Bảo mật cấp quyền theo tài khoản:", "Quyền lưu tại data/desktop-permissions.json gắn với chủ máy; hỗ trợ chế độ xem trước xác nhận hoặc tự thực hiện tối đa 4 bước."),
            ]
        ),
    ]

    for idx, (btitle, col, bitems) in enumerate(desktop_blocks):
        by = 1.15 + idx * 1.94
        add_card(s6, 5.15, by, 7.75, 1.82, fill_color=C_CARD_BG, border_color=col, accent_left_color=col)
        add_textbox(s6, 5.35, by + 0.08, 7.40, 0.30, btitle, font_size=12.5, color=col, bold=True)
        add_bullet_list(s6, 5.35, by + 0.40, 7.40, 1.35, bitems, font_size=10.8, space_after=4, bullet_color=col)

    # =========================================================================
    # SLIDE 07: CHỨC NĂNG (3) - BUDDY CODER & QUẢN TRỊ BẢO MẬT
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s7, content_bg, 7, total_slides,
        "02 // CORE FEATURES: BUDDY CODER & SECURITY",
        "Chức Năng (3): Không Gian Lập Trình Buddy Coder & Quản Trị Hệ Thống",
        "Kết hợp Agentic Coding (Devstral-24B / OpenCode) với cơ chế bảo mật đa lớp",
        "Slide 7 giới thiệu phân hệ lập trình Buddy Coder, kiến trúc hai nhánh Agent và hệ thống quản trị Admin/Security."
    )

    # Cột trái: Buddy Coder & CodexEngine
    add_card(s7, 0.42, 1.15, 6.20, 5.75, fill_color=C_CARD_BG, border_color=C_CYAN, accent_top_color=C_CYAN)
    add_textbox(s7, 0.62, 1.30, 5.80, 0.35, "PHÂN HỆ LẬP TRÌNH: BUDDY CODER & CODEX ENGINE", font_size=13.5, color=C_CYAN, bold=True)
    add_bullet_list(
        s7, 0.62, 1.72, 5.80, 5.05,
        [
            ("Duyệt dự án & Ngữ cảnh thông minh:", "Mở thư mục được cấp quyền, lọc cây thư mục (tự động loại trừ .env, node_modules, khóa OAuth), hỗ trợ @file, @folder, @symbol, @problems, @git-diff."),
            ("Đề xuất sửa đổi & Xem trước Inline Diff:", "Tạo bản vá tối đa 6 tệp/lượt với giao diện so sánh dòng trước/sau trực quan; kiểm tra mã băm SHA-256 chống ghi đè tệp đã bị sửa ngoài."),
            ("Thực thi Script & Tự sửa lỗi (Repair Loop):", "Chạy npm test/build/lint/typecheck với cờ --ignore-scripts, giới hạn 120s, tự động đọc lỗi và vá mã nguồn tối đa 3 vòng liên tiếp."),
            ("Agent Manager (13 Vai trò Chuyên gia):", "Hàng đợi phân tích tuần tự tối đa 3 vai trò (Planner, Architect, Frontend, Backend, Security, Testing, Reviewer...) dùng chung ngân sách token."),
            ("Scoped Memory & Local MCP Manager:", "Bộ nhớ phân tách theo User/Project/Session (chặn lưu nhầm khóa bí mật) và kết nối máy chủ MCP qua HTTP/SSE loopback chuẩn 2026-07-28."),
            ("Quản lý Phiên bản Git & Checkpoint:", "Xem trạng thái Git, tạo nhánh, review diff bằng AI, quản lý worktree và khôi phục tức thì qua Shadow Git Checkpoints."),
        ],
        font_size=11.0, space_after=6, bullet_color=C_CYAN
    )

    # Cột phải trên: Quản trị hệ thống (Admin Console)
    add_card(s7, 6.80, 1.15, 6.10, 2.85, fill_color=C_CARD_BG, border_color=C_PURPLE, accent_top_color=C_PURPLE)
    add_textbox(s7, 7.00, 1.30, 5.75, 0.32, "TRANG QUẢN TRỊ HỆ THỐNG (ADMIN CONSOLE)", font_size=13, color=C_PURPLE, bold=True)
    safe_add_image(s7, "artifacts/admin-overview.png", 7.00, 1.68, 2.75, 2.10)
    add_bullet_list(
        s7, 9.88, 1.68, 2.90, 2.15,
        [
            ("Kiểm soát Quyền server-side:", "Chỉ role admin trong DB được phép gọi API quản trị."),
            ("Quản lý Hạn mức & Phiên:", "Cấp/điều chỉnh quota 1M token, khóa tài khoản & thu hồi phiên tức thì."),
            ("Bảo vệ Quyền riêng tư:", "Ghi log Audit trong cùng transaction; không trả nội dung chat/tài liệu riêng tư."),
        ],
        font_size=10.5, space_after=5, bullet_color=C_PURPLE
    )

    # Cột phải dưới: Lá chắn bảo mật AI (Security Gate)
    add_card(s7, 6.80, 4.15, 6.10, 2.75, fill_color=C_CARD_ALT, border_color=C_EMERALD, accent_top_color=C_EMERALD)
    add_textbox(s7, 7.00, 4.30, 5.75, 0.32, "KIẾN TRÚC AN TOÀN & CHỐNG TẤN CÔNG AI (SECURITY GATE)", font_size=13, color=C_EMERALD, bold=True)
    add_bullet_list(
        s7, 7.00, 4.68, 5.75, 2.10,
        [
            ("Chống Prompt Injection:", "Tích hợp bộ phân loại Protect AI DeBERTa-v3 Injection v2 và Qwen3Guard 0.6B để cách ly dữ liệu ngoài độc hại trước khi đưa vào mô hình."),
            ("Cô lập Môi trường Thực thi:", "Loại bỏ hoàn toàn biến môi trường chứa khóa DB/AI/OAuth của Buddy khi chạy script dự án; phân loại mức độ rủi ro lệnh (Safe vs Dangerous)."),
            ("Giao dịch Thanh toán An toàn (payOS):", "Xác minh chữ ký webhook, khớp chính xác số tiền/mã đơn và cộng hạn mức token trong một giao dịch DB duy nhất chống phát lại (anti-replay)."),
        ],
        font_size=10.8, space_after=5, bullet_color=C_EMERALD
    )

    # =========================================================================
    # SLIDE 08: THUẬT TOÁN (1) - XỬ LÝ NGÔN NGỮ TỰ NHIÊN & GIỌNG NÓI TIẾNG VIỆT
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s8, content_bg, 8, total_slides,
        "03 // ALGORITHMS: VIETNAMESE SLU / NLU & ASR",
        "Thuật Toán (1): Nhận Dạng Ý Định, Trích Xuất Thực Thể & Xử Lý Giọng Nói",
        "Kết hợp LinearSVC, Context-CRF, giải mã Viterbi có ràng buộc BIO & tổ hợp Posterior V7",
        "Slide 8 phân tích chi tiết các thuật toán học máy và học sâu áp dụng cho bài toán hiểu lệnh tiếng Việt (SLU/NLU) và nhận dạng giọng nói."
    )

    # Sơ đồ pipeline ngang ở phần trên
    pipe_steps = [
        ("1. Tiền xử lý & Chuẩn hóa", "Chuẩn hóa Unicode NFC, giữ nguyên dấu thanh & từ phủ định, chuẩn hóa số/ngày (ITN).", C_CYAN),
        ("2. Phân loại Ý định (Intent)", "LinearSVC trên đặc trưng n-gram từ/ký tự, dự đoán xác suất/nhãn ý định với độ chính xác 95.54%.", C_BLUE),
        ("3. Trích xuất Đặc trưng CRF", "Cửa sổ ngữ cảnh ±3 từ, hình thái từ, chữ số, ý định dự đoán & từ điển 880 cụm thực thể.", C_PURPLE),
        ("4. Giải mã Viterbi Ràng buộc", "Quy hoạch động Viterbi ép luật chuyển nhãn BIO/BILOU & lọc theo Schema thực thể của từng Intent.", C_EMERALD),
    ]
    for idx, (st_title, st_desc, col) in enumerate(pipe_steps):
        px = 0.42 + idx * 3.16
        add_card(s8, px, 1.12, 3.00, 1.32, fill_color=C_CARD_BG, border_color=col, accent_top_color=col)
        add_textbox(s8, px + 0.12, 1.20, 2.76, 0.28, st_title, font_size=11.5, color=col, bold=True)
        add_textbox(s8, px + 0.12, 1.50, 2.76, 0.85, st_desc, font_size=10.2, color=C_TEXT)
        if idx < 3:
            add_textbox(s8, px + 3.00, 1.58, 0.16, 0.35, "➜", font_size=14, color=C_CYAN, bold=True, align=PP_ALIGN.CENTER)

    # Khối trái dưới: Công thức & Thuật toán CRF + Constrained Viterbi + Ensemble V7
    add_card(s8, 0.42, 2.60, 6.20, 4.35, fill_color=C_CARD_BG, border_color=C_CYAN, accent_left_color=C_CYAN)
    add_textbox(s8, 0.62, 2.72, 5.85, 0.34, "CƠ SỞ TOÁN HỌC & THUẬT TOÁN GIẢI MÃ CHUỖI NHÃN (V1 → V7)", font_size=13, color=C_CYAN, bold=True)

    # Hộp công thức toán học
    add_card(s8, 0.62, 3.12, 5.80, 0.92, fill_color=C_CARD_DARK, border_color=C_BLUE)
    add_textbox(
        s8, 0.74, 3.18, 5.56, 0.80,
        "• Giải mã Viterbi có ràng buộc (V3):  y* = argmax_{y ∈ Ω(Î)} ∑_t [ w^T f(x, y_{t-1}, y_t, t, Î) ]\n"
        "• Tổ hợp Posterior 50/50 (V7):  P_ens(y_t | x) = 0.5 · P_BIO(y_t | x) + 0.5 · π(P_BILOU(y_t | x))",
        font_size=10.5, color=C_CYAN, bold=True, font_name=FONT_MONO, line_spacing=1.25
    )

    add_bullet_list(
        s8, 0.62, 4.14, 5.80, 2.70,
        [
            ("Ràng buộc miền hợp lệ Ω(Î):", "Loại bỏ mọi đường đi vi phạm quy tắc BIO (ví dụ I-entity đứng sau O hoặc khác loại B-entity) và chỉ cho phép các slot thuộc Schema của ý định Î học từ tập train."),
            ("Ánh xạ nhãn BILOU → BIO trong V7:", "Quy đổi phân bố hậu nghiệm từ không gian nhãn BILOU (U→B, L→I) về BIO trước khi giải mã, giúp sửa lỗi biên thực thể dài mà không cần huấn luyện lại."),
            ("Tối ưu hàm mục tiêu L-BFGS:", "Phạt chuẩn hóa đàn hồi L1/L2 (c1 = 0.05, c2 = 0.01) trong 60 vòng lặp giúp triệt tiêu đặc trưng nhiễu và chống quá khớp (overfitting)."),
        ],
        font_size=10.8, space_after=5, bullet_color=C_CYAN
    )

    # Khối phải dưới: Kiến trúc Deep Learning (Joint XLM-R, BamiBERT & Audio-Tower LoRA)
    add_card(s8, 6.80, 2.60, 6.10, 4.35, fill_color=C_CARD_BG, border_color=C_PURPLE, accent_left_color=C_PURPLE)
    add_textbox(s8, 7.00, 2.72, 5.75, 0.34, "THUẬT TOÁN HỌC SÂU: BAMIBERT, JOINT XLM-R & ASR LORA", font_size=13, color=C_PURPLE, bold=True)
    add_bullet_list(
        s8, 7.00, 3.12, 5.75, 3.70,
        [
            ("Mô hình Đồng huấn luyện (Joint Intent & Slot Filling):", "Xây dựng kiến trúc cảm hứng từ JointIDSF trên XLM-R Base và BamiBERT: vector ngữ cảnh phân phối mềm của Intent được nối vào biểu diễn ẩn của từng token trước tầng phân loại Slot + CRF."),
            ("Thuật toán Căn chỉnh Nhãn Raw-Offset (BamiBERT):", "Giải quyết bài toán lệch subword của bộ từ vựng Byte-level BPE tiếng Việt bằng cách ánh xạ nhãn BIO vào đúng token đầu tiên giao cắt với từng từ gốc, chỉ tính hàm mất mát (Cross-Entropy/CRF Loss) trên các vị trí neo hợp lệ."),
            ("Thích nghi Miền Âm thanh (Qwen3-ASR 1.7B LoRA):", "Đóng băng toàn bộ trọng số bộ giải mã văn bản (Text Decoder), chỉ gắn ma trận hạng thấp LoRA (rank r=8, α=16) vào các tầng tự chú ý q_proj, v_proj của Audio Tower (đúng 96 tensor khả huấn luyện)."),
            ("Kiểm chứng Đồng thuận Kép (Two-Agree Verification):", "So khớp kết quả giải mã và chặn tự động các lệnh có độ bất định cao hoặc thực thể ngoài danh mục."),
        ],
        font_size=10.8, space_after=6, bullet_color=C_PURPLE
    )

    # =========================================================================
    # SLIDE 09: THUẬT TOÁN (2) - TRUY XUẤT TÀI LIỆU, LẬP LỊCH & ĐIỀU PHỐI LỆNH
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s9, content_bg, 9, total_slides,
        "03 // ALGORITHMS: RETRIEVAL, PLANNER & ACTION ROUTING",
        "Thuật Toán (2): Truy Xuất Tài Liệu, Lập Lịch Học & Phân Giải Lệnh",
        "Thiết kế thuật toán xác định (Deterministic) nhanh, chính xác và không bịa đặt thông tin",
        "Slide 9 trình bày 3 thuật toán cốt lõi trong vận hành ứng dụng: Truy xuất tài liệu, Lập lịch Pomodoro và Phân giải lệnh điều khiển máy."
    )

    algo_cols = [
        (
            "1. THUẬT TOÁN TRUY XUẤT TÀI LIỆU\n& SINH CÂU HỎI QUIZ",
            C_CYAN,
            "lib/resources.ts · lib/tutor.ts",
            [
                ("Phân đoạn Văn bản (Chunking):", "Chia tài liệu lớn (tối đa 250.000 ký tự) thành các đoạn ngữ cảnh có kích thước chuẩn hóa, bảo toàn ranh giới câu và đoạn văn."),
                ("So khớp Từ khóa Tiếng Việt Kép:", "Kết hợp chuẩn hóa bỏ dấu tiếng Việt (giúp tìm kiếm linh hoạt) với so khớp có dấu để chấm điểm độ liên quan của từng đoạn với câu hỏi."),
                ("Chống Ảo giác Nguồn (Anti-Hallucination):", "Chỉ đính kèm trích dẫn khi điểm khớp vượt ngưỡng; nếu không có đoạn khớp, AI trả lời dựa trên kiến thức chung và không tự bịa nguồn."),
                ("Sinh Quiz Điền Từ Tự động:", "Lọc các câu giàu thông tin từ tài liệu, chọn cụm từ khóa trọng tâm làm chỗ trống, tạo 4 phương án nhiễu hợp lý và ẩn đáp án ở phía server."),
            ]
        ),
        (
            "2. THUẬT TOÁN LẬP KẾ HOẠCH HỌC TẬP\n(DEADLINE-FIRST POMODORO PLANNER)",
            C_BLUE,
            "lib/task-plan.ts · lib/task-schedule.ts",
            [
                ("Sắp xếp Ưu tiên Đa tiêu chí:", "Xếp hạng các nhiệm vụ chưa hoàn thành theo hàm trọng số kết hợp giữa thời hạn (Earliest Deadline First) và mức độ ưu tiên do người dùng gán."),
                ("Phân bổ Khung giờ (Time-Slot Packing):", "Chia quỹ thời gian rảnh trong ngày/tuần thành các phiên tập trung Pomodoro tối đa 50 phút, tự động chèn 5 phút nghỉ chuyển tiếp."),
                ("Phát hiện Xung đột & Quá hạn:", "Đánh dấu tức thì các đầu việc có nguy cơ trễ hạn, hỗ trợ xuất lịch chuẩn RFC 5545 (.ICS) tương thích Google/Apple Calendar."),
                ("Bộ đếm Nhàn rỗi Chủ động:", "Theo dõi số giây không thao tác trên Desktop hoặc sự hiện diện khuôn mặt trên Web để kích hoạt lời nhắc học tập đúng thời điểm."),
            ]
        ),
        (
            "3. THUẬT TOÁN PHÂN GIẢI LỆNH\n(SELECTIVE-CAUTIOUS RESOLVER)",
            C_EMERALD,
            "lib/request-understanding.ts · lib/spoken-open.ts",
            [
                ("Định tuyến Lệnh nhanh (Fast-Path):", "Nhận diện trực tiếp các mẫu câu mở ứng dụng, mở web, tìm kiếm YouTube bằng bộ phân tích cú pháp cục bộ mà không cần chờ LLM."),
                ("Phân giải Danh mục An toàn (Catalog Resolver):", "Đối chiếu tên ứng dụng/thư mục với danh sách cấp quyền (allowedFolders) và bảng bí danh (alias) có phân biệt dấu tiếng Việt."),
                ("Cơ chế Hỏi lại Khi Nhập nhằng:", "Nếu tên thư mục trùng nhau sau chuẩn hóa hoặc chỉ khớp một phần (ví dụ nghe nhầm “Triết” thành “chiết”), hệ thống bắt buộc dừng lại hỏi người dùng thay vì tự đoán."),
                ("Bảo toàn Tham số Nguyên văn:", "Giữ nguyên cụm từ tìm kiếm mới (chữ Việt–Anh, chữ hoa, số) và mã hóa bằng URLSearchParams, ngăn LLM tự ý viết lại nội dung."),
            ]
        ),
    ]

    for idx, (ctitle, col, cfiles, citems) in enumerate(algo_cols):
        cx = 0.42 + idx * 4.22
        add_card(s9, cx, 1.15, 4.04, 5.75, fill_color=C_CARD_BG, border_color=col, accent_top_color=col)
        add_textbox(s9, cx + 0.16, 1.28, 3.72, 0.56, ctitle, font_size=12.5, color=col, bold=True)
        add_pill(s9, cx + 0.16, 1.90, 3.72, 0.28, cfiles, fill_color=C_CARD_DARK, text_color=C_MUTED, border_color=C_BORDER, font_size=9.5)
        add_bullet_list(s9, cx + 0.16, 2.28, 3.72, 4.48, citems, font_size=10.8, space_after=7, bullet_color=col)

    # =========================================================================
    # SLIDE 10: THUẬT TOÁN (3) - AGENT LẬP TRÌNH TỰ SỬA LỖI & MULTI-STRATEGY EDIT
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s10, content_bg, 10, total_slides,
        "03 // ALGORITHMS: AGENTIC CODING & SELF-HEALING",
        "Thuật Toán (3): Vá Mã Nguồn Đa Chiến Lược & Vòng Lặp Tự Sửa Lỗi",
        "Trái tim kỹ thuật của Buddy Coder & CodexEngine (Tier-1 Agentic Workstation)",
        "Slide 10 đi sâu vào thuật toán sửa tệp 3 tầng, phân tích cây cú pháp AST RepoMap và vòng lặp tự kiểm chứng – tự sửa lỗi."
    )

    # Khối trái: Multi-Strategy Edit Engine + Atomic Write + AST RepoMap
    add_card(s10, 0.42, 1.15, 6.18, 5.75, fill_color=C_CARD_BG, border_color=C_CYAN, accent_top_color=C_CYAN)
    add_textbox(s10, 0.62, 1.28, 5.80, 0.34, "1. THUẬT TOÁN SỬA MÃ NGUỒN 3 TẦNG & ĐỒ THỊ AST REPOMAP", font_size=13, color=C_CYAN, bold=True)

    tiers = [
        ("Tầng 1 — Exact Match & SHA-256 Guard", C_CYAN,
         "Tìm vị trí xuất hiện duy nhất của chuỗi mục tiêu (oldText) và đối chiếu mã băm tệp gốc. Từ chối áp dụng nếu có từ 2 vị trí trùng trở lên hoặc tệp đã bị sửa bên ngoài."),
        ("Tầng 2 — Line-Trimmed & CRLF Normalization", C_BLUE,
         "Chuẩn hóa ký tự xuống dòng (\\r\\n ↔ \\n) và bỏ khoảng trắng thừa cuối dòng để khớp chính xác ngay cả khi mô hình AI sinh lệch định dạng dòng trên Windows."),
        ("Tầng 3 — Indentation-Aware Re-anchoring", C_PURPLE,
         "So khớp theo độ lệch thụt lề tương đối của khối lệnh và tự động căn chỉnh lại khoảng trắng đầu dòng của đoạn mã thay thế khớp với ngữ cảnh tệp đích."),
    ]
    for idx, (ttitle, col, tdesc) in enumerate(tiers):
        ty = 1.70 + idx * 1.08
        add_card(s10, 0.62, ty, 5.78, 0.98, fill_color=C_CARD_ALT, border_color=col, accent_left_color=col)
        add_textbox(s10, 0.80, ty + 0.06, 5.48, 0.26, ttitle, font_size=11.5, color=col, bold=True)
        add_textbox(s10, 0.80, ty + 0.34, 5.48, 0.58, tdesc, font_size=10.2, color=C_TEXT)

    add_bullet_list(
        s10, 0.62, 5.02, 5.78, 1.75,
        [
            ("Giao dịch Ghi tệp Nguyên tử (Atomic All-or-Nothing):", "Kiểm tra trước (preflight) toàn bộ các tệp trong bản vá; ghi vào tệp tạm cùng thư mục → gọi fsync → đổi tên nguyên tử; tự động hoàn tác (rollback) nếu bất kỳ tệp nào lỗi."),
            ("Thuật toán AST RepoMap (tools/code-intel.ts):", "Trích xuất chữ ký hàm/lớp thực tế bằng trình biên dịch TypeScript AST & Python ast; xếp hạng độ quan trọng của tệp theo bậc vào trên đồ thị import để nạp tối ưu vào ngân sách token."),
        ],
        font_size=10.5, space_after=5, bullet_color=C_CYAN
    )

    # Khối phải: Vòng lặp tự sửa lỗi (Bounded Self-Healing & Verify Loop)
    add_card(s10, 6.78, 1.15, 6.12, 5.75, fill_color=C_CARD_BG, border_color=C_EMERALD, accent_top_color=C_EMERALD)
    add_textbox(s10, 6.98, 1.28, 5.75, 0.34, "2. VÒNG LẶP TỰ KIỂM CHỨNG & SỬA LỖI (SELF-HEALING LOOP)", font_size=13, color=C_EMERALD, bold=True)

    loop_steps = [
        ("BƯỚC 1: KHỞI TẠO & CHỤP CHECKPOINT", "Tự động chụp trạng thái mã nguồn vào Shadow Git riêng biệt trước khi thực hiện thay đổi hoặc chạy lệnh đầu tiên."),
        ("BƯỚC 2: PHÂN TÍCH & ÁP DỤNG BẢN VÁ", "Model tìm kiếm bằng Grep worker (tôn trọng .gitignore), đọc dòng có phân trang và áp dụng multiEdit / applyPatch."),
        ("BƯỚC 3: KIỂM TRA TĨNH TỨC THÌ (DIAGNOSTICS)", "Chạy TypeScript LanguageService trong worker (kèm các tệp được import trực tiếp), Python compile() và JSON.parse."),
        ("BƯỚC 4: CHẠY TEST & PHẢN TƯ (VERIFY & REFLECT)", "Thực thi lệnh kiểm thử trong phiên Shell bền; nếu lỗi biên dịch hoặc test ≠ 0, đẩy toàn bộ stderr/diagnostics ngược vào vòng lặp sửa (tối đa 3 vòng)."),
        ("BƯỚC 5: PHÁT HIỆN VÒNG LẶP KẸT (STUCK DETECTOR)", "Nếu xuất hiện cùng một lỗi, cùng một lệnh hoặc cùng một bản vá 3 lần liên tiếp: lần 1 cảnh báo chiến lược, lần 2 tự động ngắt để bảo toàn token."),
    ]
    for idx, (lhead, lbody) in enumerate(loop_steps):
        ly = 1.72 + idx * 1.00
        add_card(s10, 6.98, ly, 5.72, 0.90, fill_color=C_CARD_ALT, border_color=C_BORDER, accent_left_color=C_EMERALD)
        add_textbox(s10, 7.16, ly + 0.06, 5.42, 0.25, lhead, font_size=11, color=C_EMERALD, bold=True)
        add_textbox(s10, 7.16, ly + 0.32, 5.42, 0.52, lbody, font_size=10.0, color=C_TEXT)

    # =========================================================================
    # SLIDE 11: HIỆU SUẤT & THỰC NGHIỆM (1) - KẾT QUẢ MÔ HÌNH AI, NLU & ASR
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s11, content_bg, 11, total_slides,
        "04 // PERFORMANCE BENCHMARKS: AI, NLU & ASR",
        "Hiệu Suất (1): Kết Quả Thực Nghiệm Các Mô Hình NLU & Nhận Dạng Lệnh",
        "Đánh giá khách quan trên 12.979 câu huấn luyện, 1.345 câu kiểm thử (VN-SLU) & 244 mẫu âm thanh",
        "Slide 11 tổng hợp toàn bộ kết quả thực nghiệm các phiên bản thuật toán hiểu lệnh tiếng Việt từ Baseline đến CRF V7 và BamiBERT."
    )

    # 4 thẻ KPI nổi bật trên cùng
    kpis_11 = [
        ("95.99%", "Độ chính xác Ý định (Intent)", "Đạt đỉnh với BamiBERT (CRF giữ ổn định 95.54%)", C_CYAN),
        ("78.36%", "Độ chính xác Thực thể (Entity Exact)", "BamiBERT Joint-CRF (Tăng +25.79% so với Baseline)", C_BLUE),
        ("70.04%", "Đúng Toàn Lệnh trên CPU (CRF V7)", "Tăng +19.18 điểm % so với Baseline (50.86%)", C_EMERALD),
        ("15 Giây", "Thời gian Giải mã 1.345 Câu Dev", "Chạy trên 2 nhân CPU (Không cần GPU khi suy luận)", C_PURPLE),
    ]
    for idx, (val, label, sub, col) in enumerate(kpis_11):
        kx = 0.42 + idx * 3.16
        add_card(s11, kx, 1.12, 3.00, 1.25, fill_color=C_CARD_BG, border_color=col, accent_top_color=col)
        add_textbox(s11, kx + 0.12, 1.18, 2.76, 0.48, val, font_size=24, color=col, bold=True)
        add_textbox(s11, kx + 0.12, 1.68, 2.76, 0.26, label, font_size=11, color=C_WHITE, bold=True)
        add_textbox(s11, kx + 0.12, 1.94, 2.76, 0.35, sub, font_size=9.5, color=C_MUTED)

    # Bảng so sánh chi tiết các mô hình (Native PowerPoint Table)
    rows_data = [
        ["Phiên bản / Kiến trúc Mô hình", "Môi trường Chạy", "Đúng Ý định (Intent)", "Đúng Toàn bộ Entity", "Đúng Toàn lệnh (Full Exact)", "Đánh giá & Quyết định Kỹ thuật"],
        ["Baseline (LinearSVC + Slot cũ)", "CPU Local", "95,54%", "52,57%", "50,86% (684/1345)", "Mốc cơ sở ban đầu; hay lỗi ranh giới thực thể dài."],
        ["Joint XLM-R Base (V2 - 3 Epochs)", "GPU (404s)", "94,87%", "43,57%", "41,78% (562/1345)", "Loại bỏ — subword làm phân mảnh nhãn thực thể."],
        ["Context-CRF + LinearSVC (V1)", "CPU (148s)", "95,54%", "70,78%", "68,62% (923/1345)", "Tăng vọt +17,77 điểm % nhờ ngữ cảnh ±3 từ & Intent."],
        ["Context-CRF + 880 Cụm Entity (V2)", "CPU (212.4s)", "95,54%", "71,45%", "69,44% (934/1345)", "Thêm đặc trưng cụm từ tần suất ≥ 3 & mẫu chữ số."],
        ["Constrained Viterbi BIO Schema (V3)", "CPU", "95,54%", "71,60%", "69,74% (938/1345)", "Sửa 4 câu lỗi biên mà không làm sai thêm câu nào."],
        ["Posterior Ensemble 50/50 BIO+BILOU (V7)", "2 CPU (15s eval)", "95,54%", "71,90%", "70,04% (942/1345)", "Điểm CPU cao nhất; suy luận cực nhanh không cần GPU."],
        ["BamiBERT Joint Intent+CRF (4 Epochs)", "GPU A10 (361.8s)", "95,99%", "78,36%", "76,51% (1029/1345)", "Độ chính xác cao trên văn bản nhờ căn chỉnh raw-offset."],
    ]

    table_shape = s11.shapes.add_table(len(rows_data), 6, Inches(0.42), Inches(2.52), Inches(12.48), Inches(4.38))
    table = table_shape.table
    col_widths = [2.95, 1.45, 1.35, 1.45, 1.85, 3.43]
    for c_idx, width_in in enumerate(col_widths):
        table.columns[c_idx].width = Inches(width_in)

    for r_idx, row in enumerate(rows_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(20, 42, 84)
            elif r_idx in (6, 7):
                cell.fill.fore_color.rgb = RGBColor(16, 38, 68)
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = C_CARD_BG
            else:
                cell.fill.fore_color.rgb = C_CARD_DARK

            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.08)
            tf.margin_right = Inches(0.08)
            tf.margin_top = Inches(0.03)
            tf.margin_bottom = Inches(0.03)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if c_idx in (1, 2, 3, 4) else PP_ALIGN.LEFT
            run = p.add_run()
            run.text = val
            run.font.name = FONT_MAIN
            run.font.size = Pt(10.2 if r_idx > 0 else 10.5)
            run.font.bold = (r_idx == 0 or c_idx == 0 or (r_idx in (6, 7) and c_idx == 4))
            if r_idx == 0:
                run.font.color.rgb = C_CYAN
            elif r_idx in (6, 7) and c_idx in (0, 4):
                run.font.color.rgb = C_EMERALD
            elif r_idx == 2 and c_idx == 4:
                run.font.color.rgb = C_AMBER
            else:
                run.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 12: HIỆU SUẤT & THỰC NGHIỆM (2) - HIỆU NĂNG HỆ THỐNG & KIỂM THỬ QA
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s12, content_bg, 12, total_slides,
        "04 // PERFORMANCE BENCHMARKS: RUNTIME & QA METRICS",
        "Hiệu Suất (2): Hiệu Năng Runtime, Độ Trễ Điều Khiển & Độ Phủ Kiểm Thử",
        "Đo lường thực tế trên máy Windows 10 (Node v24.22.1), trình duyệt Edge/Playwright & Modal Gateway",
        "Slide 12 chứng minh hiệu năng vận hành thực tế của hệ thống qua dung lượng bundle, tốc độ điều khiển Windows và số lượng bài kiểm thử tự động."
    )

    # 4 thẻ chỉ số lớn
    kpis_12 = [
        ("181 / 181", "Unit Test Files PASS (100%)", "Hơn 525 test cases + 93/93 tests trong codex-engine", C_EMERALD),
        ("236–598 ms", "Độ Trễ Điều Khiển Máy (Fast-Path)", "5/5 tác vụ mở ứng dụng, thư mục & trình duyệt thật", C_CYAN),
        ("~315 KB", "Dung Lượng Client JS (Node Lite)", "CSS ~66–76 KB, Server ~157 KB (Khởi động tức thì)", C_BLUE),
        ("42s / 108s", "Tự Sửa Lỗi Code Thực Tế (Tier-1)", "Devstral-24B tự sửa bài test TypeScript & Python", C_PURPLE),
    ]
    for idx, (val, label, sub, col) in enumerate(kpis_12):
        kx = 0.42 + idx * 3.16
        add_card(s12, kx, 1.12, 3.00, 1.25, fill_color=C_CARD_BG, border_color=col, accent_top_color=col)
        add_textbox(s12, kx + 0.12, 1.18, 2.76, 0.48, val, font_size=23, color=col, bold=True)
        add_textbox(s12, kx + 0.12, 1.68, 2.76, 0.26, label, font_size=11, color=C_WHITE, bold=True)
        add_textbox(s12, kx + 0.12, 1.94, 2.76, 0.35, sub, font_size=9.5, color=C_MUTED)

    # Cột trái dưới: Bảng kết quả kiểm thử tự động đa tầng
    add_card(s12, 0.42, 2.55, 6.20, 4.40, fill_color=C_CARD_BG, border_color=C_CYAN, accent_top_color=C_CYAN)
    add_textbox(s12, 0.62, 2.68, 5.80, 0.32, "1. MA TRẬN KIỂM THỬ TỰ ĐỘNG & NGHIỆM THU KỸ THUẬT", font_size=13, color=C_CYAN, bold=True)
    add_bullet_list(
        s12, 0.62, 3.08, 5.80, 3.75,
        [
            ("Kiểm tra Kiểu Tĩnh (TypeScript):", "tsc --noEmit đạt exit code 0 trên toàn bộ kho mã nguồn chính, tiện ích mở rộng và giao diện."),
            ("Unit & Contract Suites:", "331/331 cases PASS trong gói Runtime V2; 181/181 tệp kiểm thử PASS toàn repo; 93/93 bài kiểm thử hạt nhân CodexEngine PASS."),
            ("Kiểm thử Tích hợp Cô lập (API Integration):", "33+ bài kiểm tra tạo tài khoản tạm, xác minh phân tách dữ liệu chéo, chống giả mạo CSRF origin, thu hồi phiên khi khóa tài khoản và hoàn trả hạn mức token."),
            ("Kiểm thử Trình duyệt & Thị giác (Playwright E2E):", "9/9 kịch bản E2E hoàn tất (~39.6s) cùng 23 ảnh chụp Visual QA trên cả Desktop và Mobile không có lỗi tràn khung ngang."),
            ("Nghiệm thu Thực tế Điều khiển Windows:", "Mở Notepad, Calculator, thư mục QA, Facebook trên Edge và tìm kiếm YouTube trên Chrome đạt 5/5 với biên nhận tiến trình thật."),
        ],
        font_size=10.8, space_after=6, bullet_color=C_CYAN
    )

    # Cột phải dưới: Biểu đồ thanh ngang trực quan hóa Hiệu suất & Benchmark Coder Tier-1
    add_card(s12, 6.80, 2.55, 6.10, 4.40, fill_color=C_CARD_BG, border_color=C_EMERALD, accent_top_color=C_EMERALD)
    add_textbox(s12, 7.00, 2.68, 5.75, 0.32, "2. CHỈ SỐ ĐỘ TIN CẬY & HIỆU SUẤT THỰC THI (VISUAL METRICS)", font_size=13, color=C_EMERALD, bold=True)

    bars = [
        ("Độ phủ Unit & Engine Tests (181/181 & 93/93)", 1.00, "100% PASS", C_EMERALD),
        ("Độ chính xác Phân loại Ý định Tiếng Việt (NLU)", 0.96, "95.99%", C_CYAN),
        ("Nghiệm thu Công cụ Lập trình Tier-1 (T1–T5)", 1.00, "10/10 PASS", C_BLUE),
        ("Độ chính xác Thực thể Hoàn chỉnh (BamiBERT)", 0.784, "78.36%", C_PURPLE),
        ("Đúng Toàn lệnh trên CPU (Ensemble CRF V7)", 0.70, "70.04%", C_AMBER),
    ]
    for idx, (blabel, ratio, bval, col) in enumerate(bars):
        by = 3.12 + idx * 0.62
        add_textbox(s12, 7.00, by, 4.30, 0.24, blabel, font_size=10.5, color=C_TEXT, bold=True)
        add_textbox(s12, 11.30, by, 1.40, 0.24, bval, font_size=10.5, color=col, bold=True, align=PP_ALIGN.RIGHT)
        # Nền thanh tiến trình
        track = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.00), Inches(by + 0.26), Inches(5.70), Inches(0.18))
        track.fill.solid()
        track.fill.fore_color.rgb = C_CARD_DARK
        track.line.color.rgb = C_BORDER
        track.line.width = Pt(0.6)
        # Thanh giá trị
        fill_bar = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.00), Inches(by + 0.26), Inches(5.70 * ratio), Inches(0.18))
        fill_bar.fill.solid()
        fill_bar.fill.fore_color.rgb = col
        fill_bar.line.fill.background()

    add_textbox(
        s12, 7.00, 6.26, 5.70, 0.58,
        "Ghi chú minh bạch: Các chỉ số được trích xuất trực tiếp từ biên bản kiểm thử thực tế trong dự án (TEST_REPORT.md, BUDDY-CODER-TIER1-ACCEPTANCE-2026-11-07.md).",
        font_size=9.8, color=C_MUTED, italic=True
    )

    # =========================================================================
    # SLIDE 13: KỸ THUẬT TỐI ƯU HÓA TOÀN DIỆN & ĐỊNH HƯỚNG PHÁT TRIỂN
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(
        s13, content_bg, 13, total_slides,
        "05 // OPTIMIZATION TECHNIQUES & FUTURE ROADMAP",
        "Kỹ Thuật Tối Ưu Hóa Hệ Thống & Định Hướng Mở Rộng Đồ Án",
        "5 giải pháp tối ưu hóa trọng tâm giúp Buddy chạy mượt, tiết kiệm tài nguyên và an toàn",
        "Slide 13 tổng kết 5 kỹ thuật tối ưu hóa quan trọng nhất trong đồ án và lộ trình phát triển tiếp theo. Cảm ơn Hội đồng đã lắng nghe!"
    )

    opt_cards = [
        (
            "1. TỐI ƯU RUNTIME & BỘ NHỚ (NODE LITE)",
            C_CYAN,
            [
                ("Loại bỏ Next.js Dev Overhead:", "Đóng gói sẵn giao diện và API vào máy chủ Node Lite (~157 KB) giúp chạy mượt trên máy 8 GB RAM."),
                ("Cache Busting bằng SHA-256:", "Gắn mã băm phiên bản cho JS/CSS, đặt HTML no-store để trình duyệt luôn nạp giao diện mới nhất."),
                ("Giới hạn Tài nguyên Trình duyệt:", "Khóa tối đa 6 tab WebContentsView trong Electron và giải phóng media track ngay khi ẩn robot."),
            ]
        ),
        (
            "2. TỐI ƯU ĐỘ TRỄ LỆNH (FAST-PATH ROUTING)",
            C_BLUE,
            [
                ("Bỏ qua LLM cho Lệnh Rõ ràng:", "Các lệnh mở ứng dụng, mở trang web hoặc tìm kiếm YouTube đi thẳng qua bộ phân tích cục bộ (236–598ms)."),
                ("Suy luận NLU trên CPU (15s/1345 câu):", "Dùng tổ hợp tuyến tính LinearSVC + Context-CRF V7 nhẹ và ổn định thay vì gọi mô hình tỷ tham số cho mọi bước lọc."),
            ]
        ),
        (
            "3. TỐI ƯU TOKEN & NGỮ CẢNH (COMPACTION 85%)",
            C_PURPLE,
            [
                ("Cửa sổ Trượt Nén Ngữ cảnh:", "Khi chạm 85% ngân sách token, tự động thu gọn kết quả đọc tệp/grep cũ thành stub, giữ lại mục tiêu gốc và tệp vừa sửa."),
                ("Quota Reservation & Refund:", "Tạm giữ hạn mức trước khi gọi AI và tự động hoàn trả 100% nếu kết nối lỗi hoặc người dùng bấm Dừng."),
            ]
        ),
        (
            "4. TỐI ƯU HUẤN LUYỆN AI & AN TOÀN DỮ LIỆU",
            C_EMERALD,
            [
                ("Audio-Tower LoRA (96 Tensors):", "Chỉ huấn luyện 96 tensor LoRA trên tầng chú ý âm thanh của Qwen3-ASR 1.7B kèm 1.024 mẫu FLEURS chống quên kiến thức."),
                ("Shadow Git & Atomic File Write:", "Ghi tệp qua file tạm + fsync + rename và lưu ảnh chụp vào kho Git ẩn giúp hoàn tác tức thì không làm bẩn lịch sử dự án."),
            ]
        ),
    ]

    for idx, (otitle, col, oitems) in enumerate(opt_cards):
        r = idx // 2
        c = idx % 2
        ox = 0.42 + c * 4.25
        oy = 1.15 + r * 2.88
        add_card(s13, ox, oy, 4.10, 2.74, fill_color=C_CARD_BG, border_color=col, accent_top_color=col)
        add_textbox(s13, ox + 0.14, oy + 0.10, 3.82, 0.30, otitle, font_size=11.8, color=col, bold=True)
        add_bullet_list(s13, ox + 0.14, oy + 0.44, 3.82, 2.20, oitems, font_size=10.2, space_after=4, bullet_color=col)

    # Cột phải: Định hướng phát triển & Kết luận
    add_card(s13, 8.92, 1.15, 3.98, 5.62, fill_color=C_CARD_ALT, border_color=C_AMBER, accent_top_color=C_AMBER)
    add_textbox(s13, 9.10, 1.28, 3.62, 0.34, "LỘ TRÌNH PHÁT TRIỂN TIẾP THEO", font_size=13, color=C_AMBER, bold=True)
    add_bullet_list(
        s13, 9.10, 1.68, 3.62, 2.75,
        [
            ("Voice Realtime & Barge-in:", "Phát hiện kết thúc câu tự động (VAD) và cho phép ngắt lời AI theo thời gian thực qua WebRTC/LiveKit."),
            ("Semantic RAG & OCR Tài liệu Scan:", "Kết hợp tìm kiếm từ khóa với Vector Embedding và nhận dạng chữ quang học cho PDF bản chụp."),
            ("Mở rộng Tập dữ liệu Giọng thật:", "Đánh giá độc lập theo người nói (speaker-disjoint) trong môi trường nhiễu thực tế và từ vựng pha Việt–Anh."),
            ("Đóng gói Bộ cài Độc lập:", "Hoàn thiện trình cài đặt Windows tự động và đồng bộ hóa lai giữa máy cá nhân với đám mây."),
        ],
        font_size=10.5, space_after=5, bullet_color=C_AMBER
    )

    safe_add_image(s13, "public/images/buddy-graduate-original-face.png", 9.95, 4.48, 1.90, 1.55)
    add_textbox(
        s13, 9.08, 6.08, 3.66, 0.60,
        "TRÂN TRỌNG CẢM ƠN HỘI ĐỒNG & QUÝ THẦY CÔ!\nQ&A — Thảo luận & Demo trực tiếp hệ thống Buddy AI",
        font_size=11.2, color=C_CYAN, bold=True, align=PP_ALIGN.CENTER
    )

    out_pptx = OUT_DIR / "Buddy_AI_Tech_Presentation_13_Slides.pptx"
    prs.save(str(out_pptx))
    print(f"SAVED: {out_pptx}")
    return out_pptx


if __name__ == "__main__":
    build_presentation()
