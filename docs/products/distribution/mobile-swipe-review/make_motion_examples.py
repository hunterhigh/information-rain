"""Generate small, story-stage motion studies for the Information Rain reader."""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


OUT = Path(__file__).parent
W, H = 360, 640
FONT_BODY = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 14)
FONT_SMALL = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 11)
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc", 24)


def lerp(a, b, t):
    return round(a + (b - a) * t)


def scene(seed, top, mid, ground, light, title, author, lines):
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H))
    px = img.load()
    colors = [tuple(bytes.fromhex(c)) for c in (top, mid, ground)]
    for y in range(H):
        q = min(1, y / (H * .68))
        a, b = (colors[0], colors[1]) if q < .55 else (colors[1], colors[2])
        q = q / .55 if q < .55 else (q - .55) / .45
        row = tuple(lerp(a[i], b[i], q) for i in range(3))
        for x in range(W):
            vignette = max(0, 1 - abs(x - W / 2) / (W * .82))
            px[x, y] = tuple(lerp(v, min(255, v + 13), vignette * .23) for v in row)

    art = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(art, "RGBA")
    # A receding rain corridor: architectural shapes, reflections and one warm source.
    d.ellipse((W * .42, H * .22, W * .58, H * .39), fill=(*bytes.fromhex(light), 125))
    for side in (-1, 1):
        x0 = W / 2 + side * 30
        x1 = W / 2 + side * 176
        d.polygon([(x0, 140), (x1, 40), (x1, 492), (W / 2 + side * 34, 420)], fill=(3, 10, 17, 142))
        for n in range(5):
            x = W / 2 + side * (50 + n * 23)
            d.line((x, 75 - n * 9, x, 452 - n * 20), fill=(133, 175, 184, 29), width=2)
        for n in range(4):
            y = 105 + n * 72
            d.line((W / 2 + side * 39, y, W / 2 + side * (160 - n * 4), y - 30), fill=(171, 199, 191, 27), width=1)
    d.polygon([(0, 441), (W / 2, 356), (W, 441), (W, 532), (0, 532)], fill=(5, 13, 21, 98))
    if seed == 29:
        # The branch opens into a different place: a lit side passage, not a recolored copy.
        d.polygon([(W * .52, 246), (W * .78, 214), (W * .98, 274), (W * .98, 444), (W * .52, 418)], fill=(12, 23, 29, 174))
        d.polygon([(W * .66, 278), (W * .83, 252), (W * .91, 279), (W * .91, 420), (W * .66, 401)], fill=(7, 13, 18, 188))
        d.ellipse((W * .74, 304, W * .83, 367), fill=(*bytes.fromhex(light), 94))
        d.line((W * .58, 419, W * .96, 449), fill=(219, 192, 135, 50), width=2)
    for n in range(8):
        y = 405 + n * 17
        d.line((W * .14 + n * 3, y, W * .86 - n * 3, y), fill=(150, 190, 188, 18), width=1)
    glow = art.filter(ImageFilter.GaussianBlur(24))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    img = Image.alpha_composite(img, art)

    rain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rain, "RGBA")
    for _ in range(42):
        x = rng.randrange(W)
        y = rng.randrange(30, 460)
        rd.line((x, y, x - 4, y + rng.randrange(8, 22)), fill=(186, 221, 223, rng.randrange(13, 37)), width=1)
    img = Image.alpha_composite(img, rain)

    # Text remains part of the page surface: no detached caption or floating toast.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sp = shade.load()
    for y in range(400, H):
        alpha = round(35 + 210 * ((y - 400) / (H - 400)) ** 1.25)
        for x in range(W):
            sp[x, y] = (2, 5, 9, alpha)
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((24, 477), title, font=FONT_TITLE, fill=(245, 240, 226, 255), stroke_width=0)
    d.text((25, 514), author, font=FONT_SMALL, fill=(221, 222, 218, 215))
    y = 549
    for line in lines:
        d.text((25, y), line, font=FONT_BODY, fill=(237, 237, 230, 245))
        y += 24
    return img.convert("RGB")


CURRENT = scene(17, "07131d", "143542", "070b12", "f3c174", "未寄出的信", "@夜行 · 7 分钟", ["雨停以后，站台只剩一盏灯。", "她把写了一半的信重新装进口袋。"])
LEFT_BRANCH = scene(29, "09221f", "24645b", "07120f", "83ead0", "另一封回信", "@夜行 · 左侧分支", ["灯光照见纸背上的第二行字。", "那不是她写下的笔迹。"])
RIGHT_BRANCH = scene(38, "24130e", "75452c", "160b08", "ffc17a", "雨里的来客", "@夜行 · 右侧分支", ["街角有人把伞留在了门外。", "门后传来一段熟悉的旋律。"])
UP_BRANCH = scene(44, "17152b", "414678", "090b18", "b6b8ff", "灯塔之上", "@夜行 · 上方分支", ["她沿着旋梯走向灯塔顶层。", "窗外的雨正从海面倒着升起。"])
NEXT_WORLD = scene(51, "08111b", "21364a", "070b11", "8ec5d0", "第七个站台", "@雾中人 · 新作品", ["末班车驶过以后，站台向海面延伸。", "有人在远处举起一盏蓝色的灯。"])


def place(canvas, page, x, y):
    canvas.paste(page, (round(x), round(y)))


