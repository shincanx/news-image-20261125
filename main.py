#!/usr/bin/env python3
"""news-image-20261125: one-page broadsheet summing up the world news of
Wednesday 25 November 2026. Draws a 1024x1024 PNG with PIL only, no network,
fully deterministic. Writes to $MAKEFUN_OUTPUT_DIR/entry.png (or /output)."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

PAPER = (248, 244, 233)
INK = (25, 21, 18)
RED = (179, 39, 30)
BLUE = (29, 78, 137)
GOLD = (185, 138, 47)
GRAY = (107, 101, 90)
LIGHT = (239, 232, 214)
DARKBLUE = (16, 32, 54)
ORANGE = (214, 96, 20)
GREEN = (46, 110, 58)

F_SERIF = os.path.join(BASE, "DejaVuSerif-Bold.ttf")
F_BOLD = os.path.join(BASE, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(BASE, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, x, y, w, s, fnt, fill=INK):
    tw = draw.textlength(s, font=fnt)
    draw.text((x + (w - tw) / 2, y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- stories
# (headline, source, claim?) — every story happened / was first reported
# on Wednesday 25 November 2026.
COLUMNS = [
    [("NORTH AMERICA", [
        ("Nvidia +31.5% in a day as Huang returns as CEO", "Al Jazeera"),
        ("Wall St falls after rally: S&P -0.5%, Nasdaq -1.5%", "Al Jazeera"),
        ("Fulton County judge halts 2020 ballot handover", "NBC News"),
        ("Judge refuses long-term ban on pro-Trump ads", "NBC News"),
        ("Wrongly deported Salvadoran reaches Spain", "Euronews"),
        ("US Army detonates 5t of toxic explosives in Iowa", "Euronews"),
    ]),
     ("LATIN AMERICA", [
        ("Colombia frees 76 hostages after 17-hour siege", "BBC"),
     ]),
     ("EUROPE", [
        ("UK energy price cap to rise 26% to \u00a32,166", "Ofgem"),
        ("Greece: 14,000 march in Athens general strike", "Euronews"),
        ("Poland plans no-fly zone on Ukraine border", "Kyiv Independent"),
        ("Russian strikes kill 7; Kyiv hits 3 refineries", "Euronews"),
        ("Ukraine laser downs Russian drone in combat", "Kyiv Independent", True),
        ("Eurostar strike halts Paris-London trains", "Euronews"),
        ("EU coalition talks halt after EPP-far right vote", "Euronews"),
        ("EU approves new medicines rules to end shortages", "Euronews"),
     ])],
    [("MIDDLE EAST", [
        ("UN: new Gaza attacks point to \u2018atrocity crimes\u2019", "UN News"),
        ("UN aid chief lands in Yemen; millions hungry", "UN News"),
        ("Iraq opens its first Jewish museum in Baghdad", "Euronews"),
    ]),
     ("AFRICA", [
        ("Cairo fuel tanker fire kills 31, injures 21", "AP"),
        ("Ebola teams evacuated in DR Congo amid fighting", "UN News"),
        ("Gavi to buy 1.5m doses of candidate Ebola vaccine", "UN News"),
    ]),
     ("SOUTH ASIA", [
        ("Pakistan\u2019s first astronaut docks at Tiangong", "Reuters"),
        ("Karachi building collapse kills 3; 17 missing", "Dawn"),
        ("Shenzhou-24: one astronaut to stay a year", "Reuters"),
    ]),
     ("EAST ASIA", [
        ("Kospi -6.2%; Samsung -9.9%, SK Hynix -11.1%", "Al Jazeera"),
        ("Taiwan Taiex -4.8%; TSMC -3.6%, Foxconn -8.8%", "Al Jazeera"),
        ("Japan chipmakers dive: Tokyo Electron -12.5%", "Al Jazeera"),
        ("Seoul curbs programme selling as Kospi slides", "Anadolu"),
     ])],
    [("SOUTHEAST ASIA", [
        ("Flooded West Java gold mine: 9 dead, 17 trapped", "AP"),
    ]),
     ("OCEANIA", [
        ("Bowen \u2018frustrated\u2019 as COP31 ends with no deal", "ABC News"),
        ("Australia on track for 2030 climate target", "ABC News"),
    ]),
     ("SPACE & SCIENCE", [
        ("ESA\u2019s Hera finds stadium-size crater on asteroid", "Science"),
        ("Dimorphos \u2018tumbling\u2019 amid hundreds of boulders", "Science"),
        ("Global AI spending forecast at $2.7 trillion", "Gartner"),
    ]),
     ("GLOBAL", [
        ("COP31 collapses over fossil-fuel language", "ABC News"),
        ("Russia \u2018preparing nuclear satellite launch\u2019", "Euronews", True),
        ("Serbia skips Brussels summit; thaw via volleyball", "Euronews"),
        ("Riner: Ukraine \u2018is not France\u2019s war\u2019", "Euronews"),
    ]),
     ("CULTURE & BUSINESS", [
        ("Italy\u2019s young bell-ringers keep old craft alive", "Euronews"),
        ("Indra targets \u20ac12bn revenue by 2030", "Euronews"),
        ("Greece grows 1.8% but households still struggle", "Euronews"),
     ])],
]

TIMELINE = [
    ("00:27", "Shenzhou-24 docks"),
    ("03:31", "Kospi plunge"),
    ("07:10", "Mine toll: 9 dead"),
    ("09:23", "Karachi collapse"),
    ("09:56", "Hostages freed"),
    ("12:00", "UK cap +26%"),
    ("13:15", "Tariffs unveiled"),
    ("19:14", "Cairo toll: 31"),
]

NUMBERS = [
    ("31", "killed in Cairo tanker fire"),
    ("76", "hostages freed in Cartagena"),
    ("9", "dead in West Java mine flood"),
    ("6.2%", "Kospi fall in one day"),
    ("20%", "top tariff proposed by US"),
    ("\u00a32,166", "UK energy price cap from Jan"),
    ("1st", "Pakistani in orbit"),
]

# ---------------------------------------------------------------- drawing
def draw_ship(d, x, y, w, h):
    """Container ship under a tariff wall: the lead story, drawn."""
    d.rectangle([x, y, x + w, y + h], fill=(213, 232, 240))
    # sun
    d.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(240, 190, 60))
    # sea
    d.rectangle([x, y + 66, x + w, y + h], fill=(58, 110, 150))
    d.line([x, y + 66, x + w, y + 66], fill=(255, 255, 255), width=2)
    # hull
    d.polygon([(x + 18, y + 96), (x + w - 18, y + 96), (x + w - 44, y + 128),
               (x + 44, y + 128)], fill=(140, 30, 24))
    d.rectangle([x + 18, y + 96, x + w - 18, y + 104], fill=(90, 18, 14))
    # containers
    cols = [(214, 96, 20), (29, 78, 137), (185, 138, 47), (46, 110, 58),
            (214, 96, 20), (29, 78, 137)]
    for i, c in enumerate(cols):
        cx = x + 34 + i * 46
        d.rectangle([cx, y + 66, cx + 42, y + 94], fill=c, outline=(255, 255, 255))
        d.text((cx + 12, y + 72), "%", font=font(F_BOLD, 18), fill=(255, 255, 255))
    # bridge tower
    d.rectangle([x + w - 62, y + 44, x + w - 34, y + 96], fill=(240, 240, 240),
                outline=INK)
    d.rectangle([x + w - 62, y + 52, x + w - 34, y + 60], fill=(29, 78, 137))
    # waves
    for i in range(5):
        wx = x + 12 + i * 64
        d.arc([wx, y + 132, wx + 34, y + 146], 180, 360, fill=(255, 255, 255), width=2)


def draw_tiangong(d, x, y, w, h):
    """Tiangong station with Shenzhou docking, Earth below."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 12, 24))
    for i in range(26):
        sx = x + (i * 67) % w
        sy = y + (i * 41) % (h - 34)
        r = 1 if i % 3 else 2
        d.ellipse([sx, sy, sx + r, sy + r], fill=(255, 255, 255))
    # Earth arc
    d.ellipse([x - 60, y + h - 26, x + w + 60, y + h + 90], fill=(52, 110, 170))
    d.ellipse([x - 60, y + h - 26, x + w + 60, y + h + 90], outline=(120, 190, 230))
    # station core
    cx, cy = x + w // 2, y + h // 2 - 6
    d.rectangle([cx - 66, cy - 10, cx + 66, cy + 10], fill=(210, 210, 205),
                outline=(255, 255, 255))
    d.rectangle([cx - 22, cy - 16, cx + 22, cy + 16], fill=(180, 180, 175),
                outline=(255, 255, 255))
    # solar wings
    for sgn in (-1, 1):
        wx0 = cx + sgn * 70
        wx1 = cx + sgn * 148
        d.rectangle([min(wx0, wx1), cy - 14, max(wx0, wx1), cy + 14],
                    fill=(30, 70, 160), outline=(140, 180, 255))
        for gx in range(min(wx0, wx1) + 8, max(wx0, wx1), 16):
            d.line([gx, cy - 14, gx, cy + 14], fill=(140, 180, 255))
    # Shenzhou capsule docking on the right
    d.ellipse([cx + 66, cy - 8, cx + 96, cy + 8], fill=(230, 120, 40),
              outline=(255, 255, 255))
    d.polygon([(cx + 96, cy - 6), (cx + 112, cy), (cx + 96, cy + 6)],
              fill=(230, 120, 40))
    # label
    d.text((x + 8, y + h - 20), "SHENZHOU-24  •  14:35 UTC",
           font=font(F_BOLD, 9), fill=(255, 255, 255))


