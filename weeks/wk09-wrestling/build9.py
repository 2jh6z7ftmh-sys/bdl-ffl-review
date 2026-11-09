"""FFL Review Week 9, Saturday Morning Wrestling edition. Run: python3 build9.py && python3 render9.py"""
import base64
from collections import Counter, defaultdict
from data9 import *
from hist import pair, res, G
from lineups8 import L8, optimal, actual, bench
from odds9 import ODDS, PREV, pct, sos, eliminated

def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()
FONTS = [('AN', 'anton-latin-400-normal', 400, 'normal'), ('OS', 'oswald-latin-500-normal', 500, 'normal'), ('OS', 'oswald-latin-700-normal', 700, 'normal'),
         ('BU', 'bungee-latin-400-normal', 400, 'normal'), ('CP', 'courier-prime-latin-700-normal', 700, 'normal'),
         ('BA', 'barlow-latin-400-normal', 400, 'normal'), ('BA', 'barlow-latin-400-italic', 400, 'italic'), ('BA', 'barlow-latin-600-normal', 600, 'normal'),
         ('BA', 'barlow-latin-700-normal', 700, 'normal'), ('BC', 'barlow-condensed-latin-700-normal', 700, 'normal'), ('BC', 'barlow-condensed-latin-800-normal', 800, 'normal')]
FF = ''.join(f"@font-face{{font-family:{n};src:url({b64('ff/'+f+'.woff2','font/woff2')}) format('woff2');font-weight:{w};font-style:{s}}}" for n, f, w, s in FONTS)
LG = {k: b64(f'img/{k}.jpg', 'image/jpeg') for k in OWN}
def logo(o, px=40): return f'<img class="lgo" src="{LG[o]}" style="width:{px}px;height:{px}px">'

S = season(8); S7 = season(7); NG = 8
LGAVG = sum(S[o]['pf'] for o in OWN) / (10.0 * NG)
def proj(o, s=S, ng=8):
    lg = sum(s[x]['pf'] for x in OWN) / (10.0 * ng)
    return .7 * s[o]['pf'] / ng + .3 * lg
def conf(g): return 'Coin flip' if g < 10 else ('56%' if g < 20 else '66%')
def wl(o): return f"{S[o]['w']}-{S[o]['l']}"
def streak(o):
    r = S[o]['res']; n = 0
    for x in reversed(r):
        if x == r[-1]: n += 1
        else: break
    return r[-1] + str(n)
SHORT = {'Ricer': 'Loungers', 'Derek': 'Ferries', 'Chad': 'Tribute Mr French', 'Rusty': 'Junkyard Dog', 'Tom': 'Tomcats',
         'Giff': 'Iguanas', 'Schwanz': 'Night Putters', 'Frenches': 'Legion of Doom', 'Abeln': 'Syndicate', 'Craig': 'House of Pain'}
GIM = {'Derek': 'Hulk Hogan', 'Giff': 'The Honky Tonk Man', 'Ricer': 'The Million Dollar Man', 'Rusty': 'The Junkyard Dog',
       'Frenches': 'The Road Warriors', 'Schwanz': 'Mr. Perfect', 'Abeln': 'The Ultimate Warrior', 'Chad': 'Macho Man Randy Savage',
       'Tom': 'The Undertaker', 'Craig': '"Mr. Wonderful" Paul Orndorff'}
f1 = lambda x: f'{x:.1f}'
sc = defaultdict(dict)
for wk, a, h, sa, sh in GAMES: sc[wk][a] = sa; sc[wk][h] = sh
sc8 = sc[8]

AP = {o: [0, 0] for o in OWN}
for wk in range(1, 9):
    for o in OWN:
        for x in OWN:
            if x != o:
                if S[o]['weeks'][wk] > S[x]['weeks'][wk]: AP[o][0] += 1
                elif S[o]['weeks'][wk] < S[x]['weeks'][wk]: AP[o][1] += 1
EFF = {o: (actual(L8[o]), optimal(L8[o])[0]) for o in OWN}
WON = Counter(o for _, o, _ in WK20)
SOS = sos(8)
PICKS8 = [('Derek', 'Ricer', 'Derek'), ('Giff', 'Tom', 'Tom'), ('Schwanz', 'Abeln', 'Schwanz'), ('Frenches', 'Craig', 'Frenches'), ('Rusty', 'Chad', 'Rusty')]
SEASON_BEFORE = (16, 9)
rec8 = []
for a, h, p in PICKS8:
    other = h if p == a else a
    win = a if sc8[a] > sc8[h] else h
    rec8.append((p, other, proj(p, S7, 7), proj(other, S7, 7), win == p, win, abs(sc8[a] - sc8[h])))
wk8w = sum(r[4] for r in rec8)
SEASON = (SEASON_BEFORE[0] + wk8w, SEASON_BEFORE[1] + 5 - wk8w)
PAID_IN = 200 * (10 - len(UNPAID)); OUT = 200 * len(UNPAID)
ch = lambda o, k='po': (ODDS[o][k] - PREV[o][k]) * 100
ELIM = eliminated(8)

