# pipeline_flowchart.png — Flowchart Drawing Guide

**Tool:** draw.io (app.diagrams.net) — no special shape library needed, use the default General shapes  
**Export:** File → Export As → PNG → 200 dpi → save as `figures/pipeline_flowchart.png`  
**Orientation:** Landscape, wide canvas (approx 2400 × 800 px)  
**Notation:** Standard flowchart (ISO 5807)

> The flowchart represents the **logical design** of the pipeline.  
> It does NOT show n8n internals (polling loops, Telegram nodes) — those are implementation details shown in the n8n screenshot.  
> The diagram shows: what happens, in what order, with what decision points.

---

## Lane Structure

Use a **two-lane swim lane container** (draw.io: Extras → Edit Diagram, or drag a Pool from General shapes):

| Lane | Label | Color tint |
|---|---|---|
| Top lane | `Data Processing` | light blue / #EAF4FB |
| Bottom lane | `Orchestration & Monitoring` | light grey / #F5F5F5 |

The top lane carries the actual data transformations (process boxes).  
The bottom lane carries the start/end terminators and the configuration step.

---

## Flowchart Shapes Needed

| Shape | Flowchart Name | draw.io shape |
|---|---|---|
| Rounded rectangle (stadium) | Terminator (Start / End) | General > Rounded Rectangle |
| Rectangle | Process (task) | General > Rectangle |
| Diamond | Decision (Yes / No) | General > Rhombus |
| Parallelogram | Input / Output (data passing between phases) | General > Parallelogram |
| Solid arrow | Flow direction | Connector (default) |
| Dashed arrow | Data association (to I/O shapes) | Connector > Dashed |

---

## Full Sequence — Step by Step

Draw **left to right**. Each numbered item is one flowchart shape.

---

### BOTTOM LANE — Orchestration

```
[START] ──► [Set Configuration] ──► (arrow up into top lane, Phase 1)
```

**Element 1 — Terminator: Start**
- Shape: Rounded rectangle
- Label: `Pipeline Start`
- Fill: white, thick border
- Position: far left of bottom lane

**Element 2 — Process: Configure Parameters**
- Shape: Rectangle
- Label: `Set Configuration`  
  (sub-text, smaller): `years, timeouts, paths`
- Fill: light grey / #EEEEEE

---

### TOP LANE — Phase 1: PDF Acquisition (Scraping)

**Element 3 — Process: Scrape JORT PDFs**
- Shape: Rectangle
- Label: `Scrape JORT PDFs`  
  (sub-text): `Playwright / iort.gov.tn`
- Fill: light blue / #DAE8FC

**Element 4 — Process: Monitor Scraping**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 5 — Decision: Scraping Done?**
- Shape: Diamond
- Label: `Scraping Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 6 (Phase 2), arrow goes right
  - `No / Error` → Element E1 (End Error), arrow goes down or loops back

**Element E1 — Terminator: Error**
- Shape: Rounded rectangle
- Label: `Pipeline Aborted`  
  (sub-text): `Scraping Failed`
- Fill: light red / #FFCCCC

**I/O between Phase 1 and Phase 2:**
- Shape: Parallelogram
- Label: `Raw PDFs`  
  (sub-text): `pdfs/ folder`
- Place on the arrow between Element 5 (Yes) and Element 6
- Connect with a dashed arrow

---

### TOP LANE — Phase 2: Cloud Backup (Google Drive)

**Element 6 — Process: Upload to Google Drive**
- Shape: Rectangle
- Label: `Upload PDFs to Google Drive`  
  (sub-text): `rclone`
- Fill: light blue / #DAE8FC

**Element 7 — Process: Monitor Upload**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 8 — Decision: Upload Done?**
- Shape: Diamond
- Label: `Upload Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 9 (Phase 3)
  - `No / Error` → Element E2 (End Error)

**Element E2 — Terminator: Error**
- Label: `Pipeline Aborted`  
  (sub-text): `Upload Failed`
- Fill: light red / #FFCCCC

**I/O between Phase 2 and Phase 3:**
- Shape: Parallelogram
- Label: `Backup Confirmed`  
  (sub-text): `Google Drive`

---

### TOP LANE — Phase 3: Text Extraction