def direction_page(page, direction, progress, incoming=False):
    e = progress * progress * (3 - 2 * progress)
    x = y = 0
    if direction == "left": x = W * (1 - e) if incoming else -W * e
    if direction == "right": x = -W * (1 - e) if incoming else W * e
    if direction == "up": y = H * (1 - e) if incoming else -H * e
    canvas = Image.new("RGBA", (W, H), (3, 6, 10, 255))
    place(canvas, page, x, y)
    return canvas


def branch_frame(p, style, direction):
    p = max(0, min(1, p)); e = p * p * (3 - 2 * p)
    target = {"left": LEFT_BRANCH, "right": RIGHT_BRANCH, "up": UP_BRANCH}[direction]
    canvas = Image.new("RGBA", (W, H), (3, 6, 10, 255))
    if style == "ribbon":
        # A flat finger-led page follows the swipe; luminous currents cross the artwork toward that edge.
        place(canvas, target, *(({"left": (W*(1-e),0), "right": (-W*(1-e),0), "up": (0,H*(1-e))})[direction]))
        old = CURRENT.convert("RGBA"); fx = Image.new("RGBA", (W,H), (0,0,0,0)); d=ImageDraw.Draw(fx)
        for n in range(5):
            pts=[]
            for j in range(20):
                q=j/19
                if direction in ("left","right"):
                    x=(W*(.82-.72*q) if direction=="left" else W*(.18+.72*q)); y=205+n*34+math.sin(q*8+n)*9
                else: x=58+n*55+math.sin(q*8+n)*8; y=H*(.75-.55*q)
                pts.append((x,y))
            d.line(pts, fill=(255,222,160,round(205*e)), width=4)
        old=Image.alpha_composite(old,fx.filter(ImageFilter.GaussianBlur(7)))
        pos={"left":(-W*e,0),"right":(W*e,0),"up":(0,-H*e)}[direction]; place(canvas,old,*pos)
    elif style == "aperture":
        # A soft-edged expanding opening reveals a target scene; this is a mask transition, not page-follow.
        canvas.paste(target.convert("RGBA"),(0,0)); old=CURRENT.convert("RGBA")
        mask=Image.new("L",(W,H),0); d=ImageDraw.Draw(mask)
        if direction=="left": box=(-W*.7,-H*.15,W*1.2,H*1.15); anchor=(W,H*.5)
        elif direction=="right": box=(-W*.2,-H*.15,W*1.7,H*1.15); anchor=(0,H*.5)
        else: box=(-W*.25,-H*.5,W*1.25,H*1.25); anchor=(W*.5,H)
        cx,cy=anchor; rx=max(2,(box[2]-box[0])*.5*e); ry=max(2,(box[3]-box[1])*.5*e)
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255)
        mask=mask.filter(ImageFilter.GaussianBlur(18)); old.putalpha(Image.eval(mask,lambda a:255-a)); canvas.alpha_composite(old)
        glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow); gd.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),outline=(203,255,224,round(180*e)),width=7); canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
    else:
        # The complete outgoing page, text included, folds/narrows toward the selected edge.
        place(canvas,target,0,0); old=CURRENT.convert("RGBA")
        width=max(2,round(W*(1-.72*e))); height=max(2,round(H*(1-.42*e)))
        old=old.resize((width,height),Image.Resampling.BICUBIC)
        if direction=="left": pos=(-W*e,(H-height)//2)
        elif direction=="right": pos=(W-width+W*e,(H-height)//2)
        else: pos=((W-width)//2,-H*e)
        place(canvas,old,*pos)
        sparks=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(sparks)
        edge={"left":(0,H*.5),"right":(W,H*.5),"up":(W*.5,0)}[direction]
        for i in range(18):
            sx=(i*73)%W; sy=(i*127)%H; t=e
            ex=sx+(edge[0]-sx)*t; ey=sy+(edge[1]-sy)*t
            d.line((sx,sy,ex,ey),fill=(255,210,135,round(150*e)),width=2)
        canvas.alpha_composite(sparks.filter(ImageFilter.GaussianBlur(2)))
    return canvas.convert("RGB")


def world_frame(p):
    p = max(0, min(1, p))
    eased = p * p * (3 - 2 * p)
    canvas = Image.new("RGBA", (W, H), (3, 6, 10, 255))
    place(canvas, NEXT_WORLD, 0, -H * (1 - eased))
    place(canvas, CURRENT, 0, H * eased)
    return canvas.convert("RGB")


def sequence_frame(style, direction, p):
    if direction == "down": return world_frame(p)
    return branch_frame(p, style, direction)


def write_gif(name, maker):
    frames = [maker(0), maker(0)]
    for i in range(1, 23):
        frames.append(maker(i / 22))
    frames.extend([maker(1)] * 8)
    frames[0].save(OUT / name, save_all=True, append_images=frames[1:], duration=46, loop=0, optimize=True, disposal=2)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for style, name in [("ribbon","四向-光流牵引.gif"),("aperture","四向-图像开口.gif"),("suction","四向-场景吸入.gif")]:
        frames=[]
        for direction in ("left","right","up","down"):
            if frames: frames.extend([Image.new("RGB",(W,H),(3,6,10))]*3)
            frames.extend([sequence_frame(style,direction,0)]*5)
            frames.extend(sequence_frame(style,direction,i/18) for i in range(1,19))
            frames.extend([sequence_frame(style,direction,1)]*5)
        frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=48,loop=0,optimize=True,disposal=2)
    print("Wrote three four-direction motion studies to", OUT)
