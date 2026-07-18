# PerfectMemory Paper Specification (Draft v0.3)

## Goals
- Easy home printing on standard A4 paper.
- Foldable into A5 notebook signatures.
- Unique lifelong page identity.
- Support freeform writing and isometric diagramming.
- **Robust geometric registration** under real-world phone photos, including parallax, folds, bends, and roughly scrunched-then-unfolded pages.
- Minimal visual weight and interference with handwriting / OCR. Large discrete boxes and oversized QR are avoided.

## Page Geometry
- Target finished page: A5 (148 mm × 210 mm).
- Printed on A4 and folded for signatures (correct imposition).
- Margins: Binding edge 12–15 mm; other edges 8–10 mm; top/bottom ~10 mm.
- Writing area maximised: the registration system lives primarily in the margin / border zone so the central writing region stays large and clean.

## Unique Identification
- Primary: Structured payload carried by a modest integrated 2D code (see Registration) **or** distributed across the border marker sequence.
- Recommended payload form: `PM1|{notebook_id}|{page_uuid}|{seq}` (or compact UUID + notebook).
- Human-readable short code (e.g. `PM-NB01-0042`) always printed in the footer for manual reference.

## Registration Marks (v0.3 — Perimeter-Stretched + Dense Interior)

The previous large corner ArUco squares + prominent QR felt out of scale on A5. The new design stretches registration around the border and uses the isometric dots for surface-wide control points.

### 1. Perimeter Registration Frame (stretched marks)
- Thin continuous high-contrast black border frame (≈0.8–1.2 pt), inset a few mm from the physical edge.
- Along all four edges: a sequence of **small** high-contrast markers or coded segments (target size 8–11 mm) spaced approximately every 22–28 mm.
- Corners receive distinctive L-shaped or dual-segment treatments that hug both edges (strong orientation cues without large solid squares).
- This distributes many control points around the entire perimeter — excellent for boundary conditions when fitting non-rigid warps on scrunched paper — while leaving the interior almost entirely free.

### 2. Embedded / Integrated Unique ID
- Preferred practical approach: One modest high-ECC QR or DataMatrix (≈14–17 mm) cleanly integrated into the top or top-right border zone. The border frame flows into or around it. This remains easily readable by modern phone cameras at normal distances but no longer dominates the page.
- Alternative / complementary: Encode identity bits (or a strong hash) into the sequence of small border markers themselves, plus the short human-readable footer code.
- The large standalone corner QR of earlier drafts is retired.

### 3. Dense Surface Registration via Isometric Dots (primary interior features)
- Equilateral triangular lattice (60°), spacing 5 mm across the writing area.
- Dot diameter ~0.35–0.5 mm.
- Color: light-to-medium gray, tuned slightly higher contrast than pure aesthetic (target ~20–30% black) so the lattice is reliably detectable after coarse alignment.
- Optional: a sparse "super-lattice" of slightly larger or ringed dots every 15–20 mm as guaranteed interior anchors.
- **Role**: After the perimeter frame supplies coarse pose + page ID, blob detection + lattice fitting on the dots yields hundreds of interior correspondences. These drive high-quality non-rigid dewarping (TPS / RBF / mesh) across the whole surface, recovering local creases from scrunching far better than sparse corner markers alone.

### 4. Supporting Elements
- Quiet zones around markers and the integrated 2D code.
- Optional very light header guide line for title/date.
- Footer with human-readable short code and page sequence.

**Expected capture / dewarp pipeline**:
1. Detect the perimeter markers / border features + integrated 2D code → page identity + sparse strong correspondences to the known flat template.
2. Coarse alignment / perspective correction.
3. Detect the isometric lattice (and any super-dots).
4. Fit non-rigid model (TPS recommended) using all available points → warp photo to clean rectified A5.
5. Proceed to OCR / VLM on the flattened image. Original photo is always retained.

## Printing Notes
- Black for border, markers, 2D code, and text. Tuned gray for dots.
- Print at 100% scale, preferably laser for sharp edges. Test detection under realistic phone conditions (angle, distance, lighting, after deliberate scrunching).
- Avoid placing critical markers exactly on fold lines of signatures.
- Standard 80 gsm (or slightly heavier) smooth paper.

## Generator Requirements
- Python script / CLI that produces the perimeter-stretched layout:
  - Configurable notebook ID, page sequence / UUID, marker size & spacing, dot contrast, whether to include a modest integrated QR/DataMatrix, mid-edge density, etc.
  - Precise mm positioning.
  - High-quality embedding of small ArUco (or custom coded segments) and the integrated 2D code.
  - Single-page test mode and multi-page / signature mode.
  - Output PDF ready for 100% printing + optional metadata log of IDs and expected template coordinates (useful for the dewarp script).

## Open Questions / Validation
- Exact optimal small-marker size and spacing after real print + phone-photo tests.
- Continuous coded strip vs discrete small markers along edges.
- How aggressively to raise dot contrast before it becomes visually annoying.
- Full A4 signature imposition with the new border system.
- Empirical dewarp quality on deliberately scrunched pages.

---
*v0.3 — response to feedback that large discrete registration boxes and oversized QR felt out of scale. Emphasis shifted to perimeter distribution + dense isometric lattice for surface coverage.*