**Element 9 — Process: Extract Text from PDFs**
- Shape: Rectangle
- Label: `Extract Text`  
  (sub-text): `PyMuPDF + Gemini OCR`
- Fill: light blue / #DAE8FC
- Add a small annotation note box beside it:
  ```
  Digital pages → PyMuPDF
  Scanned pages → Gemini Vertex AI
  ```

**Element 10 — Process: Monitor Text Extraction**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 11 — Decision: Extraction Done?**
- Shape: Diamond
- Label: `Extraction Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 12 (Phase 4)
  - `No / Error` → Element E3 (End Error)

**Element E3 — Terminator: Error**
- Label: `Pipeline Aborted`  
  (sub-text): `Text Extraction Failed`
- Fill: light red / #FFCCCC

**I/O between Phase 3 and Phase 4:**
- Shape: Parallelogram
- Label: `Plain Text Files`  
  (sub-text): `.txt, one per issue`

---

### TOP LANE — Phase 4: Article Extraction (GPT-4.1)

**Element 12 — Process: Extract and Structure Articles**
- Shape: Rectangle
- Label: `Extract Articles`  
  (sub-text): `GPT-4.1, Two-Stage`
- Fill: light blue / #DAE8FC
- Add annotation note:
  ```
  Stage 1: Boundary detection
  Stage 2: 64-field enrichment
  ```

**Element 13 — Process: Monitor Article Extraction**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 14 — Decision: Article Extraction Done?**
- Shape: Diamond
- Label: `Article Extraction Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 15 (Phase 5)
  - `No / Error` → Element E4 (End Error)

**Element E4 — Terminator: Error**
- Label: `Pipeline Aborted`  
  (sub-text): `Article Extraction Failed`
- Fill: light red / #FFCCCC

**I/O between Phase 4 and Phase 5:**
- Shape: Parallelogram
- Label: `Structured JSON`  
  (sub-text): `64 fields per article`

---

### TOP LANE — Phase 5: Validation & Scoring

<!--
  Phase 5 is a two-layer quality gate that runs on every article produced by Phase 4.

  Layer 1 — Rule-based scoring (applied to every article):
    Six deterministic checks, each carrying a weight. Checks cover: required fields
    present, minimum body length, OCR noise ratio, date format, language consistency
    between Arabic and French fields, and non-empty embedding_text.
    Weights sum to 1.0. Score = sum of weights of passing checks.
      - Score >= 0.75  →  passed, skip Layer 2
      - Score  < 0.50  →  rejected, skip Layer 2
      - Score 0.50–0.74 →  borderline, proceed to Layer 2

  Layer 2 — LLM semantic check (borderline articles only):
    A single GPT-4.1 call assesses whether the article body is coherent with its title.
    Model responds: "valid" (score +0.10), "garbled" or "mismatch" (score -0.10, flag added).
    Keeps API costs low by skipping clear passes and clear fails.

  Output: the same JSON files enriched in-place, each article gains a `validation`
  block with score, passed (bool), flags[], and layer ("rule" or "llm").
  Phase 6 (embedding) skips any article where validation.passed = false.
-->

**Element 15 — Process: Validate and Score Articles**
- Shape: Rectangle
- Label: `Validate & Score Articles`  
  (sub-text): `Rule-based + LLM scoring`
- Fill: light blue / #DAE8FC
- Add annotation note:
  ```
  Layer 1 (all articles):
    6 rule-based checks → score [0–1]
    pass ≥ 0.75 | borderline 0.50–0.74 | reject < 0.50
  Layer 2 (borderline only):
    GPT-4.1 semantic check → valid / garbled / mismatch
  Result: validation block appended in-place to each article JSON
  ```

**Element 15b — Process: Monitor Validation**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 15c — Decision: Validation Done?**
- Shape: Diamond
- Label: `Validation Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 16 (Phase 6)
  - `No / Error` → Element E5 (End Error)

**Element E5 — Terminator: Error**
- Label: `Pipeline Aborted`  
  (sub-text): `Validation Failed`
- Fill: light red / #FFCCCC

**I/O between Phase 5 and Phase 6:**
- Shape: Parallelogram
- Label: `Validated JSON`  
  (sub-text): `validation.passed = true`

---

### TOP LANE — Phase 6: Embedding (BGE-M3)

**Element 16 — Process: Generate Embeddings**
- Shape: Rectangle
- Label: `Generate Embeddings`  
  (sub-text): `BAAI/bge-m3, local GPU`
- Fill: light blue / #DAE8FC
- Add annotation note:
  ```
  Dense vector: 1024-dim
  Sparse vector: lexical weights
  Input: embedding_text field
  ```

**Element 17 — Process: Monitor Embedding**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 18 — Decision: Embedding Done?**
- Shape: Diamond
- Label: `Embedding Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 19 (Phase 7)
  - `No / Error` → Element E5 (End Error)

