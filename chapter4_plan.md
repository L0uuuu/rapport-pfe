# Chapter IV: Demonstration and Evaluation — Plan

## Key Facts from Training (Notebooks)

### Gemma 4 E4B — OVHcloud AI Notebooks
| Metric | Value |
|---|---|
| Platform | OVHcloud AI Notebooks |
| GPU | 1× NVIDIA Tesla V100S, 32 GiB VRAM |
| Framework | PyTorch 2.11.0, CUDA 12.8, Python 3.13 |
| Method | LoRA (fp16, no quantization) |
| Training time | 3,357 seconds (~56 minutes) |
| Total steps | 609 (3 epochs × 1,619 examples ÷ effective batch 8) |
| Final loss | 0.0586 |
| Peak VRAM | 30.8 GiB / 32 GiB |
| Trainable parameters | 40,583,168 / 7,981,684,000 (0.51%) |
| Adapter size | 185.6 MB (adapter_model.safetensors: 154.9 MB) |
| LoRA adapter (HF) | `L0uu/gemma4-e4b-etafakna-lora` |
| GGUF quantization | q4_k_m (to convert locally — GGUF export failed on OVHcloud) |

### Qwen3.5 9B — OVHcloud AI Notebooks
| Metric | Value |
|---|---|
| Platform | OVHcloud AI Notebooks |
| GPU | 1× NVIDIA Tesla V100S, 32 GiB VRAM |
| Framework | PyTorch 2.10.0, CUDA 12.8 |
| Method | QLoRA (4-bit) |
| Training time | 15,223 seconds (~253 minutes / ~4.2 hours) |
| Total steps | 609 (3 epochs × 1,619 examples ÷ effective batch 8) |
| Final loss | 0.8208 |
| Peak VRAM | 11.2 GiB |
| Trainable parameters | 29,097,984 / 9,438,911,728 (0.31%) |
| Adapter size | 130.1 MB (adapter_model.safetensors: 111.0 MB) |
| LoRA adapter (HF) | `L0uu/qwen35-9b-etafakna-lora` |
| GGUF quantization | q4_k_m |

### Shared Training Config (both models)
- Dataset: 1,619 cleaned examples (1 broken entry removed from 1,620)
- Per-device batch size: 1 | Gradient accumulation: 8 | Effective batch: 8
- Epochs: 3 | Learning rate: 2e-4 (cosine scheduler, warmup ratio 0.05)
- Optimizer: AdamW 8-bit | Max sequence length: 2,048 | Packing: disabled
- train_on_responses_only applied — loss computed only on assistant turns

### Test Inference (same question for both)
**Question:** "Quelles sont les conditions pour qu'un contrat soit valable en droit tunisien?"
**Documents pertinents:** Article 2 du COC

**Gemma 4 E4B response (from notebook):**
> "En vertu de l'article 2 du Code des obligations et des contrats, quatre conditions sont nécessaires à la validité d'un contrat né d'une déclaration de volonté : la capacité des parties à s'obliger, une déclaration de volonté valable portant sur les éléments essentiels du contrat, un objet certain pouvant former objet d'obligation, et une cause licite. [...] Sources: art. 2 du COC. Ceci ne constitue pas un avis juridique."

**Qwen3.5 9B response (from notebook):**
> "En vertu de l'article 2 du Code des obligations et des contrats, la validité d'une obligation contractuelle repose sur quatre conditions cumulatives : la capacité de s'obliger, une déclaration de volonté valable portant sur les éléments essentiels, un objet certain, et une cause licite. [...] Sources: art. 2 du COC. Ceci ne constitue pas un avis juridique."

---

## ⚠️ Remaining TODOs Before Writing

| Item | Status |
|---|---|
| Qwen final training loss | Not captured during OVH run — fill in if you have it |
| Qwen trainable params now confirmed | 29,097,984 / 9,438,911,728 (0.31%) — update Ch. 3 table |
| Loss curves for both models | Need screenshots from OVH notebook outputs |

---

## 1. Introduction

Brief paragraph situating this chapter within the DSR lifecycle: the artifact built in Chapter III is now demonstrated in operation and evaluated against the three objectives (O1, O2, O3) defined in Section 2 of Chapter III.

---

## 2. Part I: Demonstration

### 2.1 System Overview at Demo Time

Short paragraph describing the deployed stack:
- Fine-tuned model served locally via Ollama (GGUF)
- Qdrant running on-premises with the full JORT corpus indexed
- FastAPI service layer + n8n orchestrating the query flow
- Chat interface accessible 

### 2.2 Example Queries and System Responses

Use the test query already captured in both notebooks as a baseline example:
- "Quelles sont les conditions pour qu'un contrat soit valable en droit tunisien?" (COC, Art. 2)
- Both model responses are available verbatim from notebook outputs above

Add 2–3 more representative examples covering different categories:

| # | Language | Category | What it demonstrates |
|---|---|---|---|
| 1 | French | Direct QA | COC Art. 2 — contract validity (already in notebook) |
| 2 | Arabic | Multi-article synthesis | Answer drawing on 2–3 articles |
| 3 | French | In-domain refusal | Model correctly declines and recommends a lawyer |
| 4 | French | Confidence gate / out-of-scope | Gate fires, bilingual fallback returned |

