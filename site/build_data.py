import csv, json, re
from collections import defaultdict
import os
M=os.environ.get('BDL_MEMORY', os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','Claude Memory'))+'/'
games=[]
for r in csv.DictReader(open(M+'data/games_1990_2026.csv',encoding='utf-8-sig')):
    games.append([int(r['year']),int(r['week']),r['type'],r['owner_a'],float(r['score_a']),r['owner_b'],float(r['score_b']),int(r['placeholder'])])
assert not any(g[0]==2026 and g[1]==10 for g in games)
W10={('Derek','Tom'):(173.9,114.4),('Craig','Ricer'):(123.6,170.3),('Rusty','Frenches'):(174.5,150.7),('Abeln','Giff'):(107.8,123.9),('Chad','Schwanz'):(75.2,125.9)}
for (a,h),(sa,sh) in W10.items(): games.append([2026,10,'reg',a,sa,h,sh,0])
# Week 11 finals from CBS live scoring (pulled 11/24/26)
W11={('Rusty','Derek'):(126.7,134.6),('Ricer','Abeln'):(120.2,82.1),('Giff','Frenches'):(119.3,96.7),('Chad','Tom'):(76.4,119.2),('Schwanz','Craig'):(153.5,92.2)}
for (a,h),(sa,sh) in W11.items(): games.append([2026,11,'reg',a,sa,h,sh,0])
for g in games:
    for i in (3,5):
        if g[i]=='Chewy' and g[0]<=2002: g[i]='Chad'
# drop Southside self-play rows
games=[g for g in games if g[3]!=g[5]]
CUR=['Derek','Ricer','Rusty','Tom','Chad','Abeln','Giff','Schwanz','Craig','Frenches']
RIGHT=['Derek','Ricer','Rusty','Tom','Chad']; LEFT=['Abeln','Giff','Schwanz','Craig','Frenches']
TEAM={'Ricer':'Barca City Loungers','Derek':'Washington Island Ferries','Chad':'Tribute Mr French - AKA Mark','Rusty':'Junkyard Dog','Tom':'Tennessee Tomcats','Giff':'Boulder Giant Iguanas','Schwanz':'Bushwood Night Putters','Frenches':'Legion of Doom','Abeln':'Bloomington Syndicate','Craig':"Craig's House of Pain!"}
seasons=[]
for r in csv.DictReader(open(M+'data/owner_seasons.csv',encoding='utf-8-sig')):
    f=lambda k: (None if r[k]=='' else float(r[k]))
    seasons.append(dict(y=int(r['year']),o=r['owner'],div=r['division'],W=f('W'),L=f('L'),T=f('T'),PF=f('PF'),PA=f('PA'),df=f('division_finish'),po=r['playoff_finish'],aw=r['awards']))
# 2026 recompute through wk10
s26={o:dict(W=0,L=0,T=0,PF=0,PA=0,dw=0,dl=0,res=[]) for o in CUR}
for y,w,t,a,sa,b,sb,p in games:
    if y!=2026: continue
    for o,x,yy,opp in ((a,sa,sb,b),(b,sb,sa,a)):
        s=s26[o]; s['PF']+=x; s['PA']+=yy; r='W' if x>yy else 'L' if x<yy else 'T'; s[r]+=1; s['res'].append(r)
        if (o in RIGHT)==(opp in RIGHT): s['dw']+=r=='W'; s['dl']+=r=='L'
for s in seasons:
    if s['y']==2026:
        x=s26[s['o']]; s.update(W=x['W'],L=x['L'],T=x['T'],PF=round(x['PF'],1),PA=round(x['PA'],1))
# champions table
champs=[]
for line in open(M+'03_season_by_season.md'):
    m=re.match(r'^\| (\d{4}) \|(.*)$',line)
    if m:
        c=[x.strip() for x in m.group(2).split('|')]
        champs.append(dict(y=int(m.group(1)),champ=c[0],ru=c[1],final=c[2],right=c[3],left=c[4],pts=c[5]))
def nm(x):
    x=x.strip()
    if x.startswith('Chewy/Chad'): return 'Chad'
    return x.split(' ')[0] if x else ''
for c in champs:
    for k in ('champ','ru','right','left','pts'): c[k+'_o']=nm(c[k])
for s in seasons:
    if s['o']=='Chewy' and s['y']<=2002: s['o']='Chad'
# career for current owners computed from seasons + games
def rec(o):
    reg=[0,0,0]; po=[0,0]
    for y,w,t,a,sa,b,sb,p in games:
        if o not in (a,b): continue
        x,yy=(sa,sb) if a==o else (sb,sa)
        if t=='reg': reg[0 if x>yy else 1 if x<yy else 2]+=1
        else: po[0 if x>yy else 1]+=1
    return reg,po
career={}
for o in CUR+['Woody','Chewy','Marv','Downs','Jim','Rick']:
    reg,po=rec(o); ss=[s for s in seasons if s['o']==o]
    yrs=sorted({s['y'] for s in ss})
    career[o]=dict(reg=reg,po=po,first=yrs[0] if yrs else None,last=yrs[-1] if yrs else None,seasons=len(yrs),
      titles=[c['y'] for c in champs if c['champ_o']==o],ru=[c['y'] for c in champs if c['ru_o']==o],
      divs=[c['y'] for c in champs if o in (c['right_o'],c['left_o'])],pts=[c['y'] for c in champs if c['pts_o']==o],
      missed=sum(1 for s in ss if s['po']=='Missed playoffs'),playoffs=sum(1 for s in ss if s['po'] in('Champion','Runner-up','Lost semifinal','Lost quarterfinal')))
CR={r['owner']:r for r in csv.DictReader(open(M+'data/career_records.csv',encoding='utf-8-sig'))}
for o,c in career.items():
    if o in CR and o!='Chad': c['first']=int(CR[o]['first']); c['seasons']=int(CR[o]['seasons'])
keepers=[r for r in csv.DictReader(open(M+'data/keepers.csv',encoding='utf-8-sig'))]
# records
real=[g for g in games if not g[7]]
def tops(fil,key,n=10):
    out=[]
    for y,w,t,a,sa,b,sb,p in real:
        if not fil(y,t): continue
        for o,x,opp,yy in ((a,sa,b,sb),(b,sb,a,sa)): out.append(dict(y=y,w=w,t=t,o=o,s=x,opp=opp,os=yy))
    return out
sc=tops(lambda y,t:y>=2019,None)
high=sorted(sc,key=lambda d:-d['s'])[:10]
low=sorted([d for d in sc if d['y']<2026 or d['w']<=11],key=lambda d:d['s'])[:10]
blow=sorted([d for d in sc if d['s']>d['os']],key=lambda d:-(d['s']-d['os']))[:10]
close=sorted([d for d in sc if d['s']>d['os']],key=lambda d:(d['s']-d['os']))[:10]
data=dict(updated='Through 2026 Week 11',cur=CUR,right=RIGHT,left=LEFT,team=TEAM,games=games,seasons=seasons,champs=champs,career=career,keepers=keepers,
  s26={o:dict(W=v['W'],L=v['L'],T=v['T'],PF=round(v['PF'],1),PA=round(v['PA'],1),dw=v['dw'],dl=v['dl'],res=''.join(v['res'])) for o,v in s26.items()},
  week11=[['Derek','Schwanz'],['Giff','Rusty'],['Tom','Ricer'],['Frenches','Abeln'],['Craig','Chad']],
  rec=dict(high=high,low=low,blow=blow,close=close))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets','data.js'),'w').write('window.BDL='+json.dumps(data,separators=(',',':'))+';')
for o in CUR: print(o,career[o]['reg'],career[o]['po'],career[o]['titles'],len(career[o]['divs']),s26[o]['W'],s26[o]['L'],round(s26[o]['PF'],1))
print(high[:3],blow[:2],close[:2],low[:2])
