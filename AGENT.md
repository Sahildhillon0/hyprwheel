# hyprwheel — Agent Guide

GTA5-style radial app launcher for Hyprland. Single Python file, no build step, no daemon.

## Layout

| File | Purpose |
|---|---|
| `hyprwheel` | The entire app: GTK3 + Cairo + gtk-layer-shell radial menu (no `.py` extension — it's the installed binary) |
| `config.example.json` | Default 6-slice config; installed to `~/.config/hyprwheel/config.json` |
| `install.sh` | Copies script to `~/.local/bin`, seeds config, offers to append the Hyprland bind |
| `test_hyprwheel.py` | Self-check: slice hit-testing, desktop detection (mocked `hyprctl`), fallback resolution |

## How it works

- Triggered by `bindn = , mouse:273, exec, hyprwheel --desktop` in Hyprland config. `bindn` is non-consuming, so right-click still reaches windows.
- `--desktop` queries `hyprctl -j` (cursorpos/monitors/clients/layers) and exits silently unless the cursor is over empty desktop (no mapped client, no top/overlay layer surface).
- UI: one fullscreen transparent window on the OVERLAY layer, wheel drawn with Cairo at the (clamped) cursor position. Text/emoji rendered via PangoCairo — never Cairo's toy text API (no emoji fallback).
- `exec` entries in config are fallback chains; `resolve()` picks the first candidate whose binary exists. Launch is `subprocess.Popen(shell=True, start_new_session=True)` — do NOT switch to `hyprctl dispatch exec` (breaks on Lua-shimmed Hyprland setups).
- Single instance via pidfile `~/.cache/hyprwheel.pid`; a second invocation kills the first (toggle behavior).

## Rules

- Keep it ONE file with zero deps beyond gtk3, gtk-layer-shell, python-gobject, python-cairo. Portability across Arch/Hyprland setups is the point.
- GTK3 (not GTK4): gtk4-layer-shell is far less ubiquitous.
- Requires `gi.require_version` for Gtk, Gdk, GtkLayerShell, AND PangoCairo before import.

## Verify changes

```
python3 -m py_compile hyprwheel   # syntax
python3 test_hyprwheel.py         # logic self-check
./hyprwheel                       # live render (run again to close), screenshot with grim
hyprctl configerrors              # after any bind changes
```
