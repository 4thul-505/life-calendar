#!/usr/bin/env python3
from datetime import date, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ═══════════════════════════════════════
#  ⚙️  CHANGE THESE TO YOUR OWN VALUES
# ═══════════════════════════════════════
BIRTHDATE   = date(2007, 5, 29)   # ← your birthdate
LIFE_YEARS  = 80                   # ← life expectancy
W, H        = 1920, 1080           # ← your screen resolution

# GNOME panel offsets — wallpaper is 1920x1080 but panels sit on top
# Top panel  ≈ 32px
# Bottom dock ≈ 72px
# Add extra padding so nothing touches panel edges
TOP_PANEL   = 52
BOT_DOCK    = 85

# ═══════════════════════════════════════
#  CALCULATIONS
# ═══════════════════════════════════════
today     = date.today()
birth_str = BIRTHDATE.strftime("%B %-d / %Y").upper()

# Build a lookup: for each (year_idx, week_idx) cell,
# is it lived or not?
# year_idx 0 = first year of life (birth → 1st birthday)
# week_idx 0..51 = weeks within that year
def cell_start(year_idx, week_idx):
    """Return the date when this cell starts."""
    return BIRTHDATE + timedelta(weeks = year_idx * 52 + week_idx)

# Current position: how many total weeks lived
# using exact calendar — count from birthday
total_days_lived = (today - BIRTHDATE).days
weeks_lived      = total_days_lived // 7   # total weeks completed

# For display: exact years + weeks
years_lived  = 0
temp         = BIRTHDATE
while True:
    next_bday = date(temp.year + 1, temp.month, temp.day)
    if next_bday > today:
        break
    years_lived += 1
    temp = next_bday
# weeks since last birthday
weeks_in_year = (today - temp).days // 7

total_weeks = LIFE_YEARS * 52
weeks_left  = total_weeks - weeks_lived
age_str     = f"AGE  {years_lived}Y  {weeks_in_year}W"

# ═══════════════════════════════════════
#  COLORS
# ═══════════════════════════════════════
BG            = (13, 18, 42)
FUTURE_FILL   = (22, 30, 58)
FUTURE_BORDER = (38, 50, 85)
TEXT          = (215, 220, 238)
DIM           = (95, 108, 145)

GRADIENT = [
    (255,  55, 125),
    (255, 110,  45),
    (248, 190,  40),
    (155, 210,  65),
    (55,  200, 150),
    (50,  145, 215),
    (80,   95, 190),
]

def lerp(stops, t):
    t  = max(0.0, min(1.0, t))
    n  = len(stops) - 1
    fi = t * n
    lo = int(fi)
    hi = min(lo + 1, n)
    f  = fi - lo
    return tuple(int(stops[lo][i] + (stops[hi][i] - stops[lo][i]) * f) for i in range(3))

# ═══════════════════════════════════════
#  LAYOUT
#  Header zone: TOP_PANEL+8 → TOP_PANEL+90
#  Grid zone:   TOP_PANEL+90 → H-BOT_DOCK-10
# ═══════════════════════════════════════
COLS = 52
ROWS = LIFE_YEARS

PAD_LEFT  = 120
PAD_RIGHT = 55

HEADER_TOP = TOP_PANEL + 8      # 40  — where header text starts
HEADER_BOT = TOP_PANEL + 110    # more space for counter label
XLBL_H     = 18                 # x-axis label height above grid

GY = HEADER_BOT + XLBL_H       # grid top y = 138
GB = H - BOT_DOCK - 12         # grid bottom y = 996

GX = PAD_LEFT                  # grid left x  = 120
GR = W - PAD_RIGHT             # grid right x = 1865

avail_w = GR - GX              # 1745
avail_h = GB - GY              # 858

CELL_W = avail_w // COLS       # 33
CELL_H = avail_h // ROWS       # 10

GRID_W = CELL_W * COLS
GRID_H = CELL_H * ROWS

BOX_W = CELL_W - 3
BOX_H = CELL_H - 2

# ═══════════════════════════════════════
#  FONTS
# ═══════════════════════════════════════
def font(name, size):
    for p in [f"/usr/share/fonts/truetype/dejavu/{name}", name]:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

f_counter = font("DejaVuSans-Bold.ttf", 55)
f_heading = font("DejaVuSans-Bold.ttf", 16)
f_label   = font("DejaVuSans.ttf",      11)
f_tiny    = font("DejaVuSans.ttf",       9)

# ═══════════════════════════════════════
#  CANVAS
# ═══════════════════════════════════════
img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════
#  HEADER LEFT — "WEEK OF YEAR"
# ═══════════════════════════════════════
draw.text((GX, HEADER_TOP), "WEEK OF YEAR", fill=TEXT, font=f_heading)

arr_y  = HEADER_TOP + 26
arr_x2 = GX + 210
draw.line([(GX, arr_y), (arr_x2, arr_y)], fill=DIM, width=1)
draw.polygon([(arr_x2, arr_y-4), (arr_x2+9, arr_y), (arr_x2, arr_y+4)], fill=DIM)
draw.text((GX + 4, arr_y + 6), birth_str, fill=DIM, font=f_tiny)

