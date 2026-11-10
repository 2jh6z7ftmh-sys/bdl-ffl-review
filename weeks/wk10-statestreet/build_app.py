"""FFL Review league app: one link, five tabs (This Week, Standings, Teams, Head-to-Head, History).
Run: python3 build_app.py  ->  ffl_app.html
Reuses the Week 10 issue pieces from build10.py and the game log from hist.py."""
import csv, json, html
import build10 as B
import data10 as D, hist as H, odds10 as O

OWN = D.OWN
S = B.S
# ---------------------------------------------------------------- data for the app
CAREER = {  # Derek's career numbers, through 2025: titles, runner-ups, division titles, scoring titles, missed playoffs
 'Derek': (6, 3, 7, 3, 19), 'Ricer': (4, 7, 9, 4, 12), 'Abeln': (4, 3, 9, 2, 12), 'Giff': (5, 3, 5, 1, 17),
 'Schwanz': (2, 2, 4, 2, 8), 'Craig': (1, 1, 2, 0, 6), 'Rusty': (1, 6, 11, 3, 8), 'Frenches': (0, 3, 4, 2, 6),
 'Tom': (3, 1, 6, 0, 17), 'Chad': (4, 0, 2, 2, 10)}
SINCE = {'Derek': 1990, 'Tom': 1990, 'Ricer': 1991, 'Rusty': 1991, 'Abeln': 1993, 'Giff': 1993, 'Chad': 1995,
         'Schwanz': 1996, 'Frenches': 2009, 'Craig': 2010}
games = [[g['y'], g['w'], g['a'], g['b'], round(g['sa'], 2), round(g['sb'], 2),
          ('P' if g['t'].startswith('po') else 'R') + ('e' if H.est(g) else '')] for g in H.G]
champs = []
_ch, _ru = {}, {}
for r in csv.DictReader(open('../../shared/history/owner_seasons.csv')):
    if r['playoff_finish'] == 'Champion': _ch[int(r['year'])] = r['owner']
    if r['playoff_finish'] == 'Runner-up': _ru[int(r['year'])] = r['owner']
_fin = {g['y']: g for g in H.G if 'Final' in g['t']}
def _nm(o, y):  # Chad was half owner of Chewy's team, 1997-2002
    return ('Chewy', 'Chad, half owner') if o == 'Chad' and 1997 <= y <= 2002 else (o, '')
for y in sorted(_ch, reverse=True):
    c, csub = _nm(_ch[y], y); r, _ = _nm(_ru.get(y, ''), y); g = _fin.get(y); sc = None
    if g and not H.est(g):
        a, b = (g['sa'], g['sb']) if g['a'] == _ch[y] else (g['sb'], g['sa'])
        f = lambda x: str(int(x)) if x == int(x) else f'{x:.1f}'
        sc = f(a) + '-' + f(b)
    champs.append([y, c, csub, r, sc])
TITLES = {}
for y, c, csub, r, sc in champs: TITLES[c] = TITLES.get(c, 0) + 1
sched = {wk: pairs for wk, pairs in O.SCHED.items() if wk >= 10}
APP = dict(
    owners=OWN, right=D.RIGHT, team=D.OWNER, logo=B.LOGO, career=CAREER, since=SINCE,
    season={o: dict(w=S[o]['w'], l=S[o]['l'], dw=S[o]['dw'], dl=S[o]['dl'], pf=round(S[o]['pf'], 1),
                    weeks=S[o]['weeks'], po=O.ODDS[o]['po'], div=O.ODDS[o]['div'], st=O.ODDS[o]['st'],
                    chg=round(B.chg(o))) for o in OWN},
    sched=sched, games=games, champs=champs, titles=TITLES, unpaid=D.UNPAID, prov=B.PROV)

# ---------------------------------------------------------------- views
WEEK = ('<header class="mast" id="top"><div class="k">Bullwinkle\'s Dance League &middot; Week 10 &middot; Nov. 10 to 16</div>'
        '<h1><span>FFL</span>Review</h1><div class="sub">The State Street Bar Tour</div><div class="series">Five games, five stops</div></header>'
        + ('<div class="prov">Sample. Week 9 as it stood Sunday night; Monday night is still to play, so scores, picks and odds will move.</div>' if B.PROV else '')
        + B.three() + B.results()
        + '<section id="games"><h2>The State Street Bar Tour</h2><p class="dek">Week 10: five games, five stops.</p></section>'
        + ''.join(B.stop(s) for s in B.STOPS) + B.PICKNOTE)
