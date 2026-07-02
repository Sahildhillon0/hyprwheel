# hyprwheel

GTA5-style radial app launcher for [Hyprland](https://hypr.land). Right-click
on an empty spot of your desktop and a wheel pops up under your cursor —
pick a slice to launch your browser, terminal, file manager, or anything else.

- Single Python file, no daemon, no build step
- Opens **only** when the cursor is over empty desktop (windows and bars keep
  their normal right-click)
- App fallback chains: the first installed candidate wins, so one config works
  across machines (`alacritty` → `kitty` → `foot` → …)
- Missing apps show as dimmed slices
- Right-click again or press `Esc` to close

## Requirements

Available on virtually every Wayland setup (Arch package names shown):

```
pacman -S gtk3 gtk-layer-shell python-gobject python-cairo
```

Hyprland ≥ 0.41 (for the `bindn` non-consuming bind flag).

## Install

```
git clone https://github.com/YOURUSER/hyprwheel
cd hyprwheel
./install.sh
```

Or manually: copy `hyprwheel` somewhere on your `$PATH` and add to your
Hyprland config:

```
bindn = , mouse:273, exec, hyprwheel --desktop
```

`bindn` is non-consuming: the right-click still reaches windows normally.
`--desktop` makes hyprwheel exit silently unless the cursor is over an empty
part of the desktop — so the wheel only ever appears on your wallpaper.

You can also bind it to anything else, e.g. a key:

```
bind = SUPER, grave, exec, hyprwheel
```

(without `--desktop` it opens unconditionally, wherever the cursor is)

## Configure

Edit `~/.config/hyprwheel/config.json` (see `config.example.json`):

```json
{
  "outer_radius": 220,
  "inner_radius": 70,
  "items": [
    { "label": "Terminal", "icon": "💻",
      "exec": ["xdg-terminal-exec", "$TERMINAL", "alacritty", "kitty"] },
    { "label": "YouTube", "icon": "▶",
      "exec": ["xdg-open https://youtube.com"] }
  ]
}
```

- `exec` is a fallback chain: the first entry whose binary exists is used.
  Entries can include arguments and URLs (`xdg-open https://…`).
- `$TERMINAL`-style env vars are expanded; unset vars are skipped.
- Any number of slices works — the wheel divides itself evenly.
- Icons are just text: emoji, Nerd Font glyphs, or plain letters.

## How it works

One GTK3 window on a `wlr-layer-shell` overlay, wheel drawn with Cairo at the
cursor position. `--desktop` asks `hyprctl` whether the cursor overlaps any
mapped window or top/overlay layer surface (bars, notifications) and bails out
if so. Launching a second instance while the wheel is open closes it (toggle).

## License

MIT
