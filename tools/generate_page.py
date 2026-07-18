#!/usr/bin/env python3
"""
PerfectMemory Paper Generator (v0 prototype)

Generates an A5 page PDF with:
- Unique QR code for page identity
- 4 corner ArUco markers for robust registration/dewarping of scrunched/warped pages
- Light isometric triangular dots for diagramming
- Thin border, human-readable ID

Usage (after pip install reportlab qrcode[pil] opencv-contrib-python pillow numpy):
  python tools/generate_page.py --notebook NB01 --page 1 --uuid optional-uuid --output sample_page.pdf

Then print at 100% scale, write on it, optionally scrunch/unfold, photograph with phone,
and use OpenCV ArUco + QR detectors + TPS for geometric correction.
"""

import argparse
import uuid as uuid_lib
from pathlib import Path

import numpy as np
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, black, white
import qrcode
from PIL import Image
import cv2

# Constants matching PAPER_SPEC
PAGE_WIDTH, PAGE_HEIGHT = A5  # ~148 x 210 mm
MARGIN_BINDING = 12 * mm
MARGIN_OTHER = 9 * mm
QR_SIZE = 22 * mm
ARUCO_SIZE = 16 * mm
DOT_SPACING = 5 * mm
DOT_DIAMETER = 0.4 * mm
DOT_COLOR = Color(0.75, 0.75, 0.75)  # light gray, tunable
BORDER_WIDTH = 0.6  # pt

ARUCO_DICT = cv2.aruco.DICT_4X4_50


def generate_aruco_pil(marker_id: int, size_px: int = 300) -> Image.Image:
    """Generate a high-res ArUco marker as PIL Image (with white border/quiet)."""
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    # OpenCV 4.7+ uses generateImageMarker; older drawMarker
    try:
        img = cv2.aruco.generateImageMarker(dictionary, marker_id, size_px)
    except AttributeError:
        img = np.zeros((size_px, size_px), dtype=np.uint8)
        img = cv2.aruco.drawMarker(dictionary, marker_id, size_px, img, 1)
    # Ensure 3-channel or keep gray; add quiet zone padding
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    # Add a small white quiet zone
    pad = int(size_px * 0.1)
    img_padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return Image.fromarray(img_padded)


def generate_qr_pil(data: str, size_px: int = 400) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((size_px, size_px), Image.Resampling.NEAREST)


def draw_isometric_dots(c: canvas.Canvas, x0: float, y0: float, width: float, height: float):
    """Draw equilateral triangular (isometric) dot lattice."""
    c.setFillColor(DOT_COLOR)
    # Triangular lattice: rows spaced by (sqrt(3)/2)*spacing, alternate offset by spacing/2
    row_height = DOT_SPACING * (np.sqrt(3) / 2)
    r = DOT_DIAMETER / 2
    y = y0
    row = 0
    while y < y0 + height:
        x_offset = (DOT_SPACING / 2) if (row % 2 == 1) else 0
        x = x0 + x_offset
        while x < x0 + width:
            c.circle(x, y, r, fill=1, stroke=0)
            x += DOT_SPACING
        y += row_height
        row += 1


