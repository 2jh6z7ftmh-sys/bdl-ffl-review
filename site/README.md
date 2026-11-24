# Bullwinkle's Dance League website

Static site (no build step). Netlify publishes this folder as-is.
Live at: https://bullwinkles.kosiorek.com

## Weekly update
1. Add the new issue: copy its HTML and/or PDF into `issues/` as `2026-wkNN.html` / `.pdf`,
   a cover image into `thumbs/`, and add a line at the top of `assets/issues.js`.
2. Refresh the numbers: add the week's final scores to `Claude Memory/data/games_1990_2026.csv`
   (or the W10-style dict in `build_data.py`), update `week11` (next week's matchups) and `updated`,
   then run `python3 build_data.py` to regenerate `assets/data.js`.
3. Push / redeploy.

## Native issues (Week 12 on)
An issue can be a page of the site instead of a PDF or embedded file: `issues/2026-wkNN.html`, loading
`assets/review.css` (layout) and `assets/review.js` (issue nav plus blocks that fill from `data.js`: last week's
scores and pick grades, standings, the weekly high and low, this week's games with the all-time series, luck, streaks).
Set `window.WEEK` in the page, add the issue to `assets/issues.js` with `"native": true`, and add its line to
`_redirects` above the catch-all. Dashed boxes are copy still to write. `weeks/wk12-hairmetal/render12.py`
makes the screenshots, the cover thumb and the 1200x630 link-preview image.

## Pages
- index.html: latest issue, this week's games with all-time series, 2026 standings, recent champions
- review.html: every FFL Review issue plus the 1991 vault
- records.html: championships, career records, head-to-head tool and grid, season by season, game records
- owners.html / owner.html?o=Name: owner pages
- rules.html: rules, scoring, payouts

Data source: the Bullwinkles/Claude Memory folder (source of truth).
