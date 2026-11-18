#!/usr/bin/env python3
"""Generate the broadsheet front page for 17 November 2026 world news.

Draws a dense classic newspaper front page with PIL, deterministically:
same input -> same bytes every run. Output: entry.png, 1024x1024.
Layout: masthead, lead story with bridge panel, locator-map strip,
four columns of short headed stories, day-in-numbers strip, footer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 90, 86)
RULE = (40, 40, 40)
BLUE = (38, 70, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 72)
F_MAST_SUB = font("DejaVuSans.ttf", 14)
F_DATE = font("DejaVuSans-Bold.ttf", 14)
F_KICK = font("DejaVuSans-Bold.ttf", 12)
F_LEAD = font("DejaVuSerif-Bold.ttf", 38)
F_LEAD_DECK = font("DejaVuSerif.ttf", 16)
F_SEC = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSerif-Bold.ttf", 13)
F_DECK = font("DejaVuSerif.ttf", 10)
F_CAP = font("DejaVuSans.ttf", 10)
F_NUM = font("DejaVuSerif-Bold.ttf", 20)
F_NUMLAB = font("DejaVuSans-Bold.ttf", 9)
F_FOOT = font("DejaVuSans.ttf", 10)

# ---------------------------------------------------------------- stories
# (headline, deck) -- each happened or was first reported on Tuesday
# 17 November 2026, per BBC, APEC/ASEAN releases and major outlets.
WORLD = [
    ("West urges Israel to open Gaza crossings",
     "Four Western allies demand aid access."),
    ("Settlers shoot dead Palestinian woman, 72",
     "Killed near Jericho, ministry says."),
    ("Houthis advance as Yemeni troops fall back",
     "Troops quit Red Sea coast to defend Aden."),
    ("Japan scrambles jets as Russian planes intrude",
     "Tokyo protests the airspace violation."),
    ("Russian military plane crashes, 19 killed",
     "Blamed on suspected fault in Kemerovo."),
    ("Sudan RSF drone strikes on El Obeid condemned",
     "Monitors: may be war crimes."),
    ("Moldova: Russian drone flew over Chisinau",
     "Sandu: drone crossed capital's airspace."),
]
ASIA = [
    ("Shenzhen hosts APEC as leaders gather",
     "CEO Summit opens; leaders meet 18-19 Nov."),
    ("Trump, Xi and Putin to meet in Shenzhen",
     "First three-way summit set for Thursday."),
    ("Trump leaves ASEAN summit for China",
     "Wraps Manila meetings, flies to Shenzhen."),
    ("Xi pushes open trade at Shenzhen summit",
     "Xi champions open markets in Shenzhen."),
    ("Modi lands in Manila for ASEAN summits",
     "PM joins India-ASEAN and East Asia summits."),
    ("India and Japan hold 2+2 defence talks",
     "Fourth round of dialogue opens in Tokyo."),
    ("Mongolian president resigns in scandal",
     "Khurelsukh quits amid corruption probe."),
]
ECON = [
    ("US curbs remote Chinese use of AI chips",
     "Rules tightened; Beijing vows a response."),
    ("Nvidia spy scandal clouds Trump-Xi talks",
     "China fears tighter US chip curbs."),
    ("Disney revenue jumps 16% to $25.9bn",
     "Profits nearly double on sports strength."),
    ("Tanker fires in Hormuz reach fourth in a day",
     "Ships hit as Iran keeps strait closed."),
]
TECH = [
    ("Ten nations sign AI supply-chain pact",
     "US, India and eight others sign the pact."),
    ("UN climate chief warns AI on energy use",
     "Urged to curb power use, share the gains."),
    ("Disney to fold Hulu into Disney+ in Dec.",
     "Live TV joins flagship app in December."),
    ("ESPN confirms interest in World Series",
     "Chairman calls it 'a marquee event'."),
]
SPORT = [
    ("India chase 10th SAFF title vs Pakistan",
     "Final vs Pakistan in Dhaka today."),
    ("ICC sets men's event windows to 2035",
     "India to host 2029 Trophy, co-host 2031."),
    ("Major League Volleyball unveils 2027 TV deal",
     "Four networks to carry record 140 matches."),
]
CULTURE = [
    ("Depardieu admits sex assault charge",
     "Actor drops appeal, pleads guilty in Paris."),
    ("US loses measles-free status after 26 years",
     "5,400+ cases, 10 deaths as status ends."),
    ("Man charged over attack on US plane in Ireland",
     "Aircraft destroyed while parked."),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
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


def draw_rule(d, x0, y, x1, wdt=1):
    d.line([(x0, y), (x1, y)], fill=RULE, width=wdt)


def draw_section(d, x, y, width, title, items):
    """Section header + stacked stories; returns y below the block."""
    d.rectangle([x, y, x + width, y + 21], fill=INK)
    d.text((x + 6, y + 4), title, font=F_SEC, fill=PAPER)
    y += 29
    for head, deck in items:
        for ln in wrap(d, head, F_HEAD, width):
            d.text((x, y), ln, font=F_HEAD, fill=INK)
            y += 15
        for ln in wrap(d, deck, F_DECK, width):
            d.text((x, y), ln, font=F_DECK, fill=(58, 58, 54))
            y += 12
        y += 4
        draw_rule(d, x, y, x + width, 1)
        y += 6
    return y


def draw_bridge(d, x, y, w, h):
    """Stylised Kerch Strait bridge with a broken span and smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 140, 160))
    d.line([(x + 6, y + h - 34), (x + w - 6, y + h - 34)], fill=INK, width=4)
    for tx in (x + 40, x + w - 52):
        d.line([(tx, y + 12), (tx, y + h - 34)], fill=INK, width=4)
        d.line([(tx - 16, y + 12), (tx + 16, y + 12)], fill=INK, width=3)
        d.line([(tx, y + 14), (tx - 34, y + h - 34)], fill=GREY, width=1)
        d.line([(tx, y + 14), (tx + 34, y + h - 34)], fill=GREY, width=1)
    mid = x + w // 2
    d.line([(mid - 34, y + h - 34), (mid - 8, y + h - 18)], fill=INK, width=4)
    d.line([(mid + 8, y + h - 18), (mid + 34, y + h - 34)], fill=INK, width=4)
    for cx, cy, r in ((mid - 14, y + 26, 12), (mid + 4, y + 16, 15),
                      (mid + 22, y + 28, 10)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 148))
    d.text((x + 6, y + h - 20), "KERCH STRAIT  •  UKRAINE STRIKE",
           font=F_CAP, fill=(238, 238, 236))


