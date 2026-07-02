#!/usr/bin/env bash
# hyprwheel installer - copies the script, seeds config, prints the Hyprland bind.
set -euo pipefail
cd "$(dirname "$0")"

# deps
for dep in python3 hyprctl; do
    command -v "$dep" >/dev/null || { echo "missing: $dep"; exit 1; }
done
python3 - <<'EOF' || { echo "missing python deps: install gtk3, gtk-layer-shell, python-gobject, python-cairo"; exit 1; }
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, GtkLayerShell
EOF

# files
install -Dm755 hyprwheel "$HOME/.local/bin/hyprwheel"
if [ ! -f "$HOME/.config/hyprwheel/config.json" ]; then
    install -Dm644 config.example.json "$HOME/.config/hyprwheel/config.json"
    echo "seeded ~/.config/hyprwheel/config.json"
fi

BIND='bindn = , mouse:273, exec, ~/.local/bin/hyprwheel --desktop'
BINDINGS="$HOME/.config/hypr/bindings.conf"
if [ -f "$BINDINGS" ] && ! grep -qF "hyprwheel" "$BINDINGS"; then
    read -rp "Add right-click bind to $BINDINGS? [y/N] " yn
    if [ "${yn,,}" = "y" ]; then
        printf '\n# hyprwheel: radial launcher on right-click over empty desktop\n%s\n' "$BIND" >> "$BINDINGS"
        hyprctl reload >/dev/null 2>&1 || true
        echo "bind added + config reloaded"
        exit 0
    fi
fi
echo "add this to your hyprland config:"
echo "  $BIND"
