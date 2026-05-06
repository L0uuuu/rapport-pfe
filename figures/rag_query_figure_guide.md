# RAG Query Flow — Figure Drawing Guide

**Purpose:** Describe the runtime query flow of `rag/query.py` so a diagram tool can produce a clean figure for the thesis.  
**Suggested tool:** draw.io, Lucidchart, or any flowchart tool.  
**Orientation:** Portrait or landscape, single vertical flow (top to bottom).  
**Notation:** Standard flowchart (ISO 5807) — same shape language as the pipeline flowchart.

---

## Shape Legend

| Shape | Meaning |
|---|---|
| Rounded rectangle (stadium) | Start / End terminator |
| Rectangle | Process step |
| Diamond | Decision / branch |
| Parallelogram | Input / Output (data) |
| Solid arrow | Control flow |
| Dashed arrow | Data association |

---

## Color Coding

| Element | Fill color |
|---|---|
| Start / End terminators | White `#FFFFFF`, thick border |
| Process boxes | Light blue `#DAE8FC` |
| Decision diamonds | Light yellow `#FFF2CC` |
| I/O parallelograms | White `#FFFFFF`, grey border |
| Model / external service boxes | Light purple `#E1D5E7` |

---

## Full Flow — Top to Bottom

---

### Step 1 — Start

**Terminator: Start**
- Label: `User Query`
- Sub-text: `French or Arabic question`
- Shape: Rounded rectangle, white, thick border

---

### Step 2 — Language Detection

**Process: Detect Language**
- Label: `Detect Query Language`
- Sub-text: `Arabic Unicode chars > 20% → AR, else → FR`
- Shape: Rectangle, light blue

**Decision: Language?**
- Label: `Language?`
- Shape: Diamond, light yellow
- Two outgoing arrows:
  - `Arabic` → mark variable `lang = AR`
  - `French` → mark variable `lang = FR`
- Both arrows rejoin into Step 3

---

### Step 3 — Query Embedding

**Process: Embed Query**
- Label: `Embed Query`
- Sub-text: `BAAI/bge-m3 (same model as indexing)`
- Shape: Rectangle, light purple (model box)
- Add annotation note:
  ```
  Output:
  • Dense vector  — 1024-dim float array
  • Sparse vector — token-id → weight mapping
  max_length = 512
  ```

---

### Step 4 — Hybrid Vector Search

**Process: Hybrid Search in Qdrant**
- Label: `Hybrid Search`
- Sub-text: `Qdrant — jort_articles_v2`
- Shape: Rectangle, light blue
- Add annotation note:
  ```
  Prefetch dense  → 80 candidates
  Prefetch sparse → 80 candidates
  FusionQuery(RRF) → 20 candidates
  Optional: FieldCondition filter on "year"
  ```

**I/O — Output of search:**
- Shape: Parallelogram
- Label: `20 Candidate Articles`
- Sub-text: `RRF-ranked`

---

### Step 5 — Cross-Encoder Reranking

**Process: Rerank Candidates**
- Label: `Cross-Encoder Reranking`
- Sub-text: `BAAI/bge-reranker-v2-m3`
- Shape: Rectangle, light purple (model box)
- Add annotation note:
  ```
  Score each (question, article) pair jointly
  normalize=True → sigmoid [0, 1]
  Keep top-k articles (default k = 5)
  ```

**I/O — Output of reranking:**
- Shape: Parallelogram
- Label: `Top-k Articles`
- Sub-text: `reranker score + metadata`

---

### Step 6 — Context Formatting

**Process: Format Retrieved Context**
- Label: `Format Context`
- Sub-text: `Select content field by lang`
- Shape: Rectangle, light blue
- Add annotation note:
  ```
  lang = AR → content_arabic
  lang = FR → content_french
  Include: law type, number, date per article
  ```

---

### Step 7 — Prompt Construction

**Process: Build Prompt**
- Label: `Construct Prompt`
- Shape: Rectangle, light blue
- Add annotation note:
  ```
  System prompt (bilingual, matches lang)
  + Conversation history (interactive mode only)
  + Retrieved articles as context
  + User question
  ```

---

### Step 8 — LLM Answer Generation

**Process: Generate Answer**
- Label: `Generate Answer`
- Sub-text: `Fine-tuned Legal LLM`
- Shape: Rectangle, light purple (model box)
- Add annotation note:
  ```
  Streaming output
  temperature = 0.1
  ```

---

### Step 9 — Stream Answer

**I/O — Output:**
- Shape: Parallelogram
- Label: `Streamed Answer`
- Sub-text: `with legal citations`

---

### Step 10 — Interactive Mode Branch

**Decision: Interactive Mode?**
- Label: `Interactive Mode?`
- Shape: Diamond, light yellow
- Two outgoing arrows:
  - `Yes` → Step 11 (save to history)
  - `No`  → End

---

### Step 11 — Save to History

**Process: Update Conversation History**
- Label: `Append to History`
- Sub-text: `Trim to last N turns`
- Shape: Rectangle, light blue
- Arrow loops back up to **Step 1** (next user question)

---

### Step 12 — End

**Terminator: End**
- Label: `Session End`
- Shape: Rounded rectangle, white, thick border

---

## Simplified Version (for thesis figure — recommended)

If the full flow is too wide, use this condensed 6-box vertical layout:

```
[User Query]
     ↓
[Language Detection]  ←  AR or FR
     ↓
[Query Embedding]     ←  BAAI/bge-m3
     ↓
[Hybrid Search]       ←  Qdrant (dense + sparse → RRF → 20 candidates)
     ↓
[Cross-Encoder Reranking]  ←  BAAI/bge-reranker-v2-m3 → top-k articles
     ↓
[Prompt Construction]  ←  system prompt + history + context + question
     ↓
[Answer Generation]   ←  Fine-tuned Legal LLM (streaming)
     ↓
[Streamed Answer with Legal Citations]
```

Annotations on arrows are sufficient — no need for decision diamonds in the simplified version.

---

## What NOT to include

- Internal Python class names (`BGEM3FlagModel`, `FlagReranker`)
- CLI argument names (`--top-k`, `--no-rerank`, `--history-turns`)
- The `<think>` token stripping detail
- Checkpoint or job IDs
- Qdrant SDK internals (`FusionQuery`, `MatchValue`)

---

## Export

- Format: PNG, 200 dpi minimum
- Save as: `figures/rag_query_flow.png`
