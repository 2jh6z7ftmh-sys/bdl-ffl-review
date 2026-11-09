# Weeks 1-7 carried from data8.py (verified on CBS). Week 8 from CBS live scoring; fill W8 when MNF (CHI at SEA) is final.
OWNER = {
 'Ricer':'Barca City Loungers','Derek':'Washington Island Ferries','Chad':'Tribute Mr French - AKA Mark',
 'Rusty':'Junkyard Dog','Tom':'Tennessee Tomcats','Giff':'Boulder Giant Iguanas',
 'Schwanz':'Bushwood Night Putters','Frenches':'Legion of Doom','Abeln':'Bloomington Syndicate',
 'Craig':"Craig's House of Pain!"}
RIGHT = ['Ricer','Derek','Chad','Rusty','Tom']
LEFT = ['Giff','Schwanz','Frenches','Abeln','Craig']
GAMES = [
 (1,'Giff','Derek',132.5,123.9),(1,'Schwanz','Chad',111.1,109.8),(1,'Abeln','Ricer',129.0,130.7),(1,'Craig','Tom',166.2,99.4),(1,'Frenches','Rusty',140.4,139.6),
 (2,'Frenches','Derek',117.9,164.0),(2,'Chad','Giff',87.1,90.6),(2,'Schwanz','Ricer',109.9,118.1),(2,'Rusty','Tom',141.0,106.8),(2,'Abeln','Craig',151.2,110.6),
 (3,'Derek','Rusty',144.9,110.7),(3,'Chad','Ricer',106.1,92.8),(3,'Abeln','Tom',115.5,123.4),(3,'Schwanz','Frenches',123.1,158.2),(3,'Craig','Giff',105.3,112.9),
 (4,'Ricer','Derek',101.7,86.9),(4,'Giff','Abeln',123.0,95.7),(4,'Rusty','Craig',139.9,116.4),(4,'Frenches','Chad',109.5,168.3),(4,'Tom','Schwanz',120.3,182.6),
 (5,'Derek','Craig',122.9,114.8),(5,'Rusty','Ricer',145.3,156.9),(5,'Giff','Schwanz',124.1,147.4),(5,'Tom','Chad',122.6,138.3),(5,'Abeln','Frenches',114.4,122.4),
 (6,'Abeln','Derek',64.7,122.9),(6,'Ricer','Tom',133.7,121.8),(6,'Chad','Rusty',97.4,134.3),(6,'Frenches','Giff',121.7,77.9),(6,'Craig','Schwanz',79.8,141.5),
 (7,'Chad','Derek',130.3,141.7),(7,'Craig','Abeln',104.3,88.7),(7,'Schwanz','Rusty',119.2,111.4),(7,'Ricer','Giff',84.2,125.5),(7,'Tom','Frenches',140.9,117.8),
]
# Week 8 (home team second, as in WEEK8 of the last issue). FILL WHEN FINAL.
W8 = {('Derek','Ricer'): (91.4,126.9), ('Giff','Tom'): (122.4,117.4), ('Schwanz','Abeln'): (112.2,80.0), ('Frenches','Craig'): (133.6,90.4), ('Rusty','Chad'): (109.8,125.6)}  # CBS live scoring, all final 11/2/26 ~10:25 pm CT
for (a, h), v in W8.items():
    if v: GAMES.append((8, a, h, v[0], v[1]))
NG = max(g[0] for g in GAMES)
WK20 = [(1,'Craig',166.2),(2,'Derek',164.0),(3,'Frenches',158.2),(4,'Schwanz',182.6),(5,'Ricer',156.9),(6,'Schwanz',141.5),(7,'Derek',141.7),(8,'Frenches',133.6)]
UNPAID = ['Rusty','Chad']   # ledger-2026 as of 10/31/26 (Craig paid 10/31)
WEEK8 = [('Derek','Ricer'),('Giff','Tom'),('Schwanz','Abeln'),('Frenches','Craig'),('Rusty','Chad')]
WEEK9 = [('Derek','Giff'),('Frenches','Schwanz'),('Chad','Abeln'),('Ricer','Rusty'),('Tom','Craig')]  # verify on CBS schedule
OWN = RIGHT + LEFT
def season(upto=None):
    upto = upto or NG
    S = {o: dict(pf=0.0, pa=0.0, w=0, l=0, t=0, dw=0, dl=0, weeks={}, res=[]) for o in OWN}
    for wk, a, h, sa, sh in GAMES:
        if wk > upto: continue
        for o, x, y, opp in ((a, sa, sh, h), (h, sh, sa, a)):
            s = S[o]; s['pf'] += x; s['pa'] += y; s['weeks'][wk] = x
            r = 'W' if x > y else 'L' if x < y else 'T'; s['res'].append(r)
            s['w'] += r == 'W'; s['l'] += r == 'L'; s['t'] += r == 'T'
            if (o in RIGHT) == (opp in RIGHT):
                s['dw'] += r == 'W'; s['dl'] += r == 'L'
    return S
