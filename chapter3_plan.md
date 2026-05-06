# Chapter 3 — Design and Development
## Full Planning Reference (updated from context_rag)

---

## Chapter Title
**DESIGN AND DEVELOPMENT**

---

## Overall Structure

The chapter is divided into two independent but complementary parts:

- **Section 1 & 2:** Introduction + Definition of Objectives (keep as-is)
- **Part I — Sections 3–6:** RAG System: Data Pipeline + Indexing + Retrieval
- **Part II — Sections 7–9:** Fine-Tuning: Data Synthesis + Model Training + Evaluation

---

## Section 1: Introduction  ← KEEP AS-IS

---

## Section 2: Definition of Objectives  ← KEEP AS-IS

---

---

# PART I: RAG SYSTEM IMPLEMENTATION

---

## Section 3: RAG System Architecture

### 3.1 Overall Architecture and Data Flow
- End goal: user asks a question in Arabic or French → system retrieves relevant JORT articles → LLM generates a grounded, sourced answer
- Two distinct flows running in the same system:
  - **Offline pipeline:** raw PDFs → text → structured articles → embeddings → Qdrant (runs once, updated when new JORT issues are published)
  - **Online flow (inference):** user query → embed → vector search → retrieved articles injected into LLM prompt → response
- Figure: high-level architecture diagram (draw in draw.io, export as PNG)

### 3.2 Pipeline Architecture — BPMN Diagram  ← USE BPMN HERE
- BPMN diagram covering the full offline pipeline (7 phases)
- Show the two flows as separate pools or lanes:
  - Offline lane: Scraping → GDrive Upload → Text Extraction → Article Extraction → Embedding → Qdrant
  - Online lane: Query → BGE-M3 embed → Qdrant hybrid search → Prompt assembly → LLM → Response
- Tool: draw.io with BPMN shapes (free)

### 3.3 Technology Stack
| Layer | Technology | Role |
|-------|-----------|------|
| Scraping | Playwright (Python) | Browser automation on iort.gov.tn |
| Storage | Google Drive + rclone | Backup of raw PDFs |
| Text Extraction (digital) | PyMuPDF | Direct text layer extraction |
| Text Extraction (scanned) | Gemini via Vertex AI | OCR for image-based pages |
| Article Extraction | GPT-4.1 (Azure OpenAI) | Two-stage structured extraction |
| Embedding | BAAI/bge-m3 (local) | Dense + sparse vectors (Arabic + French) |
| Vector Database | Qdrant (Docker) | Hybrid search collection `jort_articles_v2` |
| Orchestration | n8n (self-hosted) | Workflow automation across all phases |
| API | FastAPI | HTTP interface for each pipeline phase |

---

## Section 4: Legal Corpus Acquisition

### 4.1 Source: Journal Officiel de la République Tunisienne (JORT)
- Official source: iort.gov.tn — the Tunisian official gazette publishing all laws, decrees, decisions, and official notices
- Three journal sections scraped, each available in Arabic and French:
  - Lois, Décrets, Décisions, Avis (primary legislative content)
  - Annonces Légales (legal notices, sharia, judicial decisions)
  - Tribunal Foncier (land registry court)
- Coverage: [specify year range, e.g., 2015–2026]
- Total: [N issues, N PDFs]

### 4.2 Scraping Pipeline (Phase 1)
- Site uses a legacy WinDev/WebDev application with no public API — browser automation required
- Tool: Playwright (Python, sync API) driving a Chromium instance
- Resumable: checkpoint JSON tracks each file as `downloaded`, `skipped`, or `failed`
- Download triggers differ per section (JavaScript evaluation vs. date link click)
- Triggered via FastAPI endpoint `POST /legal_extraction/scraping/run`, not run directly

### 4.3 Google Drive Backup (Phase 2)
- PDFs mirrored to Google Drive using rclone, orchestrated by n8n
- Preserves the same folder tree: `JORT/<section>/<year>/`
- Serves as backup and allows collaborative access during the project

---

## Section 5: Text Extraction and Article Structuring

