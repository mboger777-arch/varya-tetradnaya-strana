# Моргание NPC и Кляксы: глаз закрывается веком цвета кожи (эллипс с мягким краем и лёгкой тенью), сверху — дуга с ресничками.
import numpy as np,cv2,sys
from PIL import Image
EY={'snail':[(435,270,36,32),(532,265,26,29)],'granny':[(194,238,27,25),(275,247,23,21)],
 'zebra':[(90,197,28,34),(195,222,33,37)],'cirkul':[(160,195,18,22),(200,195,20,23)],
 'klyaksa_angry':[(146,353,59,35),(270,353,49,35)],'klyaksa_kind':[(180,335,52,57),(293,342,45,55)]}
SKIN={'granny':(240,186,156),'zebra':(236,226,210),'cirkul':(214,206,192),'klyaksa_angry':(38,62,118),'klyaksa_kind':(38,62,122)}
LID={'klyaksa_angry':(12,20,45),'klyaksa_kind':(12,20,45)}
only=sys.argv[1:]
for n,eyes in EY.items():
  if only and n not in only:continue
  im=np.array(Image.open(f'assets/sprites/{n}.png').convert('RGBA'));H,W=im.shape[:2];al=im[...,3];rgb=im[...,:3].astype(float)
  yy,xx=np.mgrid[0:H,0:W];S=4
  big=cv2.resize(im,(W*S,H*S),interpolation=cv2.INTER_LANCZOS4).astype(float)
  for (cx,cy,rx,ry) in eyes:
    d=((xx-cx)/rx)**2+((yy-cy)/ry)**2;ring=(d>1.5)&(d<2.6)&(al>250)
    sk=np.array(SKIN.get(n) or np.median(rgb[ring],0),float)
    lc=np.array(LID.get(n,(60,35,25)),float)
    Y,Xg=np.mgrid[0:H*S,0:W*S];dd=((Xg/S-cx)/(rx*1.06))**2+((Y/S-cy)/(ry*1.06))**2
    a=np.clip((1.0-dd)*ry*1.06/1.6,0,1)  # мягкий край ~1.5px
    t=np.clip((Y/S-(cy-ry))/(2*ry),0,1)
    col=sk[None,None,:]*(1.06-0.16*t[...,None])  # сверху светлее, к ресницам темнее
    col=np.clip(col,0,255)
    big[...,:3]=big[...,:3]*(1-a[...,None])+col*a[...,None]
    # дуга закрытого глаза
    layer=np.ascontiguousarray(big[...,:3].astype(np.uint8))
    hw=rx*.92*S;yc=(cy+ry*.18)*S;sag=ry*.42*S;th=max(3,int(min(rx,ry)*.16*S))
    pts=np.array([[cx*S+u*hw,yc+sag*(1-u*u)] for u in np.linspace(-1,1,48)],np.int32)
    c=tuple(int(v) for v in lc);cv2.polylines(layer,[pts],False,c,th,cv2.LINE_AA)
    for u in (-.75,0,.75):
      px,py=cx*S+u*hw,yc+sag*(1-u*u);cv2.line(layer,(int(px),int(py)),(int(px+u*hw*.12),int(py+sag*.55)),c,max(2,int(th*.6)),cv2.LINE_AA)
    big[...,:3]=layer
  out=cv2.resize(np.clip(big,0,255).astype(np.uint8),(W,H),interpolation=cv2.INTER_AREA);out[...,3]=al
  Image.fromarray(out).save(f'assets/sprites/{n}_blink.png');print(n)
