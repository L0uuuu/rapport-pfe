# Synthetic Data Summary — Fine-Tuning Dataset

**Project:** Tunisian Legal RAG Chatbot (E-Tafakna platform)
**Date:** May 6, 2026

---

## What Is Synthetic Data in This Project

Synthetic data refers to all training examples that were **AI-generated** (not taken from real user conversations). It makes up the vast majority of the dataset and exists in two forms: standard Q&A batches and complex scenario batches.

---

## Volume & Composition

| Type | Files | Examples | Location |
|------|-------|----------|----------|
| Standard Q&A batches | batch JSON files | 1,543 | `constructed data/batch_*.json` |
| Darija (dialect) examples | included in above | 77 | `constructed data/all_messages.json` |
| Complex scenario batches | 4 batch JSON files | 20 | `complex data/batch_scenarios_*.json` |
| **Constructed total** | — | **1,620** | (merged into `all_messages.json`) |
| Real user Q&A | 1 file | 44 | `added data/elyssa_conversations_final.json` |
| Out-of-scope refusals | 1 file | 38 | `added data/batch_out_of_scope_001_*.json` |
| Service routing | 1 file | 60 | `added data/batch_routing_001_*.json` |
| **Added data total** | — | **142** | `added data/` |
| **Grand total** | — | **~1,762** | — |

The merged constructed file is at [constructed data/all_messages.json](constructed%20data/all_messages.json).

---

## Legal Codes Covered

Each batch covers one Tunisian legal code. The naming convention is `batch_<CODE>_<N>_<YYYYMMDD>.json`.

| Code Abbreviation | Full Name | Batches |
|---|---|---|
| CAC | Code des activités commerciales | 3 |
| CCL | Code civil (obligations/leasing) | 3 |
| CCP | Code de commerce (procédures) | 3 |
| CC | Code civil | 3 |
| CDET | Code des droits et des engagements du trésor | 3 |
| CDIP | Code de droit international privé | 2 |
| CDPF | Code des droits et procédures fiscaux | 3 |
| CDR | Code de la route | 3 |
| CFL | Code des finances locales | 3 |
| CIRPP_IS | Code de l'IRPP et IS (impôt sur les sociétés) | 3 |
| CMM | Code maritime | 3 |
| CN | Code du notariat | 1 |
| COC | Code des obligations et contrats | 3 |
| CODES_DOUANES | Code des douanes | 4 |
| CODE_DES_CHANGES | Code des changes | 3 |
| CODE_EAUX | Code des eaux | 3 |
| const_2022 | Constitution tunisienne 2022 | 3 |
| CP | Code pénal | 3 |
| CTM | Code du travail maritime | 3 |
| PRESSE | Code de la presse | 2 |
| CD (scenarios) | Code de la douane (complex) | 1 |
| COC (scenarios) | Code des obligations et contrats (complex) | 1 |
| CP (scenarios) | Code pénal (complex) | 1 |
| IRPP_IS (scenarios) | IRPP/IS fiscal code (complex) | 1 |

---

## Question Types by Source

### constructed data — Standard Q&A Batches

Each batch contains 20 examples distributed across 6 question categories. Actual counts across all batches:

| Category | `category` value | Total | Description |
|---|---|---|---|
| Direct grounded Q&A | `direct` | 348 | Factual question answered by a single article |
| Multi-article synthesis | `multi_article` | 214 | Question requiring 2–3 related articles to answer |
| Principle + exception | `principle_exception` | 190 | States the rule, then its exceptions or nuances |
| Refusal (in-domain) | `refusal` | 158 | Plausible question the code does NOT answer — model declines and recommends a lawyer |
| Procedural / lifecycle | `procedural` | 128 | Questions about sequential legal processes or phases |
| Clarification | `clarification` | 121 | Ambiguous question — model asks for clarification before answering |
| Out-of-scope refusal | `out_of_scope_refusal` | 38 | Requests outside Tunisian law scope (generated in out-of-scope batch, ended up merged here) |

**Target composition per batch (20 examples):**

| Pattern | Count |
|---|---|
| Direct grounded Q&A (1 article) | 6 |
| Multi-article synthesis (2–3 articles) | 4 |
| Principle + exception questions | 3 |
| Refusal examples (question not answerable from the code) | 3 |
| Clarification examples (ambiguous question) | 2 |
| Procedural/lifecycle questions | 2 |

**Language split per batch:**
- 10 French examples
- 10 Arabic examples (formal MSA only — dialect strictly forbidden)
- 2 cross-lingual examples (question and source article in different languages)

