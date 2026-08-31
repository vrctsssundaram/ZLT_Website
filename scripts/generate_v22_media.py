from PIL import Image, ImageDraw, ImageFilter
import math, os, random, subprocess
import numpy as np

OUT="assets/media"
os.makedirs(OUT, exist_ok=True)
random.seed(2206)

PALETTES={
    "hero":((4,10,24),(9,24,53),(35,229,255),(116,92,255),(255,78,163),(74,239,187),(255,190,64)),
    "ip":((4,12,27),(10,32,58),(34,226,255),(72,110,255),(146,91,255),(64,236,189),(255,183,65)),
    "engineering":((5,10,27),(22,18,57),(50,216,255),(133,91,255),(255,79,165),(255,166,74),(79,235,185)),
    "applications":((4,15,27),(8,39,49),(42,230,255),(52,113,255),(67,235,185),(204,246,78),(255,184,64)),
    "research":((7,9,28),(29,14,56),(61,214,255),(143,84,255),(255,77,169),(87,236,190),(255,185,69)),
}
BG={}

def lerp(a,b,t): return a+(b-a)*t

def bg_image(W,H,palette):
    key=(W,H,palette[0],palette[1])
    if key in BG: return BG[key]
    c0=np.array(palette[0],dtype=float); c1=np.array(palette[1],dtype=float)
    y=np.linspace(0,1,H)[:,None,None]
    arr=c0[None,None,:]*(1-y)+c1[None,None,:]*y
    arr=np.repeat(arr,W,axis=1)
    x=np.linspace(-1,1,W)[None,:,None]
    sheen=np.exp(-((x-.45)/.55)**2)*12
    arr=arr+sheen
    arr=np.clip(arr,0,255).astype(np.uint8)
    im=Image.fromarray(arr,"RGB").convert("RGBA")
    d=ImageDraw.Draw(im,"RGBA")
    step=max(34,W//24)
    for xx in range(0,W,step): d.line((xx,0,xx,H),fill=(120,185,255,10),width=1)
    for yy in range(0,H,step): d.line((0,yy,W,yy),fill=(120,185,255,8),width=1)
    BG[key]=im
    return im

def glow_layer(W,H,x,y,r,color,alpha=90):
    layer=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer,"RGBA")
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,alpha))
    return layer.filter(ImageFilter.GaussianBlur(max(3,int(r*.55))))

