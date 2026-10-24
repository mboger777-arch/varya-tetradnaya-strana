# Ставит выбранные дубли: {k: путь к mp3, текст для озвучки}. Меняет lines.json ('s' при переписанном ударении), удаляет старые mp3, пересобирает voice.js.
import json,hashlib,os,shutil,subprocess,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=R+'/assets/voice'
P=json.load(open(sys.argv[1]));LP=R+'/tools/lines.json';L=json.load(open(LP))
sp=lambda o:o.get('s',o['t'])
for o in L:
  if o['k'] not in P:continue
  f,t=P[o['k']];old=f"{o['k']}_{hashlib.sha1(f'v311|{o[chr(119)+chr(104)+chr(111)]}|{sp(o)}'.encode()).hexdigest()[:8]}.mp3"
  if t!=o['t']:o['s']=t
  else:o.pop('s',None)
  new=f"{o['k']}_{hashlib.sha1(f'v311|{o[chr(119)+chr(104)+chr(111)]}|{sp(o)}'.encode()).hexdigest()[:8]}.mp3"
  if old!=new and os.path.exists(f'{OUT}/{old}'):os.remove(f'{OUT}/{old}')
  shutil.copy(f,f'{OUT}/{new}');print(o['k'],old,'->',new)
json.dump(L,open(LP,'w'),ensure_ascii=False,indent=0)