STANDINGS = B.door().replace('id="door"', 'id="door-s"') + B.money().replace('id="money"', 'id="money-s"')

APPCSS = """
.raf{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px 10px;margin:8px 0 6px}
.ban{position:relative;background:var(--red);color:#fff;text-align:center;padding:16px 8px 30px;
 clip-path:polygon(0 0,100% 0,100% 86%,50% 100%,0 86%);animation:drop .55s cubic-bezier(.2,.9,.3,1.2) both}
.ban .yr{font:400 34px/1 'Anton';letter-spacing:1px}
.ban img,.ban .noimg{width:54px;height:54px;border-radius:50%;border:3px solid #fff;margin:8px auto 6px;display:block;background:#fff;object-fit:cover}
.ban .noimg{background:rgba(255,255,255,.18);font:400 26px/48px 'Anton';color:#fff}
.ban .who{font:700 19px/1.05 'Barlow Condensed';text-transform:uppercase;letter-spacing:.04em}
.ban .sub{font:500 11.5px 'Barlow';opacity:.85;margin-top:2px}
.ban .ov{font:600 12.5px/1.3 'Barlow';margin-top:6px;opacity:.95;overflow-wrap:anywhere}
.ban.top1{grid-column:1/-1;background:var(--ink);padding:22px 12px 40px}
.ban.top1 .yr{font-size:20px;letter-spacing:.2em;color:#ff4b52}
.ban.top1 img{width:96px;height:96px;margin:12px auto 8px}
.ban.top1 .who{font:400 40px/1 'Anton';letter-spacing:1px}
.ban.top1 .ov{font-size:15px}
.dec{grid-column:1/-1;font:400 22px/1 'Anton';color:var(--ink);border-bottom:3px solid var(--ink);padding:14px 0 4px;letter-spacing:1px}
@keyframes drop{from{opacity:0;transform:translateY(-36px) rotate(-4deg)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.ban{animation:none}}
.lead .r{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--rule)}
.lead .r .n{font:700 17px 'Barlow Condensed';text-transform:uppercase;width:92px}
.lead .cups{display:flex;gap:3px;flex-wrap:wrap;flex:1}
.lead .cups svg{width:17px;height:20px}
.lead .r b{font:400 22px 'Anton';margin-left:auto}

html,body{overflow-anchor:none} body{padding-bottom:76px}
.top{position:sticky;top:0;z-index:6;background:var(--red);color:#fff;display:flex;align-items:center;justify-content:center;height:44px;
 font:400 22px/1 'Anton';letter-spacing:2px;text-transform:uppercase}
.top span{background:#fff;color:var(--red);padding:2px 6px;margin-right:6px;transform:skew(-8deg);display:inline-block}
.tabs{position:fixed;left:0;right:0;bottom:0;z-index:7;background:var(--ink);display:flex;padding-bottom:env(safe-area-inset-bottom)}
.tabs a{flex:1;text-align:center;color:#bdb5a6;text-decoration:none;font:700 12px/1 'Barlow Condensed';letter-spacing:.08em;text-transform:uppercase;padding:12px 2px 14px}
.tabs a b{display:block;height:22px;margin:0 auto 5px;color:inherit} .tabs a b svg{height:22px;width:auto;display:block;margin:0 auto}
.tabs a.on{color:#fff;box-shadow:inset 0 3px 0 var(--red)}
.view{display:none} .view.on{display:block}
.tlist a{display:flex;align-items:center;gap:12px;padding:10px 2px;border-bottom:1px solid var(--rule);color:var(--ink);text-decoration:none}
.tlist .nm{font:700 19px/1.1 'Barlow Condensed';text-transform:uppercase} .tlist .nm small{display:block;font:500 13.5px 'Barlow';text-transform:none;color:var(--mut)}
.tlist .rt{margin-left:auto;text-align:right;font:700 17px 'Barlow Condensed'} .tlist .rt small{display:block;font:500 12.5px 'Barlow';color:var(--mut)}
.hero{display:flex;align-items:center;gap:14px;margin:6px 0 10px} .hero h2{margin:0}
.hero .sm{font:500 14px 'Barlow';color:var(--mut)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}
.stats div{background:var(--card);border:2px solid var(--ink);padding:8px 6px;text-align:center}
.stats b{display:block;font:400 26px/1 'Anton'} .stats span{font:700 11.5px 'Barlow Condensed';letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.bars{display:flex;align-items:flex-end;gap:5px;height:110px;margin:8px 0 2px;border-bottom:2px solid var(--ink)}
.bars i{flex:1;background:var(--red);position:relative;min-height:2px} .bars i.l{background:#9a948a}
.bars i em{position:absolute;bottom:-18px;left:0;right:0;text-align:center;font:700 11px 'Barlow Condensed';font-style:normal;color:var(--mut)}
.rows .r{display:flex;gap:8px;padding:7px 0;border-bottom:1px solid var(--rule);font-size:15.5px;align-items:center}
.rows .r .wk{width:38px;font:700 13px 'Barlow Condensed';color:var(--mut)} .rows .r .wl{width:22px;font:700 15px 'Barlow Condensed'}
.rows .r .wl.W{color:var(--red)} .rows .r .sc{margin-left:auto;font-variant-numeric:tabular-nums;white-space:nowrap}
.rows a{color:var(--ink)}
select{font:700 17px 'Barlow Condensed';text-transform:uppercase;padding:8px;border:2px solid var(--ink);background:var(--card);border-radius:0;width:100%;color:var(--ink)}
.pick2{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;margin:8px 0 14px} .pick2 .at{font:400 20px 'Anton';color:var(--red)}
.big{font:400 54px/1 'Anton';text-align:center;margin:6px 0} .bigsub{text-align:center;color:var(--mut);font-size:14px;margin-bottom:12px}
.champ .r{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--rule)} .champ .r b{font:700 17px 'Barlow Condensed';text-transform:uppercase}
table.car td,table.car th{text-align:center} table.car td:first-child,table.car th:first-child{text-align:left}
.back{display:inline-block;margin:10px 0 0;font:700 14px 'Barlow Condensed';letter-spacing:.08em;text-transform:uppercase;color:var(--red);text-decoration:none}
"""

