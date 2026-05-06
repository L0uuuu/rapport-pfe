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

"Cannot find reference" warnings in VSCode are usually stale `.aux` file artifacts — a full recompile clears them.

## Document Structure

```
main.tex               — Entry point; loads packages, formatting, inputs all chapters
titlepage.tex          — Cover page with institutional logos and signatures
acronyms.tex           — All \DeclareAcronym definitions (acro package)
references.bib         — Biber/BibLaTeX bibliography (IEEE style)
chapters/
  chapter1.tex         — Chapter I:   Cadre Général du Projet (General Framework)
  chapter2.tex         — Chapter II:  État de l'Art (Literature Review)
  chapter3.tex         — Chapter III: Design and Development
                           Section 1: Definition of Objectives
                           Section 2: Part I — RAG System Implementation
                             2.1 System Architecture
                               2.1.1 Overall Architecture
                               2.1.2 Pipeline Data Flow
                               2.1.3 Technology Stack
                             2.2 Legal Corpus Acquisition
                               2.2.1 Source: JORT
                               2.2.2 Automated PDF Acquisition
                               2.2.3 Cloud Backup
                             2.3 Text Extraction and Article Structuring
                               2.3.1 Hybrid PDF-to-Text Conversion
                               2.3.2 Article-Level Extraction Using GPT-4.1
                               2.3.3 Why Article-Level Extraction Is Preferable
                               2.3.4 Two-Layer Validation and Scoring
                             2.4 Embedding and Vector Storage
                               2.4.1 Embedding Model: BAAI/bge-m3
                               2.4.2 Hybrid Vector Database: Qdrant
                               2.4.3 Retrieval at Inference Time
                             2.5 Pipeline Orchestration
                               2.5.1 FastAPI Service Layer
                               2.5.2 n8n Workflow Automation
                           Part II: Fine-Tuning (to be written)
  annex1.tex           — Appendix A: Legal Article Enrichment Schema (all ~45 fields)
figures/               — All images (logos, diagrams, n8n workflow screenshots)
context_rag/           — Technical documentation for each pipeline phase (source of truth)
```

## LaTeX Conventions

**Numbering:**
- Chapters: Roman numerals (`\renewcommand{\thechapter}{\Roman{chapter}}`)
- Sections: Arabic numerals only (`\renewcommand{\thesection}{\arabic{section}}`)
- Subsubsections: numbered (`\setcounter{secnumdepth}{3}`)
- Figures: chapter-prefixed, continuous within chapter (`\thefigure` = `chapter.figure`)
- Tables: default LaTeX report numbering (chapter-prefixed)

**Key packages:** `biblatex` (biber, IEEE), `acro`, `titlesec`, `fancyhdr`, `geometry`, `float`, `rotating`, `needspace`, `setspace`, `array`, `chngcntr`

**Margins:** top 3cm, bottom 2.5cm, left/right 2.5cm

**Language:** Chapter 3 is in English. Other chapters in French. Acronyms are defined in `acronyms.tex` and used with `\ac{}`, `\acp{}`, `\acl{}` etc.

**Citations:** Use `\cite{}` with keys from `references.bib`. Bibliography printed at end of `main.tex` via `\printbibliography`.

**Appendix:** Added via `\appendix` then `\input{chapters/annex1}` after `\printbibliography` in `main.tex`. LaTeX labels it Appendix A automatically.

**Sideways figures:** Large pipeline diagrams use `\begin{sidewaysfigure}` (from `rotating` package), wrapped in `\clearpage` before and after.

## Writing Style

- **Never use em dashes (—)** in any generated content. Use commas, colons, or rephrase.
- Write in a natural, human-like academic tone. Avoid mechanical or formulaic phrasing.
- **Every figure must be mentioned in the surrounding text.** Always include a `Figure~\ref{fig:label}` reference before or after the figure environment. Never place `\begin{figure}` without a corresponding in-text reference.
- **Do not mention improvements or future work** inside implementation sections. Keep to what was actually built.
- The fine-tuned model is referenced as "the fine-tuned language model, whose training and architecture are detailed in Part II of this chapter." Never name Ollama or qwen3:4b in chapter3.

## Acronyms Defined (acronyms.tex)

`MENA`, `AI`, `SLM`, `LLM`, `TDSP`, `CRISP-DM`, `API`, `SME`, `IBM`, `SPSS`, `ATI`, `RAG`, `DSR`, `PDF`, `HTTP`, `OCR`, `NLP`, `GPU`, `CPU`, `VRAM`, `RAM`, `BERT`, `GPT`, `PEFT`, `LoRA`, `QLoRA`, `FAISS`, `GGUF`, `GPTQ`, `RRF`

When adding new acronyms, declare them in `acronyms.tex` and use `\ac{KEY}` on first occurrence (auto-expands to "Long Form (SHORT)").

## Citation Keys (references.bib) — Chapter 3 relevant

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

## Architecture Notes

- New chapters: add as `chapters/chapterN.tex`, input in `main.tex`.
- New appendices: add after `\appendix` in `main.tex` using `\input{chapters/annexN}`.
- Figures go in `figures/` and are referenced with `\includegraphics{figures/filename}`.
- Figure drawing guides for ChatGPT/draw.io are saved in `figures/*_guide.md`.
