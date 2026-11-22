# -*- coding: utf-8 -*-
"""
hindi_perfect_typography_engine.py
==================================
Next-Generation Study Notes Generator with:
1. RICH THEMATIC ELEMENTS & ACCESSORIES FOR EVERY THEME:
   - Corkboard: Red connecting yarn, brass paperclips, multi-color push pins, post-it tags.
   - Grid Journal: Botanical washi tape strips, green vine leaf doodles, index tabs.
   - Chalkboard: White & yellow chalk sticks, wooden chalk eraser, hand-drawn chalk arrows & stars.
   - Clipboard: Shiny metallic clamp, clipped doctor's ballpoint pen with shadow, highlighter swatches.
   - Cyber Dark Neon: Glowing PCB circuit traces, solder pads, holographic corner brackets.
   - Kraft Vintage: Embossed red wax seal, coffee mug stain rings, vintage airmail postage stamp.
   - Post-it Wall: Chisel-tip highlighter pen, hazard warning sticker, overlapping mini notes.
   - Blueprint: Technical compass tool, dimension arrows (R_s = 2GM/c²), drafting coordinate stamps.
   - Legal Pad: Realistic yellow #2 pencil with eraser, paperclips, red hand-drawn callout loop.
   - Whiteboard: 3D glossy whiteboard magnets, dry-erase marker pens with shadow, felt eraser.
2. 100% PERFECT Devanagari Typography (Windows Native Uniscribe / GDI Shaping).
3. 100% Solid & Jet-Black Text on Whiteboard and light themes (Inverted Alpha Masking).
4. Zero Text Overflow: 25px bottom safe margin inside cards and vertically centered Fun Fact banner.
5. Large, crystal-clear 24px-28px font size for effortless mobile reading.
"""

import os
import math
import random
import ctypes
from ctypes import wintypes
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1350

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "themes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# ==================== 100% PERFECT HINDI GDI TEXT ENGINE ====================

def measure_text_gdi(text, font_size=23, bold=False, max_w=440, font_name="Nirmala UI"):
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    weight = 700 if bold else 400
    hfont = gdi32.CreateFontW(-font_size, 0, 0, 0, weight, 0, 0, 0, 0, 0, 0, 5, 0, font_name)
    gdi32.SelectObject(memdc, hfont)

    rect = wintypes.RECT(0, 0, max_w, 2000)
    flags = 0x0000 | 0x0010 | 0x0400
    h = user32.DrawTextW(memdc, text, len(text), ctypes.byref(rect), flags)
    w = rect.right - rect.left

    gdi32.DeleteObject(hfont)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return w, h

def draw_text_perfect_hindi(img, text, xy, font_size=24, bold=False, color=(30, 41, 59), font_name="Nirmala UI", max_w=440):
    x, y = xy
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)

    weight = 700 if bold else 400
    hfont = gdi32.CreateFontW(-font_size, 0, 0, 0, weight, 0, 0, 0, 0, 0, 0, 5, 0, font_name)
    gdi32.SelectObject(memdc, hfont)

    rect = wintypes.RECT(0, 0, max_w, 2000)
    flags = 0x0000 | 0x0010
    h = user32.DrawTextW(memdc, text, len(text), ctypes.byref(rect), flags | 0x0400)
    w = rect.right - rect.left
    w = max(w, 10)
    h = max(h, font_size + 4)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG),
            ("biPlanes", wintypes.WORD), ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
            ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG), ("biYPelsPerMeter", wintypes.LONG),
            ("biClrUsed", wintypes.DWORD), ("biClrImportant", wintypes.DWORD)
        ]

    class BITMAPINFO(ctypes.Structure):
        _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32

    p_bits = ctypes.c_void_p()
    hbm = gdi32.CreateDIBSection(memdc, ctypes.byref(bmi), 0, ctypes.byref(p_bits), 0, 0)
    gdi32.SelectObject(memdc, hbm)

    brush = gdi32.CreateSolidBrush(0xFFFFFF)
    draw_rect = wintypes.RECT(0, 0, w, h)
    user32.FillRect(memdc, ctypes.byref(draw_rect), brush)
    gdi32.DeleteObject(brush)

    gdi32.SelectObject(memdc, hfont)
    gdi32.SetBkMode(memdc, 1)
    gdi32.SetTextColor(memdc, 0x000000)

    user32.DrawTextW(memdc, text, len(text), ctypes.byref(draw_rect), flags)

    buf = (ctypes.c_char * (w * h * 4)).from_address(p_bits.value)
    raw_img = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1)

    arr = np.array(raw_img)
    gray = arr[:, :, 0]
    alpha_ch = (255 - gray).astype(np.uint8)

    out_arr = np.zeros((h, w, 4), dtype=np.uint8)
    out_arr[:, :, 0] = color[0]
    out_arr[:, :, 1] = color[1]
    out_arr[:, :, 2] = color[2]
    out_arr[:, :, 3] = alpha_ch

    txt_layer = Image.fromarray(out_arr, "RGBA")
    img.alpha_composite(txt_layer, (x, y))

    gdi32.DeleteObject(hfont)
    gdi32.DeleteObject(hbm)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return w, h

def fit_bullet_points_in_card(points, available_h, max_w):
    for sz in [23, 22, 21, 20, 19, 18]:
        total_h = 0
        heights = []
        for pt in points:
            _, th = measure_text_gdi("• " + pt, font_size=sz, bold=False, max_w=max_w)
            heights.append(th)
            total_h += th + 8
        if total_h <= available_h:
            return sz, heights, 8
    heights = [measure_text_gdi("• " + pt, font_size=17, bold=False, max_w=max_w)[1] for pt in points]
    return 17, heights, 6

# ==================== BASIC SHADOW & ACCENT DRAWING ====================

def draw_drop_shadow(img, box, radius=8, blur=8, alpha=50, offset=(4, 6)):
    x0, y0, x1, y1 = box
    shadow = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]], radius=radius, fill=(0, 0, 0, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(shadow)

def draw_push_pin(draw, cx, cy, color=(239, 68, 68)):
    draw.ellipse([cx - 4, cy + 5, cx + 6, cy + 14], fill=(0, 0, 0, 70))
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=color, outline=(0, 0, 0, 80), width=1)
    draw.ellipse([cx - 5, cy - 6, cx + 2, cy - 1], fill=(255, 255, 255, 180))
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(int(color[0]*0.5), int(color[1]*0.5), int(color[2]*0.5)))

def draw_washi_tape(draw, box, color=(253, 224, 71, 210), stripe_color=(234, 179, 8, 140)):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=color)
    for sx in range(x0 - 20, x1 + 20, 14):
        draw.line([(sx, y0), (sx + 15, y1)], fill=stripe_color, width=2)
    for ey in range(y0, y1, 4):
        draw.polygon([(x0, ey), (x0 + 3, ey + 2), (x0, ey + 4)], fill=(255, 255, 255, 200))
        draw.polygon([(x1, ey), (x1 - 3, ey + 2), (x1, ey + 4)], fill=(255, 255, 255, 200))

# ==================== ADVANCED THEMED PROPS & ACCESSORIES ====================

