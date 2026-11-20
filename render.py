#!/usr/bin/env python3
"""Render the news-image-20261120 entry: a broadsheet front page, 'THE WORLD TODAY',
summing up Friday 20 November 2026. Drawn fresh with PIL. Output: entry.png (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (20, 20, 20)
RED = (163, 22, 33)
GREY = (90, 86, 76)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- borders ----
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

MX = 38                      # content margin
CW = W - 2 * MX              # 948 content width

# ---- masthead ----
y = 32
f = font(SANS_B, 18)
t = "THE WORLD IN ONE IMAGE"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=GREY)
y = 52
f = font(SERIF_B, 76)
t = "THE WORLD TODAY"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
y = 138
d.line([(MX, y), (W - MX, y)], fill=INK, width=2)
y = 146
f = font(SANS_B, 25)
t = "FRIDAY, 20 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
y = 180
d.line([(MX, y), (W - MX, y)], fill=RED, width=5)

# ---- LEAD: ICJ Myanmar ruling ----
y = 194
LEAD_W = 636
f = font(SANS_B, 20)
d.text((MX, y), "THE HAGUE  ·  THE WORLD COURT", font=f, fill=RED)
y += 28
f = font(SERIF_B, 44)
lines = wrap(d, "MYANMAR COMMITTED GENOCIDE, UN COURT RULES", f, LEAD_W)
y = draw_lines(d, lines, MX, y, f, INK, 50)
y += 6
f = font(SANS, 21)
lines = wrap(d, "Judges rule 9–6: the 2017 crackdown on the Rohingya was genocide — the first state ever convicted.", f, LEAD_W)
y = draw_lines(d, lines, MX, y, f, INK, 26)
lead_bottom = y

# scales-of-justice motif, right of the lead
PX0, PY0 = 700, 196
PX1 = 986
PY1 = lead_bottom + 6
d.rectangle([PX0, PY0, PX1, PY1], outline=INK, width=2)
cx = (PX0 + PX1) // 2
top = PY0 + 22
bot = PY1 - 46
d.line([(cx, top + 8), (cx, bot)], fill=INK, width=5)                    # post
d.ellipse([cx - 7, top - 6, cx + 7, top + 8], fill=INK)                   # finial
d.line([(PX0 + 28, top + 30), (PX1 - 28, top + 30)], fill=INK, width=5)  # beam
for pan_x in (PX0 + 62, PX1 - 62):
    d.line([(pan_x, top + 30), (pan_x, top + 100)], fill=INK, width=3)
    d.line([(pan_x - 32, top + 72), (pan_x, top + 100)], fill=INK, width=3)
    d.line([(pan_x + 32, top + 72), (pan_x, top + 100)], fill=INK, width=3)
    d.arc([pan_x - 32, top + 72, pan_x + 32, top + 122], 0, 180, fill=INK, width=4)
d.line([(PX0 + 40, bot), (PX1 - 40, bot)], fill=INK, width=5)             # base
f = font(SERIF, 17)
t = "The Peace Palace, The Hague"
d.text((PX0 + (PX1 - PX0 - d.textlength(t, font=f)) / 2, PY1 - 34), t, font=f, fill=GREY)

y = max(lead_bottom, PY1) + 10
d.line([(MX, y), (W - MX, y)], fill=INK, width=2)
y += 12

# ---- two-column rows ----
COLW = 456
RX = MX + COLW + 36  # right column x = 530

def column(x, y, kicker, headline, deck):
    f = font(SANS_B, 19)
    d.text((x, y), kicker, font=f, fill=RED)
    y += 27
    f = font(SERIF_B, 31)
    lines = wrap(d, headline, f, COLW)
    y = draw_lines(d, lines, x, y, f, INK, 36)
    y += 5
    f = font(SANS, 19)
    lines = wrap(d, deck, f, COLW)
    y = draw_lines(d, lines, x, y, f, INK, 24)
    return y

y0 = y
yL = column(MX, y0, "INDIA  ·  CYCLONE AKVAN",
            "AKVAN SLAMS INTO ODISHA",
            "Severe storm crosses the coast near Gopalpur at noon; more than 100,000 people moved to shelters as winds gust to 110 km/h.")
yR = column(RX, y0, "WASHINGTON  ·  IRAN",
            "TRUMP: NO RUSH ON IRAN",
            "\u201cWe\u2019ll see what happens after Jan 1,\u201d the president says, pushing any decision on new strikes into 2027.")
y = max(yL, yR) + 10
d.line([(MX, y), (W - MX, y)], fill=INK, width=2)
d.line([(MX + COLW + 18, y0), (MX + COLW + 18, y - 10)], fill=GREY, width=1)
y += 12

y0 = y
yL = column(MX, y0, "CULTURE  ·  GAMES",
            "GTA VI SALES TOP $1.8BN",
            "Rockstar\u2019s epic outgrosses The Odyssey\u2019s entire global run, with 17 million copies sold.")
yR = column(RX, y0, "EUROPE  ·  UKRAINE",
            "EUROPE READY FOR RUSSIA TALKS",
            "European leaders say they are prepared to negotiate an end to the war in Ukraine.")
y = max(yL, yR) + 10
d.line([(MX, y), (W - MX, y)], fill=INK, width=2)
d.line([(MX + COLW + 18, y0), (MX + COLW + 18, y - 10)], fill=GREY, width=1)
y += 12

# ---- ALSO TODAY strip ----
f = font(SANS_B, 19)
d.text((MX, y), "ALSO TODAY", font=f, fill=RED)
y += 27
fB = font(SANS_B, 19)
fN = font(SANS, 19)
items = [
    ("VOYAGER 1 A LIGHT-DAY AWAY — ",
     "NASA\u2019s 1977 probe is 16bn miles out; a signal takes a day each way."),
    ("HAYABUSA2 DROPS ASTEROID LANDING — ",
     "Engine trouble forces Japan\u2019s probe to change course."),
]
strip_bottom = y
for x, (bold, rest) in zip((MX, RX), items):
    # word-by-word wrap, tracking bold vs regular segments
    words = [(w, True) for w in bold.split()] + [(w, False) for w in rest.split()]
    lines, cur, cur_w = [], [], 0.0
    for w, b in words:
        fnt = fB if b else fN
        ww = d.textlength(w + " ", font=fnt)
        if cur and cur_w + ww > COLW:
            lines.append(cur)
            cur, cur_w = [], 0.0
        cur.append((w, b))
        cur_w += ww
    if cur:
        lines.append(cur)
    yy = y
    for ln in lines:
        xx = x
        for w, b in ln:
            fnt = fB if b else fN
            d.text((xx, yy), w, font=fnt, fill=INK)
            xx += d.textlength(w + " ", font=fnt)
        yy += 24
    strip_bottom = max(strip_bottom, yy)
y = strip_bottom + 8
d.line([(MX, y), (W - MX, y)], fill=INK, width=2)

# ---- footer ----
y += 12
f = font(SANS, 17)
t = "Sources: BBC  ·  Reuters  ·  The Hindu  ·  NASA  ·  IMD  ·  Space  —  Friday 20 November 2026"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=GREY)
print("footer y:", y, "(canvas 1024, inner border 1001)")
assert y + 20 < 1001, "OVERFLOW: footer past inner border"
img.save("entry.png", optimize=True)
print("entry.png bytes:", os.path.getsize("entry.png"))