### 5.1 Hybrid Text Extraction Strategy (Phase 3)
- Two-condition page routing per page:
  - **Digital pages** (text layer present, >50 chars, <15% image area): extracted with `PyMuPDF` (`page.get_text()`)
  - **Scanned/image pages** (text absent or heavily image-based): sent to Gemini via Vertex AI for OCR
- Gemini handles Arabic RTL tables (rendered as markdown pipe tables), mixed Arabic/French content
- Output: one `.txt` file per JORT issue, with `--- Page N ---` separators

### 5.2 Article-Level Extraction: Two-Stage GPT-4.1 Pipeline (Phase 4)
This is the core structuring step. Rather than generic chunking, legal articles are extracted and enriched as individual semantic units.

**Stage 1 — Boundary Detection:**
GPT-4.1 reads the full document text and identifies article boundaries, returning a raw array with article content, number, title, parent law, and chapter.

**Stage 2 — Semantic Enrichment:**
Each raw article is individually passed back to GPT-4.1 and expanded into the full ~45-field schema:

Key fields per article:
```
jurisdiction, institution, law_type, law_number, year, status
title_french, title_arabic
article_number, article_order, article_type
content_french, content_arabic, content_combined
summary_french, summary_arabic
embedding_text  ← purpose-built field combining title + content + key metadata
keywords, legal_domains, legal_concepts
has_obligations, has_penalties, has_deadlines, has_exceptions
is_abrogation, is_transitional
source_name, source_number, source_date, publication_date
parent_document_id (e.g. tn-jort-035-2026-04-03)
```

Note: the `embedding_text` field is deliberately constructed in Phase 4 to combine the most semantically relevant information before embedding — this is more reliable than generic chunking for legal texts.

**Fallback chain:**
- If Stage 1 AI fails → regex fallback (`Article \d+` pattern)
- If Stage 2 enrichment fails → `_build_fallback()` fills schema with raw content, empty enrichment fields

### 5.3 Why Article-Level Extraction Instead of Generic Chunking
This connects back to the chunking strategies discussed in Chapter II. For JORT documents, the legally meaningful unit is the article — splitting across article boundaries destroys the semantic integrity of legal obligations. The two-stage GPT-4.1 extraction is therefore a form of semantic chunking guided by the document's legal structure, which is the approach recommended in the literature for legal corpora.

---

## Section 6: Embedding and Vector Storage

### 6.1 Embedding Model: BGE-M3 (Phase 6)
- Model: `BAAI/bge-m3` (loaded locally via `FlagEmbedding.BGEM3FlagModel`)
- Produces **two** vector types per article in a single pass:
  - **Dense vector:** 1024-dimensional float list — captures semantic similarity
  - **Sparse vector:** dict of `{token_id: weight}` — captures lexical/keyword precision
- `use_fp16=True` to fit in 4GB VRAM (RTX 3050 compatible)
- Input field: `embedding_text` (constructed in Phase 4, not raw content)
- Batch size: 4 articles per encode call (conservative for VRAM)
- No API call — fully local inference

### 6.2 Hybrid Vector Database: Qdrant (Phase 7)
- Vector DB: Qdrant running in Docker (`docker run ... qdrant/qdrant`)
- Collection: `jort_articles_v2`
- Named vectors: `dense` (1024-dim, cosine similarity) + `sparse` (lexical weights, SparseVectorParams)
- **Hybrid search with RRF fusion at query time:** combines semantic (dense) and keyword (sparse) signals — critical for legal retrieval where exact article numbers and law references matter
- 10 payload fields indexed for filtered retrieval: `year`, `law_type`, `institution`, `legal_domains`, `has_obligations`, `has_penalties`, `is_abrogation`, `source_date`, `parent_document_id`, `status`
- Upsert is idempotent (insert-or-overwrite by UUID) — re-running is safe

### 6.3 Retrieval at Inference Time
- User query embedded with the same BGE-M3 model (dense + sparse)
- Qdrant queried with hybrid search (dense ANN + sparse exact match, fused with RRF)
- Optional payload filters: by law_type, year, language, legal_domain
- Top-k articles returned (k to be tuned during evaluation)
- Retrieved articles injected into LLM prompt as context with source metadata (law_number, article_number, source_date)

