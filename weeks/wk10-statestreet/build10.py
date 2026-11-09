"""FFL Review Week 10, "State Street, 1990" bar crawl. Phone-first web issue.
Run: python3 build10.py  ->  ffl_wk10.html
SAMPLE: Week 9 scores are provisional (CBS live, Sunday night), see data10.PROVISIONAL9."""
import base64, html
import data10 as D, hist as H, odds10 as O

def img(p, mime='image/jpeg'): return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()
LOGO = {o: img(f'web/logo_{o.lower()}.jpg') for o in D.OWN}
PH = {k: img(f'web/{k}.jpg') for k in ('red_shed_group', 'rusty_moose_brats', 'rusty_mattress', 'tom_downs_shotgun', 'union_terrace_group')}
S = D.season(9); S8 = D.season(8)
LG = sum(S[o]['pf'] for o in D.OWN) / 90.0
def proj(o): return .7 * S[o]['pf'] / 9 + .3 * LG
def conf(g): return 'Coin flip' if g < 10 else ('56%' if g < 20 else '66%')
def wl(o): return f"{S[o]['w']}-{S[o]['l']}"
def pct(o, k='po'): return O.pct(O.ODDS[o][k])
def chg(o): return (O.ODDS[o]['po'] - O.PREV[o]['po']) * 100
def lg(o, px=40): return f'<img class="lg" src="{LOGO[o]}" width="{px}" height="{px}" alt="{o}">'
TEAM = D.OWNER
PROV = D.PROVISIONAL9

# ---------------------------------------------------------------- Week 9 results (provisional)
W9 = [(a, h, D.W9[(a, h)]) for a, h in D.W9]
PICKS9 = {('Derek', 'Giff'): 'Derek', ('Frenches', 'Schwanz'): 'Schwanz', ('Chad', 'Abeln'): 'Chad', ('Ricer', 'Rusty'): 'Rusty', ('Tom', 'Craig'): 'Tom'}
hits9 = sum((PICKS9[(a, h)] == (a if sa > sh else h)) for a, h, (sa, sh) in W9)
SEASON = (18 + hits9, 12 + 5 - hits9)
RECAP = {
 ('Derek', 'Giff'): "Giff's third straight. The Ferries have now lost two in a row and are 2-2 in the division.",
 ('Frenches', 'Schwanz'): "Six straight for Schwanz, who also leads the league in points. The Frenches fall to 5-4.",
 ('Chad', 'Abeln'): "Abes still has three players going Monday night and needs about 75 points to catch up.",
 ('Ricer', 'Rusty'): "The week's high score, and Ricer goes 7-2. Meeting No. 86 goes to Ricer; he now leads the series 43-39-4.",
 ('Tom', 'Craig'): "Tom's first win since Week 7. Craig has lost two straight.",
}

# ---------------------------------------------------------------- Week 10 stops
STOPS = [
 dict(pair=('Craig', 'Ricer'), n=1, bar=None,
      text=("Ricer is 7-2 and two games clear in the Right. Craig is 2-7 and at 1%, though he has beaten Ricer in two of their last four.")),
 dict(pair=('Chad', 'Schwanz'), n=2, bar=None,
      text=("A rematch of last year's final, which Chad won by 50. Schwanz has won six straight and leads the league in points; "
            "Chad just climbed to 80% playoff odds.")),
 dict(pair=('Rusty', 'Frenches'), n=3, bar=None,
      text=("Rusty is second in the league in points and 3-6, which takes some doing. His playoff odds are down to 32%. "
            "The Frenches have won the last three in this series, including Week 1 by 0.8.")),
 dict(pair=('Abeln', 'Giff'), n=4, bar=None,
      text=("Old housemates. Giff is 7-2 on three straight wins with the fewest points of any contender, which is its own kind of talent. "
            "Abes is 1-8. Giff leads the series 38-33-2.")),
 dict(pair=('Derek', 'Tom'), n=5, bar=None,
      text=("The oldest rivalry in the league: 73 games since 1990, Derek up 36-34-3. The Ferries have lost two straight and slipped to 68%. "
            "Tom has outscored them both of the last two weeks.")),
]

