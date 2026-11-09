"""Master game log: raw All_Games 1991-2018 regular season (deduped, owner fixes)
plus recent.csv (2019-2025 regular season, 1993 Wk15, all playoffs) plus 2026 from data9."""
import csv
from data10 import GAMES
RAW = 'all_games.csv'
FIX = {'CRAIG': 'Craig', 'Ricer (T)': 'Ricer', 'Rusty (T)': 'Rusty', 'Delevan': 'Delavan', 'Kodiak': 'Rusty'}
def nm(o, y):
    o = FIX.get(o, o)
    if o == 'Chewy' and 1997 <= y <= 2002: o = 'Chad'
    return o
G = []; seen = set()
for r in csv.DictReader(open(RAW, encoding='utf-8-sig')):
    if not r['Year'] or not r['Owner']: continue
    y, w = int(r['Year']), int(r['Week'])
    if w >= 15 or y == 1990: continue
    if w == 14 and y >= 2015: continue
    a, b = nm(r['Owner'], y), nm(r['Opponent'], y)
    k = (y, w, frozenset((a, b)))
    if k in seen: continue
    seen.add(k)
    G.append(dict(y=y, w=w, a=a, b=b, sa=float(r['Points Scored']), sb=float(r['Points Allowed']), t='reg'))
for r in csv.DictReader(open('recent.csv')):
    G.append(dict(y=int(r['year']), w=int(r['week']), a=r['a'], b=r['b'], sa=float(r['sa']), sb=float(r['sb']), t=r['type']))
for wk, a, h, sa, sh in GAMES:
    G.append(dict(y=2026, w=wk, a=a, b=h, sa=sa, sb=sh, t='reg'))
def est(g): return 'est' in g['t'] or g['y'] == 2000
def pair(A, B):
    out = []
    for g in G:
        if {g['a'], g['b']} == {A, B}:
            x, yv = (g['sa'], g['sb']) if g['a'] == A else (g['sb'], g['sa'])
            out.append(dict(y=g['y'], w=g['w'], A=x, B=yv, po=g['t'].startswith('po'), est=est(g), t=g['t']))
    out.sort(key=lambda d: (d['y'], d['w']))
    return out
def res(d): return 'W' if d['A'] > d['B'] else 'L' if d['A'] < d['B'] else 'T'
def rec(ls):
    w = sum(res(d) == 'W' for d in ls); l = sum(res(d) == 'L' for d in ls); t = sum(res(d) == 'T' for d in ls)
    return f'{w}-{l}' + (f'-{t}' if t else '')
if __name__ == '__main__':
    chk = {('Derek','Ricer'): '41-34-1', ('Giff','Tom'): '26-19', ('Schwanz','Abeln'): '26-24', ('Frenches','Craig'): '20-15-2', ('Chad','Rusty'): '39-34'}
    for (A, B), want in chk.items():
        P = [d for d in pair(A, B) if not (d['y'] == 2026 and d['w'] >= 8)]
        print(A, B, rec(P), len(P), 'want', want)