### 6.4 n8n Orchestration  ← SHOW n8n SCREENSHOT HERE
- All 7 pipeline phases triggered and monitored through n8n workflows
- Each phase follows the same pattern:
  1. Trigger: call FastAPI endpoint `POST /legal_extraction/<phase>/run`
  2. Poll: `GET /legal_extraction/status/{job_id}` every 30–60 seconds
  3. Branch: `done` → continue to next phase / `failed` → notify
- n8n is self-hosted (Docker), no data leaves the local environment
- Figure: screenshot of the n8n workflow canvas showing the full pipeline

---

---

# PART II: FINE-TUNING

---

## Section 7: Dataset Construction for Fine-Tuning

### 7.1 Data Synthesis Approach
Fine-tuning requires a labeled instruction dataset, not just raw legal text. Since no annotated Tunisian legal Q&A dataset exists publicly, we built one through a guided data synthesis process combining three inputs:

1. **Structured prompt:** defines the format and quality constraints for the generated Q&A pairs
2. **Jurist-generated example questions:** a set of real legal questions written by a legal professional, grounding the synthetic data in authentic legal reasoning patterns
3. **Source PDFs (legal codes and laws):** the actual text of Tunisian legal codes (Code des Obligations et Contrats, Code du Travail, Code de Commerce, etc.) provided as context

GPT-4.1 uses these three inputs to generate additional question-answer pairs in the same style as the jurist examples, ensuring the synthetic data reflects how legal professionals actually query the law.

### 7.2 Dataset Format
Instruction-tuning format (system + user + assistant):

```json
{
  "system": "Tu es un assistant juridique expert en droit tunisien. Réponds uniquement en te basant sur les textes de loi tunisiens.",
  "user": "Quelles sont les conditions de validité d'un contrat selon le COC ?",
  "assistant": "Selon l'article 2 du Code des Obligations et des Contrats tunisien, la validité d'un contrat requiert..."
}
```

Answers include:
- The relevant article number and law name
- The legal content paraphrased or quoted
- Reasoning connecting the question to the legal provision

### 7.3 Dataset Statistics
[To fill in once synthesis is complete]
- Number of source laws/codes covered: [N]
- Number of jurist seed questions: [N]
- Number of synthesized examples: [N]
- Languages: Arabic / French / mixed
- Train / validation split: 90% / 10%

---

## Section 8: Model Selection and Training

### 8.1 Base Model Selection Rationale
Before listing candidates, document the justification for choosing an SLM over a large cloud model:
- **O3 (on-premises):** no external API at inference time — rules out GPT-4.1, Gemini, etc.
- **Hardware budget:** available GPU VRAM limits the maximum model size that can run locally
- **Inference latency:** SLMs return answers in seconds on local hardware; larger models are impractical
- **Selection criteria used:** multilingual support (Arabic + French), instruction-following capability, permissive open-weight license, GGUF-exportable for local inference runtime

### 8.1b Candidate Models
Three open-weight models are evaluated in parallel:

| Model | Parameters | Arabic Support | License | Notes |
|-------|-----------|---------------|---------|-------|
| Qwen 3.5 9B | 9B | Strong | Apache 2.0 | Strong multilingual, good Arabic |
| Gemma 4 4B | 4B | Partial | Gemma ToU | Lightest option, efficient on-premises |
| LLaMA 4 14B | 14B | Moderate | Llama License | Largest of the three, strong general capability |

If none of the three achieve acceptable performance on Tunisian legal Q&A, a larger variant of the best-performing family will be evaluated (e.g., Qwen 3.5 32B).

### 8.2 Fine-Tuning Strategy: QLoRA
- Full fine-tuning excluded: cost and hardware constraints
- QLoRA: 4-bit NF4 base quantization + LoRA adapters trained in bf16
- Target modules: q_proj, v_proj (attention projection layers)
- Approximate trainable parameters: ~1% of total per model