# ---------------------------------------------------------------- page
FONTS = ''.join(f"@font-face{{font-family:'{n}';src:url({img('ff/'+f+'.woff2','font/woff2')}) format('woff2');font-weight:{w};font-style:{st};font-display:swap}}"
                for n, f, w, st in [('Anton','anton-latin-400-normal',400,'normal'),('Barlow','barlow-latin-400-normal',400,'normal'),
                                    ('Barlow','barlow-latin-400-italic',400,'italic'),('Barlow','barlow-latin-500-normal',500,'normal'),
                                    ('Barlow','barlow-latin-700-normal',700,'normal'),('Barlow Condensed','barlow-condensed-latin-700-normal',700,'normal'),
                                    ('Courier Prime','courier-prime-latin-700-normal',700,'normal')])
CSS = """
:root{--red:#c5050c;--redd:#8f0309;--ink:#15121c;--paper:#f7f0e1;--card:#fffaf0;--mut:#6b6455;--rule:#d9c9a6;--gold:#f2b632}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.5 'Barlow',system-ui,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:680px;margin:0 auto;padding:0 16px 40px}
.nav{position:sticky;top:0;z-index:5;background:var(--ink);display:flex;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.nav a{color:#fff;text-decoration:none;font:700 13px/1 'Barlow Condensed';letter-spacing:.1em;text-transform:uppercase;padding:13px 12px;flex:none}
.nav a:first-child{color:var(--gold)}
section{scroll-margin-top:46px;padding-top:22px}
.mast{background:var(--red);color:#fff;margin:0 -16px;padding:22px 18px 18px}
.mast .k{font:700 12px 'Courier Prime',monospace;letter-spacing:.18em;text-transform:uppercase;opacity:.9}
.mast h1{font:400 64px/0.9 'Anton';letter-spacing:2px;margin:8px 0 6px;text-transform:uppercase}
.mast h1 span{display:inline-block;background:#fff;color:var(--red);padding:0 8px;transform:skew(-8deg);margin-right:6px}
.mast .sub{font:700 20px/1.2 'Barlow Condensed';text-transform:uppercase;letter-spacing:.04em}
.prov{background:var(--gold);color:var(--ink);font:700 13px/1.35 'Barlow Condensed';letter-spacing:.06em;text-transform:uppercase;padding:9px 12px;margin:0 -16px}
h2{font:400 32px/1 'Anton';text-transform:uppercase;letter-spacing:.5px;margin:0 0 4px}
h2 .no{display:inline-block;background:var(--red);color:#fff;font-size:20px;padding:4px 8px 2px;margin-right:8px;transform:skew(-8deg);vertical-align:4px}
.dek{font:italic 15px/1.4 'Barlow';color:var(--mut);margin:0 0 12px}
.rule{height:4px;background:var(--red);margin:16px 0 0}
.three li{margin:0 0 10px} .three b{font:700 19px/1.2 'Barlow Condensed';text-transform:uppercase;display:block}
ol.three{padding-left:22px;margin:8px 0 0}
.map{background:var(--card);border:2px solid var(--ink);padding:6px;margin-top:6px}
.map svg{display:block;width:100%;height:auto}
.map a text{font:700 13px 'Barlow Condensed';fill:var(--ink);text-transform:uppercase}
.map a:hover circle{fill:var(--ink)}
.legend{display:grid;grid-template-columns:1fr;margin-top:8px;border-top:2px solid var(--ink)}
.legend .li{display:flex;align-items:center;gap:10px;padding:8px 2px;border-bottom:1px solid var(--rule);color:var(--ink);text-decoration:none;font:700 17px 'Barlow Condensed';text-transform:uppercase}
.legend .n{display:inline-block;width:26px;height:26px;border-radius:50%;background:var(--red);color:#fff;text-align:center;line-height:26px;font-size:15px;flex:none}
.legend em{margin-left:auto;font:italic 14px 'Barlow';text-transform:none;color:var(--mut)}
.res{border-bottom:1px solid var(--rule);padding:10px 0}
.res .sc{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;font:700 18px/1.15 'Barlow Condensed';text-transform:uppercase}
.res .sc .w{color:var(--red)} .res .sc .pts{margin-left:auto;font-size:17px;font-variant-numeric:tabular-nums;white-space:nowrap}
.res p{margin:4px 0 0;font-size:15.5px}
.lg{border-radius:50%;border:2px solid var(--ink);object-fit:cover;background:#fff;flex:none}
table{width:100%;border-collapse:collapse;font-size:15px;font-variant-numeric:tabular-nums}
th{font:700 12px 'Barlow Condensed';letter-spacing:.1em;text-transform:uppercase;color:var(--mut);text-align:right;border-bottom:2px solid var(--ink);padding:4px 0}
th:first-child,td:first-child{text-align:left}
td{padding:6px 0;border-bottom:1px solid var(--rule);text-align:right}
.dv{font:700 13px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--red);margin:14px 0 2px}
.owe{font:700 10.5px 'Courier Prime';color:#fff;background:var(--red);padding:1px 5px;margin-left:6px;letter-spacing:.04em;white-space:nowrap}
.up{color:#1f7a3a} .dn{color:var(--red)}
.board{background:var(--ink);color:#fff;padding:14px 16px;margin-top:6px}
.board .row{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed rgba(255,255,255,.25);padding:7px 0;font-size:16px}
.board .row b{font:700 17px 'Barlow Condensed';text-transform:uppercase;letter-spacing:.04em;color:var(--gold)}
.board .row:last-child{border:0}
.pot{display:flex;height:26px;margin:10px 0 4px;border:2px solid #fff;font:700 13px/22px 'Barlow Condensed';text-transform:uppercase;text-align:center}
.pot .in{background:var(--gold);color:var(--ink)} .pot .out{background:repeating-linear-gradient(45deg,#fff 0 6px,#ddd 6px 12px);color:var(--ink)}
.tab{background:var(--card);border:2px solid var(--ink);padding:10px 14px;margin-top:10px;font-family:'Courier Prime',monospace;font-size:15px}
.tab .l{display:flex;justify-content:space-between;border-bottom:1px dotted var(--mut);padding:3px 0}
.stop .bar{font:700 13px 'Courier Prime';letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.vs{display:flex;align-items:center;gap:8px;margin:10px 0 8px}
.vs .t{flex:1;min-width:0;font:700 16px/1.12 'Barlow Condensed';text-transform:uppercase;overflow-wrap:anywhere}
.vs .t small{display:block;font:500 14px 'Barlow';text-transform:none;color:var(--mut)}
.vs .at{font:400 22px 'Anton';color:var(--red)}
.vs .t.r{text-align:right}
figure{margin:12px 0}
figure img{width:100%;height:auto;display:block;border:3px solid #fff;box-shadow:0 2px 0 var(--rule),0 0 0 1px var(--rule);transform:rotate(-.6deg)}
figcaption{font:italic 14px/1.35 'Barlow';color:var(--mut);margin-top:6px}
.h3{font:700 22px/1.15 'Barlow Condensed';text-transform:uppercase;margin:12px 0 6px}
.stake{border-left:5px solid var(--red);padding:2px 0 2px 12px;margin:12px 0}
.call{background:var(--card);border:3px solid var(--ink);box-shadow:5px 5px 0 var(--red);padding:12px 14px;margin:14px 0 6px}
.call .k{font:700 12px 'Courier Prime';letter-spacing:.16em;text-transform:uppercase;color:var(--red)}
.call .p{font:400 26px/1.05 'Anton';text-transform:uppercase;margin:4px 0}
.call p{margin:4px 0 0;font-size:15px}
.small{font-size:13.5px;color:var(--mut)}
.stopcard{background:var(--card);border:2px solid var(--ink);padding:14px 14px 6px;margin:14px 0}
.stopcard .sn{display:inline-block;background:var(--red);color:#fff;font:700 13px 'Barlow Condensed';letter-spacing:.14em;text-transform:uppercase;padding:3px 9px;transform:skew(-8deg)}
.stopcard h3{font:400 30px/1 'Anton';text-transform:uppercase;margin:8px 0 2px}
.stopcard .addr{font:700 12px 'Courier Prime';letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
.pick{font:700 17px 'Barlow Condensed';text-transform:uppercase;letter-spacing:.03em;margin:4px 0 14px}
.pick span{background:var(--red);color:#fff;padding:2px 7px;margin-right:6px;font-size:14px;letter-spacing:.1em}
.vs .t{font-size:20px!important}
.stamp{display:inline-block;border:2px solid var(--red);color:var(--red);font:700 12px 'Courier Prime';letter-spacing:.12em;text-transform:uppercase;padding:3px 8px;transform:rotate(-3deg);margin-left:6px}
.foot{background:var(--red);color:#fff;margin:30px -16px 0;padding:14px 16px;font:700 12px/1.5 'Barlow Condensed';letter-spacing:.14em;text-transform:uppercase;text-align:center}
"""

