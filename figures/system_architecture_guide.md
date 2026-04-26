# system_architecture.png — Drawing Guide

**Tool:** draw.io (app.diagrams.net) — File → Export → PNG at 150+ dpi  
**Canvas size:** Landscape, roughly 1400 × 700 px  
**Style goal:** Clean, two-lane block diagram. No icons required — labeled rectangles are enough.

---

## What "offline" and "query-time" mean

Both flows run **entirely on-premises**. No internet connection is used at inference time.

- **Offline / Indexing pipeline:** runs once when the system is set up, and again whenever new JORT issues are published. Produces the vector database. Users never interact with it directly.
- **Query-time flow:** runs every time a user asks a question. Retrieves articles from the already-built vector database and generates a response using the local Ollama model. 100% on-premises.

The word "online" is a technical ML term for "at runtime" and does NOT mean "internet-connected." The guide below uses the clearer label **"Query-Time Flow"** instead.

---

## What the figure must show

The figure illustrates the **two flows** of the legal AI system that share the same data layer:

1. **Data Indexing Pipeline** (top lane) — runs once / on update
2. **Query-Time Flow** (bottom lane) — runs per user question, fully on-premises
3. **Shared Data Layer** (center) — the Qdrant vector database that both flows touch

---

## Layout (left → right)

### LANE 1 — DATA INDEXING PIPELINE (top half)

Draw a horizontal sequence of 7 boxes connected by arrows →

```
[ iort.gov.tn ]
      ↓ (Playwright)
[ Raw PDFs ]
      ↓ (rclone)
[ Google Drive Backup ]
      ↓ (PyMuPDF / Gemini OCR)
[ Plain Text Files ]
      ↓ (GPT-4.1 Azure — Stage 1 + Stage 2)
[ Structured JSON Articles ]
      ↓ (BGE-M3 local)
[ Dense + Sparse Vectors ]
      ↓ (Qdrant Docker)
[ Qdrant — jort_articles_v2 ]   ← SHARED LAYER
```

Label each arrow with the tool name (small grey text under arrow).

Add a label/badge on Google Drive: "Cloud Backup (rclone)"  
Add a label/badge on GPT-4.1 step: "45-field schema"  
Add a label/badge on Qdrant: "dense + sparse vectors"

### LANE 2 — QUERY-TIME FLOW (bottom half, fully on-premises)

Draw a horizontal sequence going left → right, arriving at Qdrant from the bottom:

```
[ User Query ]
      ↓ (BGE-M3 local — same model)
[ Query Embedding ]
      → [ Qdrant Hybrid Search ] ← same Qdrant box as above
              ↓ (Top-k articles + metadata)
      [ Prompt Assembly ]
              ↓
      [ LLM (Ollama — fine-tuned model) ]
              ↓
      [ Response to User ]
```

### SHARED ELEMENT (center)

The **Qdrant** box appears once and is touched by both lanes (arrow from offline pointing in from top, arrow from online pointing in from left, arrow out going down to Prompt Assembly).

---

## Box colors (suggested)

| Element | Color |
|---|---|
| External source (iort.gov.tn) | Light orange / #FFD580 |
| Offline pipeline boxes | Light blue / #DAE8FC |
| Shared Qdrant box | Dark blue / #6C8EBF with white text |
| Online inference boxes | Light green / #D5E8D4 |
| LLM box (Ollama) | Light purple / #E1D5E7 |
| User boxes (query + response) | White with grey border |

---

## Labels to include

- Top-left corner: small label **"Data Indexing Pipeline"** (grey, italic)
- Bottom-left corner: small label **"Query-Time Flow (on-premises)"** (grey, italic)
- Arrow from Qdrant to Prompt Assembly: **"Top-k articles + metadata"**
- Arrow from BGE-M3 (offline) to Qdrant: **"Upsert (idempotent)"**
- Arrow from BGE-M3 (online) to Qdrant: **"Hybrid search (RRF)"**

---

## What NOT to draw

- Do NOT draw n8n internals here (that is the BPMN figure)
- Do NOT draw FastAPI boxes (too much detail)
- Do NOT show the article schema fields

---

## Minimum elements checklist

- [ ] iort.gov.tn source box
- [ ] Playwright arrow label
- [ ] Raw PDFs box
- [ ] Google Drive backup box
- [ ] Text Extraction box (label: "PyMuPDF / Gemini OCR")
- [ ] Article Extraction box (label: "GPT-4.1 Azure")
- [ ] Embedding box (label: "BGE-M3 (local)")
- [ ] Qdrant box (central shared element)
- [ ] User Query box
- [ ] Query Embedding box (same BGE-M3 model)
- [ ] Prompt Assembly box
- [ ] LLM / Ollama box
- [ ] Response box
- [ ] Two lane separators or background rectangles
- [ ] Legend or lane labels (Offline / Online)

---

## Example draw.io steps

1. Open app.diagrams.net → Blank diagram
2. Set page to Landscape (File → Page Setup)
3. Draw two large background rectangles side by side vertically (top = offline, bottom = online) — set fill to very light grey, no border
4. Add process boxes inside each lane
5. Connect with directional arrows
6. Add small grey text labels on arrows
7. Export: File → Export As → PNG → 150 dpi → scale 100%
8. Save as `figures/system_architecture.png`
