#!/usr/bin/env python3
"""Add accented glyphs needed by the Selectric font."""
from __future__ import annotations

from copy import deepcopy
from math import cos, radians, sin
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.ttProgram import Program

FONT_PATH = Path("static/fonts/IBM_Selectric_Light_Italic.ttf")


def ensure_glyph(font: TTFont, glyph_name: str) -> None:
    order = font.getGlyphOrder()
    if glyph_name not in order:
        order.append(glyph_name)
        font.setGlyphOrder(order)


def add_unicode_mapping(font: TTFont, codepoint: int, glyph_name: str) -> None:
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[codepoint] = glyph_name


def build_accented(
    font: TTFont,
    target: str,
    base: str,
    accent_source: str,
    gap: int,
    flip_x: bool = False,
    rotate_deg: float = 0.0,
    scale: float = 1.0,
    x_shift: int = 0,
    y_shift: int = 0,
    rotate_origin: str | tuple[float, float] | None = None,
) -> None:
    glyf = font["glyf"]
    base_glyph = deepcopy(glyf[base])
    base_glyph.expand(glyf)
    accent_glyph = deepcopy(glyf[accent_source])
    accent_glyph.expand(glyf)

    base_coords = base_glyph.coordinates
    accent_coords = accent_glyph.coordinates.copy()
    accent_end_pts = accent_glyph.endPtsOfContours[:]
    accent_flags = accent_glyph.flags[:]

    if flip_x:
        ax_min, _, ax_max, _ = accent_coords.calcBounds()
        center = (ax_min + ax_max) / 2
        accent_coords.translate((-center, 0))
        accent_coords.transform(((-1, 0), (0, 1)))
        accent_coords.translate((center, 0))

    if rotate_deg or scale != 1.0:
        ax_min, ay_min, ax_max, ay_max = accent_coords.calcBounds()
        center_x = (ax_min + ax_max) / 2
        center_y = (ay_min + ay_max) / 2

        origin_x, origin_y = center_x, center_y
        if isinstance(rotate_origin, tuple):
            origin_x, origin_y = rotate_origin
        elif rotate_origin == "bottom":
            origin_y = ay_min
        elif rotate_origin == "top":
            origin_y = ay_max
        elif rotate_origin == "bottom_left":
            origin_x, origin_y = ax_min, ay_min
        elif rotate_origin == "bottom_right":
            origin_x, origin_y = ax_max, ay_min
        elif rotate_origin == "top_left":
            origin_x, origin_y = ax_min, ay_max
        elif rotate_origin == "top_right":
            origin_x, origin_y = ax_max, ay_max

        accent_coords.translate((-origin_x, -origin_y))
        if scale != 1.0:
            accent_coords.transform(((scale, 0), (0, scale)))
        if rotate_deg:
            angle = radians(rotate_deg)
            rotation = ((cos(angle), sin(angle)), (-sin(angle), cos(angle)))
            accent_coords.transform(rotation)
        accent_coords.translate((origin_x, origin_y))

    bx_min, _, bx_max, by_max = base_coords.calcBounds()
    ax_min, ay_min, ax_max, _ = accent_coords.calcBounds()
    base_center = (bx_min + bx_max) / 2
    accent_center = (ax_min + ax_max) / 2

    dx = round(base_center - accent_center) + x_shift
    dy = round((by_max + gap) - ay_min) + y_shift
    accent_coords.translate((dx, dy))

    offset = len(base_coords)
    base_coords.extend(accent_coords)
    base_glyph.endPtsOfContours.extend([pt + offset for pt in accent_end_pts])
    base_glyph.flags.extend(accent_flags)
    base_glyph.numberOfContours = len(base_glyph.endPtsOfContours)
    base_glyph.recalcBounds(glyf)
    empty_program = Program()
    empty_program.fromAssembly([])
    base_glyph.program = empty_program

    glyf[target] = base_glyph
    font["hmtx"][target] = font["hmtx"][base]
    ensure_glyph(font, target)


def thin_numbersign(font: TTFont, scale: float = 0.92) -> None:
    glyf = font["glyf"]
    glyph = glyf["numbersign"]
    glyph.expand(glyf)

    coords = glyph.coordinates
    x_min, y_min, x_max, y_max = coords.calcBounds()
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    coords.translate((-center_x, -center_y))
    coords.transform(((scale, 0), (0, scale)))
    coords.translate((center_x, center_y))

    glyph.recalcBounds(glyf)
    empty_program = Program()
    empty_program.fromAssembly([])
    glyph.program = empty_program
    ensure_glyph(font, "numbersign")


def main() -> None:
    font = TTFont(str(FONT_PATH))

    build_accented(font, "eacute", "e", "quoteright", gap=35, rotate_deg=-40)
    build_accented(font, "Eacute", "E", "quoteright", gap=45, rotate_deg=-40)
    build_accented(
        font,
        "agrave",
        "a",
        "quoteleft",
        gap=30,
        rotate_deg=60,
        x_shift=100,
        y_shift=-5,
        rotate_origin="bottom_right",
    )
    build_accented(
        font,
        "Agrave",
        "A",
        "quoteleft",
        gap=10,
        rotate_deg=60,
        scale=0.85,
        x_shift=100,
        y_shift=-15,
        rotate_origin="bottom_right",
    )

    for codepoint, glyph_name in [
        (0x00E9, "eacute"),
        (0x00C9, "Eacute"),
        (0x00E0, "agrave"),
        (0x00C0, "Agrave"),
        (0x0023, "numbersign"),
    ]:
        add_unicode_mapping(font, codepoint, glyph_name)

    thin_numbersign(font, scale=0.92)

    font["maxp"].numGlyphs = len(font.getGlyphOrder())

    font.save(str(FONT_PATH))
    print(f"Updated font saved to {FONT_PATH}")


if __name__ == "__main__":
    main()