def nav():
    items = [('top', 'Top'), ('tour', 'Bar Tour'), ('results', 'Last week'), ('money', 'Specials'), ('door', 'The door')]
    items += [('games', 'This week')]
    return '<nav class="nav">' + ''.join(f'<a href="#{k}">{v}</a>' for k, v in items) + '</nav>'

def crawl_map():
    pts = [('s1', 'Red Shed', 'Craig v Ricer', 214, 186), ('s3', 'State Street Brats', 'Rusty v Frenches', 176, 248),
           ('s1', "La Bamba's", 'Craig v Ricer', 300, 118), ('terrace', 'Union Terrace', 'Last call', 52, 70)]
    o = ['<svg viewBox="0 0 400 380" role="img" aria-label="Crawl map">', '<rect width="400" height="380" fill="#fffaf0"/>',
         '<path d="M-10 60 C60 20 120 30 170 10" stroke="#9bb7c9" stroke-width="30" fill="none" opacity=".55"/>',
         '<text x="10" y="22" style="font:italic 14px Barlow;fill:#4f7488">Lake Mendota</text>',
         '<path d="M368 46 L120 300" stroke="#15121c" stroke-width="9" stroke-linecap="round"/>',
         '<text x="262" y="138" transform="rotate(-46 262 138)" style="font:700 13px Barlow Condensed;letter-spacing:.2em;fill:#6b6455">STATE ST</text>',
         '<path d="M0 352 L400 352" stroke="#15121c" stroke-width="6" opacity=".5"/>',
         '<text x="250" y="372" style="font:700 12px Barlow Condensed;letter-spacing:.2em;fill:#6b6455">UNIVERSITY AVE</text>',
         '<rect x="330" y="8" width="62" height="34" fill="#c5050c"/><text x="361" y="30" text-anchor="middle" style="font:700 13px Barlow Condensed;fill:#fff">CAPITOL</text>']
    for i, (a, name, game, x, y) in enumerate(pts, 1):
        o.append(f'<a href="#{a}"><circle cx="{x}" cy="{y}" r="15" fill="#c5050c" stroke="#fff" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 6}" text-anchor="middle" style="font:700 17px Barlow Condensed;fill:#fff">{i}</text></a>')
    o.append('</svg>')
    leg = ''.join(f'<a class="li" href="#{a}"><span class="n">{i}</span><span>{html.escape(name)}</span><em>{game}</em></a>'
                  for i, (a, name, game, x, y) in enumerate(pts, 1))
    return '<div class="map">' + ''.join(o) + f'</div><div class="legend">{leg}</div>'