JS = r"""
const A = DATA;
const $ = s => document.querySelector(s);
const logo = (o, px=40) => `<img class="lg" src="${A.logo[o]}" width="${px}" height="${px}" alt="">`;
const pct = x => { const p = x*100; return p>0 && p<0.5 ? '<1%' : (p>=99.5 && p<100 ? '>99%' : Math.round(p)+'%'); };
const f1 = x => (Math.round(x*10)/10).toFixed(1);
function series(A1, B1){
  const gs = A.games.filter(g => (g[2]===A1 && g[3]===B1) || (g[2]===B1 && g[3]===A1))
    .map(g => g[2]===A1 ? {y:g[0],w:g[1],a:g[4],b:g[5],t:g[6]} : {y:g[0],w:g[1],a:g[5],b:g[4],t:g[6]})
    .sort((x,y) => x.y-y.y || x.w-y.w);
  const rec = l => { let w=0,L=0,t=0; l.forEach(g => g.a>g.b?w++:g.a<g.b?L++:t++); return w+'-'+L+(t?'-'+t:''); };
  return {gs, all:rec(gs), reg:rec(gs.filter(g=>g.t[0]==='R')), po:rec(gs.filter(g=>g.t[0]==='P')), npo:gs.filter(g=>g.t[0]==='P').length};
}
function teams(){
  const list = [...A.owners].sort((a,b) => A.season[b].w-A.season[a].w || A.season[b].pf-A.season[a].pf);
  $('#v-teams').innerHTML = '<section><h2>Teams</h2><p class="dek">Tap a team for its season, history and every rivalry.</p><div class="tlist">' +
    list.map(o => { const s=A.season[o]; return `<a href="#team-${o.toLowerCase()}">${logo(o)}<div class="nm">${o}<small>${A.team[o]}</small></div>
      <div class="rt">${s.w}-${s.l}<small>${pct(s.po)} playoffs</small></div></a>`; }).join('') + '</div></section>';
}
function team(o){
  const s = A.season[o], c = A.career[o];
  const wks = Object.keys(s.weeks).map(Number).sort((a,b)=>a-b);
  const res = {};
  A.games.filter(g => g[0]===2026 && (g[2]===o || g[3]===o)).forEach(g => {
    const me = g[2]===o; res[g[1]] = {opp: me?g[3]:g[2], a: me?g[4]:g[5], b: me?g[5]:g[4]}; });
  const mx = Math.max(...wks.map(w=>s.weeks[w]));
  const bars = wks.map(w => `<i class="${res[w] && res[w].a<res[w].b?'l':''}" style="height:${s.weeks[w]/mx*100}%"><em>${w}</em></i>`).join('');
  const rows = wks.map(w => { const r=res[w]; const R = r.a>r.b?'W':r.a<r.b?'L':'T';
    return `<div class="r"><span class="wk">Wk ${w}</span><span class="wl ${R}">${R}</span><a href="#team-${r.opp.toLowerCase()}">${r.opp}</a><span class="sc">${f1(r.a)} to ${f1(r.b)}</span></div>`; }).join('');
  const left = Object.keys(A.sched).map(Number).sort((a,b)=>a-b).map(wk => { const p = A.sched[wk].find(p => p.includes(o)); const opp = p[0]===o?p[1]:p[0];
    return `<div class="r"><span class="wk">Wk ${wk}</span><a href="#team-${opp.toLowerCase()}">${opp}</a><span class="sc">${A.season[opp].w}-${A.season[opp].l}</span></div>`; }).join('');
  const vs = A.owners.filter(x=>x!==o).map(x => { const sr = series(o,x);
    return `<div class="r"><a href="#h2h" onclick="setH2H('${o}','${x}')">${x}</a><span class="sc">${sr.all}${sr.npo?` &middot; ${sr.po} playoffs`:''}</span></div>`; }).join('');
  const owe = A.unpaid.includes(o) ? '<span class="owe">Owes $200</span>' : '';
  $('#v-team').innerHTML = `<section><a class="back" href="#teams">&larr; All teams</a><div class="hero">${logo(o,64)}<div><h2>${o}${owe}</h2><div class="sm">${A.team[o]} &middot; since ${A.since[o]}</div></div></div>
    <div class="stats"><div><b>${s.w}-${s.l}</b><span>Record</span></div><div><b>${pct(s.po)}</b><span>Playoffs ${s.chg>=0?'+':''}${s.chg}</span></div><div><b>${Math.round(s.pf)}</b><span>Points</span></div></div>
    <div class="dv">2026, week by week</div><div class="bars">${bars}</div><div style="height:22px"></div><div class="rows">${rows}</div>
    <div class="dv">Still to play</div><div class="rows">${left}</div>
    <div class="dv">Career, through 2025</div><div class="stats"><div><b>${c[0]}</b><span>Titles</span></div><div><b>${c[1]}</b><span>Runner-up</span></div><div><b>${c[2]}</b><span>Division</span></div></div>
    <div class="stats"><div><b>${c[3]}</b><span>Scoring titles</span></div><div><b>${c[4]}</b><span>Missed playoffs</span></div><div><b>${2026-A.since[o]}</b><span>Seasons</span></div></div>
    <div class="dv">Against everyone</div><div class="rows">${vs}</div></section>`;
}
let H1 = 'Derek', H2 = 'Tom';
function setH2H(a,b){ H1=a; H2=b; }
function h2h(){
  const opts = sel => A.owners.map(o => `<option ${o===sel?'selected':''}>${o}</option>`).join('');
  const sr = series(H1, H2), gs = sr.gs;
  let body = '';
  if (H1 === H2) body = '<p class="dek">Pick two different teams.</p>';
  else if (!gs.length) body = '<p class="dek">They have never played.</p>';
  else {
    const real = gs.filter(g => !g.t.includes('e'));
    const big1 = real.filter(g=>g.a>g.b).sort((x,y)=>(y.a-y.b)-(x.a-x.b))[0], big2 = real.filter(g=>g.b>g.a).sort((x,y)=>(y.b-y.a)-(x.b-x.a))[0];
    const close = real.filter(g=>g.a!==g.b).sort((x,y)=>Math.abs(x.a-x.b)-Math.abs(y.a-y.b))[0];
    const line = (g, lbl) => g ? `<div class="r"><span class="wk">${g.y}</span><span>${lbl}</span><span class="sc">${f1(g.a)} to ${f1(g.b)}</span></div>` : '';
    const last = gs.slice(-5).reverse().map(g => { const R=g.a>g.b?'W':g.a<g.b?'L':'T';
      return `<div class="r"><span class="wk">${g.y} W${g.w}</span><span class="wl ${R}">${R}</span><span>${g.t[0]==='P'?'Playoffs':''}</span><span class="sc">${f1(g.a)} to ${f1(g.b)}</span></div>`; }).join('');
    body = `<div class="big">${sr.all}</div><div class="bigsub">${H1}'s record against ${H2}, ${gs.length} meetings since ${gs[0].y}${sr.npo?` &middot; playoffs ${sr.po}`:''}</div>
      <div class="dv">Last five</div><div class="rows">${last}</div>
      <div class="dv">Notable</div><div class="rows">${line(big1, H1+"'s biggest win")}${line(big2, H2+"'s biggest win")}${line(close,'Closest game')}</div>`;
  }
  $('#v-h2h').innerHTML = `<section><h2>Head to head</h2><p class="dek">Every meeting on record since 1991, playoffs included.</p>
    <div class="pick2"><select id="ha">${opts(H1)}</select><span class="at">vs</span><select id="hb">${opts(H2)}</select></div>${body}</section>`;
  $('#ha').onchange = e => { H1 = e.target.value; h2h(); };
  $('#hb').onchange = e => { H2 = e.target.value; h2h(); };
}
function history(){
  const cup = '<svg viewBox="0 0 24 28"><path fill="var(--red)" d="M5 2h14v5a7 7 0 0 1-5 6.7V18h3v3H7v-3h3v-4.3A7 7 0 0 1 5 7zM1 3h3v4a3 3 0 0 1-2-2.8zm22 0h-3v4a3 3 0 0 0 2-2.8zM6 23h12v3H6z"/></svg>';
  const pic = (o) => A.logo[o] ? `<img src="${A.logo[o]}" alt="">` : `<div class="noimg">${o[0]}</div>`;
  const ov = c => c[3] ? `over ${c[3]}${c[4] ? ', ' + c[4] : ''}` : '';
  let i = 0, dec = null, b = '';
  A.champs.forEach((c, k) => {
    if (k === 0) { b += `<div class="ban top1" style="animation-delay:0s"><div class="yr">${c[0]} champion</div>${pic(c[1])}<div class="who">${c[1]}</div>${c[2] ? `<div class="sub">${c[2]}</div>` : ''}<div class="ov">${ov(c)}</div></div>`; return; }
    const d = Math.floor(c[0] / 10) * 10;
    if (d !== dec) { dec = d; b += `<div class="dec">${d}s</div>`; }
    i++;
    b += `<div class="ban" style="animation-delay:${Math.min(i * 0.05, 1.2)}s"><div class="yr">${c[0]}</div>${pic(c[1])}<div class="who">${c[1]}</div>${c[2] ? `<div class="sub">${c[2]}</div>` : ''}<div class="ov">${ov(c)}</div></div>`;
  });
  const lead = Object.entries(A.titles).sort((x, y) => y[1] - x[1] || x[0].localeCompare(y[0]))
    .map(([o, n]) => `<div class="r">${A.logo[o] ? logo(o, 32) : '<span style="width:32px"></span>'}<span class="n">${o}</span><span class="cups">${cup.repeat(n)}</span><b>${n}</b></div>`).join('');
  const car = [...A.owners].sort((a,b)=>A.career[b][0]-A.career[a][0] || A.career[b][1]-A.career[a][1]);
  $('#v-history').innerHTML = `<section><h2>The rafters</h2><p class="dek">Every champion since 1990.</p>
    <div class="raf">${b}</div>
    <div class="dv" style="margin-top:22px">Title count</div><div class="lead">${lead}</div>
    <div class="dv" style="margin-top:22px">Career, through 2025</div><table class="car"><tr><th>Owner</th><th>Titles</th><th>2nd</th><th>Div</th><th>Scoring</th></tr>
    ${car.map(o=>{const c=A.career[o];return `<tr><td><a href="#team-${o.toLowerCase()}" style="color:var(--ink)">${o}</a></td><td><b>${c[0]}</b></td><td>${c[1]}</td><td>${c[2]}</td><td>${c[3]}</td></tr>`}).join('')}</table>
    <p class="small" style="margin-top:10px">Final scores before 1998 aren't on record.</p></section>`;
}
const VIEWS = ['week','standings','teams','h2h','history'];
function route(){
  const h = (location.hash || '#week').slice(1);
  let v = VIEWS.includes(h) ? h : (h.startsWith('team-') ? 'team' : (['top','results','games'].includes(h) || /^s\d$/.test(h) ? 'week' : 'week'));
  document.querySelectorAll('.view').forEach(e => e.classList.toggle('on', e.id === 'v-'+v));
  document.querySelectorAll('.tabs a').forEach(a => a.classList.toggle('on', a.dataset.v === (v==='team'?'teams':v)));
  if (v === 'teams') teams();
  if (v === 'team') { const o = A.owners.find(x => 'team-'+x.toLowerCase() === h); if (o) team(o); }
  if (v === 'h2h') h2h();
  if (v === 'history') history();
  if (VIEWS.includes(h) || v === 'team') window.scrollTo({top: 0, behavior: 'instant'});
}
window.addEventListener('hashchange', route); route();
"""

