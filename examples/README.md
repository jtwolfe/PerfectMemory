# PerfectMemory Examples

## sample_page_v03.pdf (or .b64)

New sample matching **PAPER_SPEC v0.3**:

- Thin continuous high-contrast border frame
- Stretched small markers + distinctive L-corner treatments around the *entire* perimeter
- Modest ~15.5 mm integrated QR-style zone (top-right, border flows around it)
- Enhanced isometric triangular dots (base lattice + stronger super-lattice every ~15-20 mm)
- Maximized clean writing area
- Human-readable short ID in footer

**This is the design that addresses the "out of scale" feedback**: registration is distributed around the border instead of large corner boxes, the QR is smaller and integrated, and the isometric dots provide the surface-wide control points for non-rigid dewarping of scrunched pages.

### How to obtain the PDF
1. Preferred: run the generator
   ```bash
   python tools/generate_page_v03.py --notebook NB01 --page 1 -o examples/sample_page_v03.pdf
   ```
2. If a .b64 file is present:
   ```bash
   python -c "
import base64, pathlib
p = pathlib.Path('examples/sample_page_v03.pdf.b64')
pathlib.Path('examples/sample_page_v03.pdf').write_bytes(base64.b64decode(p.read_text()))
print('Decoded')
"
   ```

Print at **100% actual size**, write, scrunch/unfold, photograph, and test detection + TPS dewarp.

See `docs/PAPER_SPEC.md` for the full rationale.
