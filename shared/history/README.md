# League history

| File | What it is | Source |
|---|---|---|
| `playoff_results_letters.csv` | Derek's playoff finish grid, 1990–2024 (A won final, B lost final, C lost 2nd round, D lost 1st round, F missed) | Project upload "Playoff Results.csv", unchanged |
| `playoff_finishes_from_games.csv` | The same grades, derived from the playoff games in `../data/recent.csv` (1990–2025) | Generated |
| `division_standings.csv` | Division finish by owner, 1990–2025 | Project upload "Division Standings.csv", unchanged |
| `yearly_payouts.csv` | Champion, runner-up, scoring title and division winners by year, with payouts from 2001 | Project upload "FFL Yearly Payouts.csv", unchanged |
| `keepers.csv` | Keepers and costs, 2022–2025 (2026 keepers are in `../season2026/keepers_2026.csv`) | Project upload "Keepers and costs.csv", unchanged |

Playoff game scores live in `../data/recent.csv` (type `po-QF`, `po-SF`, `po-Final`; `-est` marks reconstructed 31-30 style placeholders).
3rd- and 5th-place games are excluded everywhere.

## Owner notes
- Chad and Chewy were one franchise 1997–2002 (Chad was part owner of Chewy's team or not yet in the league), so those games and the 2002 title count as Chad's. Chewy's own team after that (2003–2008) stays separate.
- Schwanz sat out 2001–2008.

## Where the letter grid and the games disagree
Checked 11/8/26, playoff games vs. `playoff_results_letters.csv`, real-score years only:

| Year | Owner | Letter grid | Games | Evidence |
|---|---|---|---|---|
| 2023 | Giff | D | C | CBS 2023 bracket (project file "playoffs 2023.pdf"): Giff beat Craig 148.44–112.42 in the quarterfinal, lost to Abeln 131.20–116.68 in the semifinal |
| 2023 | Craig | C | D | Same bracket: Craig lost that quarterfinal |
| 2013 | Abeln | C | D | Frenches beat Abeln 106–48 in the quarterfinal |
| 2019 | Craig | F | D | Giff beat Craig 65–63 in the quarterfinal |

2023 looks like Giff and Craig swapped rows. The grid has no 2025 row yet (from games: Chad A, Schwanz B, Ricer C, Abeln C, Tom D, Craig D).
Mismatches in reconstructed years (1993–1997, 2000) are not listed: those placeholder scores can't settle anything.