def results():
    h = '<section id="results"><h2>Last week</h2><p class="dek">Week 9' + (', as it stood Sunday night. Monday night still to play.' if PROV else '.') + '</p>'
    for a, hh, (sa, sh) in W9:
        w = a if sa > sh else hh
        h += (f'<div class="res"><div class="sc">{lg(a, 34)}<span class="{"w" if w == a else ""}">{a}</span>'
              f'<span style="color:var(--mut)">at</span><span class="{"w" if w == hh else ""}">{hh}</span>{lg(hh, 34)}'
              f'<span class="pts">{sa:.1f} to {sh:.1f}</span></div><p>{RECAP[(a, hh)]}</p></div>')
    h += (f'<div class="call" style="box-shadow:5px 5px 0 var(--gold)"><div class="k">The bouncer\'s call, graded</div>'
          f'<div class="p">{hits9}-{5 - hits9} last week. {SEASON[0]}-{SEASON[1]} on the season.</div>'
          f'<p>Missed on Derek over Giff and Rusty over Ricer. Hit on Schwanz, Chad and Tom.</p></div></section>')
    return h

def money():
    winners = {}
    for wk, o, p in D.WK20: winners.setdefault(o, []).append(wk)
    tab = ''.join(f'<div class="l"><span>Wk {wk} &middot; {o}</span><span>{p:.1f} &middot; $20</span></div>' for wk, o, p in D.WK20)
    top = sorted(D.OWN, key=lambda o: -S[o]['pf'])[:3]
    return (f'<section id="money"><h2>The specials board</h2><p class="dek">Tonight\'s prizes, and who\'s drinking free.</p>'
            '<div class="board">'
            f'<div class="row"><span><b>Champion</b></span><span>$550</span></div>'
            f'<div class="row"><span><b>Runner-up</b></span><span>$450</span></div>'
            f'<div class="row"><span><b>Scoring title</b> $300</span><span>{top[0]} {S[top[0]]["pf"]:.1f}, {top[1]} {S[top[1]]["pf"]:.1f}</span></div>'
            f'<div class="row"><span><b>Right Division</b> $210</span><span>Ricer, {wl("Ricer")}</span></div>'
            f'<div class="row"><span><b>Left Division</b> $210</span><span>Schwanz, {wl("Schwanz")}, ahead of Giff on division record</span></div>'
            '<div class="pot"><div class="in" style="width:80%">In: $1,600</div><div class="out" style="width:20%">Out: $400</div></div>'
            '</div>'
            f'<div class="tab"><div style="font-weight:700;margin-bottom:4px">THE BAR TAB &middot; $20 a week for high score</div>{tab}</div>'
            f'<p class="small">Ricer, Schwanz, Derek and the Frenches have two each. Week 9 is Ricer\'s unless Monday night says otherwise.</p></section>')

