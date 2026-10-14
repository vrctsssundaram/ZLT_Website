from pathlib import Path
import random
random.seed(31)
R=Path(__file__).resolve().parents[1]
s=['''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1100" viewBox="0 0 1800 1100"><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#061724"/><stop offset=".55" stop-color="#102f44"/><stop offset="1" stop-color="#03111c"/></linearGradient><linearGradient id="metal" x2=".3" y2="1"><stop stop-color="#6195af"/><stop offset=".25" stop-color="#264e67"/><stop offset="1" stop-color="#112b3d"/></linearGradient><linearGradient id="chip" x2="1" y2="1"><stop stop-color="#235371"/><stop offset=".4" stop-color="#143348"/><stop offset="1" stop-color="#071e2e"/></linearGradient><radialGradient id="glow"><stop stop-color="#24c4f5" stop-opacity=".35"/><stop offset="1" stop-color="#0b5b80" stop-opacity="0"/></radialGradient><pattern id="vias" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="2" fill="#395b70"/><circle cx="12" cy="12" r=".7" fill="#081721"/></pattern><filter id="light"><feGaussianBlur stdDeviation="3"/></filter></defs><rect width="1800" height="1100" fill="url(#bg)"/><ellipse cx="1190" cy="470" rx="670" ry="540" fill="url(#glow)"/><g transform="translate(1150 470) matrix(.92 .45 -.92 .45 0 0)">''']
s.append('<rect x="-850" y="-850" width="1700" height="1700" rx="12" fill="#0b2638" stroke="#2d4a5d" stroke-width="4"/><rect x="-830" y="-830" width="1660" height="1660" fill="url(#vias)" opacity=".45"/>')
for k in range(4):
 s.append(f'<g transform="rotate({k*90})">')
 for j in range(38):
  x=-260+j*14;y=-305;end=-640-random.randint(0,190);turn=-370-random.randint(0,150);xx=x+random.choice([-1,1])*random.randint(20,150)
  color=random.choice(['#254b65','#285770','#3b7186','#236186'])
  d=f'M{x},{y} V{turn} L{xx},{turn-abs(xx-x)} V{end}'
  s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{random.choice([2,3,4])}"/><circle cx="{xx}" cy="{end}" r="5" fill="#315b73" stroke="#7195a6" stroke-width="1"/>')
  if j%8==0:s.append(f'<path d="{d}" fill="none" stroke="#4fdfff" stroke-width="2" opacity=".7"/><circle cx="{xx}" cy="{end}" r="8" fill="#68e5ff" opacity=".65" filter="url(#light)"/>')
 s.append('</g>')
for z in range(6):
 sz=340-z*9;y=-sz-z*8
 s.append(f'<rect x="{-sz}" y="{y}" width="{sz*2}" height="{sz*2}" rx="8" fill="#0b1e2c" stroke="{["#32566f","#3b7490"][z%2]}" stroke-width="3"/>')
s.append('<rect x="-293" y="-352" width="586" height="586" rx="12" fill="url(#metal)" stroke="#7bb9d0" stroke-width="2"/>')
for x in range(-277,280,17):
 for y in range(-335,222,17):
  if abs(x)>248 or y<-310 or y>192:s.append(f'<rect x="{x}" y="{y}" width="8" height="8" fill="#9dcedd" opacity=".45"/>')
s.append('<rect x="-243" y="-303" width="486" height="486" rx="5" fill="url(#chip)" stroke="#69c8e7" stroke-width="2"/><rect x="-224" y="-284" width="448" height="448" fill="none" stroke="#5688a3" stroke-width="1"/>')
for x,y,w,h in [(-206,-266,190,135),(0,-266,203,135),(-206,-115,92,210),(-97,-115,186,210),(106,-115,97,210),(-206,113,410,30)]:
 s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#173b54" stroke="#4389aa" stroke-width="1"/>')
 for yy in range(y+8,y+h-4,7):s.append(f'<path d="M{x+5},{yy} h{w-10}" stroke="#6899ae" stroke-width="1" opacity=".4"/>')
s.append('<rect x="-224" y="-284" width="448" height="448" fill="none" stroke="#62d8f6" stroke-width="5" filter="url(#light)" opacity=".35"/>')
for k in range(4):
 s.append(f'<g transform="rotate({k*90})">')
 for x in range(-210,220,32):s.append(f'<rect x="{x}" y="-492" width="17" height="45" rx="3" fill="#091a27" stroke="#426b83" stroke-width="2"/><path d="M{x},-490 h17 M{x},-450 h17" stroke="#90a9b6" stroke-width="4"/>')
 s.append('</g>')
s.append('</g><rect width="1800" height="1100" fill="none" stroke="#04131e" stroke-width="40"/></svg>')
(R/'assets/visuals/silicon-landscape.svg').write_text(''.join(s))
print('Original semiconductor illustration generated')
