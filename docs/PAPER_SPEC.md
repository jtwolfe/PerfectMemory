# PerfectMemory Paper Specification (Draft v0.1)

## Goals
- Easy home printing on standard A4 paper.
- Foldable into A5 notebook signatures.
- Unique lifelong page identity.
- Support freeform writing and isometric diagramming.
- High scannability (QR reliability under real phone photos).
- Minimal interference with handwriting recognition.

## Page Geometry
- Target finished page: A5 (148 mm × 210 mm).
- Printed on A4 (210 mm × 297 mm) and folded in half for signatures.
- Standard 4-page signature per A4 sheet (front: pages N and N+3; back: N+1 and N+2, or appropriate imposition for correct reading order after folding/stapling).
- Margins: 
  - Binding edge: ~12–15 mm
  - Outer edges: ~8–10 mm
  - Top/bottom: ~10 mm (room for header/footer)

## Unique Identification
- **QR Code**:
  - Position: Top-right or bottom-right corner (consistent across pages).
  - Size: ~20–25 mm side length + quiet zone.
  - Error correction: Level H (high).
  - Payload (suggested short form): `PM1|{notebook_id}|{page_uuid}|{seq}|{crc8}` or simply a UUID with a local index/manifest.
  - Prefer self-describing but keep under ~50–80 characters for denser/smaller QR if needed.
- **Human-readable**:
  - Short code e.g. `PM-NB01-0042` or notebook name + sequential page number printed near QR or in footer.
  - Full UUID can be tiny text if desired.

## Background Grid: Isometric Triangular Dots
- Equilateral triangular lattice (60° angles) for natural isometric drawing.
- Dot spacing: 5 mm (common practical size; adjustable 4–7 mm).
- Dot diameter: 0.3–0.5 mm.
- Color: Very light gray (e.g. 8–15% black, or light cyan/gray that scans well but is non-intrusive). Must not confuse OCR or reduce handwriting contrast significantly.
- Coverage: Full writing area, stopping short of margins/QR zone.

## Other Printed Elements
- Optional light header zone (title / date line).
- Footer: page sequence number, notebook ID, small decorative or functional marks.
- Optional very faint horizontal rules if hybrid lined+dot preferred (user configurable in generator).
- No heavy lines that compete with ink.

## Printing Notes
- Black for QR and text, gray for dots.
- Test on actual printer for QR readability under phone camera at angle/low light.
- Duplex printing required for signatures; careful registration.
- Paper: Standard 80 gsm or slightly heavier for notebook feel. Avoid heavy texture that hurts OCR.

## Generator Requirements
- Python script accepting:
  - Number of pages / signatures
  - Notebook ID / name
  - Starting page number or UUID seed
  - Dot spacing, colors, QR size/position options
- Output: Multi-page PDF ready for duplex print + folding instructions.
- Deterministic or logged UUID generation for reproducibility.

## Open Questions / Future
- Multiple page templates (pure dots, dots + light lines, checklist-optimized, diagram-heavy).
- Color variants or perforated options.
- Exact imposition math for multi-sheet booklets.
- Fiducials beyond QR for more robust dewarping.
