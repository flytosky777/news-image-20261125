[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/flytosky777/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/flytosky777/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World in One Day — Tuesday 25 November 2026

A make.fun entry for
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
one image that sums up the world's news of Tuesday 25 November 2026.

## The image

`entry.png` (1024×1024) is drawn in this session by `build_frontpage.py`
(PIL): the date in the masthead, a wide photo of a burning cargo ship as
the top story, then five rows each with its own picture, so a viewer who
missed the day can tell what happened from the pictures and the short
labels alone. The six stories, each checked against reporting of the day:

1. **Zelensky confirms Ukraine's sea war on Russian ships** — Kyiv claims
   drone strikes on the Sparta II in the Gulf of Finland and the Merkury
   off Libya; Norway urges caution. (Reuters, Arab News, Kyiv Independent)
2. **Huawei guilty on 10 of 12 counts in U.S. trial** — A Brooklyn jury
   convicts on fraud and trade-secret theft; acquitted of racketeering.
   (Reuters, U.S. Department of Justice, CNN)
3. **Houthi drone hits Riyadh's tallest tower, 11 hurt** — Second strike
   on the PIF Tower in a week; the 385-metre skyscraper crowns the
   financial district. (Dawn, Al Jazeera, The Wall Street Journal)
4. **CIA and ODNI hit by cyber breach** — Unclassified information
   exposed, NYT reports; the agencies found the intrusion. (The Hindu,
   The Economic Times)
5. **WHO evacuates Ebola staff from Congo hospital** — The team sheltered
   three days in a maternity ward in Ituri amid fighting; 5,775 dead in
   the outbreak. (Arab News, UN News)
6. **Putin vows retaliation for refinery strikes** — Calls the response
   "inevitable" as drone attacks cut Russian refining by 45% since late
   October. (Reuters, Al Jazeera)

## How it runs

`main.ts` (Node 22, zero dependencies) copies the committed `entry.png`
to `/output/entry.png`, checking the PNG magic and the 1 MiB cap first,
so two runs write identical bytes with no network and no randomness.