def door():
    h = '<section id="door"><h2>The line at the door</h2><p class="dek">Records through Week 9, playoff odds from 20,000 simulations of the rest of the season, and the change since last week. Top three in each division get in.</p>'
    for name, div in (('Right Division', D.RIGHT), ('Left Division', D.LEFT)):
        rows = sorted(div, key=lambda o: (-S[o]['w'], -(S[o]['dw'] / max(1, S[o]['dw'] + S[o]['dl'])), -S[o]['pf']))
        h += f'<div class="dv">{name}</div><table><tr><th>Team</th><th>W-L</th><th>Div</th><th>Pts</th><th>Odds</th><th>+/-</th></tr>'
        for i, o in enumerate(rows):
            c = chg(o); cls = 'up' if c >= 1 else 'dn' if c <= -1 else ''
            owe = '<span class="owe">Owes $200</span>' if o in D.UNPAID else ''
            h += (f'<tr><td>{o}{owe}</td><td>{wl(o)}</td><td>{S[o]["dw"]}-{S[o]["dl"]}</td><td>{S[o]["pf"]:.0f}</td>'
                  f'<td><b>{pct(o)}</b></td><td class="{cls}">{c:+.0f}</td></tr>')
        h += '</table>'
    h += ('<p class="small">Trade deadline: the week the first team is mathematically eliminated. Nobody is yet; Abes, at 1-8, '
          'is still alive on paper.</p></section>')
    return h

def stop(s):
    a, h = s['pair']
    pa, ph = proj(a), proj(h); pick = a if pa > ph else h; other = h if pick == a else a
    pp, po = max(pa, ph), min(pa, ph)
    out = (f'<section class="stop" id="s{s["n"]}">' + (f'<div class="bar">{s["bar"]}</div>' if s.get('bar') else '') +
           f'<div class="vs">{lg(a)}<div class="t">{a}<small>{wl(a)} &middot; {pct(a)}</small></div>'
           f'<div class="at">at</div><div class="t r">{h}<small>{wl(h)} &middot; {pct(h)}</small></div>{lg(h)}</div>')
    if s.get('photo'):
        out += f'<figure><img src="{PH[s["photo"]]}" alt="" loading="lazy"><figcaption>{s["cap"]}</figcaption></figure>'
    out += (f'<p>{s["text"]}</p><p class="pick"><span>Pick</span> {pick} {pp:.0f}, {other} {po:.0f} &middot; {conf(pp - po).lower()}</p>'
            '<div class="rule" style="height:2px;background:var(--rule)"></div></section>')
    return out

