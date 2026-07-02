#!/usr/bin/env python3
"""Minimal self-check: slice hit-testing + desktop detection. Run: python3 test_hyprwheel.py"""
from importlib.machinery import SourceFileLoader

hw = SourceFileLoader("hw", "hyprwheel").load_module()


class W:
    cx, cy, inner, outer = 400, 400, 70, 220
    items = [0] * 6


w = W()
w.slice_at = hw.Wheel.slice_at.__get__(w)
assert w.slice_at(400, 260) == 0, "top = slice 0"
assert w.slice_at(530, 330) == 1, "upper-right = slice 1"
assert w.slice_at(400, 540) == 3, "bottom = slice 3"
assert w.slice_at(400, 400) == -1, "center hub"
assert w.slice_at(400, 100) == -1, "outside wheel"

# desktop check with mocked hyprctl
FIX = {
    "cursorpos": {"x": 500, "y": 500},
    "monitors": [{"activeWorkspace": {"id": 1}, "specialWorkspace": {"id": 0}}],
    "clients": [{"mapped": True, "hidden": False, "workspace": {"id": 1},
                 "at": [10, 10], "size": [300, 300]}],
    "layers": {"eDP-1": {"levels": {"2": [{"x": 0, "y": 0, "w": 1280, "h": 26}]}}},
}
hw.hyprctl = lambda cmd: FIX[cmd]
assert hw.cursor_over_desktop() is True, "empty spot"
FIX["cursorpos"] = {"x": 100, "y": 100}
assert hw.cursor_over_desktop() is False, "over window"
FIX["cursorpos"] = {"x": 500, "y": 20}
assert hw.cursor_over_desktop() is False, "over bar layer"

assert hw.resolve(["definitely-not-a-real-binary-xyz"]) is None
assert hw.resolve(["definitely-not-real", "sh"]) == "sh", "fallback chain"

print("all checks pass")