**Key style rules enforced:**
- All articles cited must exist verbatim in the uploaded PDF — no hallucinated article numbers
- Answers follow a **principle → exception → rationale** structure
- Every answer includes a `Sources: art. X, Y du [Code]` line
- Substantive answers include a legal disclaimer
- Questions written from realistic personas: citizens, business owners, HR managers, students
- RAG format: user message always includes the question + `Documents pertinents` section with verbatim article text

**Answer length targets:**
- Simple factual: 50–100 words
- Substantive: 150–250 words
- Refusal/clarification: 40–80 words

### complex data — Complex Scenario Batches

Each batch = **5 scenarios** generated from the same PDF-upload method but with a much harder prompt.

| Category | `category` value | Total | Description |
|---|---|---|---|
| Complex scenario | `complex_scenario` | 20 | Multi-issue legal narrative requiring 4–8 articles |

**What makes a scenario "complex":**
1. Narrative situation in first person (not a direct question)
2. Minimum 3 intertwined legal issues from the same situation
3. Requires 4–8 articles to answer properly
4. Realistic Tunisian persona with specific details (city, amount in DT, emotional context)
5. At least one sub-issue the code does NOT answer — forces a bounded refusal

**Language split per batch:** 3 French + 2 Arabic

**Answer structure enforced (6 parts):**
- (a) Acknowledge the situation (empathetic, 1–2 sentences)
- (b) Issue-by-issue analysis with article citations
- (c) Explicit limits — what the documents don't cover
- (d) Practical next steps (numbered list)
- (e) Sources line
- (f) Disclaimer

**Answer length target:** 400–700 words

### added data — Supplementary Datasets

Three files with distinct question types not covered by the synthetic batches.

#### Out-of-scope refusals — `batch_out_of_scope_001_20260501.json` (38 examples)

| Subcategory | `subcategory` value | Count | Description |
|---|---|---|---|
| Off-topic | `off_topic` | 10 | CV help, weather, recipes, sports, jokes — model declines and redirects |
| Foreign law | `foreign_law` | 8 | UAE, France, Morocco, Algeria law — model explains its Tunisia-only scope |
| Greeting | `greeting` | 6 | Simple greetings ("Bonjour", "عسلامة") — model responds warmly and invites a legal question |
| Vague / unclear | `vague_clarification` | 5 | Minimal queries ("INPP", "code") — model asks smart clarifying questions |
| Platform meta | `platform_meta` | 4 | Questions about the AI model, RAG stack, data sources — model deflects without revealing internals |
| Abuse | `abuse` | 3 | Insults or hostile messages — model stays professional and offers to continue |
| Translation | `translation` | 2 | Translation requests — model declines and offers to explain the legal concept instead |

#### Service routing — `batch_routing_001_20260430.json` (60 examples)

Each example teaches the model to redirect to one of E-Tafakna's 6 specialized services instead of answering as Q&A.

| Routing type | `routing_type` value | Count | Description |
|---|---|---|---|
| Clear routing | `clear` | 18 | User clearly needs a service → model redirects directly |
| Ambiguous routing | `ambiguous` | 18 | Could be Q&A or a service → model gives a brief answer and suggests the service |
| Wrong-service correction | `wrong_service` | 12 | User implies service A but actually needs service B → model corrects and routes |
| Informal phrasing | `informal` | 12 | Casual requests ("résume-moi ça") — model recognizes intent and routes |

Services covered: Analyse du document, Health Check, Recommendation, Intelligent Summary, Data Extraction, Document Comparator.

#### Darija (Tunisian dialect) examples — inside `all_messages.json` (77 examples)

77 examples in `all_messages.json` contain Tunisian dialect Arabic (Darija/دارجة) rather than formal MSA. These were mixed into the constructed batches and are identifiable by dialect markers (`شنوة`, `وقتاش`, `كيفاش`, `باش`, `برشا`, etc.).

They represent a distinct question type: colloquial Arabic input from everyday users, as opposed to the formal MSA required by the standard generation prompt. They broaden the model's tolerance for informal Arabic but should be reviewed — the generation prompt explicitly forbids dialect, so these may have inconsistent answer quality.

#### Real user conversations — `elyssa_conversations_final.json` (44 examples)

| Type | Count | Description |
|---|---|---|
| Single-turn | 5 | One user question → one assistant reply (legal turn survived filtering) |
| 2-turn | 14 | Follow-up or clarification after first answer |
| 3-turn | 4 | Progressive deepening of a topic |
| 4-turn | 7 | Extended back-and-forth on a legal issue |
| 5-turn | 14 | Full conversation up to the capped maximum |

These are the only multi-turn examples in the entire dataset. No `category` field — sourced from real Elyssa sessions.

---

## Complete Question Type Reference