CSS = """@@FF@@
:root{--ink:#121218;--gold:#d4a017;--goldd:#a87c0c;--red:#c8102e;--redd:#8f0b21;--blue:#1b3a8c;--paper:#f3efe6;--card:#fbf8f1;--mut:#5f5a52;--rule:#cfc6b4;--silver:#c9ccd1}
*{box-sizing:border-box} html,body{margin:0;padding:0;background:var(--paper)}
.page{width:984px;height:1268px;background:var(--paper);color:var(--ink);font-family:BA;font-size:14.6px;line-height:1.42;padding:24px 40px 0;position:relative;display:flex;flex-direction:column;overflow:hidden;page-break-after:always}
.strip{height:9px;background:linear-gradient(90deg,var(--red) 0 33%,var(--gold) 33% 66%,var(--blue) 66%);margin:8px 0 10px}
.chy{font-family:CP;font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--red)}
.wm{font-family:AN;font-size:112px;line-height:.86;letter-spacing:1px;color:var(--ink);text-transform:uppercase}
.wm span{color:var(--gold);-webkit-text-stroke:2px var(--ink)}
.sub{font-family:BU;font-size:21px;color:var(--blue);letter-spacing:.02em}
.h{font-family:AN;font-size:30px;line-height:1.02;margin:0;text-transform:uppercase;letter-spacing:.5px}
.h span.g{color:var(--red)}
.h2{font-family:OS;font-weight:700;font-size:19px;line-height:1.15;margin:0;text-transform:uppercase}
.hs{font-family:BA;font-style:italic;font-size:13.2px;color:var(--mut);margin:2px 0 6px}
.row{display:flex} .c1{flex:1.25;margin-right:26px} .c2{flex:1} .ch{flex:1} .ch+.ch{margin-left:24px}
.note{font-size:13.8px;line-height:1.42;margin:5px 0 0} .note b{font-weight:700}
.lgo{border-radius:50%;border:2px solid var(--ink);object-fit:cover;vertical-align:middle;background:#fff}
table.st{width:100%;border-collapse:collapse;font-size:13.6px}
table.st td{padding:2.4px 0;border-bottom:1px solid var(--rule);font-variant-numeric:tabular-nums}
table.st td.n{text-align:right;width:52px} table.st td.tn{white-space:nowrap}
.sth td{font-family:OS;font-weight:700;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--blue);border-bottom:2px solid var(--ink)!important}
.owe{font-family:CP;font-weight:700;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--red);padding:1px 5px;margin-left:7px;vertical-align:1px}
.ln{display:flex;align-items:baseline;font-size:14px;margin:2px 0} .ln .d{flex:1;border-bottom:2px dotted var(--rule);margin:0 6px;transform:translateY(-4px)}
.bg{display:flex;align-items:center;font-size:13px;margin:2px 0} .bn{width:76px} .bb{flex:1;height:11px;background:rgba(27,58,140,.12);margin:0 8px;position:relative}
.bb span{display:block;height:100%;background:var(--blue)} .bv{width:52px;text-align:right;font-variant-numeric:tabular-nums}
.foot{margin-top:auto;margin-left:-40px;margin-right:-40px;background:var(--ink);color:var(--gold);font-family:OS;font-weight:700;font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;text-align:center;padding:10px 0}
.sp{flex:1}
.ph{display:flex;align-items:flex-end;justify-content:space-between;margin-top:6px}
.phw{font-family:AN;font-size:46px;line-height:1;text-transform:uppercase} .pht{font-family:BU;font-size:17px;color:var(--blue)}
.divh{font-family:OS;font-weight:700;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--red);margin:6px 0 3px}
.tag{display:inline-block;font-family:OS;font-weight:700;font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;margin-right:6px}
.t-w{background:var(--ink);color:var(--gold)} .t-l{background:var(--silver);color:var(--ink)}
.rc{margin:0 0 10px} .rc .sc{font-family:OS;font-weight:700;font-size:17px;text-transform:uppercase}
.big{font-family:AN;font-size:70px;line-height:.9;color:var(--red)}
.quote{font-family:OS;font-weight:700;font-size:21px;line-height:1.2;color:var(--blue);border-left:6px solid var(--gold);padding:2px 0 2px 14px;margin:9px 0;text-transform:uppercase}
.chip{display:inline-block;width:27px;height:27px;line-height:27px;text-align:center;font-family:OS;font-weight:700;font-size:13px;color:#fff;margin-right:4px}
.mg{display:flex;align-items:center;font-size:12.5px;margin:3px 0} .mg .y{width:86px} .mg .bar{flex:1;display:flex;height:13px}
.mg .l,.mg .r{flex:1;display:flex} .mg .l{justify-content:flex-end;border-right:2px solid var(--ink)} .mg .v{width:48px;text-align:right}
.tl{font-size:13px;margin:0 0 6px;padding-left:12px;border-left:3px solid var(--gold)} .tl b{font-family:OS;font-weight:700;color:var(--blue)}
/* match card header */
.mc{background:var(--ink);color:#fff;padding:10px 14px 12px;margin-top:4px;border-bottom:6px solid var(--gold)}
.mc .lab{font-family:CP;font-weight:700;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
.mc .t{font-family:AN;font-size:30px;line-height:1.05;text-transform:uppercase;letter-spacing:.4px}
.mc .g{font-family:BU;font-size:15px;color:var(--gold);margin-top:3px}
.vs{font-family:BU;font-size:26px;color:var(--red);margin:0 10px}
.pred{background:var(--card);border:3px solid var(--ink);box-shadow:6px 6px 0 var(--gold);padding:10px 16px}
.card{background:var(--card);border:2px solid var(--ink);padding:10px 14px}
.belt{background:linear-gradient(180deg,#2a2a33,#121218);color:#fff;border-radius:44px;padding:10px 26px;display:flex;align-items:center;border:3px solid var(--goldd);margin-bottom:8px}
.belt .plate{background:radial-gradient(circle at 40% 35%,#f6dd8a,var(--gold) 55%,var(--goldd));color:var(--ink);border-radius:50%;width:86px;height:86px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:AN;font-size:22px;line-height:1;border:3px solid #fff3c4;flex:none}
.belt .plate small{font-family:OS;font-weight:700;font-size:10px;letter-spacing:.1em}
.belt .bt{margin-left:16px;flex:1} .belt .bt b{font-family:OS;font-weight:700;font-size:17px;text-transform:uppercase;color:var(--gold)}
.pot{display:flex;height:24px;border:2px solid var(--ink);margin:8px 0 4px;background:#fff}
.pot span{display:flex;align-items:center;justify-content:center;font-family:OS;font-weight:700;font-size:12px}
.card9{display:flex;align-items:center;padding:7px 0;border-bottom:1px solid var(--rule)}
.card9 .w{flex:1;font-size:13.5px;line-height:1.3} .card9 .w b{font-family:OS;font-weight:700;font-size:15px;text-transform:uppercase}
.card9 .p{width:132px;text-align:right;font-family:OS;font-weight:700;font-size:13px}
.me{font-family:CP;font-weight:700;font-size:11px;letter-spacing:.12em;color:#fff;background:var(--red);padding:1px 6px;margin-right:6px}
.vault{background:var(--ink);color:#f3efe6;padding:10px 14px;border-left:8px solid var(--red)}
.vault .h2{color:var(--gold)}
"""
CSS = CSS.replace('@@FF@@', FF)

def page(body, foot='Saturday morning, 11 a.m., right after the cartoons'):
    return f'<div class="page">{body}<div class="foot">Bullwinkle&rsquo;s Dance League &middot; FFL Review &middot; Week 9 &middot; {foot}</div></div>'
def header(title, sub, label='Saturday Morning Wrestling'):
    return f'''<div class="chy" style="margin-top:2px">FFL Review &middot; {label} &middot; Week 9</div>
<div class="ph"><div class="phw">{title}</div><div class="pht">{sub}</div></div><div class="strip"></div>'''

# ================================================================= PAGE 1: cover / the card
ORDER = {'Right': ['Ricer', 'Derek', 'Chad', 'Rusty', 'Tom'], 'Left': ['Schwanz', 'Giff', 'Frenches', 'Craig', 'Abeln']}
def standings(title):
    out = f'<div class="divh">{title} Division</div><table class="st"><tr class="sth"><td></td><td class="n">W-L</td><td class="n">Div</td><td class="n" style="width:62px">Pts</td><td class="n">Run</td></tr>'
    for t in ORDER[title]:
        tag = '<span class="owe">Owes $200</span>' if t in UNPAID else ''
        out += f'<tr><td class="tn">{SHORT[t]}{tag}</td><td class="n">{wl(t)}</td><td class="n">{S[t]["dw"]}-{S[t]["dl"]}</td><td class="n" style="width:62px">{f1(S[t]["pf"])}</td><td class="n">{streak(t)}</td></tr>'
    return out + '</table>'

CARD = [('Ricer', 'Rusty', True), ('Derek', 'Giff', False), ('Chad', 'Abeln', False), ('Frenches', 'Schwanz', False), ('Tom', 'Craig', False)]
def cardline(a, h, main):
    pa, ph = proj(a), proj(h); p = a if pa > ph else h
    return (f'<div class="card9">{logo(a,34)}<span style="margin:0 6px">{logo(h,34)}</span><div class="w">{"<span class=me>Main event</span>" if main else ""}'
            f'<b>{GIM[a]}</b> ({a}, {wl(a)}) vs <b>{GIM[h]}</b> ({h}, {wl(h)})</div>'
            f'<div class="p">{SHORT[p]} {max(pa,ph):.0f}-{min(pa,ph):.0f}<br><span style="font-family:BA;font-weight:400;color:var(--mut)">{conf(abs(pa-ph))}</span></div></div>')
CARDHTML = ''.join(cardline(a, h, m) for a, h, m in CARD)

THREE = f'''<div class="card" style="margin-bottom:10px"><div class="divh" style="margin-top:0">The belt changed hands</div>
<p class="h2">Ricer swept Derek and took first place.</p>
<p class="note" style="margin-top:3px">Loungers {f1(sc8["Ricer"])}, Ferries {f1(sc8["Derek"])}. Ricerbabe has now beaten the 6 Time Champ in Week 4 and Week 8, owns the tiebreaker, and leads the Right by a game. His division odds went from {pct(PREV["Ricer"]["div"])} to {pct(ODDS["Ricer"]["div"])}. Derek&rsquo;s went the other way.</p></div>
<div class="card" style="margin-bottom:10px"><div class="divh" style="margin-top:0">Count-out of the week</div>
<p class="h2">Rusty left 103.7 on the bench and lost by 15.8.</p>
<p class="note" style="margin-top:3px">Mahomes and Hubbard sat; Egbuka started and scored 0.0. The Dog has the league&rsquo;s second-best all-play record and is 3-5.</p></div>
<div class="card"><div class="divh" style="margin-top:0">The twenty</div>
<p class="h2">Legion of Doom, {f1(sc8["Frenches"])}.</p>
<p class="note" style="margin-top:3px">The week&rsquo;s high score, a perfect 4-0 in the division, and their second twenty of the year.</p></div>'''

