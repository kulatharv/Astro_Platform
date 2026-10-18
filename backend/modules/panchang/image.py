"""
Share Today's Panchang Image Generator (Pillow-based).
Generates high-resolution, calm/traditional Vedic Panchang cards in Portrait (1080x1920)
and Square (1080x1080) formats for WhatsApp, Instagram, and social feed sharing.

Strictly consumes general Panchang data from get_full_panchang() and bakes mandatory
disclaimer and branding directly into image pixels.
"""
import io
import os
import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import date, datetime
from PIL import Image, ImageDraw, ImageFont

from modules.panchang.engine import get_full_panchang

logger = logging.getLogger(__name__)

DISCLAIMER_TEXT = "Traditional Vedic guidance for reflection and awareness — not a guarantee of outcomes."
BRANDING_TEXT = "Astro · Logic  |  astrologic.app"

_IMAGE_CACHE: Dict[str, bytes] = {}


def _get_fonts():
    """Load elegant system fonts with safe fallbacks."""
    def load(name, size, fallback_name="arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            try:
                return ImageFont.truetype(fallback_name, size)
            except Exception:
                return ImageFont.load_default()

    return {
        "brand": load("georgia.ttf", 40, "times.ttf"),
        "title_lg": load("georgia.ttf", 34, "times.ttf"),
        "title_md": load("georgia.ttf", 26, "times.ttf"),
        "heading": load("georgia.ttf", 22, "times.ttf"),
        "body_bold": load("segoeui.ttf", 22, "arial.ttf"),
        "body": load("segoeui.ttf", 19, "arial.ttf"),
        "body_sm": load("segoeui.ttf", 17, "arial.ttf"),
        "caption": load("segoeui.ttf", 15, "arial.ttf"),
        "micro": load("segoeui.ttf", 13, "arial.ttf"),
        "score_val": load("georgia.ttf", 46, "times.ttf"),
        "disclaimer": load("segoeui.ttf", 15, "arial.ttf"),
    }


def _draw_diamond(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color=(245, 193, 108, 255)):
    draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=color)


def _draw_sparkle(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color=(245, 193, 108, 255)):
    p_inner = r * 0.28
    points = [
        (cx, cy - r),
        (cx + p_inner, cy - p_inner),
        (cx + r, cy),
        (cx + p_inner, cy + p_inner),
        (cx, cy + r),
        (cx - p_inner, cy + p_inner),
        (cx - r, cy),
        (cx - p_inner, cy - p_inner)
    ]
    draw.polygon(points, fill=color)


def _draw_sun_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color=(245, 193, 108)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)
    ray_len = 4
    for dx, dy in [(0, -(r + ray_len)), (0, r + ray_len), (-(r + ray_len), 0), (r + ray_len, 0)]:
        draw.line([(cx + dx * 0.7, cy + dy * 0.7), (cx + dx, cy + dy)], fill=color, width=2)


def _draw_rounded_card(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    bg_color=(13, 30, 56, 220),
    border_color=(212, 175, 55, 100),
    radius=14,
    border_width=1
):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color, outline=border_color, width=border_width)


