# PerfectMemory

**Analog notes. Digital immortality. Multi-format reproduction.**

PerfectMemory is an open system for people who love writing with pen and paper but want the power of searchable, versioned, multi-format digital notes.

## The Problem
Handwritten notes in notebooks are hard to search, hard to share in different formats, easy to lose, and difficult to reproduce as clean documents or compact thermal printouts (shopping lists, runsheets, ops checklists).

## The Solution
1. **Print unique PerfectMemory pages** into your notebooks (A5 from folded A4 signatures).
2. Write freely with any pen (isometric triangular dots support easy diagramming).
3. Scan or photograph the page (phone or flatbed).
4. System detects unique QR, preprocesses, runs OCR/VLM recognition → structured Markdown + diagram images.
5. Stores immutably with Git version history.
6. Reproduce as:
   - Original high-quality scan
   - Clean formatted text + diagrams (A4 poster / document)
   - Thermal receipt-style printout

## Key Features
- **Unique page addressing**: Every page has a unique QR code (and human-readable ID).
- **Isometric triangular dots**: Light background grid ideal for isometric/3D diagrams and freeform notes.
- **Structured digital capture**: Handwriting → Markdown (lists, headings, checkboxes) + extracted diagram images (and optional ASCII/Mermaid for simple flowcharts).
- **Immutable by design**: Original scans and history never deleted. Edits create new versions via Git.
- **Multi-format output**: Scan, pretty PDF/A4, thermal ESC/POS.
- **Local-first, open**: Prefer local processing; optional cloud VLMs. Git-backed, portable Markdown.

## Status
Early design / documentation phase. Paper generator prototype coming next.

See [docs/](docs/) for detailed vision, architecture, and paper specification.

## Quick Links
- [VISION.md](docs/VISION.md)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [PAPER_SPEC.md](docs/PAPER_SPEC.md)

## Why not just Rocketbook?
Rocketbook is excellent for reusable temporary notes. PerfectMemory prioritizes:
- Permanent physical pages with unique lifelong IDs
- Strong version control and archival immutability
- Explicit multi-reproduction formats (especially thermal + large formatted)
- Isometric diagramming support
- Fully open and self-hostable pipeline

## Contributing / Roadmap
This is a collaborative project. Paper generator first, then capture pipeline, recognition, renderers.

Issues and PRs welcome once core docs settle.

---
*Created 2026 in collaboration with Grok team.*
