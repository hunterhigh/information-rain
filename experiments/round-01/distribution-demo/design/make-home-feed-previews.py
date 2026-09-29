from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'design'
ASSET = ROOT / 'images'
W, H = 1680, 945
FONT = 'C:/Windows/Fonts/msyh.ttc'

def font(size): return ImageFont.truetype(FONT, size)
def cover_crop(img, size):
    w,h=size; scale=max(w/img.width,h/img.height)
    img=img.resize((round(img.width*scale),round(img.height*scale)),Image.Resampling.LANCZOS)
    x=(img.width-w)//2; y=(img.height-h)//2
    return img.crop((x,y,x+w,y+h))
def label(draw, xy, value, size, color):
    draw.text(xy,value,font=font(size),fill=color)

def make_backdrop(mode):
    if mode=='A': return Image.new('RGB',(W,H),(13,16,21))
    if mode=='B':
        bg=cover_crop(Image.open(ASSET/'apocalypse.jpg').convert('RGB'),(W,H)).filter(ImageFilter.GaussianBlur(42))
        bg=ImageEnhance.Color(bg).enhance(.8)
        return Image.blend(bg,Image.new('RGB',(W,H),(7,11,18)),.54)
    names=['apocalypse.jpg','garden.jpg','wuxia.jpg','space.jpg','midnight.jpg','twilight.jpg']
    collage=Image.new('RGB',(W,H),(20,24,32))
    for i,name in enumerate(names):
        tile=cover_crop(Image.open(ASSET/name).convert('RGB'),(W//3,H//2))
        collage.paste(tile,((i%3)*(W//3),(i//3)*(H//2)))
    collage=collage.filter(ImageFilter.GaussianBlur(58))
    return Image.blend(collage,Image.new('RGB',(W,H),(9,13,20)),.7)

def render(mode):
    page=make_backdrop(mode).convert('RGBA')
    d=ImageDraw.Draw(page,'RGBA')
    # Transparent left rail copied in spirit and dimensions from the existing desktop shell.
    label(d,(28,27),'雨',22,'#f1dba3')
    nav=[('home',True),('discover',False),('bookmark',False),('search',False),('person',False)]
    for i,(kind,active) in enumerate(nav):
        y=105+i*76
        ink=(233,201,130,230) if active else (245,245,248,210)
        if kind=='home': d.line([(29,y+15),(40,y+6),(51,y+15),(49,y+15),(49,y+25),(32,y+25),(32,y+15),(29,y+15)],fill=ink,width=2)
        elif kind=='discover':
            d.ellipse((31,y+5,49,y+23),outline=ink,width=2); d.line((40,y+9,44,y+16,37,y+20,40,y+9),fill=ink,width=2)
        elif kind=='bookmark': d.line([(32,y+5),(48,y+5),(48,y+25),(40,y+20),(32,y+25),(32,y+5)],fill=ink,width=2)
        elif kind=='search': d.ellipse((32,y+5,45,y+18),outline=ink,width=2); d.line((44,y+17,51,y+24),fill=ink,width=2)
        else: d.ellipse((36,y+4,44,y+12),outline=ink,width=2); d.arc((31,y+12,49,y+29),180,360,fill=ink,width=2)
        names={'home':'主页','discover':'发现','bookmark':'收藏','search':'搜索','person':'记录'}
        label(d,(24,y+29),names[kind],12,'#f1dba3' if active else '#d3d5db')
    d.ellipse((19,870,54,905),outline=(220,224,232,180),width=1); label(d,(29,910),'我',15,'#d4d7df')

    # Minimal header: plain text links, no separator rules, pills, card chrome, or decorative outlines.
    x0=126
    label(d,(x0,34),'主页',31,'#ffffff')
    label(d,(x0,76),'浏览正在展开的故事',14,'#c3c7ce')
    for x,t,active in [(414,'精选',True),(490,'新近',False),(566,'短片',False),(642,'主题',False)]:
        label(d,(x,50),t,15,'#f1dba3' if active else '#c6c9d0')
    d.ellipse((1202,48,1214,60),outline=(205,210,220,220),width=2); d.line((1212,58,1218,64),fill=(205,210,220,220),width=2)
    label(d,(1228,46),'搜索作品、作者或标签',14,'#b7bbc4')
    for x,t,active in [(126,'全部',True),(178,'末世',False),(230,'悬疑',False),(282,'关系',False),(334,'奇幻',False),(386,'解谜',False),(438,'武侠',False),(490,'短片',False)]:
        label(d,(x,112),t,13,'#f1dba3' if active else '#c6c9d0')

    # Borderless Pinterest-like masonry: each image has its own shape; portrait story art
    # follows the existing Reels 9:16 cover proportion. Text is overlaid like its Reels cover.
    columns=[
      [('apocalypse.jpg','第七天早晨','@废墟行者','楼下没有消防车，门外却有人逐户敲门。','8–12 分钟',16/9),
       ('garden.jpg','绣球花开的下午','@小林','这个下午，你们要决定怎样说清彼此的未来。','7–11 分钟',9/16),
       ('campus.jpg','迟到的夏天','@南窗','毕业前的最后一个夏天，几封信还没有寄出。','9 分钟',16/9)],
      [('wuxia.jpg','竹林听雨','@竹剑客','雨中的竹林里，你醒来时忘了昨夜的事。','8–12 分钟',9/16),
       ('space.jpg','深空信标','@星尘旅人','船长、工程师与尚未醒来的乘客留下了不同的选择。','8–12 分钟',16/9)],
      [('dream.jpg','记忆当铺','@梦境商人','凌晨三点，你走进记忆当铺。','8–12 分钟',1.05),
       ('midnight.jpg','午夜食堂','@夜食记','今晚可以只吃一碗面，也可以听见别人的夜晚。','8–12 分钟',16/9),
       ('twilight.jpg','福克斯：月圆之前','@月相观测者','你注意到了那个苍白、美丽、总坐在角落的人。','5–8 分钟',9/16)],
    ]
    left=126; gap=16; cols=3; tile_w=(1492-gap*(cols-1))//cols
    top=156; row_gap=14
    for col,items in enumerate(columns):
      y=top; x=left+col*(tile_w+gap)
      for filename,title,author,desc,duration,ratio in items:
        tile_h=round(tile_w/ratio)
        tile=cover_crop(Image.open(ASSET/filename).convert('RGB'),(tile_w,tile_h)).convert('RGBA')
        # Match the existing Reels cover's bottom fade; metadata stays over the actual artwork.
        fade=Image.new('RGBA',(tile_w,tile_h),(0,0,0,0)); fd=ImageDraw.Draw(fade)
        for yy in range(tile_h):
            t=max(0,min(1,(yy-tile_h*.28)/(tile_h*.72)))
            alpha=round(220*(t**1.65))
            fd.line((0,yy,tile_w,yy),fill=(0,0,0,alpha))
        tile=Image.alpha_composite(tile,fade)
        corner=Image.new('L',(tile_w,tile_h),0)
        ImageDraw.Draw(corner).rounded_rectangle((0,0,tile_w-1,tile_h-1),radius=15,fill=255)
        tile.putalpha(corner)
        page.alpha_composite(tile,(x,y))
        td=ImageDraw.Draw(page,'RGBA')
        label(td,(x+18,y+tile_h-74),title,19,'#ffffff')
        label(td,(x+18,y+tile_h-46),author,12,'#e0e2e6')
        label(td,(x+18,y+tile_h-25),desc,11,'#e0e2e6')
        tw=td.textbbox((0,0),duration,font=font(11))[2]
        label(td,(x+tile_w-tw-16,y+tile_h-25),duration,11,'#e0e2e6')
        y+=tile_h+row_gap

    output=OUT/f'home-tab-desktop-{mode}-review.png'
    page.convert('RGB').save(output,quality=93)
    return output

if __name__=='__main__':
    for mode in ('A','B','C'): print(render(mode))
