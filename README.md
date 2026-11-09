# FFL Review

Weekly newsletter for Bullwinkle's Dance League (BDL), built as HTML and rendered to a Letter-size PDF.

## Layout

- `shared/data/` – league history the builds read
  - `all_games.csv` – raw regular-season log 1991–2018 (project upload "All Games 19912018.csv")
  - `recent.csv` – 2019–2025 regular season, 1993 Week 15, and all playoff games
  - `odds_snapshot_wk7.json` – saved odds baseline (Week 8 baseline lives in `weeks/wk09-wrestling/`)
- `shared/logos/` – original team logos
- `shared/make_assets.py` – builds `ff/` (fonts from npm @fontsource) and `img/` (owner logos) in a week folder
- `weeks/wkNN-theme/` – one folder per issue; each is self-contained apart from symlinks into `shared/data`

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

Copy the previous week's folder, rename the numbered files, then: update scores in `dataN.py`, pull lineups and moves from CBS, point odds at the previous week's snapshot, rewrite the copy and theme in `buildN.py`.

## Elsewhere

Editorial rules (Newsletter_Playbook.md), research notes such as the Week 10 bar crawl (`claude/ffl-review-code/statestreet/bars10.md`) and older issues' code (Weeks 4–8) stay in the claude.ai project.
