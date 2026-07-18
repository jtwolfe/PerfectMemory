# PerfectMemory Architecture (v0)

## Layers

### 1. Paper Layer
- Generator produces print-ready PDFs of unique pages.
- Format: Designed for A4 sheets folded into A5 notebook signatures (4 pages per sheet: 2 front, 2 back).
- Each page contains:
  - Unique identifier (UUID preferred) encoded in QR code (high error correction).
  - Human-readable short code / page number.
  - Light isometric triangular dot grid.
  - Optional header/footer zones, margins optimized for binding and scanning.
- Pre-print batches; bind into notebooks.

### 2. Capture Layer
- Input: Phone photo or scanner image of a written page.
- Process:
  - Detect and decode QR (OpenCV QRCodeDetector or robust alternatives like QReader).
  - Use QR location + page corners / other fiducials for perspective correction / dewarping.
  - Image enhancement (contrast, deskew residual, noise reduction).
  - Store original raw image + corrected version, keyed by page UUID / content hash.

### 3. Recognition / Ingestion Pipeline
- Input: Corrected page image + known page ID.
- Vision Language Model (VLM) or hybrid OCR + VLM:
  - Transcribe handwriting into clean, structured Markdown (headings, paragraphs, lists, checkboxes, tables where possible).
  - Identify and crop diagram / sketch regions as separate PNG assets.
  - Optionally generate ASCII art or Mermaid for simple flowcharts / diagrams.
  - Output confidence notes or uncertainty markers for human review.
- Write:
  - `notes/{notebook_id}/{page_uuid}.md` with YAML frontmatter (id, notebook, scanned_at, image_hashes, original_filename, etc.).
  - `assets/{page_uuid}/original.jpg`, `corrected.jpg`, `diagrams/01.png`, ...
- Commit to Git with descriptive message. This is the versioned record.

### 4. Storage & Immutability
- Primary: Git repository (one or many notebooks).
- Original scans are never deleted or overwritten.
- Digital edits create new commits / new files linked by history or frontmatter `previous_version`.
- Optional: Content-addressable storage (hash of image) for deduplication and strong integrity.
- Backups + branch protection for practical undeletability.
- Full-text search on Markdown; future vector search on content + diagram descriptions.

### 5. Reproduction / Output Layer
- **Original**: Print or view the corrected/original scan image.
- **Formatted digital**: Render Markdown + embedded diagrams to high-quality PDF/HTML (WeasyPrint, Pandoc, or browser print) sized for A4 poster or document.
- **Thermal**: Convert Markdown subset (headings, bold, lists, simple text) + optional small images/QR to ESC/POS commands for receipt printers (python-escpos or equivalent). Ideal for compact lists and runsheets. Include a QR linking back to the digital note if desired.

## Tech Preferences (initial)
- Language: Python for generators, pipelines, renderers.
- PDF generation: reportlab or similar (precise control).
- QR: qrcode / segno + OpenCV for detection.
- Image processing: OpenCV, Pillow.
- VLM: User-provided API keys (Claude, Gemini, GPT, Qwen) or local models. Prompt engineering for structured MD + region boxes.
- Thermal: python-escpos or ESC/POS libraries.
- Storage: Git + optional SQLite index for fast lookup by UUID.

## Future Extensions
- Web UI / local app for capture, review, search, print.
- Mobile capture app with offline queue.
- Obsidian / Logseq / GitJournal compatibility.
- Better diagram understanding (vectorization, semantic description).
- Batch notebook printing and binding guides.