def _draw_header(draw: ImageDraw.ImageDraw, fonts: dict, width: int, city: str, date_str: str, samvat_str: str, y_offset: int = 40) -> int:
    brand_left = "ASTRO"
    brand_right = "LOGIC"
    
    bbox_l = draw.textbbox((0, 0), brand_left, font=fonts["brand"])
    w_l = bbox_l[2] - bbox_l[0]
    bbox_r = draw.textbbox((0, 0), brand_right, font=fonts["brand"])
    w_r = bbox_r[2] - bbox_r[0]
    
    sparkle_gap = 36
    total_w = w_l + sparkle_gap + w_r
    start_x = (width - total_w) // 2
    
    draw.text((start_x, y_offset), brand_left, font=fonts["brand"], fill=(245, 193, 108))
    _draw_sparkle(draw, start_x + w_l + sparkle_gap // 2, y_offset + 20, 10, color=(245, 193, 108))
    draw.text((start_x + w_l + sparkle_gap, y_offset), brand_right, font=fonts["brand"], fill=(245, 193, 108))

    sub = "DAINIK PANCHANG · VEDIC EPHEMERIS"
    bbox = draw.textbbox((0, 0), sub, font=fonts["caption"])
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, y_offset + 50), sub, font=fonts["caption"], fill=(155, 220, 255, 220))

    line_y = y_offset + 80
    draw.line([(80, line_y), (width - 80, line_y)], fill=(212, 175, 55, 80), width=1)
    _draw_diamond(draw, width // 2, line_y, 5, color=(245, 193, 108))

    try:
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = dt_obj.strftime("%A, %d %B %Y").upper()
    except Exception:
        formatted_date = date_str.upper()

    city_display = f"{city.upper()} · {formatted_date}"
    bbox = draw.textbbox((0, 0), city_display, font=fonts["body_bold"])
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, y_offset + 96), city_display, font=fonts["body_bold"], fill=(255, 255, 255))

    if samvat_str:
        bbox = draw.textbbox((0, 0), samvat_str, font=fonts["caption"])
        w = bbox[2] - bbox[0]
        draw.text(((width - w) // 2, y_offset + 128), samvat_str, font=fonts["caption"], fill=(203, 213, 225, 200))
        return y_offset + 164

    return y_offset + 144


def _draw_footer(draw: ImageDraw.ImageDraw, fonts: dict, width: int, height: int, y_bottom: int = 34):
    line_y = height - y_bottom - 46
    draw.line([(80, line_y), (width - 80, line_y)], fill=(212, 175, 55, 80), width=1)
    _draw_diamond(draw, width // 2, line_y, 4, color=(245, 193, 108))

    bbox = draw.textbbox((0, 0), DISCLAIMER_TEXT, font=fonts["disclaimer"])
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, height - y_bottom - 36), DISCLAIMER_TEXT, font=fonts["disclaimer"], fill=(226, 232, 240, 240))

    bbox = draw.textbbox((0, 0), BRANDING_TEXT, font=fonts["caption"])
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, height - y_bottom - 14), BRANDING_TEXT, font=fonts["caption"], fill=(245, 193, 108, 220))


