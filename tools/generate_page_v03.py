#!/usr/bin/env python3
"""
PerfectMemory Paper Generator v0.3 (pure reportlab)
Perimeter-stretched registration + modest integrated QR zone + enhanced isometric dots.
Matches docs/PAPER_SPEC.md v0.3.

Usage:
  python tools/generate_page_v03.py --notebook NB01 --page 1 -o examples/sample.pdf
"""

import argparse
import uuid as uuid_lib
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
import numpy as np

# v0.3 constants
BORDER_INSET = 3.5 * mm
BORDER_WIDTH = 1.0
MARKER_SIZE = 10 * mm
QR_SIZE = 15.5 * mm
DOT_SPACING = 5 * mm
DOT_R = 0.2 * mm
DOT_COLOR = Color(0.72, 0.72, 0.72)
SUPER_DOT_R = 0.35 * mm
SUPER_COLOR = Color(0.55, 0.55, 0.55)
MARGIN_WRITE = 14 * mm

def draw_small_marker(c, cx, cy, size, variant=0):
    s = size
    c.setFillColor(black)
    c.setStrokeColor(black)
    c.setLineWidth(0.6)
    c.rect(cx - s/2, cy - s/2, s, s, fill=0, stroke=1)
    if variant % 4 == 0:
        c.line(cx - s*0.3, cy - s*0.3, cx + s*0.3, cy + s*0.3)
        c.line(cx - s*0.3, cy + s*0.3, cx + s*0.3, cy - s*0.3)
    elif variant % 4 == 1:
        c.rect(cx - s*0.25, cy - s*0.25, s*0.5, s*0.5, fill=1, stroke=0)
    elif variant % 4 == 2:
        c.line(cx - s*0.35, cy, cx + s*0.35, cy)
        c.line(cx, cy - s*0.35, cx, cy + s*0.35)
    else:
        c.circle(cx, cy, s*0.22, fill=1, stroke=0)

def draw_L_corner(c, x, y, size, orient="TL"):
    c.setStrokeColor(black)
    c.setLineWidth(1.8)
    s = size
    if orient == "TL":
        c.line(x, y, x + s*1.4, y)
        c.line(x, y, x, y - s*1.4)
        draw_small_marker(c, x + s*0.55, y - s*0.55, size*0.7, 0)
    elif orient == "TR":
        c.line(x, y, x - s*1.4, y)
        c.line(x, y, x, y - s*1.4)
        draw_small_marker(c, x - s*0.55, y - s*0.55, size*0.7, 1)
    elif orient == "BL":
        c.line(x, y, x + s*1.4, y)
        c.line(x, y, x, y + s*1.4)
        draw_small_marker(c, x + s*0.55, y + s*0.55, size*0.7, 2)
    elif orient == "BR":
        c.line(x, y, x - s*1.4, y)
        c.line(x, y, x, y + s*1.4)
        draw_small_marker(c, x - s*0.55, y + s*0.55, size*0.7, 3)