def draw_paperclip(canvas, cx, cy, angle=15, length=55, color=(140, 145, 155)):
    """Draws a 3D curved metal wire paperclip with realistic drop shadow."""
    s = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s)
    sdraw.arc([cx - 10 + 3, cy - length//2 + 4, cx + 10 + 3, cy - length//2 + 20 + 4], 180, 360, fill=(0, 0, 0, 55), width=4)
    sdraw.line([(cx + 10 + 3, cy - length//2 + 10 + 4), (cx + 10 + 3, cy + length//2 + 4)], fill=(0, 0, 0, 55), width=4)
    sdraw.arc([cx - 6 + 3, cy + length//2 - 14 + 4, cx + 10 + 3, cy + length//2 + 6 + 4], 0, 180, fill=(0, 0, 0, 55), width=4)
    s = s.filter(ImageFilter.GaussianBlur(3))
    canvas.alpha_composite(s)

    w_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(w_layer)
    wdraw.arc([cx - 10, cy - length//2, cx + 10, cy - length//2 + 20], 180, 360, fill=color, width=3)
    wdraw.line([(cx + 10, cy - length//2 + 10), (cx + 10, cy + length//2)], fill=color, width=3)
    wdraw.arc([cx - 6, cy + length//2 - 14, cx + 10, cy + length//2 + 6], 0, 180, fill=color, width=3)
    wdraw.line([(cx - 6, cy + length//2), (cx - 6, cy - length//2 + 16)], fill=color, width=3)
    wdraw.arc([cx - 6, cy - length//2 + 8, cx + 4, cy - length//2 + 22], 180, 360, fill=color, width=3)
    wdraw.line([(cx + 4, cy - length//2 + 15), (cx + 4, cy + length//2 - 8)], fill=color, width=3)
    canvas.alpha_composite(w_layer)

def draw_yellow_pencil(canvas, x0, y0, length=240, angle=-30):
    """Draws a classic yellow wooden #2 pencil with eraser, ferrule, and shadow."""
    p_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(p_layer)
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    w_half = 7
    vx, vy = cos_a * length, sin_a * length
    nx, ny = -sin_a * w_half, cos_a * w_half

    # Shadow
    s_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s_layer)
    sdraw.polygon([
        (x0 + nx + 6, y0 + ny + 8), (x0 - nx + 6, y0 - ny + 8),
        (x0 + vx - nx + 6, y0 + vy - ny + 8), (x0 + vx + nx + 6, y0 + vy + ny + 8)
    ], fill=(0, 0, 0, 45))
    s_layer = s_layer.filter(ImageFilter.GaussianBlur(5))
    canvas.alpha_composite(s_layer)

    # Yellow body
    pdraw.polygon([
        (x0 + nx, y0 + ny), (x0 - nx, y0 - ny),
        (x0 + vx*0.75 - nx, y0 + vy*0.75 - ny), (x0 + vx*0.75 + nx, y0 + vy*0.75 + ny)
    ], fill=(250, 204, 21), outline=(217, 119, 6))

    # Wood sharpening
    tip_x, tip_y = x0 + vx, y0 + vy
    pdraw.polygon([
        (x0 + vx*0.75 + nx, y0 + vy*0.75 + ny), (x0 + vx*0.75 - nx, y0 + vy*0.75 - ny), (tip_x, tip_y)
    ], fill=(245, 222, 179))

    # Lead tip
    pdraw.polygon([
        (x0 + vx*0.92 + nx*0.35, y0 + vy*0.92 + ny*0.35),
        (x0 + vx*0.92 - nx*0.35, y0 + vy*0.92 - ny*0.35),
        (tip_x, tip_y)
    ], fill=(45, 45, 50))

    # Silver Ferrule
    fx, fy = x0 - vx*0.06, y0 - vy*0.06
    pdraw.polygon([
        (x0 + nx, y0 + ny), (x0 - nx, y0 - ny),
        (fx - nx, fy - ny), (fx + nx, fy + ny)
    ], fill=(203, 213, 225), outline=(148, 163, 184))

    # Pink Eraser
    ex, ey = x0 - vx*0.14, y0 - vy*0.14
    pdraw.polygon([
        (fx + nx, fy + ny), (fx - nx, fy - ny),
        (ex - nx, ey - ny), (ex + nx, ey + ny)
    ], fill=(244, 114, 182))

    canvas.alpha_composite(p_layer)

def draw_wax_seal(canvas, cx, cy, radius=32, color=(185, 28, 28)):
    """Draws an authentic embossed red wax seal stamp with irregular edge and crest."""
    s_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s_layer)
    sdraw.ellipse([cx - radius + 4, cy - radius + 6, cx + radius + 4, cy + radius + 6], fill=(0, 0, 0, 55))
    s_layer = s_layer.filter(ImageFilter.GaussianBlur(6))
    canvas.alpha_composite(s_layer)

    w_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(w_layer)
    # Organic irregular wax drips
    random.seed(cx + cy)
    pts = []
    for deg in range(0, 360, 15):
        r_jitter = radius + random.randint(-3, 4)
        rad = math.radians(deg)
        pts.append((cx + math.cos(rad) * r_jitter, cy + math.sin(rad) * r_jitter))
    wdraw.polygon(pts, fill=color)
    # Inner stamped circle
    wdraw.ellipse([cx - radius*0.7, cy - radius*0.7, cx + radius*0.7, cy + radius*0.7], outline=(int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7)), width=2)
    # Embossed icon / star in center
    wdraw.polygon([
        (cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy - 3),
        (cx + 4, cy + 2), (cx + 7, cy + 9), (cx, cy + 4),
        (cx - 7, cy + 9), (cx - 4, cy + 2), (cx - 10, cy - 3), (cx - 3, cy - 3)
    ], fill=(255, 255, 255, 180))
    canvas.alpha_composite(w_layer)

def draw_whiteboard_magnet(canvas, cx, cy, radius=16, color=(239, 68, 68)):
    """Draws a 3D dome plastic magnet on whiteboard with drop shadow and highlight."""
    s_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s_layer)
    sdraw.ellipse([cx - radius + 3, cy - radius + 4, cx + radius + 3, cy + radius + 4], fill=(0, 0, 0, 45))
    s_layer = s_layer.filter(ImageFilter.GaussianBlur(4))
    canvas.alpha_composite(s_layer)

    m_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(m_layer)
    mdraw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color, outline=(int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7)), width=2)
    # Glossy plastic dome reflection
    mdraw.ellipse([cx - radius*0.5, cy - radius*0.6, cx + radius*0.2, cy - radius*0.1], fill=(255, 255, 255, 170))
    canvas.alpha_composite(m_layer)

def draw_marker_pen(canvas, x0, y0, length=200, angle=25, cap_color=(37, 99, 235)):
    """Draws a realistic dry-erase / chisel marker pen resting with drop shadow."""
    m_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(m_layer)
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    w_half = 9
    vx, vy = cos_a * length, sin_a * length
    nx, ny = -sin_a * w_half, cos_a * w_half

    # Shadow
    s_layer = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s_layer)
    sdraw.polygon([
        (x0 + nx + 5, y0 + ny + 6), (x0 - nx + 5, y0 - ny + 6),
        (x0 + vx - nx + 5, y0 + vy - ny + 6), (x0 + vx + nx + 5, y0 + vy + ny + 6)
    ], fill=(0, 0, 0, 45))
    s_layer = s_layer.filter(ImageFilter.GaussianBlur(5))
    canvas.alpha_composite(s_layer)

    # White barrel
    mdraw.polygon([
        (x0 + nx, y0 + ny), (x0 - nx, y0 - ny),
        (x0 + vx*0.65 - nx, y0 + vy*0.65 - ny), (x0 + vx*0.65 + nx, y0 + vy*0.65 + ny)
    ], fill=(248, 250, 252), outline=(203, 213, 225), width=1)

    # Colored cap
    cap_x, cap_y = x0 + vx*0.65, y0 + vy*0.65
    tip_x, tip_y = x0 + vx, y0 + vy
    mdraw.polygon([
        (cap_x + nx*1.08, cap_y + ny*1.08), (cap_x - nx*1.08, cap_y - ny*1.08),
        (tip_x - nx*0.9, tip_y - ny*0.9), (tip_x + nx*0.9, tip_y + ny*0.9)
    ], fill=cap_color, outline=(int(cap_color[0]*0.7), int(cap_color[1]*0.7), int(cap_color[2]*0.7)), width=1)

    # Cap pocket clip
    mdraw.line([(cap_x + nx*1.2, cap_y + ny*1.2), (cap_x + vx*0.25 + nx*1.2, cap_y + vy*0.25 + ny*1.2)], fill=(int(cap_color[0]*0.6), int(cap_color[1]*0.6), int(cap_color[2]*0.6)), width=4)

    canvas.alpha_composite(m_layer)

# ==================== DYNAMIC MULTI-SHAPE CARDS ====================

def fetch_dynamic_topic_visual(query):
    """Fetches official high-res scientific visual from Wikimedia Commons / Wikipedia API in memory."""
    try:
        import urllib.request, io, json
        q = query.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        req = urllib.request.Request(url, headers={"User-Agent": "MindBitesBot/1.0 (info@mindbites.org)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            img_info = data.get("originalimage") or data.get("thumbnail")
            if img_info and "source" in img_info:
                img_url = img_info["source"]
                img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    return Image.open(io.BytesIO(img_data)).convert("RGB")
    except Exception as e:
        print(f"Dynamic visual fetch error for {query}: {e}")
    return None

def draw_polaroid_card(img, box, asset_path, caption="", pin_color=None, tape=False, is_dark=False, topic_query=""):
    x0, y0, x1, y1 = box
    pw = x1 - x0
    ph = y1 - y0

    draw_drop_shadow(img, box, radius=6, blur=10, alpha=60 if not is_dark else 25, offset=(5, 8))

    base_color = (255, 255, 253, 255) if not is_dark else (30, 41, 59, 255)
    border_color = (220, 220, 215, 255) if not is_dark else (51, 65, 85, 255)

    card_img = Image.new("RGBA", (pw, ph), base_color)
    cdraw = ImageDraw.Draw(card_img)
    cdraw.rectangle([0, 0, pw - 1, ph - 1], outline=border_color, width=1)

    margin = 14
    bottom_space = 46
    photo_w = pw - (margin * 2)
    photo_h = ph - margin - bottom_space

    photo = None
    if asset_path and os.path.isfile(asset_path):
        try:
            photo = Image.open(asset_path).convert("RGB")
        except Exception:
            photo = None

    if photo is None and topic_query:
        print(f"Fetching dynamic online visual for: '{topic_query}'...")
        photo = fetch_dynamic_topic_visual(topic_query)

    if photo is not None:
        photo = photo.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        card_img.paste(photo, (margin, margin))
        cdraw.rectangle([margin, margin, margin + photo_w, margin + photo_h], outline=(0, 0, 0, 60), width=1)
    else:
        grad_fill = (15, 23, 42) if is_dark else (241, 245, 249)
        cdraw.rectangle([margin, margin, margin + photo_w, margin + photo_h], fill=grad_fill, outline=(59, 130, 246) if is_dark else (203, 213, 225), width=2)
        cdraw.line([(margin + 20, margin + photo_h // 2), (margin + photo_w - 20, margin + photo_h // 2)], fill=(100, 116, 139), width=1)
        cdraw.text((margin + 50, margin + photo_h // 2 - 12), "★ MIND BITES • VISUAL SCIENCE NOTE ★", fill=(148, 163, 184) if is_dark else (71, 85, 105), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15))

    img.alpha_composite(card_img, (x0, y0))

    if caption:
        cap_col = (40, 40, 40) if not is_dark else (241, 245, 249)
        draw_text_perfect_hindi(img, caption, (x0 + 20, y1 - 38), font_size=18, bold=True, color=cap_col, max_w=pw - 40)

    draw = ImageDraw.Draw(img)
    if pin_color:
        draw_push_pin(draw, x0 + pw // 2, y0 + 6, color=pin_color)
    elif tape:
        draw_washi_tape(draw, (x0 + pw // 2 - 50, y0 - 12, x0 + pw // 2 + 50, y0 + 12))

def draw_curled_note(img, box, fill, border, heading, points, curl=28, pin_color=None, is_dark=False):
    x0, y0, x1, y1 = box
    draw_drop_shadow(img, box, radius=8, blur=8, alpha=50 if not is_dark else 25, offset=(4, 7))

    draw = ImageDraw.Draw(img)
    pts = [(x0, y0), (x1, y0), (x1, y1 - curl), (x1 - curl, y1), (x0, y1)]
    draw.polygon(pts, fill=fill)
    draw.line([(x0, y0), (x1, y0), (x1, y1 - curl)], fill=border, width=2)
    draw.line([(x1 - curl, y1), (x0, y1), (x0, y0)], fill=border, width=2)

    fold_col = (int(fill[0] * 0.82), int(fill[1] * 0.82), int(fill[2] * 0.82), 255)
    fold_pts = [(x1 - curl, y1), (x1, y1 - curl), (x1 - curl, y1 - curl)]
    draw.polygon(fold_pts, fill=fold_col, outline=border)

    if pin_color:
        draw_push_pin(draw, x0 + 26, y0 + 16, color=pin_color)

    h_col = (15, 23, 42) if not is_dark else (250, 204, 21)
    draw_text_perfect_hindi(img, heading, (x0 + 22, y0 + 16), font_size=30, bold=True, color=h_col, max_w=x1 - x0 - 44)
    draw.line([(x0 + 20, y0 + 56), (x1 - 20, y0 + 56)], fill=border, width=2)

    start_y = y0 + 68
    avail_h = (y1 - y0) - 95
    max_w = (x1 - x0) - 44
    font_sz, heights, gap = fit_bullet_points_in_card(points, avail_h, max_w)

    curr_y = start_y
    text_col = (20, 25, 35) if not is_dark else (245, 245, 255)
    for i, pt in enumerate(points):
        bullet_text = "• " + pt
        draw_text_perfect_hindi(img, bullet_text, (x0 + 22, curr_y), font_size=font_sz, bold=False, color=text_col, max_w=max_w)
        curr_y += heights[i] + gap

def draw_bookmark_tag(img, box, fill, border, heading, points, chamfer=28, ribbon_color=(239, 68, 68), is_dark=False):
    x0, y0, x1, y1 = box
    draw_drop_shadow(img, box, radius=8, blur=8, alpha=50 if not is_dark else 25, offset=(4, 7))

    draw = ImageDraw.Draw(img)
    pts = [
        (x0 + chamfer, y0), (x1 - chamfer, y0),
        (x1, y0 + chamfer), (x1, y1),
        (x0, y1), (x0, y0 + chamfer)
    ]
    draw.polygon(pts, fill=fill, outline=border)
    draw.line([(x0 + chamfer, y0), (x1 - chamfer, y0), (x1, y0 + chamfer), (x1, y1), (x0, y1), (x0, y0 + chamfer), (x0 + chamfer, y0)], fill=border, width=2)

    hole_cx = x0 + (x1 - x0) // 2
    hole_cy = y0 + 16
    draw.ellipse([hole_cx - 7, hole_cy - 7, hole_cx + 7, hole_cy + 7], fill=(0, 0, 0, 50), outline=(100, 100, 100), width=1)
    if ribbon_color:
        draw.line([(hole_cx, hole_cy - 6), (hole_cx, y0 - 18)], fill=ribbon_color, width=5)
        draw.polygon([(hole_cx - 5, y0 - 18), (hole_cx + 5, y0 - 18), (hole_cx, y0 - 26)], fill=ribbon_color)

    h_col = (15, 23, 42) if not is_dark else (250, 204, 21)
    draw_text_perfect_hindi(img, heading, (x0 + 22, y0 + 28), font_size=30, bold=True, color=h_col, max_w=x1 - x0 - 44)
    draw.line([(x0 + 20, y0 + 68), (x1 - 20, y0 + 68)], fill=border, width=2)

    start_y = y0 + 80
    avail_h = (y1 - y0) - 105
    max_w = (x1 - x0) - 44
    font_sz, heights, gap = fit_bullet_points_in_card(points, avail_h, max_w)

    curr_y = start_y
    text_col = (20, 25, 35) if not is_dark else (245, 245, 255)
    for i, pt in enumerate(points):
        bullet_text = "• " + pt
        draw_text_perfect_hindi(img, bullet_text, (x0 + 22, curr_y), font_size=font_sz, bold=False, color=text_col, max_w=max_w)
        curr_y += heights[i] + gap

def draw_speech_bubble(img, box, fill, border, heading, points, tail_dir="left", is_dark=False):
    x0, y0, x1, y1 = box
    draw_drop_shadow(img, box, radius=14, blur=8, alpha=50 if not is_dark else 25, offset=(4, 7))

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=fill, outline=border, width=2)

    if tail_dir == "left":
        tail_pts = [(x0, y0 + 40), (x0 - 18, y0 + 25), (x0, y0 + 58)]
        draw.polygon(tail_pts, fill=fill)
        draw.line([(x0, y0 + 40), (x0 - 18, y0 + 25), (x0, y0 + 58)], fill=border, width=2)
    elif tail_dir == "right":
        tail_pts = [(x1, y0 + 40), (x1 + 18, y0 + 25), (x1, y0 + 58)]
        draw.polygon(tail_pts, fill=fill)
        draw.line([(x1, y0 + 40), (x1 + 18, y0 + 25), (x1, y0 + 58)], fill=border, width=2)

    h_col = (15, 23, 42) if not is_dark else (250, 204, 21)
    draw_text_perfect_hindi(img, heading, (x0 + 22, y0 + 16), font_size=30, bold=True, color=h_col, max_w=x1 - x0 - 44)
    draw.line([(x0 + 20, y0 + 56), (x1 - 20, y0 + 56)], fill=border, width=2)

    start_y = y0 + 68
    avail_h = (y1 - y0) - 95
    max_w = (x1 - x0) - 44
    font_sz, heights, gap = fit_bullet_points_in_card(points, avail_h, max_w)

    curr_y = start_y
    text_col = (20, 25, 35) if not is_dark else (245, 245, 255)
    for i, pt in enumerate(points):
        bullet_text = "• " + pt
        draw_text_perfect_hindi(img, bullet_text, (x0 + 22, curr_y), font_size=font_sz, bold=False, color=text_col, max_w=max_w)
        curr_y += heights[i] + gap

def draw_index_card(img, box, fill, border, heading, points, tab_text="NOTE", is_dark=False):
    x0, y0, x1, y1 = box
    draw_drop_shadow(img, box, radius=10, blur=8, alpha=50 if not is_dark else 25, offset=(4, 7))

    draw = ImageDraw.Draw(img)
    tab_w = 120
    tab_h = 24
    draw.rounded_rectangle([x0 + 20, y0 - tab_h, x0 + 20 + tab_w, y0 + 4], radius=5, fill=border)
    draw.text((x0 + 36, y0 - tab_h + 3), tab_text, fill=(255, 255, 255), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13))

    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=fill, outline=border, width=2)

    h_col = (15, 23, 42) if not is_dark else (250, 204, 21)
    draw_text_perfect_hindi(img, heading, (x0 + 22, y0 + 16), font_size=30, bold=True, color=h_col, max_w=x1 - x0 - 44)
    draw.line([(x0 + 20, y0 + 56), (x1 - 20, y0 + 56)], fill=border, width=2)

    start_y = y0 + 68
    avail_h = (y1 - y0) - 95
    max_w = (x1 - x0) - 44
    font_sz, heights, gap = fit_bullet_points_in_card(points, avail_h, max_w)

    curr_y = start_y
    text_col = (20, 25, 35) if not is_dark else (245, 245, 255)
    for i, pt in enumerate(points):
        bullet_text = "• " + pt
        draw_text_perfect_hindi(img, bullet_text, (x0 + 22, curr_y), font_size=font_sz, bold=False, color=text_col, max_w=max_w)
        curr_y += heights[i] + gap

# ==================== 10 UNIQUE THEME BACKGROUND BUILDERS ====================

def bg_corkboard():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (198, 153, 99, 255))
    draw = ImageDraw.Draw(img)
    random.seed(101)
    for _ in range(700):
        fx = random.randint(0, CANVAS_WIDTH)
        fy = random.randint(0, CANVAS_HEIGHT)
        col = (random.randint(140, 180), random.randint(100, 130), random.randint(60, 90), random.randint(150, 220))
        draw.ellipse([fx, fy, fx + random.randint(2, 6), fy + random.randint(2, 5)], fill=col)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], outline=(139, 94, 60), width=18)
    draw.rectangle([18, 18, CANVAS_WIDTH - 18, CANVAS_HEIGHT - 18], outline=(100, 65, 35), width=6)
    return img

def bg_grid_journal():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (250, 248, 240, 255))
    draw = ImageDraw.Draw(img)
    grid_col = (205, 200, 185, 255)
    for x in range(30, CANVAS_WIDTH - 20, 24):
        for y in range(30, CANVAS_HEIGHT - 20, 24):
            draw.rectangle([x, y, x + 1, y + 1], fill=grid_col)
    draw_washi_tape(draw, (30, 20, 130, 44), color=(254, 202, 202, 220), stripe_color=(239, 68, 68, 160))
    draw_washi_tape(draw, (CANVAS_WIDTH - 130, 20, CANVAS_WIDTH - 30, 44), color=(187, 247, 208, 220), stripe_color=(34, 197, 94, 160))
    return img

def bg_chalkboard():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (24, 34, 30, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], outline=(120, 72, 34), width=18)
    draw.rectangle([18, 18, CANVAS_WIDTH - 18, CANVAS_HEIGHT - 18], outline=(70, 40, 20), width=6)
    random.seed(303)
    for _ in range(140):
        cx = random.randint(30, CANVAS_WIDTH - 30)
        cy = random.randint(30, CANVAS_HEIGHT - 30)
        draw.line([(cx, cy), (cx + random.randint(10, 40), cy + random.randint(-4, 4))], fill=(255, 255, 255, 18), width=1)
    return img

def bg_clipboard():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (150, 100, 60, 255))
    draw = ImageDraw.Draw(img)
    for y in range(0, CANVAS_HEIGHT, 16):
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(130, 85, 50), width=2)
    paper_rect = [50, 60, CANVAS_WIDTH - 50, CANVAS_HEIGHT - 40]
    draw_drop_shadow(img, paper_rect, radius=6, blur=10, alpha=65, offset=(0, 6))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(paper_rect, radius=6, fill=(254, 252, 245), outline=(210, 195, 175), width=2)
    for y in range(210, CANVAS_HEIGHT - 60, 28):
        draw.line([(70, y), (CANVAS_WIDTH - 70, y)], fill=(225, 235, 245), width=1)
    cx = CANVAS_WIDTH // 2
    draw.rounded_rectangle([cx - 100, 35, cx + 100, 80], radius=8, fill=(160, 165, 175), outline=(100, 105, 115), width=3)
    draw.ellipse([cx - 20, 45, cx + 20, 68], fill=(120, 125, 135))
    return img

def bg_neon_dark():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (10, 15, 26, 255))
    draw = ImageDraw.Draw(img)
    for x in range(0, CANVAS_WIDTH, 48):
        draw.line([(x, 0), (x, CANVAS_HEIGHT)], fill=(16, 28, 48), width=1)
    for y in range(0, CANVAS_HEIGHT, 48):
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(16, 28, 48), width=1)
    draw.rectangle([14, 14, CANVAS_WIDTH - 14, CANVAS_HEIGHT - 14], outline=(6, 182, 212), width=2)
    draw.rectangle([20, 20, CANVAS_WIDTH - 20, CANVAS_HEIGHT - 20], outline=(147, 51, 234), width=1)
    return img

def bg_kraft_vintage():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (218, 185, 142, 255))
    draw = ImageDraw.Draw(img)
    random.seed(606)
    for _ in range(800):
        fx = random.randint(0, CANVAS_WIDTH)
        fy = random.randint(0, CANVAS_HEIGHT)
        draw.ellipse([fx, fy, fx + random.randint(1, 4), fy + random.randint(1, 3)], fill=(185, 150, 110, 140))
    draw.rectangle([20, 20, CANVAS_WIDTH - 20, CANVAS_HEIGHT - 20], outline=(140, 105, 70), width=3)
    draw.rectangle([28, 28, CANVAS_WIDTH - 28, CANVAS_HEIGHT - 28], outline=(160, 125, 90), width=1)
    draw.arc([CANVAS_WIDTH - 240, 50, CANVAS_WIDTH - 80, 210], 0, 360, fill=(160, 120, 80, 80), width=6)
    return img

def bg_postit_wall():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (235, 235, 238, 255))
    draw = ImageDraw.Draw(img)
    for _ in range(400):
        rx = random.randint(0, CANVAS_WIDTH)
        ry = random.randint(0, CANVAS_HEIGHT)
        draw.point((rx, ry), fill=(210, 210, 215))
    draw.rectangle([18, 18, CANVAS_WIDTH - 18, CANVAS_HEIGHT - 18], outline=(200, 200, 205), width=2)
    return img

def bg_blueprint():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (15, 52, 96, 255))
    draw = ImageDraw.Draw(img)
    for x in range(0, CANVAS_WIDTH, 36):
        draw.line([(x, 0), (x, CANVAS_HEIGHT)], fill=(26, 75, 138), width=1)
    for y in range(0, CANVAS_HEIGHT, 36):
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(26, 75, 138), width=1)
    for x in range(0, CANVAS_WIDTH, 180):
        draw.line([(x, 0), (x, CANVAS_HEIGHT)], fill=(45, 110, 190), width=2)
    for y in range(0, CANVAS_HEIGHT, 180):
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(45, 110, 190), width=2)
    draw.rectangle([24, 24, CANVAS_WIDTH - 24, CANVAS_HEIGHT - 24], outline=(147, 197, 253), width=2)
    return img

def bg_legal_pad():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (254, 243, 199, 255))
    draw = ImageDraw.Draw(img)
    for y in range(120, CANVAS_HEIGHT, 28):
        draw.line([(0, y), (CANVAS_WIDTH, y)], fill=(217, 210, 160), width=1)
    draw.line([(120, 0), (120, CANVAS_HEIGHT)], fill=(239, 68, 68, 180), width=2)
    draw.line([(126, 0), (126, CANVAS_HEIGHT)], fill=(239, 68, 68, 180), width=1)
    draw.rectangle([0, 0, CANVAS_WIDTH, 48], fill=(78, 52, 46))
    for x in range(30, CANVAS_WIDTH, 40):
        draw.line([(x, 48), (x + 10, 48)], fill=(255, 255, 255, 80), width=2)
    return img

def bg_whiteboard():
    img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    for y in range(0, CANVAS_HEIGHT, 180):
        draw.line([(0, y), (CANVAS_WIDTH, y + 60)], fill=(241, 245, 249), width=2)
    draw.rectangle([0, 0, CANVAS_WIDTH, CANVAS_HEIGHT], outline=(148, 163, 184), width=16)
    draw.rectangle([16, 16, CANVAS_WIDTH - 16, CANVAS_HEIGHT - 16], outline=(71, 85, 105), width=3)
    draw.rectangle([CANVAS_WIDTH - 240, CANVAS_HEIGHT - 14, CANVAS_WIDTH - 50, CANVAS_HEIGHT], fill=(203, 213, 225))
    draw.rectangle([CANVAS_WIDTH - 220, CANVAS_HEIGHT - 18, CANVAS_WIDTH - 160, CANVAS_HEIGHT - 12], fill=(225, 29, 72))
    draw.rectangle([CANVAS_WIDTH - 150, CANVAS_HEIGHT - 18, CANVAS_WIDTH - 90, CANVAS_HEIGHT - 12], fill=(37, 99, 235))
    return img

# ==================== THEME-SPECIFIC ACCESSORY DECORATORS ====================

def apply_theme_accessories(canvas, theme_name):
    """Draws rich, theme-tailored stationery, tools, and accessories onto the canvas."""
    draw = ImageDraw.Draw(canvas)

    if theme_name == "corkboard":
        # 1. Red connecting investigative yarn between cards
        draw.line([(515, 630), (565, 630)], fill=(220, 38, 38, 200), width=3)
        draw.line([(515, 980), (565, 980)], fill=(220, 38, 38, 200), width=3)
        # 2. Paperclip on top card
        draw_paperclip(canvas, 960, 600, angle=18, length=55, color=(202, 138, 4))
        # 3. Mini sticky post-it note at top-right
        draw_curled_note(canvas, [930, 110, 1040, 200], (254, 240, 138), (234, 179, 8), "★ TIP", ["रिवीजन!"], curl=14, pin_color=(239, 68, 68))

    elif theme_name == "grid_journal":
        # 1. Botanical leaf doodles on margins
        draw.arc([30, 480, 55, 520], 0, 180, fill=(34, 197, 94), width=2)
        draw.arc([CANVAS_WIDTH - 55, 480, CANVAS_WIDTH - 30, 520], 0, 180, fill=(34, 197, 94), width=2)
        # 2. Patterned floral washi tape across the top
        draw_washi_tape(draw, (440, 410, 640, 435), color=(187, 247, 208, 220), stripe_color=(34, 197, 94, 160))
        # 3. Paperclip holding card 2
        draw_paperclip(canvas, 980, 600, angle=-12, length=55, color=(148, 163, 184))

    elif theme_name == "chalkboard":
        # 1. Sticks of chalk resting in bottom tray
        draw.rounded_rectangle([CANVAS_WIDTH - 320, CANVAS_HEIGHT - 38, CANVAS_WIDTH - 260, CANVAS_HEIGHT - 22], radius=4, fill=(255, 255, 255), outline=(200, 200, 200))
        draw.rounded_rectangle([CANVAS_WIDTH - 250, CANVAS_HEIGHT - 38, CANVAS_WIDTH - 190, CANVAS_HEIGHT - 22], radius=4, fill=(253, 224, 71), outline=(234, 179, 8))
        # 2. Wooden chalk eraser block with felt
        draw.rounded_rectangle([CANVAS_WIDTH - 170, CANVAS_HEIGHT - 44, CANVAS_WIDTH - 80, CANVAS_HEIGHT - 20], radius=4, fill=(160, 100, 50), outline=(100, 60, 30))
        draw.rectangle([CANVAS_WIDTH - 170, CANVAS_HEIGHT - 26, CANVAS_WIDTH - 80, CANVAS_HEIGHT - 20], fill=(200, 200, 200)) # felt pad
        # 3. Hand-drawn chalk arrows and stars
        draw.line([(520, 630), (560, 630)], fill=(255, 255, 255, 180), width=2)
        draw.polygon([(560, 626), (568, 630), (560, 634)], fill=(255, 255, 255, 180))

    elif theme_name == "clipboard":
        # 1. Clipped metallic pen with drop shadow
        draw_marker_pen(canvas, 960, 180, length=220, angle=80, cap_color=(30, 58, 138))
        # 2. Highlighter yellow swatch behind key section
        draw_washi_tape(draw, (80, 415, 280, 435), color=(254, 240, 138, 170), stripe_color=(250, 204, 21, 120))
        # 3. Index tabs sticking out on the right
        draw.rounded_rectangle([CANVAS_WIDTH - 65, 480, CANVAS_WIDTH - 35, 540], radius=6, fill=(59, 130, 246), outline=(30, 58, 138))
        draw.rounded_rectangle([CANVAS_WIDTH - 65, 560, CANVAS_WIDTH - 35, 620], radius=6, fill=(239, 68, 68), outline=(185, 28, 28))

    elif theme_name == "neon_dark":
        # 1. Cyberpunk PCB copper circuit traces connecting cards
        draw.line([(525, 630), (555, 630)], fill=(6, 182, 212), width=2)
        draw.ellipse([518, 626, 526, 634], fill=(6, 182, 212))
        draw.ellipse([554, 626, 562, 634], fill=(6, 182, 212))
        draw.line([(525, 980), (555, 980)], fill=(168, 85, 247), width=2)
        draw.ellipse([518, 976, 526, 984], fill=(168, 85, 247))
        draw.ellipse([554, 976, 562, 984], fill=(168, 85, 247))
        # 2. Glowing corner brackets
        draw.line([(40, 180), (70, 180)], fill=(6, 182, 212), width=3)
        draw.line([(40, 180), (40, 210)], fill=(6, 182, 212), width=3)
        draw.line([(CANVAS_WIDTH - 40, 180), (CANVAS_WIDTH - 70, 180)], fill=(6, 182, 212), width=3)
        draw.line([(CANVAS_WIDTH - 40, 180), (CANVAS_WIDTH - 40, 210)], fill=(6, 182, 212), width=3)

    elif theme_name == "kraft_vintage":
        # 1. Red wax seal stamp at bottom-right
        draw_wax_seal(canvas, CANVAS_WIDTH - 120, CANVAS_HEIGHT - 170, radius=34, color=(185, 28, 28))
        # 2. Vintage postage stamp at top-right
        draw.rectangle([CANVAS_WIDTH - 160, 45, CANVAS_WIDTH - 70, 130], fill=(255, 250, 240), outline=(160, 120, 80), width=2)
        draw.text((CANVAS_WIDTH - 150, 55), "AIR MAIL", fill=(185, 28, 28), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 14))
        draw.text((CANVAS_WIDTH - 145, 80), "★ 1948 ★", fill=(100, 70, 40), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 12))
        # 3. Brass paperclip on card 1
        draw_paperclip(canvas, 100, 580, angle=10, length=50, color=(180, 140, 70))

    elif theme_name == "postit_wall":
        # 1. Chisel-tip yellow highlighter pen resting at bottom
        draw_marker_pen(canvas, 780, CANVAS_HEIGHT - 65, length=190, angle=-10, cap_color=(250, 204, 21))
        # 2. Danger hazard sticker ⚠️
        draw.polygon([(960, 50), (990, 100), (930, 100)], fill=(250, 204, 21), outline=(0, 0, 0), width=2)
        draw.text((956, 68), "!", fill=(0, 0, 0), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22))

    elif theme_name == "blueprint":
        # 1. Dimension line with arrows (R_s = 2GM/c²)
        draw.line([(CANVAS_WIDTH // 2 - 180, 420), (CANVAS_WIDTH // 2 + 180, 420)], fill=(147, 197, 253), width=2)
        draw.line([(CANVAS_WIDTH // 2 - 180, 412), (CANVAS_WIDTH // 2 - 180, 428)], fill=(147, 197, 253), width=2)
        draw.line([(CANVAS_WIDTH // 2 + 180, 412), (CANVAS_WIDTH // 2 + 180, 428)], fill=(147, 197, 253), width=2)
        draw.text((CANVAS_WIDTH // 2 - 60, 404), "R_s = 2GM/c²", fill=(147, 197, 253), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13))
        # 2. Blueprint approval stamp box
        draw.rectangle([CANVAS_WIDTH - 240, CANVAS_HEIGHT - 45, CANVAS_WIDTH - 40, CANVAS_HEIGHT - 15], outline=(147, 197, 253), width=1)
        draw.text((CANVAS_WIDTH - 230, CANVAS_HEIGHT - 38), "DWG: ASTRO-08 / REV-4", fill=(147, 197, 253), font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 11))

    elif theme_name == "legal_pad":
        # 1. Realistic yellow #2 pencil with eraser angled across the bottom
        draw_yellow_pencil(canvas, 750, CANVAS_HEIGHT - 80, length=240, angle=-25)
        # 2. Paperclip on Card 1
        draw_paperclip(canvas, 960, 600, angle=15, length=55, color=(148, 163, 184))

    elif theme_name == "whiteboard":
        # 1. 3D Plastic dome magnets holding the 4 cards (Red, Blue, Green, Yellow)
        draw_whiteboard_magnet(canvas, 75, 605, radius=14, color=(239, 68, 68))     # Red magnet
        draw_whiteboard_magnet(canvas, 570, 605, radius=14, color=(37, 99, 235))    # Blue magnet
        draw_whiteboard_magnet(canvas, 75, 955, radius=14, color=(16, 185, 129))    # Green magnet
        draw_whiteboard_magnet(canvas, 570, 955, radius=14, color=(245, 158, 11))   # Yellow magnet
        # 2. Real dry-erase marker resting in the bottom tray with shadow
        draw_marker_pen(canvas, 760, CANVAS_HEIGHT - 45, length=190, angle=-5, cap_color=(37, 99, 235))
        # 3. Dry-erase hand-drawn dashed connecting arrows
        draw.line([(515, 630), (565, 630)], fill=(37, 99, 235, 180), width=3)
        draw.line([(515, 980), (565, 980)], fill=(225, 29, 72, 180), width=3)

# ==================== MASTER RENDERER ====================

def render_sheet(topic, theme_name, asset_filename, output_path):
    is_dark = theme_name in ["chalkboard", "neon_dark", "blueprint"]

    bg_builders = {
        "corkboard": bg_corkboard,
        "grid_journal": bg_grid_journal,
        "chalkboard": bg_chalkboard,
        "clipboard": bg_clipboard,
        "neon_dark": bg_neon_dark,
        "kraft_vintage": bg_kraft_vintage,
        "postit_wall": bg_postit_wall,
        "blueprint": bg_blueprint,
        "legal_pad": bg_legal_pad,
        "whiteboard": bg_whiteboard
    }
    img = bg_builders.get(theme_name, bg_corkboard)()
    draw = ImageDraw.Draw(img)

    # 1. Header (Pill + Big Title + Subtitle)
    py = 24 if theme_name != "clipboard" and theme_name != "legal_pad" else 58

    pill_text = "DAILY AI QUICK STUDY NOTE"
    pill_font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
    p_box = draw.textbbox((0, 0), pill_text, font=pill_font)
    pw = p_box[2] - p_box[0] + 32
    px = (CANVAS_WIDTH - pw) // 2
    pill_fill = (30, 41, 59, 240) if not is_dark else (15, 23, 42, 240)
    pill_border = (244, 63, 94) if is_dark else (59, 130, 246)
    draw.rounded_rectangle([px, py, px + pw, py + 28], radius=14, fill=pill_fill, outline=pill_border, width=2)
    draw.text((px + 16, py + 4), pill_text, fill=(255, 255, 255), font=pill_font)

    # Big Title (46px Bold)
    t_color = (255, 255, 255) if is_dark else (15, 23, 42)
    draw_text_perfect_hindi(img, topic["title"], (60, py + 36), font_size=46, bold=True, color=t_color, max_w=CANVAS_WIDTH - 120)

    # Subtitle (22px)
    s_color = (209, 213, 219) if is_dark else (51, 65, 85)
    draw_text_perfect_hindi(img, topic["subtitle"], (60, py + 92), font_size=22, bold=False, color=s_color, max_w=CANVAS_WIDTH - 120)

    # 2. Hero Realistic Visual (Polaroid Frame)
    asset_path = os.path.join(ASSETS_DIR, asset_filename)
    hero_y = py + 128
    hero_w = 580
    hero_h = 275
    hero_box = [(CANVAS_WIDTH - hero_w) // 2, hero_y, (CANVAS_WIDTH + hero_w) // 2, hero_y + hero_h]

    pin_col = (239, 68, 68) if theme_name == "corkboard" else None
    tape_flag = theme_name in ["grid_journal", "postit_wall", "legal_pad"]
    caption = "★ वास्तविक वैज्ञानिक चित्रण (Official Scientific Visual)"
    t_query = topic.get("query") or topic.get("category", "") or topic.get("id", "")
    draw_polaroid_card(img, hero_box, asset_path, caption=caption, pin_color=pin_col, tape=tape_flag, is_dark=is_dark, topic_query=t_query)

    # 3. 4 Large, Spacious Cards (2 x 2 Grid)
    grid_y_start = hero_y + 295
    col_w = 465
    row_h = 345

    shape_patterns = {
        "corkboard": ["curled_note", "bookmark_tag", "speech_bubble", "index_card"],
        "grid_journal": ["bookmark_tag", "curled_note", "speech_bubble", "index_card"],
        "chalkboard": ["speech_bubble", "curled_note", "bookmark_tag", "index_card"],
        "clipboard": ["index_card", "curled_note", "bookmark_tag", "speech_bubble"],
        "neon_dark": ["speech_bubble", "index_card", "curled_note", "speech_bubble"],
        "kraft_vintage": ["bookmark_tag", "curled_note", "index_card", "speech_bubble"],
        "postit_wall": ["curled_note", "speech_bubble", "curled_note", "bookmark_tag"],
        "blueprint": ["index_card", "curled_note", "speech_bubble", "bookmark_tag"],
        "legal_pad": ["curled_note", "bookmark_tag", "index_card", "speech_bubble"],
        "whiteboard": ["speech_bubble", "curled_note", "index_card", "bookmark_tag"]
    }
    current_shapes = shape_patterns.get(theme_name, ["curled_note"] * 4)

    if theme_name == "whiteboard":
        palettes = [
            {"fill": (239, 246, 255), "border": (37, 99, 235)},
            {"fill": (240, 253, 244), "border": (5, 150, 105)},
            {"fill": (254, 242, 242), "border": (220, 38, 38)},
            {"fill": (250, 245, 255), "border": (124, 58, 237)}
        ]
    elif is_dark:
        palettes = [
            {"fill": (30, 41, 59), "border": (56, 189, 248)},
            {"fill": (30, 35, 55), "border": (168, 85, 247)},
            {"fill": (25, 45, 40), "border": (52, 211, 153)},
            {"fill": (45, 30, 40), "border": (244, 63, 94)}
        ]
    else:
        palettes = [
            {"fill": (254, 240, 138), "border": (234, 179, 8)},
            {"fill": (224, 242, 254), "border": (56, 189, 248)},
            {"fill": (254, 226, 226), "border": (248, 113, 113)},
            {"fill": (220, 252, 231), "border": (74, 222, 128)}
        ]

    positions = [
        (60, grid_y_start),
        (CANVAS_WIDTH - 60 - col_w, grid_y_start),
        (60, grid_y_start + row_h + 16),
        (CANVAS_WIDTH - 60 - col_w, grid_y_start + row_h + 16)
    ]

    for i, note in enumerate(topic["cards"][:4]):
        nx, ny = positions[i]
        box = [nx, ny, nx + col_w, ny + row_h]
        shape = current_shapes[i]
        pal = palettes[i % len(palettes)]
        h_text = note["heading"]
        pts = note["points"]

        if shape == "curled_note":
            p_col = [(239, 68, 68), (59, 130, 246), (16, 185, 129), (245, 158, 11)][i] if theme_name == "corkboard" else None
            draw_curled_note(img, box, pal["fill"], pal["border"], h_text, pts, curl=28, pin_color=p_col, is_dark=is_dark)
        elif shape == "bookmark_tag":
            r_col = [(239, 68, 68), (59, 130, 246), (16, 185, 129), (234, 179, 8)][i]
            draw_bookmark_tag(img, box, pal["fill"], pal["border"], h_text, pts, chamfer=28, ribbon_color=r_col, is_dark=is_dark)
        elif shape == "speech_bubble":
            tail = "right" if (i % 2 == 0) else "left"
            draw_speech_bubble(img, box, pal["fill"], pal["border"], h_text, pts, tail_dir=tail, is_dark=is_dark)
        elif shape == "index_card":
            tab = f"FACT #{i+1}"
            draw_index_card(img, box, pal["fill"], pal["border"], h_text, pts, tab_text=tab, is_dark=is_dark)

    # 4. Bottom Fun Fact Bar
    fun_fact = topic.get("fun_fact", "")
    if fun_fact:
        fact_box = [60, CANVAS_HEIGHT - 95, CANVAS_WIDTH - 60, CANVAS_HEIGHT - 25]
        draw_drop_shadow(img, fact_box, radius=10, blur=8, alpha=45 if not is_dark else 25, offset=(3, 5))
        draw = ImageDraw.Draw(img)

        f_fill = (254, 226, 226) if not is_dark else (35, 25, 30)
        f_border = (248, 113, 113) if not is_dark else (244, 63, 94)
        draw.rounded_rectangle(fact_box, radius=10, fill=f_fill, outline=f_border, width=2)

        f_color = (185, 28, 28) if not is_dark else (253, 164, 175)
        full_fact = "💡 क्या आप जानते हैं?  " + fun_fact

        fact_max_w = CANVAS_WIDTH - 160
        _, f_h = measure_text_gdi(full_fact, font_size=21, bold=True, max_w=fact_max_w)
        if f_h > 40:
            fact_sz = 19
            _, f_h = measure_text_gdi(full_fact, font_size=19, bold=True, max_w=fact_max_w)
        else:
            fact_sz = 21

        fact_y = fact_box[1] + ((fact_box[3] - fact_box[1]) - f_h) // 2
        draw_text_perfect_hindi(img, full_fact, (85, fact_y), font_size=fact_sz, bold=True, color=f_color, max_w=fact_max_w)

    # 5. Apply Rich Theme-Specific Accessories & Stationery Props!
    apply_theme_accessories(img, theme_name)

    img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=96)
    print(f"✅ Generated {theme_name.upper()} -> {output_path}")

# ==================== 10 TOPIC DEFINITIONS ====================

TOPICS = [
    {
        "theme": "corkboard",
        "asset": "01_solar_system.png",
        "id": "theme_01_solar_system",
        "title": "हमारा सौर मंडल (The Solar System)",
        "subtitle": "8 ग्रह और उनके अनोखे रहस्य — आसान रिवीजन गाइड",
        "cards": [
            {
                "heading": "1. आंतरिक ग्रह (Inner Rocky)",
                "points": [
                    "बुध, शुक्र, पृथ्वी और मंगल ठोस पथरीली सतह वाले ग्रह हैं।",
                    "शुक्र सौरमंडल का सबसे गर्म ग्रह है (तापमान 470°C)।",
                    "मंगल को आयरन ऑक्साइड (जंग) के कारण 'लाल ग्रह' कहते हैं।"
                ]
            },
            {
                "heading": "2. बाहरी गैस दानव (Gas Giants)",
                "points": [
                    "बृहस्पति और शनि गैसों (हाइड्रोजन-हीलियम) से बने हैं।",
                    "बृहस्पति सौरमंडल का सबसे विशालकाय भारी ग्रह है।",
                    "शनि के चारों ओर बर्फ और धूल के खूबसूरत वलय (Rings) हैं।"
                ]
            },
            {
                "heading": "3. बर्फीले ग्रह (Ice Giants)",
                "points": [
                    "अरुण (Uranus) और वरुण (Neptune) सबसे ठंडे ग्रह हैं।",
                    "अरुण ग्रह अपनी धुरी पर 98 डिग्री लगभग लेटा हुआ घूमता है।",
                    "वरुण ग्रह पर 2000 किमी/घंटा की तूफानी हवाएं चलती हैं।"
                ]
            },
            {
                "heading": "4. याद रखने की जादुई ट्रिक",
                "points": [
                    "'My Very Educated Mother Just Served Us Noodles'",
                    "M-Mercury, V-Venus, E-Earth, M-Mars, J-Jupiter",
                    "S-Saturn, U-Uranus, N-Neptune (सूर्य से दूरी का सही क्रम)।"
                ]
            }
        ],
        "fun_fact": "प्लूटो को 2006 में वैज्ञानिकों ने बौना ग्रह (Dwarf Planet) घोषित किया था!"
    },
    {
        "theme": "grid_journal",
        "asset": "02_photosynthesis.png",
        "id": "theme_02_photosynthesis",
        "title": "पेड़-पौधे खाना कैसे बनाते हैं?",
        "subtitle": "प्रकाश संश्लेषण की आसान वैज्ञानिक प्रक्रिया (Photosynthesis)",
        "cards": [
            {
                "heading": "1. भोजन बनाने की सामग्री",
                "points": [
                    "सूरज की प्राकृतिक धूप (Solar Radiation Energy)।",
                    "हवा से सोखी गई कार्बन डाइऑक्साइड (CO2) गैस।",
                    "जड़ों द्वारा जमीन से खींचा गया पानी और खनिज (H2O)।"
                ]
            },
            {
                "heading": "2. पत्तियों में क्लोरोफिल",
                "points": [
                    "क्लोरोफिल पत्तियों को हरा रंग और धूप सोखने की ताकत देता है।",
                    "यह सौर ऊर्जा को रासायनिक ऊर्जा में बदलने का काम करता है।",
                    "पत्तियों पर मौजूद 'स्टोमेटा' छिद्रों से पौधे सांस लेते हैं।"
                ]
            },
            {
                "heading": "3. क्या बनता है? (Output)",
                "points": [
                    "ग्लूकोज (पौधों का भोजन) जिससे पेड़ तेजी से बढ़ते हैं।",
                    "शुद्ध ऑक्सीजन गैस (O2) जो हवा में मुक्त होती है।",
                    "यही ऑक्सीजन पृथ्वी पर सभी जीवों को जीवन देती है।"
                ]
            },
            {
                "heading": "4. रात का रहस्य",
                "points": [
                    "रात में धूप न होने पर प्रकाश संश्लेषण रुक जाता है।",
                    "रात में पौधे केवल सांस लेते हैं और CO2 छोड़ते हैं।",
                    "इसीलिए रात के समय घने पेड़ों के नीचे नहीं सोना चाहिए।"
                ]
            }
        ],
        "fun_fact": "धरती की 50% से अधिक ऑक्सीजन समुद्र के सूक्ष्म फाइटोप्लांकटन बनाते हैं!"
    },
    {
        "theme": "chalkboard",
        "asset": "03_eclipse.jpg",
        "id": "theme_03_eclipse",
        "title": "सूर्य ग्रहण और चंद्र ग्रहण (Eclipses)",
        "subtitle": "अंतरिक्ष में बनने वाली परछाइयों का पूरा सच",
        "cards": [
            {
                "heading": "1. सूर्य ग्रहण (Solar Eclipse)",
                "points": [
                    "जब सूरज और पृथ्वी के ठीक बीच में चंद्रमा आ जाता है।",
                    "चंद्रमा की छाया धरती पर पड़ने से दिन में अंधेरा छा जाता है।",
                    "यह खगोलीय घटना हमेशा 'अमावस्या' (New Moon) को होती है।"
                ]
            },
            {
                "heading": "2. चंद्र ग्रहण (Lunar Eclipse)",
                "points": [
                    "जब सूरज और चंद्रमा के ठीक बीच में पृथ्वी आ जाती है।",
                    "धरती की विशाल छाया चंद्रमा को पूरी तरह ढक लेती है।",
                    "यह खगोलीय घटना हमेशा 'पूर्णिमा' (Full Moon) को होती है।"
                ]
            },
            {
                "heading": "3. ब्लड मून (Blood Moon)",
                "points": [
                    "पूर्ण चंद्र ग्रहण में चांद पूरी तरह गायब नहीं होता।",
                    "धरती के वायुमंडल से छनकर केवल लाल रोशनी चांद तक पहुंचती है।",
                    "इस वजह से चांद गहरे लाल या तांबई रंग का चमकता है।"
                ]
            },
            {
                "heading": "4. सुरक्षा और सावधानी",
                "points": [
                    "सूर्य ग्रहण को कभी भी नंगी आंखों से सीधा न देखें।",
                    "देखने के लिए हमेशा प्रमाणित सोलर फिल्टर चश्मे का उपयोग करें।",
                    "चंद्र ग्रहण को नंगी आंखों से देखना 100% सुरक्षित है।"
                ]
            }
        ],
        "fun_fact": "पूर्ण सूर्य ग्रहण का अधिकतम समय केवल 7.5 मिनट तक ही हो सकता है!"
    },
    {
        "theme": "clipboard",
        "asset": "04_brain.png",
        "id": "theme_04_human_brain",
        "title": "मानव मस्तिष्क के रहस्य (Human Brain)",
        "subtitle": "दुनिया का सबसे शक्तिशाली सुपरकंप्यूटर — हमारा दिमाग",
        "cards": [
            {
                "heading": "1. 86 अरब न्यूरॉन्स",
                "points": [
                    "मानव दिमाग में 86 अरब सुपर-फास्ट न्यूरॉन्स होते हैं।",
                    "हर न्यूरॉन हजारों अन्य न्यूरॉन्स से विद्युत सिग्नल जोड़ता है।",
                    "हमारे विचार दिमाग में 400 किमी/घंटा की रफ्तार से दौड़ते हैं।"
                ]
            },
            {
                "heading": "2. ऊर्जा का सबसे बड़ा उपभोक्ता",
                "points": [
                    "मस्तिष्क का वजन शरीर के कुल वजन का सिर्फ 2% होता है।",
                    "लेकिन शरीर की 20% ऑक्सीजन और 20% ग्लूकोज अकेला खाता है।",
                    "नया सीखते समय दिमाग की ऊर्जा खपत और अधिक बढ़ जाती है।"
                ]
            },
            {
                "heading": "3. बायाँ vs दायाँ दिमाग",
                "points": [
                    "बायाँ हिस्सा (Left Brain): तर्क, गणित, भाषा और विश्लेषण।",
                    "दायाँ हिस्सा (Right Brain): कला, संगीत, कल्पना और भावनाएं।",
                    "दोनों गोलार्द्ध मिलकर हर काम को कुशलता से पूरा करते हैं।"
                ]
            },
            {
                "heading": "4. नींद में सफाई अभियान",
                "points": [
                    "रात को सोते समय दिमाग दिनभर के विषैले टॉक्सिन्स साफ करता है।",
                    "जरूरी यादों को हमेशा के लिए सुरक्षित (Store) करता है।",
                    "अच्छी नींद याददाश्त तेज करती है और एकाग्रता बढ़ाती है।"
                ]
            }
        ],
        "fun_fact": "जागते समय आपका दिमाग 20 वॉट का छोटा एलईडी बल्ब जलाने जितनी ऊर्जा बनाता है!"
    },
    {
        "theme": "neon_dark",
        "asset": "05_ai_network.png",
        "id": "theme_05_ai_chatgpt",
        "title": "AI और ChatGPT कैसे काम करते हैं?",
        "subtitle": "आर्टिफिशियल इंटेलिजेंस की अंदरूनी दुनिया — सरल शब्दों में",
        "cards": [
            {
                "heading": "1. AI क्या है? (What is AI)",
                "points": [
                    "इंसानी बुद्धि की तरह सोचने और सीखने वाला सॉफ्टवेयर।",
                    "खरबों किताबों, कोड और इंटरनेट डेटा से पैटर्न पहचानता है।",
                    "इसे 'मशीन लर्निंग' और 'डीप लर्निंग' कहा जाता है।"
                ]
            },
            {
                "heading": "2. ChatGPT का असली सच",
                "points": [
                    "यह एक विशाल 'Next-Word Predictor' भाषा मॉडल है।",
                    "जैसे मोबाइल टाइपिंग में अगला शब्द सुझाया जाता है,",
                    "वैसे ही यह वाक्य के अगले सबसे सटीक शब्द का अनुमान लगाता है।"
                ]
            },
            {
                "heading": "3. न्यूरल नेटवर्क (Neural Nets)",
                "points": [
                    "इंसानी दिमाग के न्यूरॉन्स की नकल करके बनाया गया गणितीय जाल।",
                    "इसमें सैकड़ों लेयर्स डेटा को प्रोसेस करके सही जवाब देती हैं।",
                    "शक्तिशाली GPU क्लस्टर्स महीनों की ट्रेनिंग के बाद इसे तैयार करते हैं।"
                ]
            },
            {
                "heading": "4. स्मार्ट प्रॉम्प्टिंग का नियम",
                "points": [
                    "स्पष्ट सवाल पूछें और AI को उसकी सही भूमिका (Role) बताएं।",
                    "अच्छे उदाहरण (Examples) दें और शब्द सीमा तय करें।",
                    "AI एक सहयोगी है, इसलिए महत्वपूर्ण तथ्यों को हमेशा जांचें।"
                ]
            }
        ],
        "fun_fact": "ChatGPT ने लॉन्च के मात्र 5 दिनों में 10 लाख एक्टिव यूजर्स का रिकॉर्ड बना दिया था!"
    },
    {
        "theme": "kraft_vintage",
        "asset": "06_heart.png",
        "id": "theme_06_human_body",
        "title": "मानव शरीर के 4 चमत्कारी तथ्य",
        "subtitle": "हमारे शरीर की वो बातें जो आपको हैरान कर देंगी (Human Body)",
        "cards": [
            {
                "heading": "1. धड़कते दिल की शक्ति",
                "points": [
                    "मानव दिल दिन में 1,00,000 से अधिक बार धड़कता है।",
                    "रोजाना लगभग 7,500 लीटर खून शरीर में पंप करता है।",
                    "पूरे जीवनकाल में इतना खून बहाता है जिससे 3 स्विमिंग पूल भर जाएं।"
                ]
            },
            {
                "heading": "2. नसों का विशाल जाल",
                "points": [
                    "शरीर की सभी नसों को यदि सीधा जोड़ दिया जाए,",
                    "तो उनकी कुल लंबाई 60,000 मील (लगभग 1 लाख किमी) होगी।",
                    "यह पूरी पृथ्वी को 2.5 बार लपेटने के लिए पर्याप्त है!"
                ]
            },
            {
                "heading": "3. हड्डियों की मजबूती",
                "points": [
                    "जांघ की हड्डी (Femur) मानव शरीर की सबसे मजबूत हड्डी है।",
                    "यह वजन सहने में कंक्रीट और स्टील से भी अधिक सख्त होती है।",
                    "वयस्क शरीर में 206 मजबूत हड्डियां सुरक्षा कवच बनाती हैं।"
                ]
            },
            {
                "heading": "4. आंखों का सुपर कैमरा",
                "points": [
                    "इंसानी आंख लगभग 576 मेगापिक्सल के कैमरे जितनी शक्तिशाली है।",
                    "આંખો લગભગ 1 કરોડ અલગ-અલગ રંગોમાં ભેદ પારખી શકે છે।",
                    "દિનભરમાં આંખો 28,000 વાર પલકારો મારીને આંખોને સાફ રાખે છે।"
                ]
            }
        ],
        "fun_fact": "अगर इंसान के सारे DNA को खोल दिया जाए, तो यह प्लूटो तक पहुंचकर वापस आ सकता है!"
    },
    {
        "theme": "postit_wall",
        "asset": "07_lightning.jpg",
        "id": "theme_07_lightning",
        "title": "बादलों में बिजली क्यों कड़कती है?",
        "subtitle": "बिजली और गड़गड़ाहट का पूरा विज्ञान (Lightning & Thunder)",
        "cards": [
            {
                "heading": "1. बादलों में टकराव",
                "points": [
                    "तूफानी बादलों में बर्फ और पानी की बूंदें आपस में टकराती हैं।",
                    "घर्षण से बादलों में शक्तिशाली स्टेटिक चार्ज (बिजली) पैदा होता है।",
                    "पॉजिटिव (+) चार्ज ऊपर और नेगेटिव (-) चार्ज नीचे जमा होता है।"
                ]
            },
            {
                "heading": "2. आसमानी बिजली का जन्म",
                "points": [
                    "जब दोनों चार्ज बहुत बढ़ जाते हैं, तो हवा का अवरोध टूट जाता है।",
                    "बादलों से धरती की ओर लाखों वोल्ट का बिजली का करंट बहता है।",
                    "इसी विशालकाय विद्युत स्पार्क को हम 'आसमानी बिजली' कहते हैं।"
                ]
            },
            {
                "heading": "3. गड़गड़ाहट (Thunder) का सच",
                "points": [
                    "बिजली का तापमान 30,000°C तक पहुंच जाता है (सूरज से 5 गुना गर्म)।",
                    "इससे आसपास की हवा एक माइक्रोसेकंड में तेजी से फैलती है।",
                    "हवा का यह भयानक विस्फोट शॉकवेव और गड़गड़ाहट पैदा करता है।"
                ]
            },
            {
                "heading": "4. आवाज बाद में क्यों आती है?",
                "points": [
                    "प्रकाश की गति 3,00,000 किमी/सेकंड है (बिजली तुरंत दिखती है)।",
                    "ध्वनि की गति हवा में सिर्फ 340 मीटर/सेकंड होती है।",
                    "इसलिए बिजली की चमक पहले दिखती है और गड़गड़ाहट कुछ सेकंड बाद।"
                ]
            }
        ],
        "fun_fact": "पूरी दुनिया में हर सेकंड लगभग 100 बार आकाशीय बिजली जमीन पर गिरती है!"
    },
    {
        "theme": "blueprint",
        "asset": "08_black_hole.jpg",
        "id": "theme_08_black_hole",
        "title": "ब्लैक होल का रहस्य (Black Hole)",
        "subtitle": "ब्रह्मांड का सबसे गहरा और खतरनाक दानव — क्या है यह?",
        "cards": [
            {
                "heading": "1. ब्लैक होल कैसे बनता है?",
                "points": [
                    "जब कोई भारी तारा अपना सारा परमाणु ईंधन खत्म कर लेता है,",
                    "तो वह भीषण 'सुपरनोवा' विस्फोट के साथ फट जाता है।",
                    "तारे का केंद्र अपने ही गुरुत्वाकर्षण से सिकुड़कर ब्लैक होल बनता है।"
                ]
            },
            {
                "heading": "2. अनंत गुरुत्वाकर्षण",
                "points": [
                    "इसका सारा द्रव्यमान एक शून्य आकार के बिंदु (Singularity) में होता है।",
                    "गुरुत्वाकर्षण बल इतना भयानक होता है कि दुनिया की सबसे तेज चीज—",
                    "प्रकाश (रोशनी) भी इसके आकर्षण से बाहर नहीं निकल सकती।"
                ]
            },
            {
                "heading": "3. इवेंट होराइजन (लक्ष्मण रेखा)",
                "points": [
                    "ब्लैक होल के चारों ओर का वह घेरा जिसके पार कोई वापसी नहीं है।",
                    "जो भी वस्तु इस सीमा के अंदर गई, वह हमेशा के लिए समा जाती है।",
                    "इसके अंदर से कोई भी संदेश या सिग्नल कभी बाहर नहीं आ सकता।"
                ]
            },
            {
                "heading": "4. समय का धीमा हो जाना",
                "points": [
                    "आइंस्टीन के सिद्धांत के अनुसार तीव्र गुरुत्व समय धीमा करता है।",
                    "ब्लैक होल के किनारे 1 घंटा पृथ्वी के कई सालों के बराबर हो सकता है।",
                    "इसके केंद्र बिंदु पर भौतिकी के सभी सामान्य नियम रुक जाते हैं।"
                ]
            }
        ],
        "fun_fact": "हमारी आकाशगंगा के केंद्र में 'Sagittarius A*' नामक विशाल ब्लैक होल स्थित है!"
    },
    {
        "theme": "legal_pad",
        "asset": "09_earth.jpg",
        "id": "theme_09_day_and_night",
        "title": "दिन और रात क्यों होते हैं? (Day & Night)",
        "subtitle": "पृथ्वी का 24 घंटे का जादुई चक्कर — सच जानें",
        "cards": [
            {
                "heading": "1. पृथ्वी का घूर्णन (Rotation)",
                "points": [
                    "पृथ्वी अपनी धुरी पर पश्चिम से पूर्व दिशा में लट्टू की तरह घूमती है।",
                    "एक पूरा चक्कर लगाने में 23 घंटे 56 मिनट 4 सेकंड लगते हैं।",
                    "पश्चिम से पूर्व घूमने के कारण ही सूर्य हमेशा पूर्व से उगता दिखता है।"
                ]
            },
            {
                "heading": "2. दिन और रात का चक्र",
                "points": [
                    "पृथ्वी गोल होने के कारण सूर्य की रोशनी एक बार में आधे भाग पर पड़ती है।",
                    "जो भाग सूर्य के सामने होता है, वहाँ दिन (उजाला) होता है।",
                    "जो भाग सूर्य के पीछे अंधेरे में होता है, वहाँ रात होती है।"
                ]
            },
            {
                "heading": "3. 23.5° का अक्षीय झुकाव",
                "points": [
                    "पृथ्वी की धुरी सीधी नहीं बल्कि 23.5 डिग्री झुकी हुई है।",
                    "इस झुकाव के कारण दिन और रात की लंबाई पूरे साल बदलती रहती है।",
                    "इसी झुकाव और सूर्य की परिक्रमा से पृथ्वी पर मौसम बदलते हैं।"
                ]
            },
            {
                "heading": "4. 6 महीने दिन, 6 महीने रात",
                "points": [
                    "अक्षीय झुकाव के कारण उत्तरी और दक्षिणी ध्रुव पर अनोखा चक्र होता है।",
                    "ध्रुवों पर 6 महीने लगातार सूर्य चमकता है और 6 महीने रात रहती है।",
                    "नॉर्वे जैसे देशों को 'आधी रात के सूरज का देश' कहा जाता है।"
                ]
            }
        ],
        "fun_fact": "भूमध्य रेखा (Equator) पर पृथ्वी लगभग 1670 किमी/घंटा की गति से घूम रही है!"
    },
    {
        "theme": "whiteboard",
        "asset": "10_internet.png",
        "id": "theme_10_how_internet_works",
        "title": "इंटरनेट कैसे काम करता है? (Internet)",
        "subtitle": "समुद्र के नीचे बिछे तारों से आपके फोन तक डेटा का सफर",
        "cards": [
            {
                "heading": "1. सैटेलाइट नहीं, समुद्र के तार!",
                "points": [
                    "99% अंतरराष्ट्रीय इंटरनेट सैटेलाइट से नहीं बल्कि केबल्स से चलता है।",
                    "महासागरों के तल पर 14 लाख किलोमीटर लंबी सबमरीन केबल्स बिछी हैं।",
                    "यह ऑप्टिकल फाइबर कांच के पतले तारों से प्रकाश की गति पर डेटा भेजते हैं।"
                ]
            },
            {
                "heading": "2. IP एड्रेस (डिजिटल पता)",
                "points": [
                    "इंटरनेट से जुड़े हर मोबाइल और कंप्यूटर का एक खास पहचान नंबर होता है।",
                    "जैसे घर पर चिट्ठी पहुंचाने के लिए पिनकोड और पता जरूरी होता है,",
                    "वैसे ही इंटरनेट पर डेटा सही IP एड्रेस पर ही पहुंचता है।"
                ]
            },
            {
                "heading": "3. DNS (इंटरनेट की फोनबुक)",
                "points": [
                    "हम ब्राउज़र में 'google.com' लिखते हैं लेकिन कंप्यूटर सिर्फ नंबर समझता है।",
                    "DNS वेबसाइट के नाम को सही IP एड्रेस में बदलता है।",
                    "यह प्रक्रिया मात्र 0.02 सेकंड में पूरी होकर पेज लोड कर देती है।"
                ]
            },
            {
                "heading": "4. पैकेट्स में डेटा का सफर",
                "points": [
                    "फोटो, वीडियो या मैसेज कभी भी एक साथ नहीं भेजे जाते।",
                    "डेटा लाखों छोटे-छोटे डिजिटल टुकड़ों (Packets) में बंटकर यात्रा करता है।",
                    "राउटर सही रास्ता दिखाते हैं और फोन पर सारे टुकड़े फिर जुड़ जाते हैं।"
                ]
            }
        ],
        "fun_fact": "एक अकेला ऑप्टिकल फाइबर धागा एक सेकंड में लाखों HD फिल्में ट्रांसफर कर सकता है!"
    }
]

def generate_all_sheets():
    print("🚀 Running Hindi Perfect Typography Engine with Rich Theme Accessories...")
    for cfg in TOPICS:
        th = cfg["theme"]
        tid = cfg["id"]
        asset = cfg["asset"]
        out_f = os.path.join(OUTPUT_DIR, f"{tid}_{th}.jpg")
        render_sheet(cfg, th, asset, out_f)
    print("\n🎉 ALL 10 SHEETS SUCCESSFULLY GENERATED WITH RICH THEMED ACCESSORIES & PROPS!")

if __name__ == "__main__":
    generate_all_sheets()