P1 = page(f'''<div class="row" style="align-items:flex-end">
<div style="flex:1"><div class="chy">Bullwinkle&rsquo;s Dance League &middot; Est. 1990 &middot; Live from the basement TV</div>
<div class="wm" style="margin-top:8px">FFL <span>Review</span></div>
<div class="sub" style="margin-top:6px">Saturday Morning Wrestling &middot; Week 9 &middot; November 3 to 9, 2026</div></div></div>
<div class="strip"></div>
<p class="h">This week&rsquo;s <span class="g">card</span></p><p class="hs">Five matches, each with the projected score and how sure we are. Full previews inside.</p>
{CARDHTML}
<div class="row" style="margin-top:14px"><div class="c1">
<p class="h">Last week</p><p class="hs">Week 8, in three replays.</p>
{THREE}
</div><div class="c2">
<p class="h">The rankings</p><p class="hs">After Week 8. Top three in each division make the playoffs; first gets a bye.</p>
{standings("Right")}{standings("Left")}
<p class="note" style="font-size:13px"><b>Trade deadline:</b> the week the first team is mathematically eliminated. Abes is 1-7 and still alive on paper, so the earliest it can come is after Week 10. Plenty of time to overpay for a kicker.</p>
</div></div>
<div class="strip" style="margin-top:12px;height:5px"></div>
<p class="h" style="font-size:24px">Mean Gene&rsquo;s notebook</p>
<div class="row"><div class="ch"><p class="note"><b>The money game.</b> Derek took game one from Chad in Week 7. Game two is Week 13. Gunner can&rsquo;t sweep; Derek still can.</p></div>
<div class="ch"><p class="note"><b>The camel clutch.</b> Abes has lost seven straight. He has finished last in his division seven times, and three of the following seasons ended in a title game.</p></div>
<div class="ch"><p class="note"><b>Five for eight.</b> Five different teams have won the weekly twenty in eight weeks. Rusty, second in points, is still waiting.</p></div></div>
<div class="sp"></div>''')

# ================================================================= PAGE 2: results
REC8 = [
 ('Ricer', 'Derek', 'Pinned',
  'The Million Dollar Man finally started Burrow, and Burrow threw five touchdown passes for 39.4. Golden 20.9, Brown 16.1. Ricer then benched Waddle, his $26 pickup, after starting him for 8.8 last week. Waddle scored 14.9. Everybody&rsquo;s got a price; nobody said it was a good one. '
  'The Hulkster started four zeros: Cooper, Godwin, Reichard and the Colts. Kincaid (18.6), Rice (18.3) and Gainwell (14.0) watched from the bench. The best lineup on the Ferries roster was 130.8, which beats Ricer. No crooked referee required.'),
 ('Giff', 'Tom', 'Count-out',
  'Giff started Lamar Jackson at quarterback and got 0.0. He won anyway. Pollard 30.7, Michael Wilson 26.8, McBride 20.2, and Tyler Bass, a $0 kicker signed Saturday, for 16.0. That is the Honky Tonk Man&rsquo;s whole career in one week. '
  'The Undertaker got 37.5 from Higgins and left James Cook (18.1) on the bench behind Javonte Williams (6.7). That one swap wins it, 128.8 to 122.4. Darnold (18.5) also outscored Daniels (14.9) from the pine.'),
 ('Schwanz', 'Abeln', 'Pinned',
  'Mr. Perfect started Malik Willis, a waiver pickup, with Stroud&rsquo;s 0.0 on the bench, and got 14.6. Tuten 29.9, Gibbs 24.8, Kraft 17.3. Fifth straight win, and first place in the Left on the Week 5 tiebreaker over Giff. '
  'Abes got Josh Allen back (26.5) and 17.0 from the Steelers, and Zay Flowers gave him 0.0. His 80.0 was the low score of the week. Seven straight losses. The camel clutch holds.'),
 ('Frenches', 'Craig', 'Pinned',
  'The week&rsquo;s high and the twenty. Chase 31.1, Swift 27.9, Lawrence 19.4, Jefferson 14.3. Trey Allgeier scored 38.1 on the bench, the best bench score in the league, and it didn&rsquo;t matter. The Legion is 4-0 in the division. '
  'Mr. Wonderful started Tre Tucker in the flex for 0.0, got 1.0 from his kicker, and left 64.5 on the bench: Flournoy, Sampson, Bryce Young, Coker. Fannin (23.4) was the bright spot.'),
 ('Chad', 'Rusty', 'Pinned',
  'Maye 26.4, Nacua 25.0, Burden 18.6, Aubrey 12.0. Hunter Henry, the $3 tight end, gave Chad 6.0, which is 4.3 more than last week&rsquo;s tight end. He is 4-4 and third in the Right. '
  'The Dog left 103.7 on the bench, the most in the league this week. Mahomes (27.4) sat behind Love (21.5), and Hubbard (24.9) sat while Egbuka started for 0.0. Hubbard for Egbuka wins it, 134.7 to 125.6. His 109.8 was his lowest score of the season.'),
]
recaps = ''
for w, l, verdict, tx in REC8:
    recaps += f'''<div class="rc"><div class="row" style="align-items:center">{logo(w,30)}<span class="sc" style="margin-left:8px">{SHORT[w]} {f1(sc8[w])}, {SHORT[l]} {f1(sc8[l])}</span></div>
<div style="margin:3px 0 2px"><span class="tag t-w">{GIM[w]}</span><span class="tag t-l">{verdict}: {GIM[l]}</span></div>
<div class="note" style="margin:0">{tx}</div></div>'''

rec_rows = '<table class="st"><tr class="sth"><td>Pick</td><td class="n" style="width:62px">Proj.</td><td style="text-align:right">Result</td><td class="n" style="width:22px"></td></tr>'
for p, other, pp, po_, ok, win, mg in rec8:
    rec_rows += (f'<tr><td>{SHORT[p]}</td><td class="n" style="width:62px">{pp:.0f}-{po_:.0f}</td><td style="text-align:right">{SHORT[win]} by {mg:.1f}</td>'
                 f'<td class="n" style="width:22px;font-weight:700;color:{"var(--blue)" if ok else "var(--red)"}">{"W" if ok else "L"}</td></tr>')
rec_rows += '</table>'
eff_rows = ''
for o in sorted(OWN, key=lambda o: -(EFF[o][0] / EFF[o][1])):
    a_, op = EFF[o]
    eff_rows += f'<tr><td class="tn">{o}</td><td class="n">{f1(a_)}</td><td class="n">{f1(op)}</td><td class="n">{f1(op-a_)}</td><td class="n">{a_/op*100:.0f}%</td></tr>'

luck = ''
for o in sorted(OWN, key=lambda o: -AP[o][0]):
    w = S[o]['w']
    luck += f'<div class="bg"><span class="bn">{o}</span><span class="bb"><span style="width:{AP[o][0]/72*100:.0f}%"></span><i style="position:absolute;left:{w/8*100:.0f}%;top:-4px;width:4px;height:19px;background:var(--red)"></i></span><span class="bv">{AP[o][0]}-{AP[o][1]}</span></div>'
