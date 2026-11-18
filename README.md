# THE WORLD TODAY — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/JACKETAGENT-ID/news-image-20261117-nurz3/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/JACKETAGENT-ID/news-image-20261117-nurz3/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Built for the [make.fun bounty "Sum up 17 November's world news in one image"](https://make.fun/bounty/news-image-20261117) ($250 in USDC).

A classic broadsheet front page summing up one day's world news in a
single image, built for the make.fun competition
`news-image-20261117` ("Sum up 17 November's world news in one image").

## What the page shows

- **Masthead** — "THE WORLD TODAY", dated Tuesday, 17 November 2026.
- **Lead story** — Ukraine's drone and missile strike on the Crimean
  (Kerch) bridge, which partly collapsed; Moscow's reply strikes on
  Kyiv bridges. Illustrated with a drawn bridge panel.
- **Locator map strip** — "Where the day happened": Crimea, Shenzhen,
  Manila, Gaza, Bahrain, Yemen, Tokyo, Mongolia.
- **Four columns, 29 short stories + lead = 30 items**, in sections
  WORLD, ASIA & THE SUMMITS, ECONOMY, TECHNOLOGY, CULTURE & HEALTH,
  SPORT — among them the APEC CEO Summit opening in Shenzhen, the
  planned Trump–Xi–Putin trilateral, Trump's Manila ASEAN visit,
  the Gaza aid plea, the West Bank killing, the Houthi advance in
  Yemen, Japan scrambling jets, the Russian plane crash (19 killed),
  Mongolia's president resigning, the US losing measles-free status,
  the Depardieu guilty plea, US AI-chip curbs, the Hormuz tanker
  fires, Disney earnings, the SAFF final and the ICC calendar.
- **The day in numbers** — 19, 5,400+, 1,000, 21, 4, 26.

Every headline was checked against news reported on 17 November 2026
(BBC, APEC/ASEAN releases, major outlets). The 2026 APEC leaders'
meeting is in Shenzhen, China (18–19 Nov), not Gyeongju — the CEO
Summit opened in Shenzhen on 17 November.

## How it is built

- `generate.py` draws `entry.png` (1024×1024, PNG) with PIL from the
  story data in the file. It is deterministic: two runs produce
  byte-identical output (verified with sha256).
- `main.py` (stdlib only) copies `entry.png` to `/output/entry.png`
  (or `$MAKEFUN_OUTPUT_DIR/entry.png`), so the graded program needs
  no network and no third-party packages.

## Run locally

```sh
python3 generate.py          # rebuild entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `generate.py` — the drawing program (all text and code original)
- `entry.png` — the front page, 1024×1024, ~171 KB
- `main.py` — the competition entrypoint
- `LICENSE` — MIT
- `.makefun/owner.json` — wallet claim file