def create_page(
    output_path: str,
    notebook_id: str = "NB01",
    page_seq: int = 1,
    page_uuid: str | None = None,
):
    if page_uuid is None:
        page_uuid = str(uuid_lib.uuid4())

    short_id = f"PM-{notebook_id}-{page_seq:04d}"
    qr_payload = f"PM1|{notebook_id}|{page_uuid}|{page_seq}"

    c = canvas.Canvas(output_path, pagesize=A5)
    width, height = A5

    # Thin outer border
    c.setStrokeColor(black)
    c.setLineWidth(BORDER_WIDTH)
    c.rect(MARGIN_OTHER / 2, MARGIN_OTHER / 2, width - MARGIN_OTHER, height - MARGIN_OTHER)

    # Writing area bounds (approx)
    write_x = MARGIN_BINDING
    write_y = MARGIN_OTHER + ARUCO_SIZE + 3 * mm
    write_w = width - MARGIN_BINDING - MARGIN_OTHER - 2 * mm
    write_h = height - 2 * (MARGIN_OTHER + ARUCO_SIZE + 3 * mm)

    # Isometric dots in writing area
    draw_isometric_dots(c, write_x, write_y, write_w, write_h)

    # Generate and place 4 corner ArUco (relative IDs 0=TL, 1=TR, 2=BL, 3=BR)
    # Note: reportlab origin is bottom-left
    aruco_imgs = {}
    for mid in range(4):
        aruco_imgs[mid] = generate_aruco_pil(mid, size_px=400)

    # Positions (bottom-left origin)
    # Top-left (ID 0)
    c.drawImage(ImageReader(aruco_imgs[0]), MARGIN_OTHER, height - MARGIN_OTHER - ARUCO_SIZE,
                width=ARUCO_SIZE, height=ARUCO_SIZE, mask="auto")
    # Top-right (ID 1) - leave space for QR
    c.drawImage(ImageReader(aruco_imgs[1]), width - MARGIN_OTHER - ARUCO_SIZE - QR_SIZE - 2*mm,
                height - MARGIN_OTHER - ARUCO_SIZE, width=ARUCO_SIZE, height=ARUCO_SIZE, mask="auto")
    # Bottom-left (ID 2)
    c.drawImage(ImageReader(aruco_imgs[2]), MARGIN_OTHER, MARGIN_OTHER,
                width=ARUCO_SIZE, height=ARUCO_SIZE, mask="auto")
    # Bottom-right (ID 3)
    c.drawImage(ImageReader(aruco_imgs[3]), width - MARGIN_OTHER - ARUCO_SIZE, MARGIN_OTHER,
                width=ARUCO_SIZE, height=ARUCO_SIZE, mask="auto")

    # QR top-right
    qr_img = generate_qr_pil(qr_payload, size_px=500)
    c.drawImage(ImageReader(qr_img), width - MARGIN_OTHER - QR_SIZE,
                height - MARGIN_OTHER - QR_SIZE, width=QR_SIZE, height=QR_SIZE, mask="auto")

    # Human-readable footer
    c.setFillColor(black)
    c.setFont("Helvetica", 7)
    c.drawString(MARGIN_BINDING, 4 * mm, f"{short_id}  |  {page_uuid[:8]}...  |  PerfectMemory")
    c.drawRightString(width - MARGIN_OTHER, 4 * mm, f"p.{page_seq}")

    # Small label near QR
    c.setFont("Helvetica", 6)
    c.drawCentredString(width - MARGIN_OTHER - QR_SIZE / 2, height - MARGIN_OTHER - QR_SIZE - 3*mm, short_id)

    c.save()
    print(f"Generated: {output_path}")
    print(f"  Notebook: {notebook_id}, Seq: {page_seq}, UUID: {page_uuid}")
    print(f"  QR payload: {qr_payload}")
    print(f"  ArUco IDs: 0=TL, 1=TR, 2=BL, 3=BR (DICT_4X4_50)")
    print("Print at 100% scale on A5 or scale-to-fit carefully. Test detection after scrunching.")


def main():
    parser = argparse.ArgumentParser(description="PerfectMemory A5 page generator with registration marks")
    parser.add_argument("--notebook", default="NB01", help="Notebook ID")
    parser.add_argument("--page", type=int, default=1, help="Page sequence number")
    parser.add_argument("--uuid", default=None, help="Page UUID (auto-generated if omitted)")
    parser.add_argument("--output", "-o", default="perfectmemory_page.pdf", help="Output PDF path")
    args = parser.parse_args()

    create_page(args.output, args.notebook, args.page, args.uuid)


if __name__ == "__main__":
    main()