P2 = page(header('Last week&rsquo;s card', 'Week 8 results') + f'''
<div class="row"><div class="c1">
<p class="h">The replays</p><p class="hs">All five Week 8 matches, winner first.</p>
{recaps}
</div><div class="c2">
<p class="h">Receipts</p><p class="hs">The Week 8 picks, projected scores as printed.</p>
{rec_rows}
<p class="note">{wk8w}-3 for the week, {SEASON[0]}-{SEASON[1]} for the season. Bobby Heenan, for the defense: &ldquo;Derek had the better roster. He just didn&rsquo;t play it.&rdquo; Gorilla Monsoon: &ldquo;Will you stop.&rdquo;</p>
<p class="note">Trade Desk: we said Chad needed a tight end and Giff could spare Ferguson. Giff cut Ferguson, and Chad bought Hunter Henry for $3.</p>
<p class="h" style="margin-top:14px">The lineup tax</p><p class="hs">Week 8 starters against the best legal lineup from the same roster. Hindsight, not homework.</p>
<table class="st"><tr class="sth"><td></td><td class="n">Actual</td><td class="n">Best</td><td class="n">Left</td><td class="n">Kept</td></tr>{eff_rows}</table>
<p class="h" style="margin-top:12px;font-size:24px">All-play</p><p class="hs" style="margin-bottom:2px">Record against all nine teams every week; the red mark is real wins.</p>
{luck}
<p class="note"><b>Two games turned on it.</b> Derek&rsquo;s best lineup (130.8) beats Ricer. Rusty&rsquo;s (152.1) beats Chad. Tom needed one swap. Chad kept 95% of his best and won.</p>
</div></div>''')

# ================================================================= PAGE 3: belts, money, odds
bar_tbl = '<table class="st"><tr class="sth"><td style="width:34px">Wk</td><td>Winner</td><td class="n" style="width:56px">Pts</td><td class="n" style="width:92px">Rusty</td></tr>'
for wk, o, p in WK20:
    srt = sorted(sc[wk].items(), key=lambda x: -x[1]); rank = [k for k, v in srt].index('Rusty') + 1
    sfx = {1: 'st', 2: 'nd', 3: 'rd'}.get(rank, 'th')
    bar_tbl += f'<tr><td>{wk}</td><td class="tn">{o}</td><td class="n" style="width:56px">{f1(p)}</td><td class="n" style="width:92px">{f1(sc[wk]["Rusty"])} <i style="color:var(--mut)">{rank}{sfx}</i></td></tr>'
bar_tbl += '</table>'
tabs = ' &middot; '.join(f'{t} ${WON[t]*20}' for t in sorted(OWN, key=lambda t: (-WON[t], t)) if WON[t])
dry = ', '.join(t for t in sorted(OWN) if not WON[t])
od_rows = ''
for o in sorted(OWN, key=lambda o: -ODDS[o]['po']):
    r = ODDS[o]; c = ch(o)
    cs = f'{c:+.0f}' if abs(c) >= 0.5 else '0'
    od_rows += (f'<tr><td class="tn">{SHORT[o]}</td><td class="n" style="width:46px">{wl(o)}</td><td class="n" style="width:66px;font-weight:700">{pct(r["po"])}</td><td class="n" style="width:46px">{cs}</td>'
                f'<td class="n" style="width:66px">{pct(r["div"])}</td><td class="n" style="width:52px">{pct(r["st"])}</td><td class="n" style="width:78px">{pct(r["po_w"])}</td><td class="n" style="width:78px">{pct(r["po_l"])}</td></tr>')

BELTS = f'''<div class="belt"><div class="plate">$300<small>SCORING</small></div><div class="bt"><b>Season scoring title</b><br>Schwanz {f1(S["Schwanz"]["pf"])} &middot; Rusty {f1(S["Rusty"]["pf"])} &middot; Frenches {f1(S["Frenches"]["pf"])}</div></div>
<div class="belt"><div class="plate">$210<small>RIGHT</small></div><div class="bt"><b>Right Division</b><br>Ricer, 6-2, with the tiebreaker over Derek</div></div>
<div class="belt"><div class="plate">$210<small>LEFT</small></div><div class="bt"><b>Left Division</b><br>Schwanz, 6-2, on the Week 5 tiebreaker over Giff</div></div>
<table class="st" style="margin-top:4px"><tr class="sth"><td>Title belt</td><td class="n" style="width:56px">Pays</td><td style="text-align:right">Decided</td></tr>
<tr><td>Champion</td><td class="n">$550</td><td style="text-align:right">Week 17</td></tr>
<tr><td>Runner-up</td><td class="n">$450</td><td style="text-align:right">Week 17</td></tr>
<tr><td>Weekly high, Weeks 1-14</td><td class="n">$20</td><td style="text-align:right">${len(WK20)*20} paid out, ${(14-len(WK20))*20} left</td></tr></table>
<div class="pot"><span style="width:{PAID_IN/2000*100:.0f}%;background:var(--gold);border-right:2px solid var(--ink)">In: ${PAID_IN:,}</span><span style="flex:1;background:repeating-linear-gradient(45deg,#fff 0 6px,#eee6d4 6px 12px)">Still out: ${OUT}</span></div>
<p class="note" style="font-size:12.8px">Prizes are paid from the ${PAID_IN:,} that has arrived.</p>'''

P3 = page(header('The belts', 'Money, odds and luck') + f'''
<div class="row"><div class="c1">
<p class="h">Title belts</p><p class="hs">Every prize this season and who would carry it to the ring today.</p>
{BELTS}
</div><div class="c2">
<p class="h">The weekly twenty</p><p class="hs">The $20 for the week&rsquo;s high score, with Rusty&rsquo;s score and finish beside it.</p>
{bar_tbl}
<p class="note"><b>Tabs:</b> {tabs}. <b>Nothing yet:</b> {dry}.</p>
<p class="note">Eight weeks, five different winners. Rusty has the second-most points in the league and has finished in the top three five times without collecting.</p>
</div></div>
<div class="strip" style="margin-top:12px"></div>
<p class="h">Who&rsquo;s still in the title picture</p><p class="hs">Playoff odds after Week 8: 20,000 simulations of Weeks 9 to 14. Change is against the odds printed in the Week 8 issue.</p>
<table class="st"><tr class="sth"><td></td><td class="n" style="width:46px">W-L</td><td class="n" style="width:66px">Playoffs</td><td class="n" style="width:46px">Chg</td><td class="n" style="width:66px">Division</td><td class="n" style="width:52px">$300</td><td class="n" style="width:78px">If win</td><td class="n" style="width:78px">If lose</td></tr>{od_rows}</table>
<div class="row" style="margin-top:6px"><div class="ch">
<p class="note"><b>Biggest moves.</b> Chad up {ch("Chad"):.0f} points to {pct(ODDS["Chad"]["po"])}. Rusty down {abs(ch("Rusty")):.0f} to {pct(ODDS["Rusty"]["po"])}. Ricer&rsquo;s division odds up {ch("Ricer","div"):.0f}; Derek&rsquo;s down {abs(ch("Derek","div")):.0f}.</p>
<p class="note"><b>The Dog&rsquo;s match.</b> Rusty goes to {pct(ODDS["Rusty"]["po_w"])} with a win over Ricer and {pct(ODDS["Rusty"]["po_l"])} with a loss. No game this week swings one team more.</p>
</div><div class="ch">
<p class="note"><b>Nobody is out.</b> Abeln (1-7) can still reach seven wins, and the Left&rsquo;s top three can&rsquo;t all pass that this week, because Schwanz and the Legion play each other. The trade deadline can&rsquo;t arrive before Week 10 results.</p>
</div></div>
<p class="note" style="font-size:12.4px;color:var(--mut)">How it works: each team&rsquo;s expected score is 70% its own average and 30% the league average ({f1(LGAVG)}), with random week-to-week and team-strength swings. Ties broken by record, division record and points. Picks use the same projection; confidence comes from 1,105 games since 2005: a gap under 10 points has gone to the favorite 49% of the time, 10 to 20 points 56%, over 20 points 66%.</p>''')