**Assets needed:** Screenshots of the chat interface OR additional Q&A outputs.

### 2.3 Pipeline Execution Demonstration

Brief walkthrough of n8n workflow executing a query:
- Embedding → Qdrant search → Reranking → Model generation
- Execution time from query to first token (if available)

**Assets needed:** Interface screenshot or timing data.

---

## 3. Part II: Evaluation

### 3.1 Training Results

#### 3.1.1 Gemma 4 E4B — Training Run

All numbers confirmed from notebook output:
- Training time: 3,357 s (~56 min)
- Final loss: 0.0586
- Peak VRAM: 30.8 GiB / 32 GiB
- Steps: 609 | Epochs: 3

Note on the loss value: Gemma 4 E4B would normally show loss of 13–15 when trained on full conversations. The low value (0.0586) is expected because `train_on_responses_only` masks system/user tokens, so the model only predicts assistant completions, which are shorter and more predictable in format.

**Assets needed:** Loss curve screenshot (logging_steps=10, so 60+ data points available from the training HTML output in the notebook).

#### 3.1.2 Qwen3.5 9B — Training Run

All numbers confirmed from notebook output:
- Platform: OVHcloud AI Notebooks, 1× NVIDIA Tesla V100S
- Training time: 15,223 s (~253 min / ~4.2 hours)
- Final loss: 0.8208
- Peak VRAM: 11.2 GiB

Note on the higher loss: Qwen3.5 9B loss (0.8208) is higher than Gemma's (0.0586), and training took ~4.5× longer. This reflects both the QLoRA 4-bit quantization constraint and the Mamba/MoE hybrid architecture of Qwen3.5, which is harder to adapt with LoRA on a narrow legal domain dataset.

**Assets needed:** Loss curve screenshot from Kaggle notebook.

#### 3.1.3 Side-by-Side Training Comparison

| Metric | Gemma 4 E4B | Qwen3.5 9B |
|---|---|---|
| Platform | OVHcloud V100S | OVHcloud V100S |
| Method | LoRA (fp16) | QLoRA (4-bit) |
| Training time | ~56 min | ~253 min |
| Final loss | 0.0586 | 0.8208 |
| Peak VRAM | 30.8 GiB | 11.2 GiB |
| Trainable params | 40.6 M (0.51%) | 29.1 M (0.31%) |
| Adapter size | 185.6 MB | 130.1 MB |
| GGUF export | q4_k_m | q4_k_m |

---

### 3.2 Model Quality Evaluation (O1)

Compare fine-tuned model vs base model (instruction-tuned, no fine-tuning).

#### 3.2.1 Evaluation Protocol

- Test set: held-out examples not seen during training
- Baseline: base model (gemma-4-E4B-it / Qwen3.5-9B-Instruct) with same RAG prompt format
- Fine-tuned model: adapter merged
- Evaluation dimensions:
  - Citation accuracy (correct article numbers cited)
  - Legal correctness (answer matches the article content)
  - Format compliance (Sources line, disclaimer, language match)
  - Refusal quality (correctly declines unanswerable questions)

#### 3.2.2 Results

**Assets needed:** Run evaluation or provide qualitative comparison from testing.

---

### 3.3 Retrieval Evaluation (O2)

Evaluate the RAG retrieval layer quality.

#### 3.3.1 Protocol

- Query set: held-out questions with known ground-truth articles
- Metrics: Precision@k, Recall@k
- top-k optimization (mentioned in Ch. 3 as "to be optimized in Ch. IV")

#### 3.3.2 Results

**Assets needed:** Retrieval evaluation script output.

---

### 3.4 On-Premises Compliance (O3)

| Component | Runs locally | External calls at inference |
|---|---|---|
| bge-m3 (embedding) | Yes | None |
| Qdrant (vector search) | Yes | None |
| bge-reranker-v2-m3 | Yes | None |
| Fine-tuned model (llama.cpp) | Yes | None |
| FastAPI service | Yes | None |

Confirm inference latency and memory footprint at runtime.

**Assets needed:** Latency measurement (time query → first token / full response).

---

### 3.5 Objectives Summary

| ID | Objective | Criterion | Result | Status |
|---|---|---|---|---|
| O1 | Domain Adaptation | Q&A accuracy vs baseline | [TODO] | [TODO] |
| O2 | Dynamic Retrieval | Retrieval precision on held-out queries | [TODO] | [TODO] |
| O3 | On-Premises Deployment | Zero external calls at inference | Confirmed | Met |

---

## 4. Conclusion

Summary: what the demonstration showed, training observations (Gemma converged faster with lower loss, Qwen took ~4.5× longer), which model is recommended for deployment and why, and confirmation that all three objectives are addressed.

---

## Assets Checklist

| Asset | Status |
|---|---|
| Training loss curve — Gemma 4 E4B | Exists in notebook HTML output — need screenshot |
| Training loss curve — Qwen3.5 9B | Exists in Kaggle notebook — need screenshot |
| Chat interface screenshots | TODO |
| Additional Q&A examples (categories 2, 3, 4) | TODO |
| Retrieval evaluation results | TODO |
| Model comparison results (base vs fine-tuned) | TODO |
| Inference latency measurement | TODO |
| Fix Ch. 3 discrepancies (Qwen platform, GGUF method) | TODO |
