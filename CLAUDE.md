# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LaTeX academic thesis (Rapport de Stage de Fin d'Études / SFE) for a bachelor's degree in Computer Science at Institut Supérieur d'Informatique (ISI), Université Tunis El Manar. The thesis documents building a domain-specific AI legal assistant for Tunisian law at the startup E-Tafakna.

**Author:** Louai Boubaker  
**Academic year:** 2025/2026  
**Subject:** Fine-tuned LLM + RAG pipeline for Tunisian legal documents, on-premises deployment at ATI Tunisie

## Building the Document

Full compilation sequence (required for bibliography and cross-references):
```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Single-pass compile (no bibliography update):
```bash
pdflatex main.tex
```

"Cannot find reference" warnings in VSCode are usually stale `.aux` file artifacts — a full recompile clears them. Close the PDF viewer before compiling or the output file will be locked and `dvipdfmx` will fail.

## Document Structure

```
main.tex               — Entry point; loads packages, formatting, inputs all chapters
titlepage.tex          — Cover page (French) with three logos: stava_isi.png, logo_E-tafakna.png, carbon_signature.png
acronyms.tex           — All \DeclareAcronym definitions (acro package)
references.bib         — Biber/BibLaTeX bibliography (IEEE style)
chapters/
  page_signature.tex   — Signature page (English): company supervisor (with signature + stamp images) and academic supervisor
  dedication.tex       — Honorable mention to children killed in war (Palestine, Lebanon, Congo, Sudan)
  dedicace.tex         — Personal dedication to parents, family, and friends
  remerciements.tex    — Acknowledgments (English) to Dhikra Ben Mahmoud, Bakhta Haouari, Norchen Mezni
  chapter1.tex         — Chapter I:   Cadre Général du Projet (General Framework) [French]
  chapter2.tex         — Chapter II:  État de l'Art (Literature Review) [French]
  chapter3.tex         — Chapter III: Design and Development [English]
                           Section 1: Definition of Objectives
                           Section 2: Part I — RAG System Implementation
                             2.1 System Architecture
                             2.2 Legal Corpus Acquisition
                               2.2.1 Source: JORT
                               2.2.2 Downloading the Legal Corpus: Automated PDF Acquisition
                               2.2.3 Cloud Backup
                             2.3 Text Extraction and Article Structuring
                               2.3.1 Reading the Documents: Hybrid PDF-to-Text Conversion
                               2.3.2 Isolating Each Legal Article: Article-Level Extraction Using GPT-4.1
                               2.3.3 Why Article-Level Extraction Is Preferable
                               2.3.4 Keeping Only Quality Articles: Two-Layer Validation and Scoring
                             2.4 Embedding and Vector Storage
                               2.4.1 Turning Text into Searchable Numbers: Embedding Model (BAAI/bge-m3)
                               2.4.2 Where the Articles Are Stored: Hybrid Vector Database (Qdrant)
                               2.4.3 When a User Asks a Question: Retrieval at Inference Time
                             2.5 Pipeline Orchestration
                               2.5.1 FastAPI Service Layer
                               2.5.2 n8n Workflow Automation
                           Section 3: Part II — Fine-Tuning
                             2.6 Base Model Selection
                             2.7 Training Data Synthesis
                             2.8 Fine-Tuning Methodology
                               2.8.1 Adapter Configuration (LoRA / QLoRA per model)
                               2.8.2 What the Model Is Trained to Do: Response-Only Masking
                               2.8.3 Out-of-Memory Error and Parameter Adjustment
                             2.9 Training Configuration
                               2.9.1 Hyperparameters (both models identical)
                               2.9.2 Training Infrastructure (OVHcloud V100S)
                             2.10 Quantization and Deployment
                               2.10.1 LoRA Adapter Export
                               2.10.2 Preparing the Model for Production: GGUF Export and Local Deployment (Ollama)
                           Section 4: Conclusion
  chapter4.tex         — Chapter IV: Demonstration and Evaluation [English]
                           Section 1: Introduction
                           Section 2: Part I — Demonstration
                             2.1 System Overview at Demo Time
                               — offline flow: n8n + FastAPI (preparation only)
                               — runtime flow: rag/query.py (bge-m3 → Qdrant → reranker → Ollama)
                             2.2 Pipeline Execution
                               — schedule trigger (manual for testing)
                               — Telegram notifications as pipeline log
                               — n8n logs + FastAPI logs figures
                             2.3 Example Queries and System Responses
                               — Query 1: COC Art.2 contract validity (both model responses)
                               — Query categories table (4 types)
                             2.4 Pipeline Execution Walkthrough (rag/query.py steps 1-7)
                             2.5 Streamlit Interface (rag/streamlit_app.py; fig:streamlit-interface)
                           Section 3: Part II — Evaluation
                             3.1 Evaluation Framework (6 categories, 20 Q each except routing=15, binary rating)
                             3.2 Results by Category (table + per-category discussion)
                             3.3 Limitations (Qwen quantization noise; routing gap)
                             — 80% acceptance threshold; routing only category below 80% for Gemma
                             — Gemma all ≥ 80%; Qwen meets 80% on all non-routing categories
  annex1.tex           — Appendix A: Legal Article Enrichment Schema (all ~45 fields)
  annex2.tex           — Appendix B: Fine-Tuning Dataset Full Reference (question types, legal codes, data format, limitations)
  annex3.tex           — Appendix C: Carbon Footprint of the Final Year Project (English)
                           — Total: 1,103.7 kg CO2e; Transport 96.1%, Hardware 1.3%, Infra 2.3%, Office 0.2%
                           — 130 pages printed; 85 km one-way commute; 26 on-site days
