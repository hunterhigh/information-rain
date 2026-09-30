from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "mobile-swipe-motion-gifs"
OUT.mkdir(exist_ok=True)
W, H, N = 270, 480, 48
FONT = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 18)
SMALL = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 12)
images = [
    Image.open(ROOT / "content-pool/packs/apocalypse/images/apocalypse.jpg").convert("RGB"),
    Image.open(ROOT / "content-pool/packs/abyss/images/abyss.jpg").convert("RGB"),
    Image.open(ROOT / "content-pool/packs/building/images/building.jpg").convert("RGB"),
]

def cover(img, w=W, h=H, zoom=1.0, pan=(0, 0)):
    scale = max(w / img.width, h / img.height) * zoom
    rw, rh = round(img.width * scale), round(img.height * scale)
    resized = img.resize((rw, rh), Image.Resampling.LANCZOS)
    x = (rw-w)//2 + int(pan[0]); y = (rh-h)//2 + int(pan[1])
    x = max(0, min(rw-w, x)); y = max(0, min(rh-h, y))
    return resized.crop((x, y, x+w, y+h))

def layer(img, title, section, brightness=.68):
    frame = cover(img)
    frame = ImageEnhance.Brightness(frame).enhance(brightness)
    shade = Image.new("RGBA", (W,H))
    pix = shade.load()
    for y in range(H):
        a = int(205 * max(0, (y/H-.48)/.52))
        for x in range(W): pix[x,y] = (3,6,9,a)
    frame = Image.alpha_composite(frame.convert("RGBA"), shade)
    d = ImageDraw.Draw(frame)
    d.text((18,18), "信息雨", font=SMALL, fill=(255,255,255,195))
    d.text((18, H-106), section, font=SMALL, fill=(226,208,160,235))
    d.text((18, H-82), title, font=FONT, fill=(255,255,255,255), stroke_width=1, stroke_fill=(0,0,0,110))
    d.text((18, H-48), "走廊尽头传来一阵水声。", font=SMALL, fill=(235,236,238,235))
    return frame

def compose(mode, t):
    p = (t % N) / (N-1)
    a = layer(images[0], "14楼的房间", "第 01 段 · 雨夜")
    b = layer(images[1], "门后有水声", "第 02 段 · 地下")
    eased = p*p*(3-2*p)
    canvas = Image.new("RGBA", (W,H), (5,8,12,255))
    if mode == "01-arrow-baseline":
        # Pause, then an orderly text crossfade with tiny settling movement.
        if p < .52: canvas.alpha_composite(a)
        else:
            q = min(1, (p-.52)/.26)
            canvas.alpha_composite(a)
            canvas.alpha_composite(b, (0, round(10*(1-eased))))
            canvas.putalpha(255)
            # fade the old layer away while new text settles into place
            overlay = Image.blend(a, b, q)
            canvas = overlay
    elif mode == "02-card-tilt":
        canvas.alpha_composite(b)
        if p < .72:
            q = min(1, p/.72)
            card = a.rotate(-7*q, resample=Image.Resampling.BICUBIC, expand=False, center=(W/2,H/2))
            x = round(-W*1.15*q)
            canvas.alpha_composite(card, (x, round(9*q)))
            d=ImageDraw.Draw(canvas); d.text((20,58), "靠近" if q>.2 else "", font=FONT, fill=(255,255,255,int(240*q)))
    elif mode == "03-full-screen-slide":
        if p < .58:
            q = p/.58
            canvas.alpha_composite(b, (0, round(H*(1-q))))
            canvas.alpha_composite(a, (0, round(-H*q)))
        else: canvas.alpha_composite(b)
    elif mode == "04-parallax":
        q = eased
        back = cover(images[0], zoom=1.12, pan=(-round(18*q), 0))
        front = layer(images[0 if p < .55 else 1], "14楼的房间" if p < .55 else "门后有水声", "第 01 段 · 雨夜" if p < .55 else "第 02 段 · 地下")
        canvas.alpha_composite(back.convert("RGBA"))
        if p < .62:
            canvas.alpha_composite(front, (0, round(-H*.28*q)))
            canvas.alpha_composite(layer(images[1], "门后有水声", "第 02 段 · 地下"), (0, round(H*(1-q))))
        else: canvas.alpha_composite(layer(images[1], "门后有水声", "第 02 段 · 地下"))
    else:  # 05 soft directional light + copy settle
        chosen = a if p < .55 else b
        canvas.alpha_composite(chosen)
        glow = Image.new("RGBA", (W,H))
        d=ImageDraw.Draw(glow)
        alpha=int(90*math.sin(math.pi*p)**2)
        d.ellipse((-110, 40, 170, 330), fill=(205,223,255,alpha))
        canvas.alpha_composite(glow)
        if .42 < p < .68:
            q=(p-.42)/.26
            d.text((W//2-32, H//2-14), "继续", font=FONT, fill=(255,255,255,int(255*math.sin(math.pi*q))))
    return canvas.convert("RGB")

names = ["01-arrow-baseline", "02-card-tilt", "03-full-screen-slide", "04-parallax", "05-direction-glow"]
for name in names:
    frames = [compose(name, i).quantize(colors=96, method=Image.Quantize.MEDIANCUT) for i in range(N)]
    frames[0].save(OUT / f"{name}.gif", save_all=True, append_images=frames[1:], duration=55, loop=0, optimize=True, disposal=2)
    print(name, (OUT / f"{name}.gif").stat().st_size)