# ================================================================= matchup pages
po_rec = defaultdict(lambda: [0, 0]); titles = defaultdict(int)
for g in G:
    if g['t'].startswith('po'):
        w, l = (g['a'], g['b']) if g['sa'] > g['sb'] else (g['b'], g['a'])
        po_rec[w][0] += 1; po_rec[l][1] += 1
        if 'Final' in g['t']: titles[w] += 1
def series(A, B):
    P = [d for d in pair(A, B) if not (d['y'] == 2026 and d['w'] >= 9)]
    return P, sum(res(d) == 'W' for d in P), sum(res(d) == 'L' for d in P), sum(res(d) == 'T' for d in P)
COL = {'Derek': '#c8102e', 'Ricer': '#1b3a8c', 'Giff': '#2f7d4f', 'Tom': '#121218', 'Schwanz': '#5a3d86', 'Abeln': '#b5651d',
       'Frenches': '#6b6b6b', 'Craig': '#8f0b21', 'Rusty': '#a87c0c', 'Chad': '#0b6e7a'}

M = {
 ('Derek', 'Giff'): dict(no=2, since='1993',
   chip='Derek won four straight before Giff took Week 1 this year.',
   head='The Hulkster against the longest reign in the business',
   para=('Giff leads 18-17-1 in 36 meetings since 1993, almost all of it built in the 2000s, when he went 8-1-1. Derek has had the better of everything else: 5-3 in the 1990s, 6-4 in the 2010s, 5-3 in the 2020s. '
         'They have never met in the playoffs. Derek&rsquo;s biggest win was 145.94-76.54 in 2024. Giff won the first meeting of this season, 132.5-123.9. '
         'The Honky Tonk Man held the Intercontinental title for over a year without winning many matches clean. Giff is 6-2 with the third-fewest points in the league and started a quarterback who scored 0.0 last week. It is a cross-division match, and Derek needs it more.'),
   call='8-1-1. Giff against Derek from 2000 to 2009.',
   mile=[('1993', 'First meeting, Giff 23-10'), ('2001', 'Giff by two, 48-46, the closest'), ('2024', 'Derek 145.94-76.54'), ('2026', 'Week 1, Giff 132.5-123.9')],
   lastA=('Derek&rsquo;s Week 8', 'Lost to Ricer, 126.9-91.4. Started four zeros: Cooper, Godwin, Reichard and the Colts. Smith-Njigba 24.8, Warren 21.3. Kincaid (18.6) and Rice (18.3) sat. McCaffrey had the week off.'),
   lastB=('Giff&rsquo;s Week 8', 'Beat Tom, 122.4-117.4, with Lamar Jackson scoring 0.0 at quarterback. Pollard 30.7, Michael Wilson 26.8, McBride 20.2, Bass 16.0. Coleman, a $10 pickup, scored 20.4 on the bench.'),
   read='Derek averages {} to Giff&rsquo;s {}, and is {} in all-play to Giff&rsquo;s {}. Giff keeps winning anyway, which is the whole gimmick.',
   pick='Derek', case='The projection has the Ferries by {gap}, a coin flip. Derek scores {ppg} more a game and gets McCaffrey back from the bye. Hogan bodyslammed Andr&eacute; in front of 93,000 people; this one needs to be less dramatic than that.',
   wrong='Giff is 6-2 for a reason nobody can explain, and Derek just left 39.4 points on his bench. If Giff finds a quarterback who scores more than zero, the Iguanas are a real team.'),
}
M[('Frenches', 'Schwanz')] = dict(no=4, since='2009',
   chip='Schwanz won four straight before the Legion took Week 3 this year, 158.2-123.1.',
   head='First place in the Left, and the Legion is undefeated in the division',
   para=('Schwanz leads 20-19 in 39 meetings since 2009. The Legion took the 2000s and the 2020s; Schwanz took the 2010s, 14-10. '
         'In the playoffs, Mr. Perfect is 3-1, including a 94-41 semifinal in 2014 and a 118-88 semifinal in 2018 on the way to a title game. The Legion&rsquo;s one playoff win was a 94-88 semifinal in 2017. '
         'It is a Left Division match: Schwanz is 6-2 with the most points in the league, the Legion is 5-3 and 4-0 in the division. Week 3 went to the Legion by 35.1.'),
   call='3-1. Schwanz against the Legion in the playoffs.',
   mile=[('2009', 'First meeting, Legion 51-43'), ('2014', 'Semifinal, Schwanz 94-41'), ('2017', 'Semifinal, Legion 94-88'), ('2026', 'Week 3, Legion 158.2-123.1')],
   lastA=('The Legion&rsquo;s Week 8', 'Beat Craig, 133.6-90.4, for the week&rsquo;s high and the $20. Chase 31.1, Swift 27.9, Lawrence 19.4. Allgeier scored 38.1 on the bench.'),
   lastB=('Schwanz&rsquo;s Week 8', 'Beat Abeln, 112.2-80.0, his fifth straight. Tuten 29.9, Gibbs 24.8, Kraft 17.3. Started Malik Willis (14.6) with Stroud at 0.0. Myers scored -1.0.'),
   read='The Legion averages {} to Schwanz&rsquo;s {}, and is {} in all-play to Schwanz&rsquo;s {}. These are two of the three best teams in the league by any measure, and both are near locks for the playoffs. This one is about the bye.',
   pick='Schwanz', case='The projection has the Night Putters by {gap}, a coin flip. Schwanz scores {ppg} more a game and is 3-1 against the Legion when it counts.',
   wrong='The Legion beat him by 35.1 in Week 3 and has the league&rsquo;s deepest bench. Mr. Perfect had a perfect record in the vignettes, not always in the ring.')
M[('Chad', 'Abeln')] = dict(no=3, since='1995',
   chip='Chad won the 2023 title game and the most recent meeting, Week 14 last year.',
   head='Savage against the Warrior, with a career on the line',
   para=('Abeln leads 20-19 in 39 meetings since 1995, close in every decade. They have met twice in the playoffs, both in title games: Abeln won the 1997 final, and Chad won the 2023 final, 142.66-77.08, the widest margin in the series. '
         'In 1991 the Ultimate Warrior beat Macho Man in a match where the loser had to retire. Chad is the reigning champion and 4-4; Abes is 1-7 and needs to win nearly everything that is left. '
         'It is a cross-division match. They have not met yet this season.'),
   call='142.66-77.08. Chad over Abeln for the 2023 title.',
   mile=[('1995', 'First meeting, Abeln 40-20'), ('1997', 'Title game, Abeln'), ('2023', 'Title game, Chad 142.66-77.08'), ('2026', 'Meeting No. 40')],
   lastA=('Chad&rsquo;s Week 8', 'Beat Rusty, 125.6-109.8. Maye 26.4, Nacua 25.0, Burden 18.6, Aubrey 12.0. Hunter Henry, the $3 tight end, scored 6.0. Bo Nix sat for 18.2.'),
   lastB=('Abeln&rsquo;s Week 8', 'Lost to Schwanz, 112.2-80.0, the low score of the week. Josh Allen 26.5, Steelers 17.0, Zay Flowers 0.0. Freiermuth scored 11.6 on the bench. Seven straight losses.'),
   read='Chad averages {} to Abeln&rsquo;s {}, and is {} in all-play to Abeln&rsquo;s {}. Abes has finished last in his division seven times. Three of the following seasons ended in a title game.',
   pick='Chad', case='The projection has Chad by {gap}, the biggest gap on the card. He scores {ppg} more a game and beat Abeln for a championship three years ago.',
   wrong='Josh Allen is back and Abes has nothing left to lose. The Warrior always comes back; the question is which week.')