# age display below arrow
draw.text((GX + 4, arr_y + 20), age_str, fill=TEXT, font=f_label)

# ═══════════════════════════════════════
#  HEADER RIGHT — weeks counter
#
#  Structure (top to bottom):
#    [line_y]  dot ———————————— line   "OPT. PERSONALIZED DATE" (right-aligned above line)
#    [num_y]   3180
#    [sub_y]   WEEKS LEFT UNTIL 80
# ═══════════════════════════════════════
RB_LEFT  = W - PAD_RIGHT - 295    # 1570
RB_RIGHT = W - PAD_RIGHT          # 1865

# connector line sits at HEADER_TOP + 10
line_y = HEADER_TOP + 10

draw.ellipse([(RB_LEFT - 8, line_y - 3), (RB_LEFT, line_y + 3)], fill=DIM)
draw.line([(RB_LEFT, line_y), (RB_RIGHT, line_y)], fill=DIM, width=1)

# "OPT. PERSONALIZED DATE" — right-aligned, above the line
opt = "OPT. PERSONALIZED DATE"
ob  = draw.textbbox((0, 0), opt, font=f_tiny)
ow  = ob[2] - ob[0]
draw.text((RB_RIGHT - ow, line_y - 13), opt, fill=DIM, font=f_tiny)

# big number below the line
num_y = line_y + 8
draw.text((RB_LEFT, num_y), str(weeks_left), fill=TEXT, font=f_counter)

# "WEEKS LEFT UNTIL 80" — use actual rendered bbox to place it below the number
nb    = draw.textbbox((RB_LEFT, num_y), str(weeks_left), font=f_counter)
sub_y = nb[3] + 5
draw.text((RB_LEFT, sub_y), "WEEKS LEFT UNTIL 80", fill=DIM, font=f_label)

# ═══════════════════════════════════════
#  X-AXIS — week numbers
# ═══════════════════════════════════════
for c in range(COLS):
    x   = GX + c * CELL_W
    num = str(c + 1)
    bb  = draw.textbbox((0, 0), num, font=f_tiny)
    tw  = bb[2] - bb[0]
    draw.text((x + (BOX_W - tw) // 2, GY - 14), num, fill=DIM, font=f_tiny)

# ═══════════════════════════════════════
#  Y-AXIS — year numbers + rotated label
# ═══════════════════════════════════════
for r in range(ROWS):
    if r % 5 == 0:
        y   = GY + r * CELL_H
        num = str(r)   # 0-indexed like the online counter
        bb  = draw.textbbox((0, 0), num, font=f_tiny)
        tw  = bb[2] - bb[0]
        draw.text((GX - tw - 8, y + (BOX_H - 9) // 2), num, fill=DIM, font=f_tiny)

lbl  = Image.new("RGBA", (160, 14), (0, 0, 0, 0))
ld   = ImageDraw.Draw(lbl)
ld.text((0, 0), "NUMBER OF YEARS", fill=(*TEXT, 180), font=f_tiny)
rot  = lbl.rotate(90, expand=True)
lx   = 18
ly   = GY + (GRID_H - rot.height) // 2
img.paste(rot, (lx, ly), rot)

ax  = lx + rot.width + 5
ay1 = GY + 10
ay2 = GY + GRID_H - 10
draw.line([(ax, ay1), (ax, ay2)], fill=DIM, width=1)
draw.polygon([(ax-3, ay2-7), (ax, ay2+3), (ax+3, ay2-7)], fill=DIM)

# ═══════════════════════════════════════
#  GRID
# ═══════════════════════════════════════
for r in range(ROWS):
    t     = r / (ROWS - 1)
    color = lerp(GRADIENT, t)
    # start date of this year-row (r-th birthday)
    try:
        row_start = date(BIRTHDATE.year + r, BIRTHDATE.month, BIRTHDATE.day)
    except ValueError:
        row_start = date(BIRTHDATE.year + r, BIRTHDATE.month, BIRTHDATE.day - 1)

    for c in range(COLS):
        x = GX + c * CELL_W
        y = GY + r * CELL_H
        # this cell starts at row_start + c weeks
        cell_date = row_start + timedelta(weeks=c)
        if cell_date < today:
            draw.rectangle([x, y, x + BOX_W, y + BOX_H], fill=color)
        else:
            draw.rectangle([x, y, x + BOX_W, y + BOX_H],
                           fill=FUTURE_FILL, outline=FUTURE_BORDER)

# ═══════════════════════════════════════
#  SAVE
# ═══════════════════════════════════════
out = Path.home() / "life_calendar.png"
img.save(out)
print(f"✓ {out}")
print(f"  header zone : y={HEADER_TOP} → {HEADER_BOT}")
print(f"  grid zone   : y={GY} → {GY+GRID_H}  (dock starts at {H-BOT_DOCK})")
print(f"  cell        : {CELL_W}×{CELL_H}  |  grid {GRID_W}×{GRID_H}")
print(f"  weeks lived : {weeks_lived}  |  weeks left : {weeks_left}")
