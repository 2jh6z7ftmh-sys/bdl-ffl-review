"""Playoff odds model v1, unchanged since Week 6. 20,000 sims, seed 7. Data through Week 8.
Adds elimination tracking: a team is mathematically out if it can't reach 3rd in its division even winning out
(checked exactly against best-case W totals, ignoring tiebreakers -> conservative)."""
import numpy as np, json
from data10 import OWN, RIGHT, season, NG
SCHED = {
 8:[('Derek','Ricer'),('Giff','Tom'),('Schwanz','Abeln'),('Frenches','Craig'),('Rusty','Chad')],
 9:[('Derek','Giff'),('Frenches','Schwanz'),('Chad','Abeln'),('Ricer','Rusty'),('Tom','Craig')],
 10:[('Derek','Tom'),('Craig','Ricer'),('Rusty','Frenches'),('Abeln','Giff'),('Chad','Schwanz')],
 11:[('Rusty','Derek'),('Ricer','Abeln'),('Giff','Frenches'),('Chad','Tom'),('Schwanz','Craig')],
 12:[('Derek','Schwanz'),('Giff','Rusty'),('Tom','Ricer'),('Frenches','Abeln'),('Craig','Chad')],
 13:[('Derek','Chad'),('Abeln','Schwanz'),('Tom','Rusty'),('Giff','Craig'),('Ricer','Frenches')],
 14:[('Tom','Derek'),('Schwanz','Giff'),('Craig','Frenches'),('Ricer','Chad'),('Rusty','Abeln')],
}
N = 20000; SD_TEAM = 8.0
idx = {o: i for i, o in enumerate(OWN)}; isR = np.array([o in RIGHT for o in OWN])
MODEL = 'v1 (70/30 projection, team-strength SD 8, 20,000 sims)'
def model(upto):
    S = season(upto)
    LG = sum(S[o]['pf'] for o in OWN) / (10.0 * upto)
    PROJ = {o: 0.7 * S[o]['pf'] / upto + 0.3 * LG for o in OWN}
    resid = [S[o]['weeks'][w] - S[o]['pf'] / upto for o in OWN for w in range(1, upto + 1)]
    SD_WEEK = float(np.sqrt(np.mean(np.square(resid))) * np.sqrt(upto / (upto - 1)))
    return S, LG, PROJ, SD_WEEK
def run(upto=NG, seed=7):
    S, LG, PROJ, SD_WEEK = model(upto)
    rng = np.random.default_rng(seed); T = len(OWN); NEXT = upto + 1
    W = np.tile(np.array([S[o]['w'] for o in OWN], float), (N, 1))
    DW = np.tile(np.array([S[o]['dw'] for o in OWN], float), (N, 1)); DL = np.tile(np.array([S[o]['dl'] for o in OWN], float), (N, 1))
    PF = np.tile(np.array([S[o]['pf'] for o in OWN]), (N, 1))
    mu = np.array([PROJ[o] for o in OWN]) + rng.normal(0, SD_TEAM, (N, T)); nxt = {}
    for wk in range(NEXT, 15):
        sc = mu + rng.normal(0, SD_WEEK, (N, T)); PF += sc
        for a, b in SCHED[wk]:
            ia, ib = idx[a], idx[b]; aw = sc[:, ia] > sc[:, ib]
            W[:, ia] += aw; W[:, ib] += ~aw
            if isR[ia] == isR[ib]:
                DW[:, ia] += aw; DL[:, ia] += ~aw; DW[:, ib] += ~aw; DL[:, ib] += aw
            if wk == NEXT: nxt[a] = aw; nxt[b] = ~aw
    key = W * 1e6 + DW / np.maximum(DW + DL, 1) * 1e4 + PF / 100.0
    div1 = np.zeros((N, T), bool); mk = np.zeros((N, T), bool); rows = np.arange(N)[:, None]
    for mask in (isR, ~isR):
        cols = np.where(mask)[0]; order = cols[np.argsort(-key[:, cols], axis=1)]
        div1[rows[:, 0], order[:, 0]] = True; mk[rows, order[:, :3]] = True
    st = np.zeros((N, T), bool); st[np.arange(N), PF.argmax(1)] = True; out = {}
    for o in OWN:
        i = idx[o]; w = nxt[o]
        out[o] = dict(div=float(div1[:, i].mean()), po=float(mk[:, i].mean()), st=float(st[:, i].mean()),
                      po_w=float(mk[w, i].mean()), po_l=float(mk[~w, i].mean()), div_w=float(div1[w, i].mean()), div_l=float(div1[~w, i].mean()))
    return out
def eliminated(upto=NG):
    """Exact: team X is out if, even winning every remaining game, at least 3 division rivals are guaranteed
    more wins. Rival guaranteed wins = current W (+ wins forced by games vs X, which X wins, so none)."""
    S = season(upto); left = 14 - upto; out = []
    for o in OWN:
        div = RIGHT if o in RIGHT else [x for x in OWN if x not in RIGHT]
        best = S[o]['w'] + left
        ahead = sum(1 for x in div if x != o and S[x]['w'] > best)
        if ahead >= 3: out.append(o)
    return out
def pct(x):
    p = x * 100
    return '<1%' if 0 < p < 0.5 else '>99%' if 99.5 <= p < 100 else f'{p:.0f}%'
def sos(upto=NG):
    S = season(upto); ppg = {o: S[o]['pf'] / upto for o in OWN}; out = {}
    for o in OWN:
        opp = [b if a == o else a for wk in range(upto + 1, 15) for a, b in SCHED[wk] if o in (a, b)]
        out[o] = sum(ppg[x] for x in opp) / len(opp)
    return out
ODDS = run(NG)
PREV = json.load(open('odds_snapshot_wk8.json'))['odds_through_wk8']
if __name__ == '__main__':
    S, LG, PROJ, SDW = model(NG); print('through wk', NG, 'LG', round(LG, 1), 'SDW', round(SDW, 1)); SO = sos()
    for o in sorted(OWN, key=lambda o: -ODDS[o]['po']):
        r = ODDS[o]; p = PREV[o]
        print(f"{o:9s} {S[o]['w']}-{S[o]['l']} div {pct(r['div']):>5} ({(r['div']-p['div'])*100:+.0f}) po {pct(r['po']):>5} ({(r['po']-p['po'])*100:+.0f}) st {pct(r['st']):>5} | win {pct(r['po_w']):>5} loss {pct(r['po_l']):>5} | sos {SO[o]:.1f} proj {PROJ[o]:.1f}")
    print('mathematically eliminated:', eliminated())
    R2 = run(NG, seed=99); print('max diff second seed', round(max(abs(ODDS[o][k] - R2[o][k]) for o in OWN for k in ODDS[o]), 3))
    if False:
        json.dump({'model': MODEL, 'data_cutoff': 'Week 8 final', 'sims': N, 'seed': 7, 'odds_through_wk8': ODDS}, open('odds_snapshot_wk8.json', 'w'), indent=1)
