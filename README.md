# 📅 Life Calendar Wallpaper

A Python script that generates a **life calendar wallpaper** (1920×1080) showing every week of your life as a grid — filled weeks are colored, future weeks are empty.

Inspired by the viral "weeks of your life" visualization. Auto-updates daily via cron.

![preview](preview.png)

---

## How it works

- Each **row** = 1 year of life (starting from age 0)
- Each **cell** = 1 week (7 days exactly)
- Filled cells = weeks you've already lived
- Empty cells = weeks remaining until age 80
- Gradient goes pink → orange → yellow → green → teal → blue across your lifetime

---

## Setup

### 1. Install dependency
```bash
pip install pillow
```

### 2. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/life-calendar
cd life-calendar
```

### 3. Set your birthdate
Open `life_calendar.py` and change this one line:
```python
BIRTHDATE = date(2000, 1, 1)  # ← change to your birthdate
```

### 4. Run it
```bash
python3 life_calendar.py
```

Output: `/home/YOUR_USERNAME/life_calendar.png`

### 5. Set as wallpaper (GNOME)
```bash
gsettings set org.gnome.desktop.background picture-uri ""
sleep 1
gsettings set org.gnome.desktop.background picture-uri "file:///home/YOUR_USERNAME/life_calendar.png"
```

---

## Auto-update daily (cron)

Edit `update_wallpaper.sh` and replace `bleak` with your username:
```bash
nano update_wallpaper.sh
```

Make it executable:
```bash
chmod +x update_wallpaper.sh
```

Add to crontab (runs every day at 6am):
```bash
crontab -e
```
Add this line:
```
0 6 * * * /home/YOUR_USERNAME/update_wallpaper.sh
```

---

## Dependencies
- Python 3
- [Pillow](https://pillow.readthedocs.io/)

---

## Tested on
- Ubuntu 24.04 LTS + GNOME (Xorg)

---

*Built by [4thul](https://github.com/4thul-505)*