def generate_panchang_image(
    city: str = "Pune",
    target_date: Optional[date] = None,
    image_format: str = "portrait",
    image_type: str = "png",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    tz_str: Optional[str] = None
) -> Tuple[bytes, str]:
    d = target_date or date.today()
    date_str = d.strftime("%Y-%m-%d")
    fmt_key = image_format.lower().strip()
    if fmt_key not in ("portrait", "square"):
        fmt_key = "portrait"
    type_key = image_type.lower().strip()
    if type_key not in ("png", "jpeg", "jpg"):
        type_key = "png"
    if type_key == "jpg":
        type_key = "jpeg"

    cache_key = f"panchang_img:{city}:{date_str}:{fmt_key}:{type_key}:{lat}:{lon}"
    if cache_key in _IMAGE_CACHE:
        media_type = "image/jpeg" if type_key == "jpeg" else "image/png"
        return _IMAGE_CACHE[cache_key], media_type

    p = get_full_panchang(city_name=city, target_date=d, lat=lat, lon=lon, tz_str=tz_str)
    fonts = _get_fonts()

    if fmt_key == "portrait":
        W, H = 1080, 1920
    else:
        W, H = 1080, 1080

    img = Image.new("RGB", (W, H), color=(3, 10, 24))
    draw = ImageDraw.Draw(img)

    for r in range(450, 0, -25):
        alpha = int(14 * (r / 450.0))
        draw.ellipse([W//2 - r, 120 - r//2, W//2 + r, 120 + r//2], fill=(12, 35, 75, alpha))

    draw.rectangle([20, 20, W - 20, H - 20], outline=(212, 175, 55, 90), width=2)
    draw.rectangle([26, 26, W - 26, H - 26], outline=(255, 255, 255, 25), width=1)

    corner_len = 22
    for cx, cy in [(20, 20), (W - 20, 20), (20, H - 20), (W - 20, H - 20)]:
        draw.line([(cx - corner_len, cy), (cx + corner_len, cy)], fill=(245, 193, 108), width=2)
        draw.line([(cx, cy - corner_len), (cx, cy + corner_len)], fill=(245, 193, 108), width=2)
        _draw_diamond(draw, cx, cy, 4, color=(245, 193, 108))

    samvat_dict = p.get("samvat", {})
    samvat_str = ""
    if samvat_dict:
        vik = samvat_dict.get("vikram_samvat", 2083)
        shk = samvat_dict.get("shaka_samvat", 1948)
        month_am = samvat_dict.get("month_amanta", "")
        month_part = f" · Month: {month_am}" if month_am else ""
        samvat_str = f"Vikram Samvat {vik} · Shaka Samvat {shk}{month_part} · Lahiri Ayanamsha"

    curr_y = _draw_header(draw, fonts, W, p.get("city", city), date_str, samvat_str, y_offset=42)

    card_margin = 46
    card_w = W - 2 * card_margin

    if fmt_key == "portrait":
        card_h = 144
        _draw_rounded_card(draw, (card_margin, curr_y, W - card_margin, curr_y + card_h), bg_color=(10, 25, 48, 240), border_color=(245, 193, 108, 120))
        
        s_rise = p.get("sunrise", "06:00 AM")
        s_set = p.get("sunset", "06:30 PM")
        _draw_sun_icon(draw, card_margin + 36, curr_y + 38, 11, color=(245, 193, 108))
        draw.text((card_margin + 58, curr_y + 26), "SOLAR CYCLE & VEDIC DAY", font=fonts["caption"], fill=(155, 220, 255))
        draw.text((card_margin + 32, curr_y + 58), f"Sunrise: {s_rise}   •   Sunset: {s_set}", font=fonts["body_bold"], fill=(255, 255, 255))
        draw.text((card_margin + 32, curr_y + 98), f"Vedic Day (Vaar): {p.get('vara', 'Sunday')}", font=fonts["body_sm"], fill=(203, 213, 225))

        score_val = p.get("today_score", 7.5)
        score_text = f"{score_val:.1f}"
        score_x = W - card_margin - 240
        draw.text((score_x, curr_y + 26), "VEDIC ALIGNMENT INDEX", font=fonts["caption"], fill=(245, 193, 108))
        draw.text((score_x, curr_y + 52), score_text, font=fonts["score_val"], fill=(245, 193, 108))
        draw.text((score_x + 90, curr_y + 70), "/ 10.0", font=fonts["body_bold"], fill=(148, 163, 184))
        draw.text((score_x, curr_y + 104), "General Auspiciousness", font=fonts["micro"], fill=(148, 163, 184))

        curr_y += card_h + 26

        _draw_diamond(draw, card_margin + 8, curr_y + 13, 5, color=(245, 193, 108))
        draw.text((card_margin + 22, curr_y), "THE FIVE SACRED LIMBS (PANCHANGA)", font=fonts["heading"], fill=(245, 193, 108))
        curr_y += 38

        limbs = [
            ("Tithi", f"{p.get('tithi', 'Pratipada')}", f"Ends: {p.get('tithi_end', '—')} ({p.get('paksha', 'Shukla')} Paksha)"),
            ("Nakshatra", f"{p.get('nakshatra', 'Ashwini')}", f"Ends: {p.get('nakshatra_end', '—')} (Pada {p.get('nakshatra_pada', 1)})"),
            ("Yoga", f"{p.get('yoga', 'Vishkambha')}", f"Ends: {p.get('yoga_end', '—')}"),
            ("Karana", f"{p.get('karana', 'Balava')}", f"Ends: {p.get('karana_end', '—')}"),
            ("Rashi Transits", f"Moon: {p.get('moon_sign', 'Mesha')}", f"Sun: {p.get('sun_sign', 'Kanya')}")
        ]

        grid_cols = 2
        col_w = (card_w - 20) // 2
        limb_card_h = 112
        for idx, (title, val_main, sub_text) in enumerate(limbs):
            row = idx // grid_cols
            col = idx % grid_cols
            x0 = card_margin + col * (col_w + 20)
            y0 = curr_y + row * (limb_card_h + 12)
            
            if idx == len(limbs) - 1 and (len(limbs) % 2 != 0):
                x1 = W - card_margin
            else:
                x1 = x0 + col_w
            y1 = y0 + limb_card_h

            _draw_rounded_card(draw, (x0, y0, x1, y1), bg_color=(12, 28, 52, 220), border_color=(74, 108, 156, 90))
            draw.text((x0 + 20, y0 + 14), title.upper(), font=fonts["caption"], fill=(155, 220, 255))
            draw.text((x0 + 20, y0 + 40), val_main, font=fonts["body_bold"], fill=(255, 255, 255))
            draw.text((x0 + 20, y0 + 74), sub_text, font=fonts["body_sm"], fill=(203, 213, 225))

        curr_y += ((len(limbs) + 1) // 2) * (limb_card_h + 12) + 16

        _draw_diamond(draw, card_margin + 8, curr_y + 13, 5, color=(245, 193, 108))
        draw.text((card_margin + 22, curr_y), "AUSPICIOUS & INAUSPICIOUS WINDOWS", font=fonts["heading"], fill=(245, 193, 108))
        curr_y += 38

        muhurtas = [
            ("Abhijit Muhurta", p.get("abhijit_muhurta", "11:48 AM – 12:36 PM"), "Auspicious Solar Window", (74, 222, 128)),
            ("Brahma Muhurta", p.get("brahma", "04:30 AM – 05:18 AM"), "Spiritual Window", (192, 132, 252)),
            ("Rahu Kaal", p.get("rahu_kaal", "04:30 PM – 06:00 PM"), "Rahu Period", (248, 113, 113)),
            ("Yamaganda", p.get("yamaganda", "12:00 PM – 01:30 PM"), "Yamaganda Period", (248, 113, 113)),
            ("Gulika Kaal", p.get("gulika", "03:00 PM – 04:30 PM"), "Gulika Period", (248, 113, 113)),
            ("Disha Shool", f"{p.get('disha_shool', {}).get('direction', 'West')}", f"Remedy: {p.get('disha_shool', {}).get('remedy', 'Ghee / Betel')}", (245, 193, 108))
        ]

        muh_card_h = 100
        for idx, (m_title, m_val, m_desc, m_color) in enumerate(muhurtas):
            row = idx // 2
            col = idx % 2
            x0 = card_margin + col * (col_w + 20)
            x1 = x0 + col_w
            y0 = curr_y + row * (muh_card_h + 12)
            y1 = y0 + muh_card_h

            _draw_rounded_card(draw, (x0, y0, x1, y1), bg_color=(12, 28, 52, 220), border_color=(m_color[0], m_color[1], m_color[2], 90))
            draw.text((x0 + 18, y0 + 12), m_title, font=fonts["body_bold"], fill=(255, 255, 255))
            draw.text((x0 + 18, y0 + 42), f"{m_val}", font=fonts["body_bold"], fill=m_color)
            draw.text((x0 + 18, y0 + 70), m_desc, font=fonts["micro"], fill=(148, 163, 184))

        curr_y += ((len(muhurtas) + 1) // 2) * (muh_card_h + 12) + 16

        chog_list = p.get("choghadiya_day", [])
        if chog_list:
            _draw_diamond(draw, card_margin + 8, curr_y + 13, 5, color=(245, 193, 108))
            draw.text((card_margin + 22, curr_y), "DAY CHOGHADIYA TIMELINE", font=fonts["heading"], fill=(245, 193, 108))
            curr_y += 36

            chog_w = (card_w - (len(chog_list) - 1) * 8) // len(chog_list)
            for c_idx, c in enumerate(chog_list[:8]):
                cx0 = card_margin + c_idx * (chog_w + 8)
                cx1 = cx0 + chog_w
                cy0 = curr_y
                cy1 = cy0 + 90

                is_good = c.get("is_auspicious", False)
                border_c = (74, 222, 128, 120) if is_good else (248, 113, 113, 100)
                fill_c = (15, 38, 45, 220) if is_good else (38, 18, 25, 220)

                _draw_rounded_card(draw, (cx0, cy0, cx1, cy1), bg_color=fill_c, border_color=border_c, radius=8)
                draw.text((cx0 + 8, cy0 + 8), c.get("name", ""), font=fonts["body_sm"], fill=(255, 255, 255))
                draw.text((cx0 + 8, cy0 + 36), c.get("start", "").replace(" AM", "A").replace(" PM", "P"), font=fonts["caption"], fill=(203, 213, 225))
                planet_str = c.get("ruling_planet", "")
                draw.text((cx0 + 8, cy0 + 60), f"Lord: {planet_str[:3]}", font=fonts["micro"], fill=(155, 220, 255))

            curr_y += 106

        planets_list = p.get("planets", [])
        if planets_list and len(planets_list) >= 7:
            _draw_diamond(draw, card_margin + 8, curr_y + 13, 5, color=(245, 193, 108))
            draw.text((card_margin + 22, curr_y), "PLANETARY POSITIONS (NAVAGRAHA)", font=fonts["heading"], fill=(245, 193, 108))
            curr_y += 36

            p_cols = 3
            p_col_w = (card_w - (p_cols - 1) * 12) // p_cols
            p_card_h = 80
            for p_idx, pl in enumerate(planets_list[:9]):
                p_row = p_idx // p_cols
                p_col = p_idx % p_cols
                px0 = card_margin + p_col * (p_col_w + 12)
                px1 = px0 + p_col_w
                py0 = curr_y + p_row * (p_card_h + 8)
                py1 = py0 + p_card_h

                p_name = pl.get("en_name", pl.get("name", ""))
                p_sign = pl.get("sign", "").split(" ")[0]
                p_nak = pl.get("nakshatra", "")
                p_retro = " (R)" if pl.get("retrograde") else ""

                _draw_rounded_card(draw, (px0, py0, px1, py1), bg_color=(10, 24, 45, 210), border_color=(74, 108, 156, 80), radius=10)
                draw.text((px0 + 12, py0 + 8), f"{p_name}{p_retro}", font=fonts["body_bold"], fill=(245, 193, 108))
                draw.text((px0 + 12, py0 + 34), f"Sign: {p_sign}", font=fonts["caption"], fill=(255, 255, 255))
                draw.text((px0 + 12, py0 + 54), f"Nak: {p_nak}", font=fonts["micro"], fill=(155, 220, 255))

    else:
        card_h = 88
        _draw_rounded_card(draw, (card_margin, curr_y, W - card_margin, curr_y + card_h), bg_color=(10, 25, 48, 240), border_color=(245, 193, 108, 120))
        s_rise = p.get("sunrise", "06:00 AM")
        s_set = p.get("sunset", "06:30 PM")
        draw.text((card_margin + 20, curr_y + 14), f"Sunrise: {s_rise}   •   Sunset: {s_set}   •   Vaar: {p.get('vara', 'Sunday')}", font=fonts["body_bold"], fill=(255, 255, 255))
        score_val = p.get("today_score", 7.5)
        draw.text((card_margin + 20, curr_y + 50), f"Vedic Alignment Index: {score_val:.1f} / 10.0 (Traditional Auspiciousness)", font=fonts["body_sm"], fill=(245, 193, 108))

        curr_y += card_h + 16

        col_w = (card_w - 20) // 2

        _draw_diamond(draw, card_margin + 6, curr_y + 11, 4, color=(245, 193, 108))
        draw.text((card_margin + 18, curr_y), "THE FIVE SACRED LIMBS", font=fonts["heading"], fill=(245, 193, 108))
        y_left = curr_y + 32
        limbs_sq = [
            ("Tithi", f"{p.get('tithi', 'Pratipada')}", f"Ends: {p.get('tithi_end', '—')} ({p.get('paksha', 'Shukla')})"),
            ("Nakshatra", f"{p.get('nakshatra', 'Ashwini')}", f"Ends: {p.get('nakshatra_end', '—')} (Pada {p.get('nakshatra_pada', 1)})"),
            ("Yoga", f"{p.get('yoga', 'Vishkambha')}", f"Ends: {p.get('yoga_end', '—')}"),
            ("Karana", f"{p.get('karana', 'Balava')}", f"Ends: {p.get('karana_end', '—')}"),
            ("Rashi Transits", f"Moon: {p.get('moon_sign', 'Mesha')}", f"Sun: {p.get('sun_sign', 'Kanya')}")
        ]
        for title, val_main, sub_text in limbs_sq:
            _draw_rounded_card(draw, (card_margin, y_left, card_margin + col_w, y_left + 84), bg_color=(12, 28, 52, 220), border_color=(74, 108, 156, 90))
            draw.text((card_margin + 16, y_left + 8), title.upper(), font=fonts["caption"], fill=(155, 220, 255))
            draw.text((card_margin + 16, y_left + 30), val_main, font=fonts["body_bold"], fill=(255, 255, 255))
            draw.text((card_margin + 16, y_left + 56), sub_text, font=fonts["body_sm"], fill=(203, 213, 225))
            y_left += 92

        x_right = card_margin + col_w + 20
        _draw_diamond(draw, x_right + 6, curr_y + 11, 4, color=(245, 193, 108))
        draw.text((x_right + 18, curr_y), "KEY TIME WINDOWS", font=fonts["heading"], fill=(245, 193, 108))
        y_right = curr_y + 32
        muhurtas_sq = [
            ("Abhijit Muhurta", p.get("abhijit_muhurta", "11:48 AM – 12:36 PM"), "Auspicious Solar Window", (74, 222, 128)),
            ("Brahma Muhurta", p.get("brahma", "04:30 AM – 05:18 AM"), "Spiritual Window", (192, 132, 252)),
            ("Rahu Kaal", p.get("rahu_kaal", "04:30 PM – 06:00 PM"), "Rahu Period", (248, 113, 113)),
            ("Yamaganda", p.get("yamaganda", "12:00 PM – 01:30 PM"), "Yamaganda Period", (248, 113, 113)),
            ("Gulika Kaal", p.get("gulika", "03:00 PM – 04:30 PM"), "Gulika Period", (248, 113, 113)),
        ]
        for m_title, m_val, m_desc, m_color in muhurtas_sq:
            _draw_rounded_card(draw, (x_right, y_right, x_right + col_w, y_right + 84), bg_color=(12, 28, 52, 220), border_color=(m_color[0], m_color[1], m_color[2], 90))
            draw.text((x_right + 16, y_right + 8), m_title, font=fonts["body_bold"], fill=(255, 255, 255))
            draw.text((x_right + 16, y_right + 32), f"{m_val}", font=fonts["body_bold"], fill=m_color)
            draw.text((x_right + 16, y_right + 58), m_desc, font=fonts["micro"], fill=(148, 163, 184))
            y_right += 92

        curr_y = max(y_left, y_right) + 8

        chog_list = p.get("choghadiya_day", [])
        if chog_list:
            _draw_diamond(draw, card_margin + 6, curr_y + 11, 4, color=(245, 193, 108))
            draw.text((card_margin + 18, curr_y), "DAY CHOGHADIYA TIMELINE", font=fonts["heading"], fill=(245, 193, 108))
            curr_y += 30

            chog_w = (card_w - (len(chog_list) - 1) * 6) // len(chog_list)
            for c_idx, c in enumerate(chog_list[:8]):
                cx0 = card_margin + c_idx * (chog_w + 6)
                cx1 = cx0 + chog_w
                cy0 = curr_y
                cy1 = cy0 + 76

                is_good = c.get("is_auspicious", False)
                border_c = (74, 222, 128, 120) if is_good else (248, 113, 113, 100)
                fill_c = (15, 38, 45, 220) if is_good else (38, 18, 25, 220)

                _draw_rounded_card(draw, (cx0, cy0, cx1, cy1), bg_color=fill_c, border_color=border_c, radius=6)
                draw.text((cx0 + 6, cy0 + 6), c.get("name", ""), font=fonts["caption"], fill=(255, 255, 255))
                draw.text((cx0 + 6, cy0 + 28), c.get("start", "").replace(" AM", "A").replace(" PM", "P"), font=fonts["micro"], fill=(203, 213, 225))
                planet_str = c.get("ruling_planet", "")
                draw.text((cx0 + 6, cy0 + 50), planet_str[:3], font=fonts["micro"], fill=(155, 220, 255))

    _draw_footer(draw, fonts, W, H, y_bottom=34)

    buf = io.BytesIO()
    if type_key == "jpeg":
        img.save(buf, format="JPEG", quality=92, optimize=True)
        media_type = "image/jpeg"
    else:
        img.save(buf, format="PNG", optimize=True)
        media_type = "image/png"

    img_bytes = buf.getvalue()
    _IMAGE_CACHE[cache_key] = img_bytes
    return img_bytes, media_type
