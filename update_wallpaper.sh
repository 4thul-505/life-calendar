#!/bin/bash
# Life Calendar — auto update wallpaper
# Works on any Linux machine with GNOME

SCRIPT="$(dirname "$0")/life_calendar.py"
WALLPAPER="$HOME/life_calendar.png"

# Delete old wallpaper
rm -f "$WALLPAPER"

# Generate new one
python3 "$SCRIPT"

# Set as wallpaper (GNOME)
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"
gsettings set org.gnome.desktop.background picture-options "zoom"
gsettings set org.gnome.desktop.background picture-uri ""
sleep 1
gsettings set org.gnome.desktop.background picture-uri "file://$WALLPAPER"
gsettings set org.gnome.desktop.background picture-uri-dark "file://$WALLPAPER"

echo "✓ Wallpaper updated"
