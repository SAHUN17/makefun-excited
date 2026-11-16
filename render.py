"""Original procedural artwork: A Small Fold in Infinity.

Pillow is a build dependency only. No external assets, fonts or model calls.
All geometry, lighting and particle distributions are authored here.
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SIZE = 1024
SS = 2
N = SIZE * SS
RNG = random.Random(712094)
ROOT = Path(__file__).resolve().parent


def canvas():
    return Image.new("RGB", (N, N))


def points(coords):
    return [(round(x * SS), round(y * SS)) for x, y in coords]


def line(draw, coords, color, width: float = 1.0):
    draw.line(points(coords), fill=color, width=max(1, round(width * SS)), joint="curve")


def polygon(draw, coords, color):
    draw.polygon(points(coords), fill=color)


def curve(a, b, c, d, steps=150):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1])
            for t in (i/steps for i in range(steps+1))]


def glow(base, layer, radius, gain: float = 1.0):
    blurred = layer.filter(ImageFilter.GaussianBlur(radius * SS))
    if gain != 1:
        blurred = blurred.point(lambda v: min(255, int(v * gain)))
    return ImageChops.add(base, blurred)


def render():
    # The abyss: smooth elliptic radiance, with a deep violet outer falloff.
    low = Image.new("RGB", (SIZE, SIZE))
    pix = low.load()
    assert pix is not None
    for y in range(SIZE):
        for x in range(SIZE):
            r = math.hypot((x-540)/420, (y-696)/266)
            halo = math.exp(-r*r*1.7)
            core = math.exp(-r*r*28)
            cyan = math.exp(-((r-0.94)/0.24)**2)
            pix[x,y] = (int(3+38*halo+133*core),
                        int(7+17*halo+78*core+18*cyan),
                        int(20+29*halo+32*core+33*cyan))
    image = low.resize((N,N), Image.Resampling.BICUBIC)
    dust = canvas()
    dd = ImageDraw.Draw(dust)
    # Four logarithmic arms: warm near the nucleus, ice blue at the rim.
    for arm in range(4):
        for _ in range(17500):
            r = RNG.random() ** 0.72
            theta = 10.8*r + arm*math.pi/2 + RNG.gauss(0,0.105+0.08*r)
            radius = 460*r
            x = 540+radius*math.cos(theta)
            y = 697+0.57*radius*math.sin(theta)
            scatter = RNG.gauss(0, 2+7*r)
            y += scatter
            mix = max(0,min(1,(r-0.47)*2.8))
            power = RNG.uniform(0.4,1)
            color = tuple(int(v*power) for v in (255*(1-mix)+55*mix, 133*(1-mix)+218*mix, 48*(1-mix)+255*mix))
            rad = RNG.choice([0.45,0.65,0.85,1.2,1.7])
            dd.ellipse(((x-rad)*SS,(y-rad)*SS,(x+rad)*SS,(y+rad)*SS),fill=color)
    image = glow(image,dust,13,0.8)
    image = glow(image,dust,3,0.65)
    image = ImageChops.add(image,dust)
    star = ImageDraw.Draw(image)
    for _ in range(700):
        x,y = RNG.uniform(0,1024),RNG.uniform(350,1024)
        r=RNG.choice([0.45,0.6,0.8,1.3])
        v=RNG.randrange(70,225)
        star.ellipse(((x-r)*SS,(y-r)*SS,(x+r)*SS,(y+r)*SS),fill=(v,int(v*.85),min(255,v+25)))
    # A compact incandescent nucleus and orbital filaments.
    nucleus=canvas()
    nd=ImageDraw.Draw(nucleus)
    for r in range(70,0,-1):
        t=1-r/70
        col=(int(80+175*t),int(28+221*t),int(10+202*t))
        nd.ellipse(((540-r)*SS,(697-r*.46)*SS,(540+r)*SS,(697+r*.46)*SS),fill=col)
    image=glow(image,nucleus,18,1.1)
    image=ImageChops.add(image,nucleus)
    fil=ImageDraw.Draw(image)
    for k in range(9):
        path=[]
        for i in range(350):
            t=i/349
            a=t*5.1+k*.12
            r=60+t*395
            path.append((540+r*math.cos(a),697+r*.57*math.sin(a)))
        line(fil,path,(45+8*k,103+8*k,125+8*k),0.55)
    # The split is a physical sheet: a narrow prow opens into huge peeled flaps.
    left=curve((551,344),(450,440),(371,638),(-100,1035))
    right=curve((551,344),(674,436),(758,690),(1120,1045))
    mask=Image.new("L",(N,N),255)
    md=ImageDraw.Draw(mask)
    md.polygon(points(left+list(reversed(right))),fill=0)
    ocean=canvas()
    od=ImageDraw.Draw(ocean)
    for y in range(N):
        t=y/N
        od.line((0,y,N,y),fill=(int(5+3*t),int(15+9*t),int(31+15*t)))
    # Quiet distant swells establish an enormous, otherwise unbroken ocean.
    for j in range(120):
        y=145+j*7.5
        for _ in range(5):
            x=RNG.uniform(-100,1024)
            length=RNG.uniform(25,190)*(0.3+y/1024)
            line(od,curve((x,y),(x+length*.3,y-4),(x+length*.8,y-4),(x+length,y)),(12,32+int(y/60),53+int(y/65)),0.65)
    image.paste(ocean,(0,0),mask)
    # Folded ocean ribbons, large planes with razor lit ridges.
    d=ImageDraw.Draw(image)
    louter=curve((551,344),(332,414),(343,657),(-70,758))
    router=curve((551,344),(781,401),(750,619),(1090,792))
    polygon(d,louter+list(reversed(left)),(14,57,77))
    polygon(d,router+list(reversed(right)),(13,48,69))
    lcrest=curve((551,344),(371,430),(411,628),(-40,845))
    rcrest=curve((551,344),(739,429),(735,658),(1060,887))
    polygon(d,lcrest+list(reversed(left)),(16,97,116))
    polygon(d,rcrest+list(reversed(right)),(15,78,104))
    # Angular paper facets distinguish the sea from a conventional liquid portal.
    polygon(d,[(551,344),(403,537),(213,688),(359,614)],(29,119,133))
    polygon(d,[(403,537),(359,614),(-10,875),(210,687)],(12,68,91))
    polygon(d,[(551,344),(716,530),(847,713),(753,617)],(25,100,122))
    polygon(d,[(716,530),(847,713),(1030,937),(753,617)],(10,57,85))
    edge=canvas()
    ed=ImageDraw.Draw(edge)
    line(ed,left,(255,163,68),3)
    line(ed,right,(255,181,83),3)
    line(ed,lcrest,(92,235,248),2.2)
    line(ed,rcrest,(76,210,242),2.2)
    image=glow(image,edge,10,0.7)
    image=ImageChops.add(image,edge)
    d=ImageDraw.Draw(image)
    # Nested tapered ribbons rush away from the little boat.
    for side in [-1,1]:
        for k in range(7):
            endx=551+side*(650+k*39)
            endy=800-k*49
            path=curve((551+side*8,352),(551+side*(100+k*12),421),
                       (551+side*(160+k*31),endy-40),(endx,endy))
            line(d,path,(24+k*4,75+k*8,99+k*9),1.1 if k else 2)
    # Selected spray lifts like tiny scraps of folded paper.
    for _ in range(100):
        t=RNG.uniform(.12,.94)
        side=RNG.choice([-1,1])
        x=551+side*(80*t+460*t*t)+RNG.gauss(0,12)
        y=344+620*t+RNG.gauss(-20,16)
        s=RNG.uniform(1,3)*(0.4+t)
        polygon(d,[(x,y-s*3),(x+s,y),(x,y+s),(x-s,y)],RNG.choice([(92,205,220),(247,186,110),(41,120,151)]))
    # The hero: crisp origami hull, golden sail and dark central crease.
    # Its upper silhouette is isolated against uninterrupted navy.
    shadow=canvas()
    sd=ImageDraw.Draw(shadow)
    line(sd,[(523,364),(551,349),(587,358)],(54,207,232),4)
    image=glow(image,shadow,9,1.2)
    d=ImageDraw.Draw(image)
    polygon(d,[(494,324),(551,341),(609,318),(571,365),(527,358)],(246,232,195))
    polygon(d,[(494,324),(551,341),(527,358)],(160,183,190))
    polygon(d,[(551,341),(609,318),(571,365)],(255,249,220))
    polygon(d,[(494,324),(552,309),(609,318),(551,341)],(235,219,179))
    polygon(d,[(552,309),(551,341),(536,325)],(91,114,131))
    line(d,[(551,338),(552,231)],(255,215,124),1.8)
    polygon(d,[(552,224),(552,318),(499,305)],(255,199,63))
    polygon(d,[(552,224),(537,292),(499,305)],(255,230,123))
    polygon(d,[(555,244),(589,307),(555,315)],(221,140,33))
    line(d,[(552,224),(537,292),(499,305)],(255,247,181),1.3)
    line(d,[(494,324),(551,341),(609,318)],(255,255,233),1.2)
    # A restrained lens streak ties the boat to the impossibly large nucleus.
    line(d,[(480,698),(599,698)],(255,235,189),0.8)
    # Downsample once for clean subpixel geometry; exact palette keeps the repo lean.
    final=image.resize((SIZE,SIZE),Image.Resampling.LANCZOS)
    final=final.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    final.save(ROOT/"entry.png",optimize=True)
    thumb=final.convert("RGB").resize((300,300),Image.Resampling.LANCZOS)
    thumb.save(ROOT/"thumbnail.png",optimize=True)
    print(f"Rendered {ROOT/'entry.png'} ({(ROOT/'entry.png').stat().st_size} bytes)")


if __name__ == "__main__":
    render()
