# Обычная скорость: логирует play/ended/pause каждой реплики и смену сцен. Реплику не должны обрывать (pause до ended).
import asyncio,os,sys,json
from playwright.async_api import async_playwright
URL=os.environ.get('URL','http://127.0.0.1:18770/index.html')
INIT='''(()=>{window.ALOG=[];const P=HTMLMediaElement.prototype,op=P.play,opa=P.pause;const t=()=>Math.round(performance.now());
P.play=function(){const s=this.src.split('/').pop();if(!this._h){this._h=1;this.addEventListener('ended',()=>ALOG.push([t(),'ended',s,this.duration]));}
 ALOG.push([t(),'play',s]);return op.call(this)};
P.pause=function(){if(!this.ended&&this.currentTime>0)ALOG.push([t(),'pause',this.src.split('/').pop(),+this.currentTime.toFixed(2),+(this.duration||0).toFixed(2)]);return opa.call(this)};
let last='';setInterval(()=>{try{if(typeof scene!=='undefined'&&scene!==last){last=scene;ALOG.push([t(),'scene',scene])}}catch(e){}},50)})()'''
async def main():
  sc=sys.argv[1] if len(sys.argv)>1 else 'intro';secs=int(sys.argv[2]) if len(sys.argv)>2 else 60
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    ctx=await b.new_context(viewport={'width':844,'height':390},has_touch=True,is_mobile=True)
    pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(INIT);await pg.goto(URL);await pg.wait_for_function('G.scene==="title"',timeout=30000)
    await pg.evaluate(os.environ.get('PRE','SV.intro=0'));await pg.evaluate(f'G.go("{sc}")')
    mt=float(os.environ.get('MIDT','0'))
    if os.environ.get('MID'):
      await pg.wait_for_timeout(mt*1000);await pg.evaluate(os.environ['MID']);secs-=mt
    await pg.wait_for_timeout(secs*1000);log=await pg.evaluate('ALOG')
    cut=[l for l in log if l[1]=='pause']
    for l in log:print(l)
    print('CUTS',len(cut),cut,'errs',errs[:5])
    await b.close()
asyncio.run(main())