def draw_map_strip(d, x, y, w, h):
    """Stylised world locator map: flat landmass blobs, red event dots."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    land = (198, 205, 190)
    blobs = [
        (8, 16, 150, 44), (150, 20, 210, 38), (30, 50, 110, 74),
        (300, 16, 372, 44), (318, 44, 400, 86), (404, 14, 560, 54),
        (452, 52, 520, 78), (540, 24, 640, 54), (600, 54, 668, 76),
        (560, 72, 616, 88),
    ]
    for bx0, by0, bx1, by1 in blobs:
        d.ellipse([x + bx0, y + by0, x + bx1, y + by1], fill=land)
    spots = [
        ("CRIMEA", 0.52, 0.28), ("SHENZHEN", 0.86, 0.52),
        ("MANILA", 0.90, 0.66), ("GAZA", 0.55, 0.42),
        ("YEMEN", 0.615, 0.68), ("BAHRAIN", 0.585, 0.50),
        ("TOKYO", 0.93, 0.34), ("MONGOLIA", 0.80, 0.30),
    ]
    for label, fx, fy in spots:
        px, py = x + int(w * fx), y + int(h * fy)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + 6, py - 6), label, font=F_CAP, fill=INK)
    d.text((x + 8, y + 5), "WHERE THE DAY HAPPENED", font=F_KICK, fill=BLUE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    X1, X2 = M, W - M
    y = 16

    # ---- masthead ------------------------------------------------------
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, y), title, font=F_MAST, fill=INK)
    y += 86
    d.text((M, y), "ONE DAY'S NEWS, IN FULL", font=F_MAST_SUB, fill=GREY)
    tag = "ALL THE WORLD'S NEWS  •  ONE PAGE"
    d.text((X2 - d.textlength(tag, font=F_MAST_SUB), y), tag,
           font=F_MAST_SUB, fill=GREY)
    y += 22
    draw_rule(d, M, y, X2, 3)
    y += 7
    d.text((M, y), "TUESDAY, 17 NOVEMBER 2026", font=F_DATE, fill=INK)
    mid = "No. 321  •  SHENZHEN  •  MANILA  •  KYIV  •  GAZA"
    d.text(((W - d.textlength(mid, font=F_DATE)) / 2, y), mid,
           font=F_DATE, fill=GREY)
    d.text((X2 - d.textlength("PRICE: ONE DAY", font=F_DATE), y),
           "PRICE: ONE DAY", font=F_DATE, fill=INK)
    y += 22
    draw_rule(d, M, y, X2, 1)
    y += 9

    # ---- lead story ----------------------------------------------------
    d.text((M, y), "UKRAINE WAR  •  LEAD STORY", font=F_KICK, fill=RED)
    y += 19
    lead_top = y
    lead_head = "UKRAINE STRIKES CRIMEAN BRIDGE; SPAN PARTLY COLLAPSES"
    for ln in wrap(d, lead_head, F_LEAD, X2 - M - 252):
        d.text((M, y), ln, font=F_LEAD, fill=INK)
        y += 44
    lead_deck = ("Kyiv hails an \u201cunprecedented\u201d drone and missile attack on the "
                 "strategic bridge to occupied Crimea; Moscow says its forces "
                 "downed a record number of drones and struck Kyiv bridges.")
    ly = y + 2
    for ln in wrap(d, lead_deck, F_LEAD_DECK, X2 - M - 252):
        d.text((M, ly), ln, font=F_LEAD_DECK, fill=(48, 48, 44))
        ly += 21
    draw_bridge(d, X2 - 240, lead_top - 19, 240, 148)
    y = max(ly, lead_top + 129) + 8
    draw_rule(d, M, y, X2, 2)
    y += 11

    # ---- map strip -----------------------------------------------------
    map_h = 84
    draw_map_strip(d, M, y, X2 - M, map_h)
    y += map_h + 11
    draw_rule(d, M, y, X2, 1)
    y += 9
    col_top = y

    # ---- four-column grid ----------------------------------------------
    gap = 12
    col_w = (X2 - M - 3 * gap) // 4
    cx = [M + i * (col_w + gap) for i in range(4)]
    ends = []
    ends.append(draw_section(d, cx[0], col_top, col_w, "WORLD", WORLD))
    ends.append(draw_section(d, cx[1], col_top, col_w,
                             "ASIA & THE SUMMITS", ASIA))
    e3 = draw_section(d, cx[2], col_top, col_w, "ECONOMY", ECON)
    e3 = draw_section(d, cx[2], e3 + 2, col_w, "CULTURE & HEALTH", CULTURE)
    ends.append(e3)
    e4 = draw_section(d, cx[3], col_top, col_w, "TECHNOLOGY", TECH)
    e4 = draw_section(d, cx[3], e4 + 2, col_w, "SPORT", SPORT)
    ends.append(e4)
    print("column end y:", ends, "limit:", H - 92)

    # ---- day in numbers -------------------------------------------------
    ny = H - 92
    draw_rule(d, M, ny, X2, 2)
    ny += 8
    d.text((M, ny), "THE DAY IN NUMBERS", font=F_KICK, fill=RED)
    ny += 19
    nums = [("19", "killed in Russian\nmilitary plane crash"),
            ("5,400+", "US measles cases\nas status is lost"),
            ("1,000", "at APEC CEO Summit\nin Shenzhen"),
            ("21", "APEC economies\nmeeting in China"),
            ("4", "tanker fires in the\nStrait of Hormuz"),
            ("26", "years of US measles-\nfree status ended")]
    nw = (X2 - M) // 6
    for i, (n, lab) in enumerate(nums):
        nx = M + i * nw
        d.text((nx, ny), n, font=F_NUM, fill=INK)
        ly2 = ny + 26
        for ln in lab.split("\n"):
            d.text((nx, ly2), ln, font=F_NUMLAB, fill=GREY)
            ly2 += 12

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
