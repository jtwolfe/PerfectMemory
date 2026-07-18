# PerfectMemory Paper Specification (Draft v0.2)

## Goals
- Easy home printing on standard A4 paper.
- Foldable into A5 notebook signatures.
- Unique lifelong page identity.
- Support freeform writing and isometric diagramming.
- High scannability and **robust geometric registration** under real-world phone photos, including parallax, folds, bends, and roughly scrunched-then-unfolded pages.
- Minimal interference with handwriting and OCR.

## Page Geometry
- Target finished page: A5 (148 mm × 210 mm).
- Printed on A4 (210 mm × 297 mm) and folded in half for signatures.
- Standard 4-page signature per A4 sheet (correct imposition for reading order after folding).
- Margins: 
  - Binding edge: 12–15 mm
  - Outer edges: 8–10 mm
  - Top/bottom: ~10 mm (room for header/footer and markers)
- Writing area: central region ~120–125 mm × 175–180 mm, kept as clear as practical.

## Unique Identification
- **QR Code**:
  - Position: Consistent corner (recommended top-right of the A5 page content orientation).
  - Size: 20–25 mm side + quiet zone.
  - Error correction: Level H (high).
  - Payload: Structured short form e.g. `PM1|{notebook_id}|{page_uuid}|{seq}|{crc}` or UUID-primary with local index.
- **Human-readable**: Short code (e.g. `PM-NB01-0042`) and sequential page number near QR or in footer.

## Registration Marks (Critical for Dewarping)
To enable reliable detection and non-rigid correction of warped, bent, folded, or scrunched pages from a single casual photo, pages carry a hybrid set of high-contrast fiducials + dense lattice:

### Primary Strong Fiducials (ArUco)
- **4 corner ArUco markers** (size 15–20 mm):
  - Placed just inside the outer margins, outside the main writing area.
  - Dictionary: OpenCV `DICT_4X4_50` or `DICT_5X5_100` (small, fast, sufficient unique IDs).
  - Unique or page-relative IDs (e.g. absolute corner codes 0=NW, 1=NE, 2=SW, 3=SE relative to page orientation, or per-page unique).
  - High contrast black-on-white, with adequate quiet zone.
- **Optional mid-edge markers** (size 10–12 mm) on the four sides for denser sampling of curvature/bends.
- These provide robust, uniquely identified control points even under heavy perspective, partial occlusion, blur, or lighting variation. OpenCV `cv2.aruco` detects them reliably.

### Unique QR as Additional Fiducial
- The page QR also serves as a strong, high-contrast feature with built-in finder patterns.

### Dense Isometric Triangular Dots (Secondary / Fine Features)
- Equilateral triangular lattice (60°) across the writing area.
- Spacing: 5 mm (adjustable).
- Diameter: 0.35–0.5 mm.
- Color: Light-to-medium gray (tune for detectability, e.g. 15–25% black). Subtle enough for comfortable writing but detectable via blob detection after coarse alignment.
- Purpose: Provides a dense regular grid of correspondences for non-rigid dewarping (thin-plate spline, RBF, mesh warp, or local affine patches). Even if some dots are covered by ink, the lattice can be fitted and interpolated.

### Supporting Marks
- Optional thin high-contrast outer border frame or L-shaped corner brackets for page segmentation and additional edge constraints.
- Quiet zones around all strong markers.

**Dewarping pipeline expectation**:
1. Detect ArUco markers + QR → obtain page ID and sparse strong correspondences to the known flat template.
2. Coarse perspective / rigid correction.
3. Detect residual isometric dots (or use them for refinement).
4. Fit non-rigid deformation model (TPS recommended) using all available control points → warp the photo to a flat, rectified A5 image.
5. This handles moderate-to-significant crumpling/scrunching far better than pure 4-point homography. Extreme cases benefit from the user flattening the page better or multi-shot, but the marks give a strong prior.

## Background Grid Details
See Registration Marks above. Pure freeform dots preferred initially; optional hybrid faint horizontal rules configurable in generator.

## Other Printed Elements
- Optional light header zone (title / date).
- Footer: human page number, notebook ID, short code.
- No heavy lines that compete with handwriting or markers.

## Printing Notes
- Black for ArUco, QR, text, and borders. Gray for isometric dots.
- High-resolution print (laser preferred for sharp marker edges). Test QR and ArUco detection under typical phone conditions (angle, flash, no-flash, partial shadow).
- Duplex printing with good registration for signatures. Avoid placing critical markers exactly on fold lines.
- Paper: 80 gsm or slightly heavier. Smooth enough for OCR.

## Generator Requirements
- Python CLI/script:
  - Inputs: notebook ID, number of pages/signatures, starting sequence/UUID seed, options for marker sizes, dot parameters, template variants.
  - Outputs: Multi-page A4 PDF with correct imposition for folding into A5 notebooks + per-page metadata log (UUIDs, marker IDs).
  - Must generate high-quality ArUco images (via OpenCV) and embed them precisely in mm coordinates.
  - Support single-page test mode and full signature mode.
  - Deterministic generation where possible for reproducibility.

## Open Questions / Future
- Exact marker ID assignment scheme (global unique vs relative + QR).
- Optimal density of mid-edge / interior markers vs writing interference.
- Tuning gray level of dots for best detection-without-annoyance balance.
- Full multi-sheet booklet imposition and binding guides.
- Multiple templates (checklist, ruled hybrid, diagram-optimized with fewer interior marks).
- Validation suite: generate pages, print, photograph under distortion, measure dewarp quality.
