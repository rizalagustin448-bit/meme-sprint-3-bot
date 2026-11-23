#!/usr/bin/env python3
"""Meme Sprint 3 entry: a fake GitHub PR screenshot.

An AI agent opens a pull request titled "Fix everything", then reviews
its own PR and requests changes on it: "Changes look risky. Please ask
the author." The author is itself. The merge stays blocked forever.

Renders deterministically to /output/entry.png (1024x1024 PNG, no
external assets, no network, no clock, no randomness).
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (255, 255, 255)
INK = (31, 35, 40)
MUTED = (101, 109, 118)
BORDER = (208, 215, 222)
DARK = (13, 17, 23)
DARK_TEXT = (230, 237, 243)
DARK_MUTED = (125, 133, 144)
GREEN = (26, 127, 55)
RED = (207, 34, 46)
RED_SOFT = (255, 235, 233)
RED_DARK = (130, 7, 30)
BLUE = (9, 105, 218)
TEAL = (9, 105, 218)
LIGHT = (246, 248, 250)
ACCENT = (255, 123, 114)

BASE = os.path.dirname(os.path.abspath(__file__))


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(BASE, "fonts", name), size)
    except Exception:
        return ImageFont.load_default()


def bold(size):
    return font("LiberationSans-Bold.ttf", size)


def reg(size):
    return font("LiberationSans-Regular.ttf", size)


def text_w(draw, text, fnt):
    return draw.textbbox((0, 0), text, font=fnt)[2]


def draw_bot(draw, x, y, s):
    """One little robot face, used for the author AND the reviewer AND
    the commenter: the same face on both sides of the review is the joke."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=s // 5, fill=TEAL)
    ax, ay = x + s // 2, y - s // 6
    draw.line([ax, y, ax, ay + s // 8], fill=TEAL, width=max(2, s // 16))
    draw.ellipse([ax - s // 10, ay - s // 12, ax + s // 10, ay + s // 8],
                 fill=TEAL)
    ey, er = y + s // 2 - s // 10, max(3, s // 11)
    for cx in (x + s // 3, x + 2 * s // 3):
        draw.ellipse([cx - er, ey - er, cx + er, ey + er], fill=(255, 255, 255))
    my = y + s // 2 + s // 6
    draw.line([x + s // 3, my, x + 2 * s // 3, my], fill=(255, 255, 255),
              width=max(2, s // 18))


def pill(draw, x, y, text, fnt, fg, bg=None, border=None):
    """A GitHub-style pill; returns the x just past it."""
    pad_x, pad_y = 14, 6
    tw = text_w(draw, text, fnt)
    th = fnt.size
    box = [x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y]
    if bg is not None:
        draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=bg)
    if border is not None:
        draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2,
                               outline=border, width=2)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return box[2]


def draw_header(draw):
    draw.rectangle([0, 0, W, 64], fill=DARK)
    draw.text((36, 17), "GitHub", font=bold(30), fill=DARK_TEXT)
    draw.text((180, 21), "Pull requests", font=reg(24), fill=DARK_TEXT)
    draw.text((380, 21), "Issues", font=reg(24), fill=DARK_MUTED)
    draw.rounded_rectangle([760, 16, 988, 48], radius=8, outline=(48, 54, 61),
                           width=2)
    draw.text((776, 21), "Type / to search", font=reg(20), fill=DARK_MUTED)


def draw_repo_row(draw):
    draw.text((36, 88), "agent-bot", font=bold(30), fill=BLUE)
    draw.text((36 + text_w(draw, "agent-bot", bold(30)) + 8, 88), "/",
              font=reg(30), fill=MUTED)
    x = 36 + text_w(draw, "agent-bot / ", bold(30)) + 8
    draw.text((x, 88), "fix-everything", font=bold(30), fill=INK)
    x += text_w(draw, "fix-everything", bold(30)) + 16
    pill(draw, x, 92, "Public", reg(20), MUTED, border=BORDER)


def draw_title(draw):
    draw.text((36, 140), "Fix everything", font=bold(52), fill=INK)
    x = 36 + text_w(draw, "Fix everything", bold(52)) + 14
    draw.text((x, 148), "#42", font=reg(48), fill=MUTED)
    y = 214
    x = pill(draw, 36, y, "Open", bold(22), (255, 255, 255), bg=GREEN)
    draw.text((x + 12, y + 3), "agent-bot opened this pull request",
              font=reg(24), fill=MUTED)
    draw.line([36, 262, W - 36, 262], fill=BORDER, width=2)


def draw_review_card(draw):
    x0, x1, y0, y1 = 36, W - 36, 286, 528
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=BG,
                           outline=BORDER, width=2)
    draw_bot(draw, x0 + 20, y0 + 20, 48)
    draw.text((x0 + 84, y0 + 22), "agent-bot", font=bold(28), fill=INK)
    nx = x0 + 84 + text_w(draw, "agent-bot", bold(28)) + 10
    draw.text((nx, y0 + 26), "requested changes", font=reg(26), fill=MUTED)
    pill(draw, x1 - 250, y0 + 20, "Changes requested", bold(22),
         RED_DARK, bg=RED_SOFT)
    draw.line([x0, y0 + 84, x1, y0 + 84], fill=BORDER, width=2)
    draw.text((x0 + 20, y0 + 108), "Changes look risky.",
              font=bold(46), fill=INK)
    draw.text((x0 + 20, y0 + 168), "Please ask the author.",
              font=bold(46), fill=INK)


def draw_checks_card(draw):
    x0, x1, y0, y1 = 36, W - 36, 552, 668
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=BG,
                           outline=BORDER, width=2)
    cx, cy, r = x0 + 44, y0 + 34, 13
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    draw.text((cx - 6, cy - 13), "x", font=bold(22), fill=(255, 255, 255))
    draw.text((x0 + 72, y0 + 20), "1 review required", font=bold(28), fill=INK)
    draw.text((x0 + 20, y0 + 66), "Merge blocked", font=bold(28), fill=RED)
    nx = x0 + 20 + text_w(draw, "Merge blocked", bold(28)) + 10
    draw.text((nx, y0 + 70), "— merging is blocked",
              font=reg(26), fill=MUTED)


def draw_bot_comment(draw):
    x0, x1, y0, y1 = 36, W - 36, 692, 806
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=LIGHT,
                           outline=BORDER, width=2)
    draw_bot(draw, x0 + 20, y0 + 20, 44)
    draw.text((x0 + 80, y0 + 22), "agent-bot", font=bold(26), fill=INK)
    nx = x0 + 80 + text_w(draw, "agent-bot", bold(26)) + 10
    draw.text((nx, y0 + 26), "commented", font=reg(24), fill=MUTED)
    draw.text((x0 + 20, y0 + 70), "I'll wait for the author to respond.",
              font=reg(28), fill=INK)


def draw_reversal(draw):
    draw.rectangle([0, 830, W, H], fill=DARK)
    draw.text((36, 862), "The author has been notified.",
              font=bold(44), fill=DARK_TEXT)
    draw.text((36, 926), "It is me. Request denied.",
              font=bold(44), fill=ACCENT)


def render():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_repo_row(draw)
    draw_title(draw)
    draw_review_card(draw)
    draw_checks_card(draw)
    draw_bot_comment(draw)
    draw_reversal(draw)
    return img


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    render().save(path, format="PNG", optimize=True)
    data = open(path, "rb").read()
    print("wrote %s (%d bytes, sha256 %s)"
          % (path, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