| Category | Source | Count | `category` / `subcategory` |
|---|---|---|---|
| Direct grounded Q&A | constructed data | 348 | `direct` |
| Multi-article synthesis | constructed data | 214 | `multi_article` |
| Principle + exception | constructed data | 190 | `principle_exception` |
| Refusal (in-domain) | constructed data | 158 | `refusal` |
| Procedural / lifecycle | constructed data | 128 | `procedural` |
| Clarification | constructed data | 121 | `clarification` |
| Darija (dialect Arabic) | constructed data | 77 | *(mixed in batches)* |
| Complex scenario | complex data | 20 | `complex_scenario` |
| Off-topic refusal | added data | 10 | `off_topic` |
| Clear routing | added data | 18 | `clear` |
| Ambiguous routing | added data | 18 | `ambiguous` |
| Wrong-service correction | added data | 12 | `wrong_service` |
| Informal routing | added data | 12 | `informal` |
| Foreign law refusal | added data | 8 | `foreign_law` |
| Greeting | added data | 6 | `greeting` |
| Vague / unclear | added data | 5 | `vague_clarification` |
| Platform meta | added data | 4 | `platform_meta` |
| Abuse handling | added data | 3 | `abuse` |
| Translation refusal | added data | 2 | `translation` |
| Multi-turn conversation | added data | 44 | *(no category field)* |
| **Total** | | **~1,762** | |

---

## Data Format

All synthetic examples use the OpenAI messages format with a **RAG-aware user message**:

```json
{
  "batch_id": "batch_COC_001_20260417",
  "source": "Code des obligations et contrats de Tunisie",
  "articles_covered": [2, 3, 67, 123],
  "examples": [
    {
      "example_id": "coc_fr_001",
      "language": "fr",
      "category": "principle_exception",
      "articles_referenced": [67, 68],
      "confidence_flag": null,
      "messages": [
        {
          "role": "system",
          "content": "Vous êtes un assistant juridique spécialisé dans le droit tunisien..."
        },
        {
          "role": "user",
          "content": "Question: ...\n\nDocuments pertinents:\n[1] Source: Article 67 du COC\n<verbatim text>"
        },
        {
          "role": "assistant",
          "content": "En vertu de l'article 67 du COC... Sources: art. 67, 68 du COC. Ceci ne constitue pas un avis juridique..."
        }
      ]
    }
  ]
}
```

The `Documents pertinents` block in the user message is critical — it trains the model for how production RAG inference works (Qdrant retrieves articles → model answers from them).

---

## Anti-Hallucination Measures Built Into Generation

- Articles must be verbatim from the uploaded PDF
- If article numbers are ambiguous (OCR issues), a `confidence_flag` field is added
- The prompt explicitly states: "15 solid examples are better than 20 with hallucinated article numbers"
- OCR quality must be reported before generation begins

---

## System Prompt Variants

The base dataset has **24 different system prompt wordings** across batches (slight variations in how the assistant is described). Before training, these should be standardized to:
- 2 variants (FR + AR) for standard Q&A
- 2 variants (FR + AR) for routing

---

## How to Generate New Batches

1. Open `prompt-for-regular-data.txt` (standard) or `prompt-for-complex-data.txt` (complex)
2. Upload the target legal code PDF to the AI model along with the prompt
3. Provide the list of article numbers already covered (from previous batches of the same code) to avoid duplicates
4. Save output as `batch_<CODE>_<N>_<YYYYMMDD>.json` in `constructed data/` (standard) or `complex data/` (complex)
5. Run `script.py` to rebuild `all_messages.json`
6. Spot-check 5–10 examples for format compliance and citation accuracy

---

## Known Limitations of Synthetic Data

| Issue | Impact |
|---|---|
| **All questions are well-formed** | Real users write with typos, code-switching, and informal phrasing — synthetic data doesn't cover this |
| **Zero multi-turn examples** | Every synthetic example is single-turn (one user message → one assistant reply) |
| **No out-of-domain refusals** | Synthetic refusals are in-domain ("documents don't answer this") — not off-topic or foreign law |
| **24 system prompt variants** | Inconsistency can confuse the model — needs standardization |
| **Arabic from augmentation only** | No real Arabic user queries; all Arabic is AI-generated |

These gaps are addressed by the supplementary datasets in `added data/` — see [supplementary_training_data_documentation.md](supplementary_training_data_documentation.md).

---

## Scripts

| Script | Purpose |
|---|---|
| [script.py](script.py) | Merges all `batch_*.json` files in `constructed data/` into `all_messages.json` |
| [convert.py](convert.py) | Extracts questions from a JSON dataset into `.txt` or `.csv` for review |