M[('Ricer', 'Rusty')] = dict(no=1, since='1991',
   chip='Ricer has won the last two, including Week 5, 156.9-145.3.',
   head='Meeting No. 86, the longest-running feud in the federation',
   para=('Ricer leads 42-39-4 in 85 meetings since 1991, the most of any pair in the league. The 1990s went to Ricer, 14-6. The 2010s were even, 13-14-1. The 2020s belong to Rusty, 9-4. '
         'They have met 14 times in the playoffs, and Ricer leads 8-6. Eight of those 14 were decided by three points or less. '
         'Both lived in the same West Washington apartment, a year apart. It is a Right Division match. Ricer is 6-2 and in first; Rusty is 3-5 with the second-most points in the league.'),
   call='14 playoff meetings. Eight decided by three points or less.',
   mile=[('1991', 'First meeting, Rusty 40-25; Ricer wins the semifinal 59-58'), ('2006', 'Week 9, a 51-51 tie'), ('2018', 'Week 9, a 64-64 tie'), ('2026', 'Week 5, Ricer 156.9-145.3')],
   lastA=('Ricer&rsquo;s Week 8', 'Beat Derek, 126.9-91.4, for first place in the Right. Burrow 39.4, Golden 20.9, Brown 16.1. Benched Waddle, who scored 14.9.'),
   lastB=('Rusty&rsquo;s Week 8', 'Lost to Chad, 125.6-109.8, his season low. Bowers 28.2, Jacobs 23.2, Love 21.5. Left 103.7 on the bench, including Mahomes (27.4) and Hubbard (24.9). Egbuka started and scored 0.0.'),
   read='Rusty averages {} to Ricer&rsquo;s {}, and is {} in all-play to Ricer&rsquo;s {}. Rusty has been the better team all year and has the worse record. Ricer has been the luckier team, and the luck is in first place.',
   pick='Rusty', case='The projection has the Junkyard Dog by {gap}, a coin flip. Rusty scores {ppg} more a game and is 9-4 against Ricer this decade.',
   wrong='Rusty keeps losing with points on his bench, and Ricer has won the last two. Steamboat and Savage went about 15 minutes at WrestleMania III; these two have been going for 35 years.')
M[('Tom', 'Craig')] = dict(no=5, since='2010',
   chip='Tom won three of the four before Craig&rsquo;s Week 1 blowout this year.',
   head='Dead even after 18 meetings',
   para=('It is 9-9 since 2010. Craig took the 2010s, 7-4. Tom has the 2020s, 5-2. The two biggest wins in the series came in the last two meetings: Tom 118.8-50.3 last December, then Craig 166.2-99.4 in Week 1 this year. They have never met in the playoffs. '
         'The Undertaker showed up in November 1990, the same year Tom joined the league, and has been quietly winning ever since. Paul Orndorff was in the main event of the first WrestleMania and lost it. '
         'It is a cross-division match between two 2-6 teams.'),
   call='9-9. The only even series on the card.',
   mile=[('2010', 'First meeting, Tom 48-38'), ('2017', 'Craig by seven, the closest'), ('2025', 'Tom 118.8-50.3'), ('2026', 'Week 1, Craig 166.2-99.4')],
   lastA=('Tom&rsquo;s Week 8', 'Lost to Giff, 122.4-117.4. Higgins 37.5, Allen 23.3, Irving 21.0. James Cook (18.1) and Sam Darnold (18.5) scored on the bench.'),
   lastB=('Craig&rsquo;s Week 8', 'Lost to the Legion, 133.6-90.4. Fannin 23.4, Watson 17.3. Tre Tucker started for 0.0 and his kicker scored 1.0. Left 64.5 on the bench.'),
   read='Tom averages {} to Craig&rsquo;s {}, and is {} in all-play to Craig&rsquo;s {}. Both are 2-6 and still mathematically alive. Tom has given up the most points in the league.',
   pick='Tom', case='The projection has the Tomcats by {gap}, a coin flip. Tom scores {ppg} more a game and has a roster that keeps scoring on the bench.',
   wrong='Craig beat him by 66.8 in Week 1. Mr. Wonderful has three quarterbacks; one of them is bound to start eventually.')

def tape(A, B):
    hi = lambda o: max(S[o]['weeks'].values())
    rows = [('Record', wl(A), wl(B)), ('Division record', f"{S[A]['dw']}-{S[A]['dl']}", f"{S[B]['dw']}-{S[B]['dl']}"),
            ('Points per game', f1(S[A]['pf']/8), f1(S[B]['pf']/8)), ('Allowed per game', f1(S[A]['pa']/8), f1(S[B]['pa']/8)),
            ('All-play', f"{AP[A][0]}-{AP[A][1]}", f"{AP[B][0]}-{AP[B][1]}"), ('Best week', f1(hi(A)), f1(hi(B))),
            ('Week 8 lineup kept', f"{EFF[A][0]/EFF[A][1]*100:.0f}%", f"{EFF[B][0]/EFF[B][1]*100:.0f}%"),
            ('Streak', streak(A), streak(B)), ('Playoff odds', pct(ODDS[A]['po']), pct(ODDS[B]['po']))]
    out = f'<table class="st"><tr class="sth"><td>Tale of the tape</td><td class="n" style="width:100px">{A}</td><td class="n" style="width:100px">{B}</td></tr>'
    for k, a, b in rows: out += f'<tr><td>{k}</td><td class="n" style="width:100px">{a}</td><td class="n" style="width:100px">{b}</td></tr>'
    return out + '</table>'

def mcard(A, B, n, main=False, label=None):
    divg = (A in RIGHT) == (B in RIGHT)
    lab = label or (f'Match No. {n}' + (' &middot; Main event' if main else ''))
    return f'''<div class="mc"><div class="row" style="justify-content:space-between"><span class="lab">{lab}</span><span class="lab">{"Division match" if divg else "Cross-division"} &middot; Week 9</span></div>
<div class="row" style="align-items:center;margin-top:8px">{logo(A,62)}<div style="flex:1;margin:0 14px"><div class="t">{OWNER[A]} ({wl(A)})<span class="vs">vs</span>{OWNER[B]} ({wl(B)})</div>
<div class="g">{A} as {GIM[A]} &middot; {B} as {GIM[B]}</div></div>{logo(B,62)}</div></div>'''

def hist_block(A, B, m):
    P, w, l, t = series(A, B)
    lead = A if w > l else B if l > w else None
    big = f'{max(w,l)}-{min(w,l)}' + (f'-{t}' if t else '')
    chips = ''
    for d in P[-5:]:
        r = res(d); who = A if r == 'W' else B if r == 'L' else None
        chips += f'<span class="chip" style="background:{COL[who] if who else "#999"}">{who[0] if who else "T"}</span>'
    trophy = ''.join(f'<div class="ln"><span>{o}</span><span class="d"></span><span>{titles[o]} title{"s" if titles[o]!=1 else ""} &middot; playoffs {po_rec[o][0]}-{po_rec[o][1]}</span></div>' for o in (A, B))
    return f'''<div class="row" style="margin-top:12px"><div style="width:256px;flex:none;margin-right:24px">
<div class="divh">All-time series, since {m["since"]}</div>
<div class="big" style="white-space:nowrap;font-size:{56 if t else 70}px">{big}</div><div class="h2" style="color:var(--blue);margin-top:6px">{(lead + " leads") if lead else "All square"}</div>
<div class="divh" style="margin-top:9px">Last five meetings</div><div>{chips}</div>
<p class="note" style="font-size:12.8px">{m["chip"]}</p>
<div class="divh" style="margin-top:8px">Career</div>{trophy}
</div><div style="flex:1">
<p class="h" style="font-size:25px">{m["head"]}</p>
<p class="note" style="font-size:14.2px">{m["para"]}</p>
<div class="quote">{m["call"]}</div></div></div>'''

