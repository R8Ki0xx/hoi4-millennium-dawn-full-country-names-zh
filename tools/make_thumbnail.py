"""生成创意工坊封面图 thumbnail.png（512x512）。"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 512
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_BOLD = r"C:/Windows/Fonts/Noto Sans SC Bold (TrueType).otf"
FONT_MED = r"C:/Windows/Fonts/Noto Sans SC Medium (TrueType).otf"

GOLD = (226, 186, 104)
WHITE = (236, 238, 244)
MUTED = (150, 160, 182)

# 深蓝径向渐变背景
img = Image.new("RGB", (S, S))
px = img.load()
for y in range(S):
    for x in range(S):
        d = math.hypot(x - S / 2, y - S * 0.42) / (S * 0.75)
        t = min(d, 1.0)
        px[x, y] = (int(22 - 12 * t), int(34 - 20 * t), int(62 - 34 * t))

# 地球经纬线
globe = Image.new("RGBA", (S, S), (0, 0, 0, 0))
g = ImageDraw.Draw(globe)
cx, cy, r = S // 2, int(S * 0.42), 200
line = (120, 150, 210, 46)
g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 150, 210, 70), width=2)
for k in range(1, 4):
    w = int(r * math.cos(math.pi / 2 * k / 4))
    g.ellipse([cx - w, cy - r, cx + w, cy + r], outline=line, width=1)
for k in range(-3, 4):
    yy = cy + int(r * math.sin(math.pi / 2 * k / 4))
    hw = int(math.sqrt(max(r * r - (yy - cy) ** 2, 0)))
    g.line([cx - hw, yy, cx + hw, yy], fill=line, width=1)
g.line([cx, cy - r, cx, cy + r], fill=line, width=1)
img.paste(globe, (0, 0), globe)

d = ImageDraw.Draw(img)

def center(text, font, y, fill, glow=None):
    w = d.textlength(text, font=font)
    x = (S - w) / 2
    if glow:
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((x, y), text, font=font, fill=glow)
        layer = layer.filter(ImageFilter.GaussianBlur(6))
        img.paste(layer, (0, 0), layer)
    d.text((x, y), text, font=font, fill=fill)

center("千禧黎明", ImageFont.truetype(FONT_BOLD, 96), 108, GOLD, glow=(226, 186, 104, 110))
center("国家全称", ImageFont.truetype(FONT_BOLD, 76), 232, WHITE)

# 分隔线
d.line([S / 2 - 120, 352, S / 2 + 120, 352], fill=(*GOLD, ), width=2)

center("中国  →  中华人民共和国", ImageFont.truetype(FONT_MED, 30), 372, WHITE)
center("MILLENNIUM DAWN · FULL COUNTRY NAMES", ImageFont.truetype(FONT_MED, 17), 440, MUTED)

img.save(os.path.join(ROOT, "thumbnail.png"), optimize=True)
print(os.path.getsize(os.path.join(ROOT, "thumbnail.png")), "bytes")
