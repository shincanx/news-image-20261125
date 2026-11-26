# Wednesday 25 November 2026 in One Picture

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261125)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](main.py)

Entry for the [make.fun bounty **news-image-20261125**](https://make.fun/bounty/news-image-20261125)
— *"Sum up 25 November's world news in one image"* ($100 prize pool).

## What it is

`main.py` (Python 3.13, PIL only, no network) draws a one-page newspaper
broadsheet — **"THE WORLD IN ONE PAGE"** — summing up Wednesday 25 November
2026 and writes it to `/output/entry.png` (1024×1024 PNG, under 1 MiB).

- **42 stories, 10 regions**, every one dated 25 November 2026 and labelled
  with its source (Reuters, AP, BBC, Al Jazeera, USTR, Ofgem, UN News,
  Euronews, Kyiv Independent, ABC News, Dawn, Science, Anadolu, Gartner).
- **Lead story:** the US proposes tariffs of up to 20% on 14 economies,
  with a "Why it matters" box.
- **4 drawn scenes:** a tariff container ship, Tiangong station with
  Shenzhou-24 docking (Pakistan's first astronaut), the Cairo tanker fire,
  and the stadium-size crater on asteroid Dimorphos.
- **Markets strip:** Kospi −6.2%, Taiex −4.8%, Nikkei −2.8%, Hang Seng −1.1%.
- **UTC timeline** of the day, and a "day in numbers" strip.
- Two stories whose sourcing is single-source are labelled **CLAIM**.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
```

Two runs produce byte-identical output (verified with sha256).

## Bounty

- Competition: https://make.fun/bounty/news-image-20261125
- Deadline: 2026-11-27T00:00:00Z
- Prize: $100 shared by the 50 highest-ranked entries
