# PerfectMemory Examples

## sample_page_A5.pdf

A sample A5 page generated for testing the registration / dewarping marks.

**Contents:**
- 4 high-contrast corner registration markers (custom ArUco-inspired patterns with unique IDs 0-3 for TL/TR/BL/BR)
- QR-code style placeholder (top-right) with short ID
- Light isometric triangular dots (5 mm) across the writing area
- Thin outer border
- Human-readable ID and footer
- Title/date guide line

**How to use:**
1. Download and print at **100% scale** (actual size) on A5 or A4 paper (scale carefully if needed).
2. Write notes and diagrams.
3. Optionally scrunch the page, unfold it, and take a quick phone photo from an angle.
4. The corner markers + QR area are designed to provide control points for non-rigid dewarping (TPS / mesh) even on wrinkled paper.

**Note:** This sample was generated with a pure-Python (reportlab + PIL) version that uses custom fiducials instead of full OpenCV ArUco + qrcode library, so that it could be produced in constrained environments. The full generator in `tools/generate_page.py` produces real ArUco (DICT_4X4_50) + proper high-ECC QR codes when the dependencies are available.

Generate more with:
```bash
pip install reportlab qrcode[pil] opencv-python-headless pillow numpy
python tools/generate_page.py --notebook NB01 --page 1 -o mypage.pdf
```

Or use the pure fallback (to be added).