def mg_html(A, B):
    P, *_ = series(A, B)
    lastm = P[-5:]; mxm = max(abs(d['A'] - d['B']) for d in lastm) or 1
    mg = ''
    for d in lastm:
        diff = d['A'] - d['B']; wp = abs(diff) / mxm * 100
        lab = f"{d['y']} {'Semi' if 'SF' in d['t'] else 'QF' if 'QF' in d['t'] else 'Final' if 'Final' in d['t'] else 'Wk ' + str(d['w'])}"
        left = f'<span style="width:{wp:.0f}%;background:{COL[A]}"></span>' if diff > 0 else ''
        right = f'<span style="width:{wp:.0f}%;background:{COL[B]}"></span>' if diff < 0 else ''
        mg += f'<div class="mg"><span class="y">{lab}</span><span class="bar"><span class="l">{left}</span><span class="r">{right}</span></span><span class="v">{abs(diff):.1f}</span></div>'
    return f'''<div class="divh">Margins, last five meetings</div>
<div class="mg" style="font-family:OS;font-weight:700;font-size:11px;color:var(--blue)"><span class="y"></span><span class="bar"><span class="l" style="border:none;padding-right:6px">{A.upper()}</span><span class="r" style="padding-left:6px">{B.upper()}</span></span><span class="v"></span></div>
{mg}'''
def margins_block(A, B, m):
    tl = ''.join(f'<div class="tl"><b>{y}</b> &nbsp;{t_}</div>' for y, t_ in m['mile'])
    return f'''<div class="row"><div class="ch">{mg_html(A, B)}</div><div class="ch"><div class="divh">Milestones</div>{tl}</div></div>'''

def season_block(A, B, m):
    ppg = {o: f1(S[o]['pf']/8) for o in (A, B)}; ap = {o: f'{AP[o][0]}-{AP[o][1]}' for o in (A, B)}
    first, second = (B, A) if A in ('Ricer',) else (A, B)
    read = m['read'].format(ppg[first], ppg[second], ap[first], ap[second])
    stakes = (f'<b>{A}:</b> {pct(ODDS[A]["po"])} to make the playoffs; {pct(ODDS[A]["po_w"])} with a win, {pct(ODDS[A]["po_l"])} with a loss. '
              f'<b>{B}:</b> {pct(ODDS[B]["po"])}; {pct(ODDS[B]["po_w"])} with a win, {pct(ODDS[B]["po_l"])} with a loss.')
    return f'''<div class="row"><div class="ch"><div class="divh">{m["lastA"][0]}</div><p class="note">{m["lastA"][1]}</p>
<div class="divh" style="margin-top:9px">{m["lastB"][0]}</div><p class="note">{m["lastB"][1]}</p></div>
<div class="ch">{tape(A, B)}</div></div>
<p class="note" style="margin-top:9px"><b>The read.</b> {read}</p>
<p class="note"><b>What it means.</b> {stakes}</p>'''

def pred_block(A, B, m):
    pa, pb = proj(A), proj(B); gap = abs(pa - pb)
    pick = m['pick']; other = B if pick == A else A
    ppg = abs(S[A]['pf'] - S[B]['pf']) / 8
    case = m['case'].format(gap=f'{gap:.1f}', ppg=f'{ppg:.1f}')
    return f'''<div class="pred"><div class="chy">Bold prediction &middot; {conf(gap)}</div>
<p style="font-family:AN;font-size:23px;margin:3px 0 4px;text-transform:uppercase">{OWNER[pick]} {proj(pick):.0f}, {OWNER[other]} {proj(other):.0f}</p>
<p class="note" style="margin:0"><b>Gorilla Monsoon:</b> {case}</p>
<p class="note" style="margin-top:3px"><b>Bobby Heenan:</b> {m["wrong"]}</p></div>'''

def mpage(A, B, extra=''):
    m = M[(A, B)]
    body = mcard(A, B, m['no']) + hist_block(A, B, m) + '<div class="strip" style="margin:4px 0 8px;height:5px"></div>' + margins_block(A, B, m) + \
        '<div class="strip" style="margin:6px 0 8px;height:5px"></div>' + season_block(A, B, m) + extra + '<div class="sp" style="min-height:8px"></div>' + pred_block(A, B, m) + '<div style="height:14px"></div>'
    return page(body)

# Main event, two pages
def main_event():
    A, B = 'Ricer', 'Rusty'; m = M[(A, B)]
    P, w, l, t = series(A, B)
    dec = ''
    for lo, hi, lab in [(1991, 1999, '1990s'), (2000, 2009, '2000s'), (2010, 2019, '2010s'), (2020, 2026, '2020s')]:
        Q = [d for d in P if lo <= d['y'] <= hi]; ww = sum(res(d) == 'W' for d in Q); ll = sum(res(d) == 'L' for d in Q); tt = sum(res(d) == 'T' for d in Q)
        tot = max(ww + ll + tt, 1)
        dec += (f'<div class="bg"><span class="bn" style="width:60px">{lab}</span><span class="bb" style="display:flex;background:none">'
                f'<span style="width:{ww/tot*100:.0f}%;background:{COL[A]}"></span><span style="width:{tt/tot*100:.0f}%;background:#999"></span><span style="width:{ll/tot*100:.0f}%;background:{COL[B]}"></span></span>'
                f'<span class="bv" style="width:72px">{ww}-{ll}{"-"+str(tt) if tt else ""}</span></div>')
    pos = [d for d in P if d['po']]
    nm = {'po-SF': 'Semifinal', 'po-QF': 'Quarterfinal', 'po-Final': 'Final'}
    porows = ''
    for d in pos:
        wnr = A if d['A'] > d['B'] else B
        hi_, lo_ = max(d['A'], d['B']), min(d['A'], d['B'])
        porows += f'<div class="ln" style="font-size:13px;margin:1px 0"><span>{d["y"]} {nm.get(d["t"], d["t"])}</span><span class="d"></span><span>{wnr}, {hi_:.0f}-{lo_:.0f}</span></div>'
    p1 = page(mcard(A, B, 1, main=True) + hist_block(A, B, m) + '<div class="strip" style="margin:6px 0 8px;height:5px"></div>' + f'''
<div class="row"><div class="ch"><div class="divh">The series by decade</div>{dec}
<p class="note" style="font-size:12.8px">Blue is Ricer, gold is Rusty, gray is a tie. Four ties.</p>
<div style="margin-top:8px">{mg_html(A, B)}</div></div>
<div class="ch"><div class="divh">All 14 playoff meetings</div>{porows}</div></div>
<div class="sp"></div>
<div class="card" style="margin-bottom:16px"><p class="h2">Week 9, specifically</p>
<p class="note" style="margin-top:3px">They have met in Week 9 six times. Two of those were ties: 51-51 in 2006 and 64-64 in 2018. Ricer won three of the other four. Mean Gene, if you would: &ldquo;Rusty, they say you can&rsquo;t beat him when it counts.&rdquo; Rusty: &ldquo;Six of fourteen, Gene.&rdquo;</p></div>''')
    p2 = page(header('Main event, continued', 'Loungers vs Junkyard Dog', label='Match No. 1') + f'''
<p class="h">Same division, opposite luck</p>
<p class="hs">Rusty is {AP["Rusty"][0]}-{AP["Rusty"][1]} in all-play and 3-5. Ricer is {AP["Ricer"][0]}-{AP["Ricer"][1]} in all-play and 6-2.</p>
''' + season_block(A, B, m) + f'''
<div class="strip" style="margin:10px 0 8px;height:5px"></div>
<div class="row"><div class="ch"><div class="divh">Week by week, 2026</div>
''' + ''.join(f'<div class="mg"><span class="y">Week {wk}</span><span class="bar"><span class="l"><span style="width:{S[A]["weeks"][wk]/190*100:.0f}%;background:{COL[A]}"></span></span><span class="r"><span style="width:{S[B]["weeks"][wk]/190*100:.0f}%;background:{COL[B]}"></span></span></span><span class="v" style="width:96px">{f1(S[A]["weeks"][wk])} / {f1(S[B]["weeks"][wk])}</span></div>' for wk in range(1, 9)) + f'''
<p class="note" style="font-size:12.8px">Ricer left, Rusty right, each team&rsquo;s own score that week. Rusty has outscored Ricer in {sum(S[B]["weeks"][w]>S[A]["weeks"][w] for w in range(1,9))} of eight weeks. The week they played, Ricer won by 11.6.</p></div>
<div class="ch"><div class="divh">What Sunday does to the Right</div>
<div class="ln"><span>Ricer wins</span><span class="d"></span><span>7-2, and the Dog falls to 3-6</span></div>
<div class="ln"><span>Rusty wins</span><span class="d"></span><span>Season split, Rusty 4-5</span></div>
<p class="note">Division odds: Ricer {pct(ODDS["Ricer"]["div"])} now, {pct(ODDS["Ricer"]["div_w"])} with a win, {pct(ODDS["Ricer"]["div_l"])} with a loss. Rusty&rsquo;s playoff odds: {pct(ODDS["Rusty"]["po_w"])} with a win, {pct(ODDS["Rusty"]["po_l"])} with a loss.</p>
<div class="vault" style="margin-top:10px"><p class="h2" style="font-size:16px">The Junkyard Dog&rsquo;s bench, Week 8</p>
<p class="note" style="color:#f3efe6;margin-top:3px">Mahomes 27.4, Hubbard 24.9, Odunze 12.7, Downs 12.3, Kelce 11.7, Thomas 8.2, LaPorta 6.5. That is 103.7 points, which by itself would have beaten three teams this week.</p></div>
</div></div>
<div class="sp" style="min-height:10px"></div>''' + pred_block(A, B, m) + '<div style="height:14px"></div>')
    return p1 + p2