def create_page(output_path, notebook_id="NB01", page_seq=1, page_uuid=None):
    if page_uuid is None:
        page_uuid = str(uuid_lib.uuid4())
    short_id = f"PM-{notebook_id}-{page_seq:04d}"

    c = canvas.Canvas(output_path, pagesize=A5)
    width, height = A5

    # Thin continuous border
    c.setStrokeColor(black)
    c.setLineWidth(BORDER_WIDTH)
    c.rect(BORDER_INSET, BORDER_INSET, width - 2*BORDER_INSET, height - 2*BORDER_INSET)

    # L-corners
    draw_L_corner(c, BORDER_INSET + 2*mm, height - BORDER_INSET - 2*mm, MARKER_SIZE, "TL")
    draw_L_corner(c, width - BORDER_INSET - 2*mm, height - BORDER_INSET - 2*mm, MARKER_SIZE, "TR")
    draw_L_corner(c, BORDER_INSET + 2*mm, BORDER_INSET + 2*mm, MARKER_SIZE, "BL")
    draw_L_corner(c, width - BORDER_INSET - 2*mm, BORDER_INSET + 2*mm, MARKER_SIZE, "BR")

    # Stretched small markers along edges
    for i, x in enumerate(np.linspace(BORDER_INSET + 25*mm, width - BORDER_INSET - 25*mm, 4)):
        draw_small_marker(c, x, height - BORDER_INSET - MARKER_SIZE/2 - 1*mm, MARKER_SIZE*0.85, i)
    for i, x in enumerate(np.linspace(BORDER_INSET + 25*mm, width - BORDER_INSET - 25*mm, 4)):
        draw_small_marker(c, x, BORDER_INSET + MARKER_SIZE/2 + 1*mm, MARKER_SIZE*0.85, i+4)
    for i, y in enumerate(np.linspace(BORDER_INSET + 30*mm, height - BORDER_INSET - 30*mm, 5)):
        draw_small_marker(c, BORDER_INSET + MARKER_SIZE/2 + 1*mm, y, MARKER_SIZE*0.85, i+8)
    for i, y in enumerate(np.linspace(BORDER_INSET + 30*mm, height - BORDER_INSET - 30*mm, 5)):
        draw_small_marker(c, width - BORDER_INSET - MARKER_SIZE/2 - 1*mm, y, MARKER_SIZE*0.85, i+13)

    # Modest integrated QR zone
    qr_x = width - BORDER_INSET - QR_SIZE - 3*mm
    qr_y = height - BORDER_INSET - QR_SIZE - 3*mm
    c.setFillColor(white)
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.rect(qr_x, qr_y, QR_SIZE, QR_SIZE, fill=1, stroke=1)
    c.setFillColor(black)
    fs = QR_SIZE * 0.18
    c.rect(qr_x + 1.2*mm, qr_y + QR_SIZE - fs - 1.2*mm, fs, fs, fill=1, stroke=0)
    c.rect(qr_x + QR_SIZE - fs - 1.2*mm, qr_y + QR_SIZE - fs - 1.2*mm, fs, fs, fill=1, stroke=0)
    c.rect(qr_x + 1.2*mm, qr_y + 1.2*mm, fs, fs, fill=1, stroke=0)
    c.setFillColor(white)
    c.rect(qr_x + 1.2*mm + 1.2, qr_y + QR_SIZE - fs - 1.2*mm + 1.2, fs-2.4, fs-2.4, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 5)
    c.drawCentredString(qr_x + QR_SIZE/2, qr_y + QR_SIZE/2 + 1, "QR")
    c.setFont("Helvetica", 4)
    c.drawCentredString(qr_x + QR_SIZE/2, qr_y + QR_SIZE/2 - 4, f"{short_id}")

    # Isometric + super lattice
    write_left = MARGIN_WRITE
    write_bottom = MARGIN_WRITE
    write_right = width - MARGIN_WRITE
    write_top = height - MARGIN_WRITE - 8*mm
    c.setFillColor(DOT_COLOR)
    row_h = DOT_SPACING * (np.sqrt(3)/2)
    y = write_bottom
    row = 0
    while y < write_top:
        x_off = (DOT_SPACING / 2) if (row % 2) else 0.0
        x = write_left + x_off
        col = 0
        while x < write_right:
            is_super = (row % 3 == 0) and (col % 3 == 0)
            if is_super:
                c.setFillColor(SUPER_COLOR)
                c.circle(x, y, SUPER_DOT_R, fill=1, stroke=0)
                c.setFillColor(DOT_COLOR)
            else:
                c.circle(x, y, DOT_R, fill=1, stroke=0)
            x += DOT_SPACING
            col += 1
        y += row_h
        row += 1

    # Footer
    c.setFillColor(black)
    c.setFont("Helvetica", 7)
    c.drawString(MARGIN_WRITE, 4*mm, f"{short_id}  |  PerfectMemory v0.3  |  perimeter + dots")
    c.drawRightString(width - MARGIN_WRITE, 4*mm, f"p.{page_seq}")
    c.setFont("Helvetica", 5)
    c.drawString(MARGIN_WRITE, height - 6*mm, "Perimeter-stretched registration + enhanced isometric lattice")

    c.save()
    print(f"Generated: {output_path}")
    print(f"  {short_id}  UUID: {page_uuid}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", default="NB01")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--uuid", default=None)
    parser.add_argument("-o", "--output", default="perfectmemory_v03.pdf")
    args = parser.parse_args()
    create_page(args.output, args.notebook, args.page, args.uuid)

if __name__ == "__main__":
    main()