### 8.3 Training Configuration (per model)
| Hyperparameter | Value |
|---------------|-------|
| Quantization | 4-bit NF4 (bitsandbytes) |
| LoRA rank (r) | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Learning rate | 2e-4 |
| Warmup ratio | 0.03 |
| Batch size | 4 (+ gradient accumulation ×4 = effective 16) |
| Epochs | 3 |
| Max sequence length | 2048 tokens |
| Optimizer | paged_adamw_8bit |

### 8.4 Training Infrastructure
- Platform: OVH AI Notebooks
- GPU: [NVIDIA A100 / V100 — confirm from OVH dashboard]
- Framework: Hugging Face Transformers + PEFT + TRL (`SFTTrainer`)
- Three separate training runs (one per model), same hyperparameters for fair comparison
- Checkpoint saved every N steps; best checkpoint selected by validation loss

---

## Section 9: Post-Training and Deployment Preparation

### 9.1 Model Export
- After training: LoRA adapter merged back into base weights
- Exported to GGUF format for Ollama compatibility
- Quantization level for inference: Q4_K_M (balance of speed and quality)

### 9.2 Preliminary Evaluation (in-training)
- Training loss curve per model (figure: export from OVH notebook)
- Validation loss at end of each epoch
- These curves guide the choice of best model before formal evaluation in Chapter 4

### 9.3 Integration with the RAG System
- Fine-tuned model loaded in Ollama as the generation backend
- RAG pipeline (Part I) remains unchanged — only the LLM endpoint changes
- FastAPI `/query` endpoint routes through RAG retrieval → fine-tuned model
- Combined system (fine-tuned LLM + RAG) is the artifact evaluated in Chapter 4

**Prompt template structure (document this in the section):**
The fine-tuned model receives a structured prompt at inference time:
1. **System prompt:** role definition + instruction to answer only from provided legal articles
2. **Retrieved context block:** top-k reranked articles, each with `law_name`, `article_number`, `source_date`, and `content` in the query language (Arabic or French)
3. **User query:** the original question
4. **Expected answer format:** answer grounded in the provided articles, with explicit citations (e.g., "Selon l'article 2 du Code des Obligations et des Contrats...")

If the confidence gate in the retrieval layer fires (best reranker score < 0.4), the model is not called and a bilingual fallback message is returned instead.

---

## Section 10: Conclusion
Two sentences:
- Summarize Part I (JORT pipeline fully operational, Qdrant indexed with hybrid search) and Part II (dataset synthesis underway, three candidate models to be trained with QLoRA on OVH)
- Transition to Chapter 4 (Demonstration and Evaluation)

---

---

## Figures Needed for Chapter 3

| Figure | File | Section | Status |
|--------|------|---------|--------|
| High-level system architecture | `figures/system_architecture.png` | 3.1 | To create (draw.io) |
| BPMN offline + online pipeline | `figures/bpmn_pipeline.png` | 3.2 | To create (draw.io) |
| n8n workflow screenshot | `figures/n8n_workflow.png` | 6.4 | Screenshot from n8n canvas |
| Training loss curves (×3 models) | `figures/training_loss_qwen.png` etc. | 9.2 | From OVH notebook after training |

---

## Citations Still Needed

| Item | Needed For | Suggested Key |
|------|-----------|---------------|
| Playwright | Scraping tool | `playwright2024docs` |
| PyMuPDF | Text extraction | `pymupdf2024docs` |
| Qdrant | Vector DB | `qdrant2024docs` (already in bib) |
| Hugging Face PEFT | QLoRA framework | `huggingface2023peft` |
| TRL / SFTTrainer | Training framework | `huggingface2023trl` |
| bitsandbytes | 4-bit NF4 quantization | already covered by `dettmers2023qlora` |
| Docker | Container deployment | `docker2024docs` |

---

## n8n vs BPMN — Final Decision

**Use BPMN in Section 3.2** for the pipeline architecture diagram:
- ISO standard (ISO 19510), immediately readable by jury
- Shows the logical design independent of the tool used
- Draw in draw.io → File → Shapes → BPMN (free)

**Use n8n screenshot in Section 6.4** for the orchestration implementation:
- Proves the system is actually built and running
- Shows real nodes, real polling loops, real phase chaining
- These two figures are complementary: design vs. implementation
