# FFL Review

Weekly newsletter for Bullwinkle's Dance League (BDL), built as HTML and rendered to a Letter-size PDF.

## Layout

- `shared/data/` – game logs the builds read: `all_games.csv` (1991–2018 regular season, project upload "All Games 19912018.csv") and `recent.csv` (2019–2025 regular season, 1993 Week 15, every playoff game since 1990)
- `shared/season2026/` – this season: `games_2026.csv` (every result), `picks_2026.csv` (every Bold Prediction and how it went), `weekly_high_2026.csv`, `keepers_2026.csv`
- `shared/odds/` – the odds printed each week (`odds_snapshot_wkN.json`), so next week's change is always against what was published
- `shared/history/` – one row per owner per season (division finish, playoff finish, awards), plus season awards and keepers
- `shared/lore.md` – owner stories Derek has supplied; the only stories that get printed
- `shared/themes_and_ribbing.md` – themes used and coming, and who's taken how much grief
- `shared/logos/` – original team logos
- `shared/make_assets.py` – builds `ff/` (fonts) and `img/` (owner logos) in a week folder
- `weeks/wkNN-theme/` – one folder per issue, with symlinks into `shared/`

## Building an issue (Week 9 example)

```
cd weeks/wk09-wrestling
python3 ../../shared/make_assets.py      # fonts + logos (needs npm, Pillow)
python3 hist.py                          # sanity check: series records
python3 odds9.py                         # playoff odds (numpy)
python3 build9.py                        # writes ffl_wk9.html
python3 render9.py                       # writes the PDF (playwright + chromium)
```

Check every page with a contact sheet (`pdftoppm`) before sending.

## Starting a new week

Copy the previous week's folder and rename the numbered files. Then:
1. Add last week's results to `shared/season2026/games_2026.csv` and `dataN.py`; grade last week's picks in `picks_2026.csv`; add the weekly high.
2. Pull lineups and moves from CBS.
3. Run the odds; save the new snapshot to `shared/odds/`.
4. Write the theme and copy in `buildN.py`; log new picks, the theme and the ribbing counts.
5. At season's end, fold `games_2026.csv` into `recent.csv`.

## Elsewhere

Editorial rules (Newsletter_Playbook.md), research notes such as the Week 10 bar crawl (`claude/ffl-review-code/statestreet/bars10.md`), the money ledger and older issues' code (Weeks 4–8) stay in the claude.ai project.