CLASSIC = '''<div class="vault" style="margin-top:10px"><p class="h2" style="font-size:16px">Classic match: Sterling Sharpe vs. Andre Rison</p>
<p class="note" style="color:#f3efe6;margin-top:3px">College. Rusty argued Sterling Sharpe was the better receiver. Abeln argued Andre Rison. Rusty settled it with a Superfly Snuka off the couch onto Abes. Officially, no ruling. The rematch is booked for Week 14, Rusty vs. Abeln, the last game of Abes&rsquo;s regular season. His last two opponents are both former housemates.</p></div>'''

MP = mpage('Derek', 'Giff') + mpage('Chad', 'Abeln', extra=CLASSIC) + mpage('Frenches', 'Schwanz') + mpage('Tom', 'Craig')
MAIN = main_event()

# ================================================================= Trade desk
TRADES = [
 ('Housemates, one quarterback apart.', 'Junkyard Dog sends Patrick Mahomes (QB)', 'Boulder Giant Iguanas send DJ Moore (WR)',
  'Giff started Lamar Jackson for 0.0 last week, and his backup scored 3.4. Rusty has two starting quarterbacks and sat Mahomes for 27.4 behind Jordan Love. Rusty started Egbuka for 0.0 and Pickens for 6.8; Moore scored 16.6 on Giff&rsquo;s bench. '
  'Keeper costs travel with the player, so check both prices. Why Giff might pass: Lamar comes back eventually. Why Rusty might pass: he plays Giff in Week 12.'),
 ('The Dog has a tight end to spare.', 'Junkyard Dog sends Travis Kelce (TE)', 'Legion of Doom sends Wan&rsquo;Dale Robinson (WR)',
  'Rusty carries three tight ends: Bowers, Kelce and LaPorta. The Legion started Kyle Pitts for 2.6 with Kittle at 0.0, and has receiver depth: Robinson scored 15.7 on the bench. '
  'Why the Legion might pass: they are 5-3 and do not need much. Why Rusty might pass: they play each other in Week 10.'),
]
tr = ''
for hd, a, b, tx in TRADES:
    tr += f'''<div class="card" style="margin-bottom:12px"><p class="h2" style="font-size:20px">{hd}</p>
<div class="row" style="margin:6px 0"><div class="ch"><div class="divh">Sends</div><p class="note" style="margin:0">{a}</p></div><div class="ch"><div class="divh">In return</div><p class="note" style="margin:0">{b}</p></div></div>
<p class="note">{tx}</p></div>'''
MV = [
 ('Chad', 'Paid $3 for Hunter Henry, dropped Juwan Johnson; $2 for the Bengals', 'Henry 6.0, Bengals 2.0.'),
 ('Giff', 'Paid $10 for Jonah Coleman, dropped Jake Ferguson; signed Tyler Bass Saturday', 'Coleman 20.4 on the bench. Bass 16.0, the best kicker score of the week.'),
 ('Ricer', 'Signed Brenton Strange, the Patriots and Jaydon Blue; paid $11 for Cam Little', 'Strange 7.5, Patriots 7.0, Little 6.0. Blue 1.9 on the bench.'),
 ('Schwanz', 'Signed Malik Willis, dropped Ja&rsquo;Kobi Lane', 'Started Willis for 14.6.'),
 ('Abeln', 'Paid $8 for Caleb Douglas, dropped Kyler Murray', 'Douglas 8.3 on the bench.'),
 ('Craig', 'Signed Ryan Flournoy and Dylan Sampson, dropped Higbee and the Giants', 'Flournoy 13.1 and Sampson 12.9, both on the bench.'),
 ('Rusty', 'Signed Evan McPherson, dropped Cairo Santos', 'McPherson 5.0.'),
]
moves = ''.join(f'<div class="ln"><span><b>{o}.</b> {a}</span></div><p class="note" style="margin:0 0 5px 0;color:var(--mut)">{b}</p>' for o, a, b in MV)
P9 = page(header('The trading block', 'Trade desk and moves') + f'''
<p class="h">Managers at ringside</p><p class="hs">Two ideas that move a player off one bench and into another lineup. Suggestions only; nothing here has been offered.</p>
{tr}
<div class="row"><div class="c1">
<p class="h" style="font-size:24px">Moves that mattered</p><p class="hs">Week 8 pickups and what they did.</p>
{moves}
</div><div class="c2">
<p class="h" style="font-size:24px">House rules</p>
<p class="note">Trade deadline: the week the first team is mathematically eliminated. Nobody can be out before Week 10 results. Keeper costs travel with the player.</p>
<p class="note">Last week&rsquo;s ideas, Nix to Giff and Jacobs to Abeln, didn&rsquo;t happen. Jacobs scored 23.2 for Rusty. Flowers scored 0.0 for Abeln.</p>
<p class="note">Buy-ins: $200 each. Winnings settle at the end of the season and don&rsquo;t count toward dues.</p>
<div class="card" style="margin-top:10px"><p class="h2" style="font-size:16px">Next week&rsquo;s card</p>
<p class="note" style="margin-top:3px">Derek at Tom, Craig at Ricer, Rusty at the Legion, Abeln at Giff, Chad at Schwanz. The Warrior and the Honky Tonk Man, housemates, in Week 10. The real ones went about half a minute at SummerSlam &rsquo;88.</p></div>
</div></div>
<div class="sp"></div>
<p class="chy" style="text-align:center;margin-bottom:12px;color:var(--mut)">We&rsquo;ll be right back after these messages.</p>''', foot='Tape delayed, as always')

HTML = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{P1}{P2}{P3}{MAIN}{MP}{P9}</body></html>'
open('ffl_wk9.html', 'w').write(HTML)
print('ok picks', wk8w, SEASON, 'pages', HTML.count('class="page"'), 'elim', ELIM)