def add_vignette(img,strength=70):
    W,H=img.size
    layer=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer,"RGBA")
    d.rectangle((0,0,W,H*.11),fill=(0,0,0,strength//2))
    d.rectangle((0,H*.89,W,H),fill=(0,0,0,strength))
    d.rectangle((0,0,W*.08,H),fill=(0,0,0,strength//2))
    d.rectangle((W*.92,0,W,H),fill=(0,0,0,strength//2))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(max(8,W//60))))

def draw_wafer(W,H,u,p):
    img=bg_image(W,H,p).copy()
    img.alpha_composite(glow_layer(W,H,W*.73,H*.20,W*.20,p[2],45))
    d=ImageDraw.Draw(img,"RGBA")
    horizon=H*.53
    for k in range(13):
        q=k/12; yy=horizon+(H-horizon)*(q*q)
        d.line((0,yy,W,yy),fill=(110,175,235,int(18+12*q)),width=1)
    cx=W*(.58+.025*math.sin(u*math.tau)); cy=H*.56; rx=W*.31; ry=H*.28
    wafer=Image.new("RGBA",(W,H),(0,0,0,0)); wd=ImageDraw.Draw(wafer,"RGBA")
    for j in range(20,0,-1):
        q=j/20; col=(100+int(45*q),145+int(55*q),190+int(55*q),18)
        wd.ellipse((cx-rx*q,cy-ry*q,cx+rx*q,cy+ry*q),fill=col)
    wd.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),outline=(183,230,255,150),width=max(1,W//480))
    mask=Image.new("L",(W,H),0); md=ImageDraw.Draw(mask)
    md.ellipse((cx-rx+4,cy-ry+4,cx+rx-4,cy+ry-4),fill=255)
    grid=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(grid,"RGBA")
    cell=max(18,W//34)
    off=int((u*cell*.7)%cell)
    for xx in range(int(cx-rx)-cell,int(cx+rx)+cell,cell):
        gd.line((xx+off,cy-ry,xx+off,cy+ry),fill=(62,225,255,68),width=1)
    for yy in range(int(cy-ry)-cell,int(cy+ry)+cell,cell):
        gd.line((cx-rx,yy,cx+rx,yy),fill=(137,101,255,55),width=1)
    grid.putalpha(Image.composite(grid.getchannel("A"),Image.new("L",(W,H),0),mask))
    wafer.alpha_composite(grid)
    scanx=cx-rx+(2*rx)*((u*1.18)%1)
    wd=ImageDraw.Draw(wafer,"RGBA")
    wd.polygon([(scanx-10,cy-ry),(scanx+18,cy-ry),(scanx+55,cy+ry),(scanx+15,cy+ry)],fill=(86,236,255,35))
    wafer=wafer.filter(ImageFilter.GaussianBlur(.15))
    img.alpha_composite(wafer)
    # robotic process arms
    armx=W*(.10+.03*math.sin(u*math.tau))
    d=ImageDraw.Draw(img,"RGBA")
    d.rounded_rectangle((armx,H*.12,armx+W*.09,H*.18),radius=8,fill=(110,129,160,90),outline=(165,205,235,60),width=1)
    d.line((armx+W*.07,H*.18,cx-rx*.62,cy-ry*.62),fill=(151,183,214,80),width=max(3,W//220))
    d.ellipse((cx-rx*.67-7,cy-ry*.67-7,cx-rx*.67+7,cy-ry*.67+7),fill=(*p[6],140))
    add_vignette(img)
    return img.convert("RGB")

def draw_lithography(W,H,u,p):
    img=bg_image(W,H,p).copy()
    d=ImageDraw.Draw(img,"RGBA")
    # cleanroom chamber
    d.rounded_rectangle((W*.08,H*.08,W*.92,H*.88),radius=28,outline=(127,181,235,55),width=2,fill=(8,18,40,95))
    cx=W*.50; cy=H*.69; rx=W*.29; ry=H*.13
    d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=(77,119,159,95),outline=(174,232,255,120),width=2)
    # reticle
    rw=W*.29; rh=H*.18; ry0=H*.21
    d.rounded_rectangle((cx-rw/2,ry0,cx+rw/2,ry0+rh),radius=12,fill=(14,31,67,220),outline=(*p[2],130),width=2)
    step=rw/9
    for i in range(1,9):
        d.line((cx-rw/2+i*step,ry0+8,cx-rw/2+i*step,ry0+rh-8),fill=(*p[3],48),width=1)
    for j in range(1,5):
        y=ry0+j*rh/5; d.line((cx-rw/2+8,y,cx+rw/2-8,y),fill=(*p[4],42),width=1)
    beamx=cx-rw/2+rw*((u*1.15)%1)
    beam=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(beam,"RGBA")
    bd.polygon([(beamx-12,ry0+rh),(beamx+12,ry0+rh),(beamx+rx*.38,cy-ry),(beamx-rx*.38,cy-ry)],fill=(*p[2],44))
    bd.line((beamx,ry0+rh,beamx,cy-ry),fill=(255,255,255,130),width=2)
    img.alpha_composite(beam.filter(ImageFilter.GaussianBlur(5)))
    d=ImageDraw.Draw(img,"RGBA")
    for i in range(12):
        a=u*math.tau*1.4+i*.7
        x=cx+math.cos(a)*rx*(.2+.7*(i%3)/2); y=cy+math.sin(a)*ry*.65
        d.ellipse((x-2,y-2,x+2,y+2),fill=(*p[2+i%4],120))
    add_vignette(img)
    return img.convert("RGB")

def draw_interconnect(W,H,u,p):
    img=bg_image(W,H,p).copy()
    img.alpha_composite(glow_layer(W,H,W*.50,H*.48,W*.27,p[3],35))
    d=ImageDraw.Draw(img,"RGBA")
    margin=W*.12; top=H*.12; bottom=H*.86
    d.rounded_rectangle((margin,top,W-margin,bottom),radius=28,fill=(7,18,43,225),outline=(105,203,255,70),width=2)
    # metal layers and macro blocks
    cols=[p[2],p[3],p[4],p[5],p[6]]
    cols_a=[(*c,80) for c in cols]
    for j in range(6):
        y=top+H*.07+j*H*.105
        for k in range(5):
            x=margin+W*.06+k*W*.145
            ww=W*(.075+.025*((j+k)%3)); hh=H*(.045+.02*((j*2+k)%2))
            c=cols_a[(j+k)%len(cols_a)]
            d.rounded_rectangle((x,y,x+ww,y+hh),radius=6,fill=c,outline=(*cols[(j+k)%5],115),width=1)
    # routed buses
    routes=[
      [(margin+W*.03,H*.27),(W*.30,H*.27),(W*.30,H*.48),(W*.50,H*.48),(W*.50,H*.69),(W*.78,H*.69)],
      [(margin+W*.05,H*.74),(W*.26,H*.74),(W*.26,H*.56),(W*.62,H*.56),(W*.62,H*.31),(W*.82,H*.31)],
      [(W*.18,H*.19),(W*.18,H*.39),(W*.43,H*.39),(W*.43,H*.62),(W*.72,H*.62),(W*.72,H*.79)]
    ]
    for ri,route in enumerate(routes):
        c=cols[ri]
        d.line(route,fill=(*c,85),width=max(2,W//420),joint="curve")
        # moving pulse along segmented route
        lens=[]; total=0
        for a,b in zip(route,route[1:]):
            L=math.hypot(b[0]-a[0],b[1]-a[1]);lens.append((a,b,L));total+=L
        target=((u*(1.1+ri*.18)+ri*.27)%1)*total;acc=0
        x,y=route[0]
        for a,b,L in lens:
            if target<=acc+L:
                q=(target-acc)/L;x=lerp(a[0],b[0],q);y=lerp(a[1],b[1],q);break
            acc+=L
        img.alpha_composite(glow_layer(W,H,x,y,max(7,W//95),c,90))
        d=ImageDraw.Draw(img,"RGBA");d.ellipse((x-3,y-3,x+3,y+3),fill=(255,255,255,225))
    # vias
    for i in range(42):
        x=margin+((i*83)%int(W-2*margin));y=top+((i*47)%int(bottom-top))
        r=2+(i%2);d.ellipse((x-r,y-r,x+r,y+r),fill=(*cols[i%5],80))
    add_vignette(img)
    return img.convert("RGB")

def draw_architecture(W,H,u,p):
    img=bg_image(W,H,p).copy();d=ImageDraw.Draw(img,"RGBA")
    # blueprint plane
    d.rounded_rectangle((W*.07,H*.09,W*.93,H*.88),radius=26,fill=(6,20,46,205),outline=(101,188,255,68),width=2)
    blocks=[
      (.14,.18,.23,.33,p[2]),(.39,.17,.58,.30,p[3]),(.65,.16,.84,.31,p[4]),
      (.13,.47,.30,.68,p[5]),(.39,.43,.59,.70,p[2]),(.68,.46,.86,.69,p[6])
    ]
    for x0,y0,x1,y1,c in blocks:
        pulse=.55+.45*math.sin((u*math.tau)+(x0+y0)*8)
        d.rounded_rectangle((W*x0,H*y0,W*x1,H*y1),radius=10,fill=(*c,int(32+20*pulse)),outline=(*c,105),width=1)
        for k in range(3):
            yy=lerp(H*y0,H*y1,(k+1)/4);d.line((W*x0+10,yy,W*x1-10,yy),fill=(*c,28),width=1)
    links=[((.23,.255),(.39,.235)),((.58,.235),(.65,.235)),((.22,.33),(.22,.47)),((.49,.30),(.49,.43)),((.75,.31),(.75,.46)),((.30,.58),(.39,.56)),((.59,.56),(.68,.56))]
    for i,(a,b) in enumerate(links):
        c=p[2+i%5];x0,y0=W*a[0],H*a[1];x1,y1=W*b[0],H*b[1]
        d.line((x0,y0,x1,y1),fill=(*c,100),width=2)
        q=(u*1.25+i*.13)%1;x=lerp(x0,x1,q);y=lerp(y0,y1,q)
        d.ellipse((x-3,y-3,x+3,y+3),fill=(255,255,255,210))
    # timing waveform
    by=H*.80; left=W*.14; right=W*.86
    d.line((left,by,right,by),fill=(121,161,205,45),width=1)
    pts=[];steps=18
    for i in range(steps+1):
        x=lerp(left,right,i/steps);state=1 if ((i+int(u*4))%4 in (1,2)) else 0
        y=by-H*.035*state;pts.append((x,y))
        if i<steps: pts.append((lerp(left,right,(i+1)/steps),y))
    d.line(pts,fill=(*p[2],150),width=2)
    add_vignette(img)
    return img.convert("RGB")

def draw_board(W,H,u,p):
    img=bg_image(W,H,p).copy();d=ImageDraw.Draw(img,"RGBA")
    x0=W*.10;y0=H*.10;x1=W*.90;y1=H*.88
    d.rounded_rectangle((x0,y0,x1,y1),radius=30,fill=(6,38,46,235),outline=(79,221,188,90),width=2)
    # traces
    trace_cols=[p[5],p[2],p[6]]
    for k in range(14):
        y=y0+H*.06+k*H*.045
        sx=x0+W*.03; ex=x1-W*.04
        mid=W*(.30+.035*(k%7))
        c=trace_cols[k%3]
        d.line((sx,y,mid,y,mid,y+H*.025,ex,y+H*.025),fill=(*c,52),width=1)
    # connectors
    for k in range(10):
        xx=x0+W*.055+k*W*.072
        d.rounded_rectangle((xx,y0+H*.025,xx+W*.03,y0+H*.075),radius=3,fill=(186,203,181,75),outline=(222,240,224,70),width=1)
    cx=W*.55;cy=H*.49;s=min(W,H)*.31
    img.alpha_composite(glow_layer(W,H,cx,cy,s*.62,p[2],35))
    d=ImageDraw.Draw(img,"RGBA")
    d.rounded_rectangle((cx-s/2,cy-s/2,cx+s/2,cy+s/2),radius=22,fill=(8,15,32,240),outline=(*p[2],155),width=2)
    for k in range(8):
        q=(k+1)/9
        xx=cx-s/2+s*q
        d.line((xx,cy-s/2-10,xx,cy-s/2),fill=(210,230,225,105),width=2);d.line((xx,cy+s/2,xx,cy+s/2+10),fill=(210,230,225,105),width=2)
    for k in range(8):
        q=(k+1)/9;yy=cy-s/2+s*q
        d.line((cx-s/2-10,yy,cx-s/2,yy),fill=(210,230,225,105),width=2);d.line((cx+s/2,yy,cx+s/2+10,yy),fill=(210,230,225,105),width=2)
    # active LEDs and pulse packets
    for k in range(6):
        a=u*math.tau*1.3+k
        xx=W*(.18+.025*k);yy=H*(.74+.03*math.sin(a))
        c=trace_cols[k%3];d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=(*c,190))
    for k in range(5):
        q=(u*.9+k*.19)%1;xx=lerp(x0+W*.05,x1-W*.08,q);yy=y0+H*(.16+.10*k)
        img.alpha_composite(glow_layer(W,H,xx,yy,8,trace_cols[k%3],85))
    add_vignette(img)
    return img.convert("RGB")

def draw_network(W,H,u,p):
    img=bg_image(W,H,p).copy()
    d=ImageDraw.Draw(img,"RGBA")
    nodes=[(.17,.27),(.34,.18),(.52,.30),(.72,.19),(.84,.38),(.68,.61),(.45,.70),(.23,.62),(.50,.48)]
    cols=[p[2],p[3],p[5],p[6],p[4]]
    for i,a in enumerate(nodes):
        for j,b in enumerate(nodes[i+1:],i+1):
            dist=math.hypot(a[0]-b[0],a[1]-b[1])
            if dist<.34:d.line((W*a[0],H*a[1],W*b[0],H*b[1]),fill=(*cols[(i+j)%5],38),width=1)
    for i,(nx,ny) in enumerate(nodes):
        c=cols[i%5];r=11+(i%3)*4
        img.alpha_composite(glow_layer(W,H,W*nx,H*ny,r*2.2,c,50))
        d=ImageDraw.Draw(img,"RGBA")
        d.ellipse((W*nx-r,H*ny-r,W*nx+r,H*ny+r),fill=(7,20,43,230),outline=(*c,140),width=2)
        d.ellipse((W*nx-3,H*ny-3,W*nx+3,H*ny+3),fill=(*c,220))
    # packets
    edges=[(0,2),(1,2),(2,4),(4,5),(5,6),(6,7),(7,0),(2,8),(8,5)]
    for k,(a,b) in enumerate(edges):
        q=(u*(.8+.07*k)+k*.11)%1;x=lerp(W*nodes[a][0],W*nodes[b][0],q);y=lerp(H*nodes[a][1],H*nodes[b][1],q);c=cols[k%5]
        d.ellipse((x-3,y-3,x+3,y+3),fill=(255,255,255,230));img.alpha_composite(glow_layer(W,H,x,y,10,c,65))
    add_vignette(img)
    return img.convert("RGB")

def draw_secure(W,H,u,p):
    img=bg_image(W,H,p).copy()
    img.alpha_composite(glow_layer(W,H,W*.5,H*.48,W*.26,p[4],34))
    d=ImageDraw.Draw(img,"RGBA")
    cx=W*.5;cy=H*.48
    # modular rings / crypto accelerator motif
    for k,(rx,ry,c) in enumerate([(W*.29,H*.17,p[2]),(W*.23,H*.29,p[3]),(W*.35,H*.34,p[4])]):
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),outline=(*c,48),width=1)
        a=u*math.tau*(1 if k!=1 else -1)+k*2.1;x=cx+math.cos(a)*rx;y=cy+math.sin(a)*ry
        img.alpha_composite(glow_layer(W,H,x,y,12,c,90))
        d=ImageDraw.Draw(img,"RGBA");d.ellipse((x-3,y-3,x+3,y+3),fill=(255,255,255,220))
    s=min(W,H)*.30
    d.rounded_rectangle((cx-s/2,cy-s/2,cx+s/2,cy+s/2),radius=24,fill=(8,17,40,238),outline=(*p[3],120),width=2)
    # shield / lock-inspired geometric core, no literal logo
    shield=[(cx,cy-s*.30),(cx+s*.24,cy-s*.18),(cx+s*.19,cy+s*.16),(cx,cy+s*.30),(cx-s*.19,cy+s*.16),(cx-s*.24,cy-s*.18)]
    d.polygon(shield,fill=(*p[3],35),outline=(*p[2],135))
    d.ellipse((cx-s*.065,cy-s*.06,cx+s*.065,cy+s*.07),outline=(*p[5],150),width=2)
    d.line((cx,cy+s*.04,cx,cy+s*.15),fill=(*p[5],150),width=3)
    # arithmetic lattice
    for i in range(8):
        yy=H*(.15+i*.09)
        phase=(u*.8+i*.13)%1
        for j in range(6):
            xx=W*(.12+j*.13+.025*math.sin((phase+j)*math.tau))
            d.ellipse((xx-2,yy-2,xx+2,yy+2),fill=(*p[2+(i+j)%5],65))
    add_vignette(img)
    return img.convert("RGB")

def draw_vision(W,H,u,p):
    img=bg_image(W,H,p).copy();d=ImageDraw.Draw(img,"RGBA")
    # stylized sensor / vision field
    x0=W*.11;y0=H*.12;x1=W*.89;y1=H*.84
    d.rounded_rectangle((x0,y0,x1,y1),radius=24,fill=(5,25,43,210),outline=(84,212,221,55),width=2)
    vanish=(W*.50,H*.32)
    for k in range(-8,9):
        xb=W*.5+k*W*.065;d.line((vanish[0],vanish[1],xb,H*.82),fill=(63,198,221,25),width=1)
    for j in range(9):
        q=(j+1)/10;yy=lerp(vanish[1],H*.82,q*q);d.line((W*.14,yy,W*.86,yy),fill=(63,198,221,20),width=1)
    # object boxes
    boxes=[(.23,.38,.34,.60,p[2]),(.57,.34,.73,.55,p[5]),(.43,.57,.58,.77,p[6])]
    for i,(a,b,cx,dy,col) in enumerate(boxes):
        pulse=.6+.4*math.sin(u*math.tau+i)
        d.rounded_rectangle((W*a,H*b,W*cx,H*dy),radius=6,outline=(*col,int(100+45*pulse)),width=2)
        d.line((W*a,H*b,W*(a+.04),H*b),fill=(*col,200),width=3)
    # scanning line
    sy=lerp(H*.18,H*.80,(u*1.1)%1)
    d.line((W*.14,sy,W*.86,sy),fill=(*p[2],70),width=2)
    img.alpha_composite(glow_layer(W,H,W*.5,sy,W*.24,p[2],18))
    add_vignette(img)
    return img.convert("RGB")

SCENES={
    "wafer":draw_wafer,"lithography":draw_lithography,"interconnect":draw_interconnect,
    "architecture":draw_architecture,"board":draw_board,"network":draw_network,
    "secure":draw_secure,"vision":draw_vision,
}

def render_sequence(W,H,t,duration,scene_names,palette):
    n=len(scene_names); seg=duration/n; idx=min(n-1,int(t/seg)); local=(t-idx*seg)/seg
    fade=.16
    current=SCENES[scene_names[idx]](W,H,local,palette)
    if local>1-fade:
        nxt=(idx+1)%n; q=(local-(1-fade))/fade
        other=SCENES[scene_names[nxt]](W,H,max(0,min(1,q*.20)),palette)
        return Image.blend(current,other,0.5-0.5*math.cos(q*math.pi))
    return current

def encode_clip(name,duration,scene_names,palette_name,W=1280,H=720,fps=18,crf=22):
    p=PALETTES[palette_name];frames=int(duration*fps)
    poster=render_sequence(W,H,duration*.18,duration,scene_names,p)
    poster.save(f"{OUT}/{name}-poster.jpg",quality=94,optimize=True,progressive=True)
    mp4=f"{OUT}/{name}.mp4";webm=f"{OUT}/{name}.webm"
    enc=subprocess.Popen([
      "ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(fps),"-i","-",
      "-an","-c:v","libx264","-preset","medium","-crf",str(crf),"-profile:v","high","-movflags","+faststart","-pix_fmt","yuv420p",mp4
    ],stdin=subprocess.PIPE)
    for i in range(frames):
        frame=render_sequence(W,H,i/fps,duration,scene_names,p)
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    if enc.wait()!=0: raise SystemExit(f"mp4 encode failed: {name}")
    subprocess.check_call([
      "ffmpeg","-y","-loglevel","error","-i",mp4,"-an","-c:v","libvpx-vp9","-row-mt","1","-deadline","good","-cpu-used","4",
      "-crf",str(crf+9),"-b:v","0","-pix_fmt","yuv420p",webm
    ])
    print(name,os.path.getsize(webm),os.path.getsize(mp4))

def derive_mobile(name):
    src=f"{OUT}/{name}.mp4";dst=f"{OUT}/{name}-mobile.mp4";webm=f"{OUT}/{name}-mobile.webm"
    subprocess.check_call([
      "ffmpeg","-y","-loglevel","error","-i",src,"-an",
      "-vf","crop=608:1080:(in_w-608)/2:0,scale=720:1280:flags=lanczos,unsharp=5:5:0.42:3:3:0.18",
      "-c:v","libx264","-preset","medium","-crf","23","-profile:v","high","-movflags","+faststart","-pix_fmt","yuv420p",dst
    ])
    subprocess.check_call([
      "ffmpeg","-y","-loglevel","error","-i",dst,"-an","-c:v","libvpx-vp9","-row-mt","1","-deadline","good","-cpu-used","4",
      "-crf","33","-b:v","0","-pix_fmt","yuv420p",webm
    ])
    poster=Image.open(f"{OUT}/{name}-poster.jpg")
    w,h=poster.size;cw=max(1,int(h*720/1280));left=max(0,(w-cw)//2)
    poster.crop((left,0,left+cw,h)).resize((720,1280),Image.Resampling.LANCZOS).save(
      f"{OUT}/{name}-mobile-poster.jpg",quality=94,optimize=True,progressive=True
    )

# V24 hero: a 64-second master that loops indefinitely in the browser.
# The sequence moves from semiconductor-industry context into Zepto Logic's actual
# engineering domain: architecture, implementation, FPGA, secure compute and applications.
hero=["wafer","lithography","interconnect","architecture","board","secure","network","vision"]
encode_clip("zlt-hero-semiconductor-journey",64,hero,"hero",1920,1080,18,22)
derive_mobile("zlt-hero-semiconductor-journey")

# Higher-resolution domain films. These remain compact enough to load only when near view.
encode_clip("zlt-film-ip",24,["wafer","interconnect","architecture","interconnect"],"ip",1280,720,18,23)
encode_clip("zlt-film-engineering",24,["architecture","interconnect","board","architecture"],"engineering",1280,720,18,23)
encode_clip("zlt-film-applications",24,["board","network","vision","network"],"applications",1280,720,18,23)
encode_clip("zlt-film-research",24,["interconnect","secure","network","secure"],"research",1280,720,18,23)

print("Generated V24 high-resolution semiconductor cinematic media.")
