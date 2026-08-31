from PIL import Image, ImageDraw, ImageFilter
import math, os, subprocess, random
import numpy as np

OUT='assets/media'
DURATION=6
FPS=20
N=DURATION*FPS
random.seed(28)
os.makedirs(OUT,exist_ok=True)

particles=[(random.random(),random.random(),random.uniform(.7,1.7),random.choice([(69,223,255),(91,110,255),(183,92,255),(255,92,180),(65,238,179),(255,176,57)]),random.random()*math.tau) for _ in range(50)]
routes=[
    [(.02,.23),(.16,.23),(.16,.36),(.32,.36),(.32,.48),(.44,.48)],
    [(.06,.76),(.19,.76),(.19,.63),(.34,.63),(.34,.54),(.44,.54)],
    [(.98,.25),(.84,.25),(.84,.39),(.70,.39),(.70,.48),(.56,.48)],
    [(.96,.73),(.82,.73),(.82,.64),(.66,.64),(.66,.55),(.56,.55)],
    [(.15,.08),(.15,.16),(.28,.16),(.28,.28),(.44,.28),(.44,.42)],
    [(.86,.90),(.86,.82),(.71,.82),(.71,.72),(.56,.72),(.56,.58)]
]
cols=[(49,209,255),(79,107,255),(174,92,255),(239,75,182),(65,238,179),(255,171,57)]

def route_point(poly,u):
    lens=[]; tot=0
    for a,b in zip(poly,poly[1:]):
        L=math.hypot(b[0]-a[0],b[1]-a[1]); lens.append((a,b,L)); tot+=L
    tar=(u%1)*tot; acc=0
    for a,b,L in lens:
        if tar<=acc+L:
            q=(tar-acc)/L if L else 0
            return a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q
        acc+=L
    return poly[-1]

