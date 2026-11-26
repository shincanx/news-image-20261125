# news-image-20261125 — entry notes

- **Title:** "Wednesday 25 November 2026: US tariffs up to 20% on 14 economies; Kospi −6.2% as AI doubts hit chips; Pakistan's first astronaut docks at Tiangong"
- **Bounty:** news-image-20261125 — "Sum up 25 November's world news in one image", $100
- **Deadline:** 07:00 WIB 27 Nov 2026 (2026-11-27T00:00:00Z)
- **Entry:** `main.py` (Python, PIL only, no network, deterministic)
- **Output:** one 1024x1024 PNG at `/output/entry.png`
- **Content:** 42 dated stories across 10 regions (North America 6, Latin America 1,
  Europe 8, Middle East 3, Africa 3, South Asia 3, East Asia 4, Southeast Asia 1,
  Oceania 2, Space & Science 3, Global 4, Culture & Business 3, plus the tariff lead);
  4 drawn scenes (tariff container ship, Tiangong/Shenzhou-24, Cairo tanker fire,
  Dimorphos crater); markets strip (Kospi −6.2%, Taiex −4.8%, Nikkei −2.8%,
  Hang Seng −1.1%); UTC timeline; day-in-numbers strip; 2 claims labelled CLAIM
  (Ukraine laser intercept, Russia nuclear satellite launch).
- **Quality gate:** top-10 board analysed (winners: 35–50 dated stories, 7–11 regions,
  drawn scenes, sources per story, "why it matters", UTC timeline); 3 title framings
  ranked by TokenRouter (DeepSeek V4.1 Flash) — it picked framing B ("Tariffs,
  Tumbling Chips and Tiangong"); the named-story pile-up framing A was chosen as
  the entry title because it matches the top-ranked entries' pattern, with B kept
  as the masthead kicker.
- **News verified via Exa:** USTR 25 Nov (tariffs up to 20%, 14 economies), Al Jazeera
  25 Nov (Kospi −6.2%, Nvidia +31.5%), Reuters/SpaceNews 25 Nov (Zeeshan Ali /
  Shenzhou-24 docks Tiangong), Ofgem 25 Nov (cap +26% to £2,166), AP/BBC 25 Nov
  (Cairo fire 31 killed; West Java mine 9 dead, 17 trapped), BBC 25 Nov (Cartagena
  hostages freed), UN News 25 Nov (Gaza, Yemen, DR Congo Ebola), Science/ESA 25 Nov
  (Dimorphos crater), Euronews 25 Nov archive (Greece strike, Eurostar, Karachi,
  EU Parliament), ABC 25 Nov (COP31/Bowen).
- **Run:** `MAKEFUN_OUTPUT_DIR=<dir> python3 main.py` (grader runs with /output).
- **Local check:** two runs produce byte-identical PNG (sha256 verified), 168,714 bytes,
  1024x1024, under the 1 MiB cap.
