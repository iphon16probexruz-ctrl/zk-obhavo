from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

from config import TEMPLATE_PATH, FONT_BOLD, FONT_REGULAR, ICONS_DIR

WEATHER_RED = (255, 10, 10)


def load_icon(name, size):
    path = os.path.join(ICONS_DIR, f"{name}.png")
    if not os.path.exists(path):
        return None

    icon = Image.open(path).convert("RGBA")
    return icon.resize(size, Image.Resampling.LANCZOS)


def create_image(data):
    img = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # FONTLAR
    font_date = ImageFont.truetype(FONT_REGULAR, 42)
    font_temp = ImageFont.truetype(FONT_BOLD, 270)
    font_info = ImageFont.truetype(FONT_REGULAR, 45)

    # SANA
    draw.text(
        (640, 140),
        data["date"],
        fill=WEATHER_RED,
        font=font_date,
        anchor="mm"
    )

    # HARORAT
    draw.text(
        (365, 350),
        f"{data['day_temp']}°",
        fill=WEATHER_RED,
        font=font_temp,
        anchor="mm"
    )

    draw.text(
        (885, 350),
        f"{data['night_temp']}°",
        fill=WEATHER_RED,
        font=font_temp,
        anchor="mm"
    )

    # IKONKALAR
    icon_size = (300, 240)

    day_icon = load_icon(data["day_icon"], icon_size)
    night_icon = load_icon(data["night_icon"], icon_size)

    if day_icon:
        img.paste(day_icon, (310, 355), day_icon)

    if night_icon:
        img.paste(night_icon, (845, 355), night_icon)

    # NAMLIK
    draw.text(
        (390, 725),
        f"{data['humidity']}%",
        fill=WEATHER_RED,
        font=font_info,
        anchor="mm"
    )

    # SHAMOL
    draw.text(
        (870, 725),
        f"{data['wind']} m/s",
        fill=WEATHER_RED,
        font=font_info,
        anchor="mm"
    )

    # SAQLASH
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)

    return buffer