def make_base(W,H):
    y=np.linspace(0,1,H)[:,None]; x=np.linspace(0,1,W)[None,:]
    r=4+8*y+2*x; g=12+15*y+13*x; b=30+20*y+32*x
    arr=np.stack([np.broadcast_to(r,(H,W)),np.broadcast_to(g,(H,W)),np.broadcast_to(b,(H,W))],axis=2).clip(0,255).astype(np.uint8)
    base=Image.fromarray(arr,'RGB').convert('RGBA')
    d=ImageDraw.Draw(base,'RGBA')
    step=max(28,W//26)
    for xx in range(0,W,step): d.line((xx,0,xx,H),fill=(95,158,230,12),width=1)
    for yy in range(0,H,step): d.line((0,yy,W,yy),fill=(95,158,230,10),width=1)
    cx=W*.5; horizon=H*.54
    for i in range(-12,13):
        xb=cx+i*W*.075
        d.line((cx+(xb-cx)*.12,horizon,xb,H),fill=(80,150,255,26),width=1)
    for j in range(11):
        q=j/10; yy=horizon+(H-horizon)*(q*q)
        d.line((0,yy,W,yy),fill=(90,165,255,20),width=1)
    for poly,col in zip(routes,cols):
        d.line([(x*W,y*H) for x,y in poly],fill=(*col,48),width=1)
    return base

def glow_sprite(radius,color,alpha=150):
    R=int(radius); size=R*6
    im=Image.new('RGBA',(size,size),(0,0,0,0)); d=ImageDraw.Draw(im)
    cx=size//2; cy=size//2
    d.ellipse((cx-R,cy-R,cx+R,cy+R),fill=(*color,alpha))
    return im.filter(ImageFilter.GaussianBlur(max(2,R*.95)))

def paste_center(img,spr,x,y):
    img.alpha_composite(spr,(int(x-spr.width/2),int(y-spr.height/2)))

def render(W,H,i,base,glows):
    ph=i/N; t=ph*math.tau
    img=base.copy(); d=ImageDraw.Draw(img,'RGBA')
    aur=[(.14+.03*math.sin(t),.18+.025*math.cos(t),(45,101,255)),(.84+.025*math.cos(t),.20+.03*math.sin(t),(239,73,183)),(.72+.03*math.sin(t+.7),.78+.02*math.cos(t),(25,220,255))]
    for nx,ny,col in aur: paste_center(img,glows[col],nx*W,ny*H)
    d=ImageDraw.Draw(img,'RGBA')
    for ri,(poly,col) in enumerate(zip(routes,cols)):
        for p in range(2):
            nx,ny=route_point(poly,ph*(1.05+ri*.06)+p*.51+ri*.13)
            paste_center(img,glows[col],nx*W,ny*H)
            d.ellipse((nx*W-2,ny*H-2,nx*W+2,ny*H+2),fill=(255,255,255,220))
    core=(W*.50,H*.49)
    orbit_specs=[(.34,.16,cols[0],1.0),(.23,.39,cols[2],-.72),(.43,.25,cols[3],.5)]
    for oi,(rw,rh,col,spd) in enumerate(orbit_specs):
        d.ellipse((core[0]-W*rw/2,core[1]-H*rh/2,core[0]+W*rw/2,core[1]+H*rh/2),outline=(*col,42),width=1)
        a=t*spd+oi*2.1; x=core[0]+math.cos(a)*W*rw*.5; y=core[1]+math.sin(a)*H*rh*.5
        paste_center(img,glows[col],x,y)
    s=min(W,H)*.23; bob=math.sin(t)*H*.008
    paste_center(img,glows[(47,171,255)],core[0],core[1]+bob)
    d=ImageDraw.Draw(img,'RGBA')
    x0=core[0]-s/2; y0=core[1]-s/2+bob; x1=core[0]+s/2; y1=core[1]+s/2+bob
    d.rounded_rectangle((x0-14,y0-14,x1+14,y1+14),radius=s*.12,outline=(96,181,255,55),width=1)
    d.rounded_rectangle((x0,y0,x1,y1),radius=s*.12,fill=(9,21,49,235),outline=(102,231,255,165),width=2)
    pad=s*.14; cells=5; cs=(s-2*pad)/cells
    pals=[(48,98,229),(74,222,255),(131,92,255),(42,197,174),(232,82,177)]
    for yy in range(cells):
        for xx in range(cells):
            col=pals[(xx+yy*2)%5]
            pulse=.45+.55*(.5+.5*math.sin(t*1.3+xx*.7+yy*.75))
            bx=x0+pad+xx*cs; by=y0+pad+yy*cs
            d.rounded_rectangle((bx+2,by+2,bx+cs-3,by+cs-3),radius=max(2,cs*.10),fill=(*col,int(45+70*pulse)),outline=(126,198,255,25),width=1)
    for k in range(7):
        q=(k+1)/8; xx=x0+s*q; yy=y0+s*q
        d.line((xx,y0-14,xx,y0-3),fill=(92,225,255,90),width=1); d.line((xx,y1+3,xx,y1+14),fill=(92,225,255,90),width=1)
        d.line((x0-14,yy,x0-3,yy),fill=(151,111,255,80),width=1); d.line((x1+3,yy,x1+14,yy),fill=(151,111,255,80),width=1)
    for nx,ny,sz,col,p0 in particles:
        xx=(nx+.012*math.sin(t+p0))%1; yy=(ny+.016*math.cos(t*.7+p0))%1
        a=int(28+58*(.5+.5*math.sin(t+p0))); rr=max(1,sz*W/1000)
        d.ellipse((xx*W-rr,yy*H-rr,xx*W+rr,yy*H+rr),fill=(*col,a))
    sx=((ph*1.25)%1.25-.1)*W
    sweep=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sweep,'RGBA')
    sd.polygon([(sx-55,0),(sx+10,0),(sx+160,H),(sx+85,H)],fill=(95,222,255,10))
    img.alpha_composite(sweep.filter(ImageFilter.GaussianBlur(12)))
    vig=Image.new('RGBA',(W,H),(0,0,0,0)); vd=ImageDraw.Draw(vig,'RGBA')
    vd.rectangle((0,0,W,H*.10),fill=(0,0,0,55)); vd.rectangle((0,H*.88,W,H),fill=(0,0,0,75))
    vd.rectangle((0,0,W*.10,H),fill=(0,0,0,38)); vd.rectangle((W*.9,0,W,H),fill=(0,0,0,38))
    img.alpha_composite(vig.filter(ImageFilter.GaussianBlur(30)))
    return img.convert('RGB')

def encode(name,W,H):
    base=make_base(W,H)
    glow_r=max(6,int(W*.008)); big=max(70,int(W*.12))
    colors=set(cols+[(47,171,255),(45,101,255),(239,73,183),(25,220,255)])
    glows={c:glow_sprite(glow_r,c,145) for c in colors}
    glows[(45,101,255)]=glow_sprite(big,(45,101,255),55)
    glows[(239,73,183)]=glow_sprite(int(big*.82),(239,73,183),46)
    glows[(25,220,255)]=glow_sprite(int(big*.9),(25,220,255),40)
    glows[(47,171,255)]=glow_sprite(int(big*.55),(47,171,255),50)
    poster=render(W,H,0,base,glows)
    poster.save(f'{OUT}/{name}-poster.jpg',quality=88,optimize=True,progressive=True)
    webm=f'{OUT}/{name}.webm'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libvpx','-deadline','realtime','-cpu-used','8','-crf','30','-b:v','0','-pix_fmt','yuv420p',webm],stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(render(W,H,i,base,glows).tobytes())
    p.stdin.close()
    if p.wait(): raise SystemExit('webm encode failed')
    subprocess.check_call(['ffmpeg','-y','-loglevel','error','-i',webm,'-an','-c:v','libx264','-preset','veryfast','-crf','27','-movflags','+faststart','-pix_fmt','yuv420p',f'{OUT}/{name}.mp4'])

encode('zlt-silicon-film',960,540)
encode('zlt-silicon-film-mobile',640,360)
print('Generated original Zepto Logic motion assets.')