def draw_cairo_fire(d, x, y, w, h):
    """Night highway, tanker fire, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 18, 26))
    # skyline glow
    d.rectangle([x, y + h - 52, x + w, y + h], fill=(52, 44, 48))
    # road
    d.polygon([(x, y + h), (x + w, y + h), (x + w - 30, y + 58),
               (x + 30, y + 58)], fill=(40, 40, 44))
    for i in range(4):
        ry = y + 66 + i * 12
        rw = 14 + i * 10
        d.line([x + w // 2 - rw // 2, ry, x + w // 2 + rw // 2, ry],
               fill=(220, 200, 90), width=2)
    # cars
    for cx, cw in [(x + 52, 30), (x + w - 96, 34), (x + w // 2 - 46, 26)]:
        d.rectangle([cx, y + h - 34, cx + cw, y + h - 20], fill=(90, 110, 140),
                    outline=(255, 255, 255))
    # tanker on its side
    d.rectangle([x + 84, y + 66, x + 190, y + 92], fill=(200, 200, 200),
                outline=INK)
    d.ellipse([x + 96, y + 88, x + 112, y + 104], fill=INK)
    d.ellipse([x + 158, y + 88, x + 174, y + 104], fill=INK)
    # flames
    fx = x + w // 2 - 10
    d.polygon([(fx - 34, y + 78), (fx - 16, y + 22), (fx - 2, y + 52),
               (fx + 14, y + 10), (fx + 30, y + 46), (fx + 40, y + 78)],
              fill=(230, 120, 20))
    d.polygon([(fx - 18, y + 78), (fx - 8, y + 40), (fx + 4, y + 58),
               (fx + 16, y + 30), (fx + 24, y + 78)], fill=(250, 200, 40))
    # smoke
    for sx, sy, sr in [(fx - 30, y + 12, 12), (fx + 6, y + 4, 15),
                       (fx + 34, y + 14, 11)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 88, 92))
    d.text((x + 8, y + 6), "31 KILLED  •  21 INJURED",
           font=font(F_BOLD, 10), fill=(255, 220, 120))


def draw_asteroid(d, x, y, w, h):
    """Dimorphos with its stadium-size crater, Hera watching."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 20))
    for i in range(22):
        sx = x + (i * 83) % w
        sy = y + (i * 37) % h
        d.ellipse([sx, sy, sx + 1, sy + 1], fill=(255, 255, 255))
    # Didymos, big parent rock behind
    d.ellipse([x + w - 120, y - 46, x + w + 60, y + 86], fill=(110, 100, 92))
    d.ellipse([x + w - 120, y - 46, x + w + 60, y + 86], outline=(160, 150, 140))
    # Dimorphos
    cx, cy, r = x + 118, y + 62, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 142, 132))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(210, 200, 190))
    # the crater: as wide as the body itself
    d.ellipse([cx - 34, cy - 26, cx + 34, cy + 30], fill=(88, 80, 72))
    d.ellipse([cx - 34, cy - 26, cx + 34, cy + 30], outline=(60, 54, 48))
    d.ellipse([cx - 8, cy - 4, cx + 10, cy + 12], fill=(60, 54, 48))
    # boulders drifting around
    for bx, by, br in [(x + 40, y + 26, 4), (x + 210, y + 30, 3),
                       (x + 250, y + 88, 5), (x + 56, y + 96, 3),
                       (x + 292, y + 66, 4)]:
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(170, 162, 152))
    # Hera spacecraft
    hx, hy = x + w - 52, y + h - 26
    d.rectangle([hx - 8, hy - 5, hx + 8, hy + 5], fill=(220, 220, 220),
                outline=(255, 255, 255))
    d.rectangle([hx - 26, hy - 3, hx - 8, hy + 3], fill=(30, 70, 160))
    d.rectangle([hx + 8, hy - 3, hx + 26, hy + 3], fill=(30, 70, 160))
    d.text((x + 8, y + h - 18), "CRATER AS WIDE AS THE MOON ITSELF",
           font=font(F_BOLD, 9), fill=(255, 255, 255))

# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = font(F_SERIF, 46)
    f_kick = font(F_BOLD, 11)
    f_date = font(F_BOLD, 12)
    f_lead = font(F_BOLD, 27)
    f_deck = font(F_REG, 12)
    f_sec = font(F_BOLD, 11)
    f_head = font(F_BOLD, 11)
    f_src = font(F_REG, 9)
    f_small = font(F_REG, 9)
    f_tiny = font(F_BOLD, 8)

    # ---- masthead
    text_center(d, 0, 8, W, "T A R I F F S ,   T U M B L I N G   C H I P S   A N D   T I A N G O N G",
                f_kick, fill=RED)
    text_center(d, 0, 24, W, "THE WORLD IN ONE PAGE", f_title)
    text_center(d, 0, 76, W,
                "WEDNESDAY 25 NOVEMBER 2026   •   42 STORIES   •   10 REGIONS   •   ALL DATED 25 NOV 2026",
                f_date)
    d.line([24, 94, W - 24, 94], fill=INK, width=2)
    d.line([24, 98, W - 24, 98], fill=INK, width=1)

    # ---- lead story
    lx, lw = 24, 596
    d.text((lx, 108), "LEAD  —  TRADE", font=f_sec, fill=RED)
    d.text((lx, 128), "US proposes tariffs of up to 20%", font=f_lead, fill=INK)
    d.text((lx, 158), "on 14 economies", font=f_lead, fill=INK)
    deck = ("USTR chief Jamieson Greer acts after an 8-month probe into excess "
            "factory capacity. China faces up to 20%, others up to 18%.")
    y = 192
    for line in wrap(d, deck, f_deck, lw):
        d.text((lx, y), line, font=f_deck, fill=INK)
        y += 16
    # why it matters
    wy = 226
    d.rectangle([lx, wy, lx + lw, wy + 34], outline=RED, width=2)
    d.text((lx + 8, wy + 4), "WHY IT MATTERS:", font=f_sec, fill=RED)
    d.text((lx + 8, wy + 19),
           "Rebuilds Trump's tariff leverage on firmer legal ground.",
           font=f_small, fill=INK)
    # lead scene (drawn on its own layer so nothing bleeds out)
    sx, sw, sh = 648, 352, 158
    tmp = Image.new("RGB", (sw, sh), PAPER)
    draw_ship(ImageDraw.Draw(tmp), 0, 0, sw, sh)
    img.paste(tmp, (sx, 108))
    d.text((sx, 270), "Container ship under the new US tariffs (up to 20%).",
           font=f_small, fill=GRAY)

    # ---- three drawn scenes
    sy, ph, pw = 290, 96, 320
    panels = [
        (24, "TIANGONG — FIRST FOREIGN ASTRONAUT", draw_tiangong,
         "Pakistan's Zeeshan Ali, first Pakistani in orbit — Reuters"),
        (352, "CAIRO — TANKER FIRE KILLS 31", draw_cairo_fire,
         "Fuel tanker overturns on Ring Road; 21 injured — AP"),
        (680, "DIMORPHOS — STADIUM-SIZE CRATER", draw_asteroid,
         "ESA's Hera surveys the scar left by NASA's DART — Science"),
    ]
    for px, title, fn, cap in panels:
        d.text((px, sy), title, font=f_sec, fill=INK)
        tmp = Image.new("RGB", (pw, ph), PAPER)
        fn(ImageDraw.Draw(tmp), 0, 0, pw, ph)
        img.paste(tmp, (px, sy + 18))
        d.text((px, sy + 18 + ph + 4), cap, font=f_small, fill=GRAY)
    d.line([24, 424, W - 24, 424], fill=INK, width=1)

    # ---- markets strip
    d.text((24, 432), "MARKETS — AI DOUBTS SINK ASIAN CHIPS", font=f_sec, fill=RED)
    bars = [("KOSPI", -6.2), ("TAIEX", -4.8), ("NIKKEI", -2.8), ("HANG SENG", -1.1)]
    bx = 24
    for name, val in bars:
        d.text((bx, 450), name, font=f_tiny, fill=GRAY)
        d.rectangle([bx, 464, bx + 140, 472], fill=LIGHT, outline=GRAY)
        bw = int(140 * abs(val) / 6.2)
        d.rectangle([bx, 464, bx + bw, 472], fill=RED)
        d.text((bx + 146, 460), "%.1f%%" % val, font=f_sec, fill=RED)
        bx += 240
    d.text((24, 478), "Samsung -9.9%  •  SK Hynix -11.1%  •  Tokyo Electron -12.5%  •  Advantest -12.9%  •  TSMC -3.6%",
           font=f_small, fill=INK)
    d.text((24, 492),
           "THE DAY IN NUMBERS:  31 killed in Cairo  •  76 freed in Cartagena  •  9 dead in West Java mine  •  Kospi -6.2%  •  top tariff 20%  •  UK cap £2,166  •  1st Pakistani in orbit",
           font=f_small, fill=INK)
    d.line([24, 506, W - 24, 506], fill=INK, width=1)

    # ---- story grid
    gy = 514
    col_x = [24, 352, 680]
    col_w = 320
    for ci, col in enumerate(COLUMNS):
        x = col_x[ci]
        y = gy
        for region, stories in col:
            d.text((x, y), region, font=f_sec, fill=RED)
            d.line([x, y + 13, x + col_w, y + 13], fill=RED, width=1)
            y += 18
            for story in stories:
                headline, source = story[0], story[1]
                claim = len(story) > 2 and story[2]
                lines = wrap(d, headline, f_head, col_w)
                for line in lines:
                    d.text((x, y), line, font=f_head, fill=INK)
                    y += 12
                src = "— " + source + ("  •  CLAIM" if claim else "")
                d.text((x, y), src, font=f_src, fill=GRAY)
                y += 10
            y += 4

    # ---- UTC timeline
    ty = 914
    d.text((24, ty), "THE DAY IN UTC", font=f_sec, fill=RED)
    d.line([24, ty + 18, W - 24, ty + 18], fill=INK, width=2)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 40 + i * (944 // (n - 1))
        d.ellipse([cx - 4, ty + 14, cx + 4, ty + 22], fill=RED)
        lx0 = max(24, min(cx - 55, W - 24 - 110))
        text_center(d, lx0, ty + 26, 110, t, f_sec, fill=INK)
        for j, ln in enumerate(wrap(d, label, f_tiny, 104)):
            text_center(d, lx0, ty + 40 + j * 10, 110, ln, f_tiny, fill=GRAY)

    # ---- footer
    d.line([24, 984, W - 24, 984], fill=INK, width=1)
    d.text((24, 990),
           "Sources: Reuters • AP • BBC • Al Jazeera • USTR • Ofgem • UN News • SpaceNews • Euronews • Kyiv Independent • ABC News • Dawn • Science • Anadolu • Gartner",
           font=f_small, fill=GRAY)
    d.text((24, 1004),
           "Drawn scenes illustrate reported events. Every story above happened, or was first reported, on Wednesday 25 November 2026.",
           font=f_small, fill=GRAY)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    print(build())