ICONS = {'week': '<svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M4 4h13v16H6a2 2 0 0 1-2-2zM17 8h3v10a2 2 0 0 1-2 2M7 8h7M7 12h7M7 16h4"/></svg>', 'standings': '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M3 13h5v8H3zM9.5 3h5v18h-5zM16 8h5v13h-5z"/></svg>', 'teams': '<svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/></svg>', 'h2h': '<svg viewBox="0 0 24 24"><text x="12" y="17" text-anchor="middle" font-family="Anton" font-size="15" fill="currentColor">VS</text></svg>', 'history': '<svg viewBox="0 0 24 28"><path fill="currentColor" d="M5 2h14v5a7 7 0 0 1-5 6.7V18h3v3H7v-3h3v-4.3A7 7 0 0 1 5 7zM1 3h3v4a3 3 0 0 1-2-2.8zm22 0h-3v4a3 3 0 0 0 2-2.8zM6 23h12v3H6z"/></svg>'}
TABS = [('week', ICONS['week'], 'This week'), ('standings', ICONS['standings'], 'Standings'), ('teams', ICONS['teams'], 'Teams'), ('h2h', ICONS['h2h'], 'Head to head'), ('history', ICONS['history'], 'History')]
HTML = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="apple-mobile-web-app-title" content="FFL Review"><meta name="application-name" content="FFL Review">'
        '<meta name="theme-color" content="#c5050c"><title>FFL Review</title>'
        f'<style>{B.FONTS}{B.CSS}{APPCSS}</style></head><body>'
        '<div class="top"><span>FFL</span>Review</div><div class="wrap">'
        f'<div class="view" id="v-week">{WEEK}</div>'
        f'<div class="view" id="v-standings">{STANDINGS}</div>'
        '<div class="view" id="v-teams"></div><div class="view" id="v-team"></div><div class="view" id="v-h2h"></div><div class="view" id="v-history"></div>'
        '</div><nav class="tabs">' + ''.join(f'<a href="#{k}" data-v="{k}"><b>{i}</b>{l}</a>' for k, i, l in TABS) + '</nav>'
        f'<script>const DATA = {json.dumps(APP, separators=(",", ":"))};{JS}</script></body></html>')
open('ffl_app.html', 'w').write(HTML)
print('ok', len(HTML) // 1024, 'KB', len(games), 'games')
