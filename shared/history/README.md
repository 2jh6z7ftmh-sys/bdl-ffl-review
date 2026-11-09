# League history

| File | One row per | What's in it |
|---|---|---|
| `owner_seasons.csv` | owner, season | division, division finish, playoff finish, awards (division title, scoring title), co-owner |
| `season_awards.csv` | season | champion, runner-up, scoring title, division winners, payouts (from 2001) |
| `keepers.csv` | keeper | 2022–2025 keepers and costs (2026 is in `../season2026/`) |

Playoff finish is one of: Champion, Runner-up, Lost semifinal, Lost quarterfinal, Missed playoffs, Not recorded (1990 and 1993, where only the final survives).
Division-winner byes show as Lost semifinal or better.

## Sources and rules
- Playoff finishes come from the playoff game scores in `../data/recent.csv`. The scores win over the old spreadsheet (Derek, 11/8/26). That fixed 2023 (Giff reached the semis, Craig lost the quarterfinal; confirmed by the CBS 2023 bracket, project file "playoffs 2023.pdf"), 2013 Abeln and 2019 Craig, and added 2025.
- `playoff_scores_reconstructed = 1` marks years where the playoff scores are 31-30 style placeholders (1990–1997, 2000). The champion is right; earlier rounds may not be.
- Division finishes come from Derek's Division Standings sheet; awards and payouts from his FFL Yearly Payouts sheet (both project uploads).
- Chewy's 1997–2002 seasons count as Chad's (one franchise). Rows before an owner's first season were dropped (the old sheet carried 1990 finishes in the Ricer and Chad columns).
- 3rd- and 5th-place games are excluded everywhere.

## Settled (Derek, 11/8/26)
- 2025 Left Division: Craig 3rd, Frenches 4th. CBS 2025 standings: both 6-8, Craig won the tiebreak (beat the Frenches twice; 4-4 division record vs 3-5). The old sheet had them swapped.
- Schwanz: the spreadsheet wins. He played 1996-1999 and 2007 on, and sat out 2000-2006.
- Chewy: wherever Chewy appears, Chad is a half owner (`co_owner` column). Chewy's 1997-2002 games also count as Chad's in the game logs.

## Note
- 2025 Right Division: CBS lists Rusty 4th and Derek 5th (both 6-8, split 1-1); the sheet has Derek 4th on division record (4-4 vs 3-5), which matches the league's posted tiebreak order. Kept the sheet. Neither made the playoffs.