**Element E5 — Terminator: Error**
- Label: `Pipeline Aborted`  
  (sub-text): `Embedding Failed`
- Fill: light red / #FFCCCC

**I/O between Phase 6 and Phase 7:**
- Shape: Parallelogram
- Label: `Vectors + Metadata`  
  (sub-text): `.embeddings.json`

---

### TOP LANE — Phase 7: Vector Storage (Qdrant)

**Element 19 — Process: Upsert to Qdrant**
- Shape: Rectangle
- Label: `Upsert Vectors to Qdrant`  
  (sub-text): `Docker, jort_articles_v2`
- Fill: light blue / #DAE8FC
- Add annotation note:
  ```
  Named vectors: dense + sparse
  Hybrid search with RRF
  ```

**Element 20 — Process: Monitor Vector Storage**
- Shape: Rectangle
- Label: `Poll Job Status`  
  (sub-text): `wait → check loop`
- Fill: light blue / #DAE8FC

**Element 21 — Decision: Storage Done?**
- Shape: Diamond
- Label: `Storage Complete?`
- Fill: light yellow / #FFF2CC
- Two outgoing arrows:
  - `Yes` → Element 22 (End Success)
  - `No / Error` → Element E6 (End Error)

**Element 22 — Terminator: Success**
- Shape: Rounded rectangle
- Label: `Pipeline Complete`  
  (sub-text): `Qdrant Indexed`
- Fill: light green / #D5E8D4, thick border

**Element E6 — Terminator: Error**
- Label: `Pipeline Aborted`  
  (sub-text): `Vector Storage Failed`
- Fill: light red / #FFCCCC

---

## I/O Data Shapes — Summary

Place these parallelograms **on the connecting arrow** between each decision `Yes` exit and the next phase's first process box:

| Between phases | Parallelogram label |
|---|---|
| Phase 1 → 2 | `Raw PDFs` / `pdfs/ folder` |
| Phase 2 → 3 | `Backup Confirmed` / `Google Drive` |
| Phase 3 → 4 | `Plain Text Files` / `.txt, one per issue` |
| Phase 4 → 5 | `Structured JSON` / `64 fields per article` |
| Phase 5 → 6 | `Validated JSON` |
| Phase 6 → 7 | `Vectors + Metadata` / `.embeddings.json` |

---

## What NOT to include in the flowchart

- Telegram notification nodes (implementation detail, shown in n8n screenshot)
- n8n node names or HTTP endpoint URLs
- The `start_year` / `end_year` config parameters
- Polling wait durations (10s, 30s, 60s)
- Internal FastAPI job IDs

---

## Color coding summary

| Element type | Fill color |
|---|---|
| Start terminator | White / #FFFFFF, thick border |
| Success end terminator | Light green / #D5E8D4 |
| Error end terminators | Light red / #FFCCCC |
| Process boxes (tasks) | Light blue / #DAE8FC |
| Decision diamonds | Light yellow / #FFF2CC |
| I/O parallelograms | White / #FFFFFF, grey border |
| Lane header — Data Processing | Dark blue / #1E4D8C, white text |
| Lane header — Orchestration | Dark grey / #444444, white text |

---

## Checklist before exporting

- [ ] All 7 phases have a process box, a polling process box (15b for Phase 5), and a decision diamond (15c for Phase 5)
- [ ] Every decision diamond has a `Yes` path (to next phase) and a `No / Error` path (to error terminator)
- [ ] Six I/O parallelograms show what data passes between phases
- [ ] Two swim lanes are visible with correct labels
- [ ] Start terminator is in the bottom lane; all phase boxes are in the top lane
- [ ] No n8n-specific implementation details included
- [ ] Exported at 200 dpi as PNG, landscape orientation
- [ ] Saved as `figures/pipeline_flowchart.png`