figures/               — All images (logos, diagrams, n8n workflow screenshots)
context_rag/           — Technical documentation for each pipeline phase (source of truth)
context_fine-tuning/   — Technical documentation for the fine-tuning pipeline (source of truth)
scripts/               — Utility scripts
  generate_charts.py              — Dataset composition/category/language charts (Chapter 3)
  generate_evaluation_chart.py    — Expert evaluation grouped bar chart → figures/jurist_evaluation.png
```

## LaTeX Conventions

**Numbering:**
- Chapters: Roman numerals (`\renewcommand{\thechapter}{\Roman{chapter}}`)
- Sections: Arabic numerals only (`\renewcommand{\thesection}{\arabic{section}}`)
- Subsubsections: numbered (`\setcounter{secnumdepth}{3}`)
- Figures: chapter-prefixed (`\thefigure` = `chapter.figure`), `\counterwithout{figure}{chapter}`
- Tables: Arabic chapter-prefixed (`\counterwithout{table}{chapter}` + `\renewcommand{\thetable}{\arabic{chapter}.\arabic{table}}`)

**Key packages (loading order matters):**
```
fontspec, polyglossia  ← MUST come before biblatex (or biblatex errors on polyglossia)
biblatex (biber, IEEE)
graphicx, tikz
titlesec, chngcntr, acro, xpatch
array, float, subcaption, rotating
geometry, setspace, needspace, fancyhdr
amsmath, amssymb
xcolor [table]         ← [table] option for \rowcolor in tables
hyperref               ← always last
```

**Margins:** top 3cm, bottom 2.5cm, left/right 2.5cm

**Language:** Chapters 3, 4, and appendices are in English. Chapters 1, 2 in French. Acronyms are defined in `acronyms.tex` and used with `\ac{}`, `\acp{}`, `\acl{}` etc.

**Citations:** Use `\cite{}` with keys from `references.bib`. Bibliography printed at end of `main.tex` via `\printbibliography`.

**Appendix:** Added via `\appendix` then `\input{chapters/annexN}` after `\printbibliography` in `main.tex`. Currently: annex1 (A), annex2 (B), annex3 (C). LaTeX labels them automatically.

**Sideways figures:** Large pipeline diagrams use `\begin{sidewaysfigure}` (from `rotating` package), wrapped in `\clearpage` before and after.

**Side-by-side figures:** Use two `\begin{minipage}[t]{0.48\textwidth}` blocks with `\hfill` between them and `\subcaption*{}` for unlabeled subcaptions (requires `subcaption` package).

**Colored table headers:** `\rowcolor{green!25}` on the header row (requires `\usepackage[table]{xcolor}`).

**Signature boxes:** `\signaturebox{Title}{Content}` defined via TikZ in `page_signature.tex`. The company supervisor box contains actual images (`signatur_nourchen.png` + `stamp_etafakna.png`, both in `.gitignore`).

## Writing Style

- **Never use em dashes (—)** in any generated content. Use commas, colons, or rephrase.
- Write in a natural, human-like academic tone. Avoid mechanical or formulaic phrasing.
- **Every figure must be mentioned in the surrounding text.** Always include a `Figure~\ref{fig:label}` reference before or after the figure environment. Never place `\begin{figure}` without a corresponding in-text reference.
- **Do not mention improvements or future work** inside implementation sections. Keep to what was actually built.
- The fine-tuned model is referenced as "the fine-tuned language model, whose training and architecture are detailed in Part II of this chapter." Never name Ollama or qwen3:4b in chapter3.

## Acronyms Defined (acronyms.tex)

`MENA`, `AI`, `SLM`, `LLM`, `TDSP`, `CRISP-DM`, `API`, `SME`, `IBM`, `SPSS`, `ATI`, `RAG`, `DSR`, `PDF`, `HTTP`, `OCR`, `NLP`, `GPU`, `CPU`, `VRAM`, `RAM`, `BERT`, `GPT`, `PEFT`, `LoRA`, `QLoRA`, `FAISS`, `GGUF`, `GPTQ`, `RRF`, `QA`, `JORT`, `PLE`

When adding new acronyms, declare them in `acronyms.tex` and use `\ac{KEY}` on first occurrence (auto-expands to "Long Form (SHORT)").

## Citation Keys (references.bib)

| Key | What it cites |
|---|---|
| `playwright2024docs` | Playwright for Python |
| `pymupdf2024docs` | PyMuPDF |
| `google2024vertexai` | Google Vertex AI (Gemini OCR) |
| `microsoft2024azureopenai` | Azure OpenAI / GPT-4.1 |
| `chen2024bgem3` | BAAI/bge-m3 embedding model |
| `bge_reranker2024` | BAAI/bge-reranker-v2-m3 |
| `qdrant2024docs` | Qdrant vector database |
| `fastapi2024docs` | FastAPI |
| `n8n2024docs` | n8n workflow automation |
| `python2024docs` | Python |
| `microsoft2024vscode` | VS Code |
| `qwen2026qwen35` | Qwen3.5 9B (Alibaba Cloud) |
| `google2025gemma4` | Gemma 4 E4B (Google DeepMind) |
| `ibm2025syntheticdata` | IBM — What Is Synthetic Data? |
| `pvml2025syntheticdata` | PVML — Synthetic Data glossary + domain figure |
| `gartner2023syntheticdata` | Gartner 60% synthetic data prediction |
| `streamlit2024docs` | Streamlit (used for rag/streamlit_app.py demo interface) |

## Context Files (context_rag/)

These markdown files are the authoritative technical reference for the RAG pipeline. Always read the relevant one before writing or editing chapter3 content.

| File | Covers |
|---|---|
| `00_overview.md` | Full pipeline overview and architecture |
| `01_scraping.md` | Phase 1: Playwright scraper for iort.gov.tn |
| `02_google_drive_upload.md` | Phase 2: rclone Google Drive backup |
| `03_text_extraction.md` | Phase 3: PyMuPDF + Gemini hybrid OCR |
| `04_article_extraction.md` | Phase 4: GPT-4.1 two-stage extraction + full schema |
| `05_validation_scoring.md` | Phase 5: two-layer rule + LLM validation |
| `06_embedding.md` | Phase 6: bge-m3 dense + sparse embeddings |
| `07_vector_storage.md` | Phase 7: Qdrant collection setup and upsert |
| `08_rag_query.md` | Query layer: language detection, hybrid search, reranking, confidence gating |
| `api_documentation.md` | FastAPI endpoint reference |
| `n8n_workflow_nodes.md` | n8n node-by-node description |

## Key Design Decisions (chapter 3)

- **Article-level chunking** over fixed/recursive chunking: each article is the natural unit of Tunisian legal citation and meaning.
- **embedding_text field**: purpose-built passage (title + body + concepts + law name) fed to the embedding model instead of raw content.
- **Two-layer validation**: rule-based scoring (threshold 0.75) + GPT-4.1 semantic check for borderline articles (0.50–0.74). Articles below 0.50 or failing Layer 2 are excluded from embedding.
- **Hybrid search**: bge-m3 produces both dense (1024-dim) and sparse (lexical) vectors. Qdrant merges via RRF. Handles both semantic and exact-term legal queries.
- **Cross-encoder reranking**: bge-reranker-v2-m3 scores (question, article) pairs jointly; 20 Qdrant candidates → top-k. More precise than vector similarity alone.
- **Confidence gating**: if best reranker score < 0.4, LLM call is skipped and a bilingual "no relevant articles" message is returned. Prevents hallucinations on out-of-domain queries.
- **On-premises**: no data leaves the local environment at any stage. All models run locally except GPT-4.1 (Azure, pipeline-only) and Gemini (OCR, pipeline-only).
- **Base models for fine-tuning**: Qwen3.5 9B (Gated Delta Networks + sparse MoE, 201 languages, Apache 2.0) and Gemma 4 E4B (PLE architecture, 128K context, Apache 2.0).
- **Fine-tuning methods**: Gemma 4 E4B uses LoRA on fp16 base; Qwen3.5 9B uses QLoRA (4-bit NF4 base) because fp16 loading exceeded 32 GiB VRAM ceiling. Both trained on OVHcloud V100S 32 GiB.
- **Training results**: Gemma — 3,357s, loss 0.0586, VRAM 30.8 GiB, 40.6M trainable params (0.51%), adapter 185.6 MB. Qwen — 15,223s, loss 0.8208, VRAM 11.2 GiB, 29.1M trainable params (0.31%), adapter 130.1 MB. Both exported to GGUF q4_k_m and served via Ollama.
- **Training dataset**: 1,619 cleaned examples across Tunisian legal codes, RAG-aware format with "Documents pertinents" block mirroring production inference.
- **RAG query pipeline** (runtime, NOT n8n/FastAPI): `rag/query.py` — language detection → bge-m3 embedding → Qdrant hybrid search (RRF, top-20) → bge-reranker reranking → confidence gate (threshold 0.4) → Ollama generation. n8n + FastAPI are offline preparation only.
- **n8n trigger**: schedule trigger in production; manual trigger for testing. Sends Telegram notifications at start/end of each phase.

## Expert Evaluation (chapter 4) — Final Numbers

6 categories evaluated by a legal domain expert. Binary correct/incorrect per question. 80% acceptance threshold.

| Category | Total Q | Gemma correct | Gemma % | Qwen correct | Qwen % |
|---|---|---|---|---|---|
| Direct QA | 20 | 19 | 95% | 18 | 90% |
| Multi-article synthesis | 20 | 17 | 85% | 16 | 80% |
| Principle and exception | 20 | 17 | 85% | 16 | 80% |
| In-domain refusal | 20 | 18 | 90% | 16 | 80% |
| Clarification | 20 | 17 | 85% | 16 | 80% |
| Routing | 15 | 11 | 73% | 9 | 60% |

- Gemma meets 80% on all categories except Routing (73%).
- Qwen meets 80% on all non-routing categories; Routing is 60%.
- Routing is the only category where both models fall below 80%.
- Qwen performance gap attributed to 4-bit NF4 quantization noise (QLoRA).
- Chart generated by `scripts/generate_evaluation_chart.py` → `figures/jurist_evaluation.png`.

## Figures in Chapter 3

| Label | File | Description |
|---|---|---|
| `fig:system-architecture` | `system_architecture.png` | Overall two-flow architecture (sidewaysfigure) |
| `fig:flowchart-pipeline` | `flowchart_pipeline.jpg` | 7-phase offline pipeline flowchart (sidewaysfigure) |
| `fig:scraping-workflow` | `scraping_workflow.png` | n8n Phase 1 sub-workflow |
| `fig:upload-workflow` | `uploding_workflow.png` | n8n Phase 2 sub-workflow |
| `fig:text-extraction-workflow` | `text_extracion_workflow.png` | n8n Phase 3 sub-workflow |
| `fig:article-extraction-workflow` | `articles_extraction_workflow.png` | n8n Phase 4 sub-workflow |
| `fig:validation-workflow` | `articles_validation_wrokflow.png` | n8n Phase 5 sub-workflow |
| `fig:embedding-workflow` | `embedding_workflow.png` | n8n Phase 6 sub-workflow |
| `fig:vector-storage-workflow` | `vector_storage_workflow.png` | n8n Phase 7 sub-workflow |
| `fig:rag-query-flow` | `rag_query_flow.png` | RAG query flow diagram |
| `fig:n8n-workflow` | `n8n_workflow.png` | Full n8n orchestration workflow |
| `fig:dataset-composition` | `dataset_composition.png` | Fine-tuning dataset composition by type |
| `fig:question-categories` | `question_categories_chart.png` | Question category distribution |
| `fig:language-distribution` | `language_distribution_chart.png` | Language distribution across training dataset |
| `fig:synthetic-data-domains` | `synthetic_data_domains.png` | Industries using synthetic data (from pvml.com) |
| `fig:ovh-notebook-gemma` | `ovh_notebook.png` | OVHcloud AI Notebook instance for Gemma 4 E4B fine-tuning |
| `fig:ovh-notebook-qwen` | `ovh_notebook_qwen.png` | OVHcloud AI Notebook instance for Qwen3.5 9B fine-tuning |

## Figures in Chapter 4

| Label | File | Description |
|---|---|---|
| `fig:qdrant-collection` | `qdrant_collection.png` | Qdrant dashboard showing jort_articles_v2 collection after indexing |
| `fig:telegram-notifications` | `telegram_1.png` + `telegram_2.png` | Telegram bot notifications during pipeline run (side by side) |
| `fig:n8n-logs` | `n8n_logs.png` | n8n execution panel during pipeline run |
| `fig:fastapi-logs` | `fastAPI_logs.png` | FastAPI server terminal logs during pipeline run |
| `fig:streamlit-interface` | `streamlit_interface.png` | Streamlit demo interface for rag/query.py |
| `fig:jurist-evaluation` | `jurist_evaluation.png` | Expert evaluation grouped bar chart (generated by scripts/generate_evaluation_chart.py) |

## Architecture Notes

- New chapters: add as `chapters/chapterN.tex`, input in `main.tex`.
- New appendices: add after `\appendix` in `main.tex` using `\input{chapters/annexN}`.
- Figures go in `figures/` and are referenced with `\includegraphics{figures/filename}`.
- Figure drawing guides for ChatGPT/draw.io are saved in `figures/*_guide.md`.
- Sensitive files in `.gitignore`: `signatur_nourchen.png`, `stamp_etafakna.png`.