def three():
    return ('<section><h2>Three things that changed</h2><ol class="three">'
            f'<li><b>Ricer took the Right.</b> Two straight wins, the week\'s high score, and a two-game lead at {wl("Ricer")}. Division odds: {pct("Ricer","div")}.</li>'
            f'<li><b>Chad got back in it.</b> Up 14 points to {pct("Chad")}, provided Abes doesn\'t find 75 on Monday night.</li>'
            f'<li><b>Rusty keeps scoring and losing.</b> Second in points, {wl("Rusty")}, down 16 to {pct("Rusty")}.</li>'
            '</ol></section>')

def terrace():
    return (f'<section id="terrace"><div class="bar" style="font:700 13px Courier Prime;letter-spacing:.14em;color:var(--red);text-transform:uppercase">Last call</div>'
            f'<h2>The Terrace</h2><p class="dek">The oasis. Same chairs, same lake, a few more years.</p>'
            f'<figure><img src="{PH["union_terrace_group"]}" alt="" loading="lazy"><figcaption>Union Terrace, more recently.</figcaption></figure>'
            '<p class="small">How the picks work: a projected score is 70% of a team\'s 2026 average plus 30% of the league average. '
            'Since 2005, a projected gap under 10 points has picked the winner 49% of the time; 10 to 20, 56%; over 20, 66%.</p>'
            '</section>')

TOUR = (
 '<section id="tour"><h2>The State Street Bar Tour</h2><p class="dek">No. 1. Two stops this week. The rest of the street isn\'t going anywhere.</p>'
 '<div class="stopcard"><div class="sn">Stop 1</div><h3>The Red Shed</h3><div class="addr">406 N. Frances, a block off State</div>'
 f'<figure><img src="{PH["red_shed_group"]}" alt="" loading="lazy"><figcaption>Back at the pool table, more recently.</figcaption></figure>'
 '<p>We played on the broken pool table and drank the Long Island Iced Teas, which came in mason jars and were potent enough that '
 'nobody remembers much else. Ricer was the biggest fan.</p>'
 '<p class="small">The Shed moved to State Street in 2024 and has since closed. This week: Ricer hosts Craig.</p></div>'
 '<div class="stopcard"><div class="sn">Stop 2</div><h3>State Street Brats</h3><div class="addr">603 State</div>'
 f'<figure><img src="{PH["rusty_moose_brats"]}" alt="" loading="lazy" style="transform:rotate(.7deg)"><figcaption>Rusty\'s 21st.</figcaption></figure>'
 '<p>At Brats, your birthday meant kissing the moose. On his 21st, Rusty did it properly: up on the bar, on his knees, both hands. '
 'There is, as you can see, documentation.</p>'
 '<p class="small">Still there. This week: Rusty visits the Frenches.</p></div></section>')
PICKNOTE = ('<p class="small" style="margin-top:14px">How the picks work: a projected score is 70% of a team\'s 2026 average plus 30% of the '
            'league average. Since 2005, a projected gap under 10 points has picked the winner 49% of the time; 10 to 20, 56%; over 20, 66%.</p>')
HTML = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>FFL Review, Week 10: The State Street Bar Tour, No. 1</title>'
        f'<style>{FONTS}{CSS}</style></head><body>{nav()}<div class="wrap">'
        '<header class="mast" id="top"><div class="k">Bullwinkle\'s Dance League &middot; Vol. 37</div>'
        '<h1><span>FFL</span>Review</h1><div class="sub">The State Street Bar Tour, No. 1 &middot; Week 10</div></header>'
        + ('<div class="prov">Sample. Week 9 as it stood Sunday night; Monday night is still to play, so scores, picks and odds will move.</div>' if PROV else '')
        + three() + TOUR
         + results() + money() + door()
        + '<section id="games"><h2>This week</h2><p class="dek">Week 10. Records, playoff odds, and the pick.</p></section>' + ''.join(stop(s) for s in STOPS) + PICKNOTE
        + '<div class="foot">Bullwinkle\'s Dance League &middot; FFL Review &middot; Week 10 &middot; Est. 1990, hand-delivered then, texted now</div>'
        + '</div></body></html>')
open('ffl_wk10.html', 'w').write(HTML)
print('ok', len(HTML) // 1024, 'KB; picks', hits9, SEASON)
