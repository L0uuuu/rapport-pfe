# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LaTeX academic thesis (Rapport de Stage de Fin d'Études / SFE) for a bachelor's degree in Computer Science at Institut Supérieur d'Informatique (ISI), Université Tunis El Manar. The thesis documents building a domain-specific AI legal assistant for Tunisian law at the startup E-Tafakna.

**Author:** Louai Boubaker  
**Academic year:** 2025/2026  
**Subject:** Fine-tuned LLM + RAG pipeline for Tunisian legal documents, on-premises deployment at ATI Tunisie via Ollama

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

## Document Structure

- `main.tex` — Entry point; loads all packages, sets global formatting, inputs all chapters
- `titlepage.tex` — Cover page with institutional logos and signatures
- `acronyms.tex` — All `\DeclareAcronym` definitions (loaded via `acro` package)
- `references.bib` — Biber/BibLaTeX bibliography (IEEE style)
- `chapters/chapter1.tex` — Chapter I: Cadre Général du Projet (General Framework)
- `figures/` — All images (logos, methodology diagrams)

## LaTeX Conventions

**Numbering:**
- Chapters: Roman numerals (`\renewcommand{\thechapter}{\Roman{chapter}}`)
- Sections: Arabic numerals
- Figures: Continuous across chapters (counter not reset per chapter)

**Key packages:** `biblatex` (biber backend, IEEE style), `acro` (acronyms), `titlesec` (section formatting), `fancyhdr` (headers/footers), `geometry` (margins: top 3cm, bottom 2.5cm, left/right 2.5cm)

**Language:** Document content is in French. Acronyms are defined in `acronyms.tex` and used with `\ac{}`, `\acp{}`, `\acl{}` etc.

**Citations:** Use `\cite{}` with keys from `references.bib`. Bibliography is printed where `\printbibliography` appears in `main.tex`.

## Writing Style

- **Never use em dashes (—)** in any generated content. Use commas, colons, or rephrase the sentence instead.
- Write in a natural, human-like academic tone. Avoid overly mechanical or formulaic phrasing.

## Architecture Notes

New chapters should be added as `chapters/chapterN.tex` and included in `main.tex` via `\input{chapters/chapterN}`. Figures go in `figures/` and are referenced with `\includegraphics{figures/filename}` (no extension needed for common formats).
