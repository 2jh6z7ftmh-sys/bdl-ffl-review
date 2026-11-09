# League history

| File | One row per | What's in it |
|---|---|---|
| `owner_seasons.csv` | owner, season | division, division finish, playoff finish, awards (division title, scoring title) |
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

## Open questions
- 2025 Left Division: the sheet has Craig 4th and the Frenches 3rd, but Craig made the playoffs and the Frenches didn't.
- Schwanz: notes say he sat out 2001–2008, but the sheet gives him Left Division finishes in 2007 (5th) and 2008 (3rd).
- 1995–96: the sheet lists Chewy, while the 1995 playoff games list Chad.
