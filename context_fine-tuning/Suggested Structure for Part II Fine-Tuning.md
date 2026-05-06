# Suggested Structure for Part II: Fine-Tuning

---

## 2.6 Base Model Selection

### 2.6.1 Motivation for Using a Small Language Model

The project's on-premises deployment constraint (O3) immediately excludes any model accessible only through an external API, such as GPT-4.1 or Gemini. The inference runtime must run entirely on ATI Tunisie's local infrastructure, so the chosen model must fit within the available GPU VRAM budget, produce answers at interactive latency, and carry a license permitting commercial on-premises deployment.

These constraints point toward open-weight SLMs in the 4B to 14B parameter range, which can be quantized and served locally with acceptable quality.

### 2.6.2 Selection Criteria

Four criteria guided the evaluation:

| Criterion | Requirement |
|---|---|
| Multilingual capability | Strong Arabic and French support, both at understanding and generation |
| Instruction-following | Capable of following a structured prompt with a system role and retrieved context |
| License | Permissive open-weight license allowing on-premises commercial use |
| GGUF compatibility | Exportable to GGUF format for serving via the local inference runtime |

### 2.6.3 Candidate Models

Two open-weight models were selected for fine-tuning and comparison:

**Qwen3.5 9B**
- Developer: Alibaba Cloud (Qwen team)
- Parameters: 9 billion
- Architecture: hybrid — Gated Delta Networks (linear attention) + sparse Mixture-of-Experts feed-forward layer; higher throughput and lower latency than dense models of the same size
- Multilingual support: 201 languages pretrained, strong Arabic and French coverage
- Context window: 262,144 tokens natively
- Instruction-following: instruction-tuned variant is Qwen3.5-9B-Instruct
- License: Apache 2.0 (permissive, commercial use allowed)
- GGUF: available via unsloth, lmstudio-community, bartowski on HuggingFace

**Gemma 4 E4B**
- Developer: Google DeepMind
- Parameters: "Effective 4B" — uses Per-Layer Embeddings (PLE): only active parameters loaded into VRAM, embedding table accessed from cheaper memory; memory footprint of a 4B model with larger representational capacity
- Architecture: hybrid attention (local sliding-window 512 tokens + full global attention), 150M-parameter vision encoder
- Multilingual support: pretrained on 140+ languages, 35+ strong out-of-the-box including Arabic and French
- Context window: 128K tokens
- Instruction-following: instruction-tuned variant is gemma-4-E4B-it (HuggingFace: google/gemma-4-E4B-it)
- License: Apache 2.0 (permissive, commercial use allowed)
- GGUF: available via unsloth/gemma-4-E4B-it-GGUF on HuggingFace; Ollama: gemma4:e4b

### 2.6.4 Rationale for This Pair

Qwen3.5 9B and Gemma 4 e4B represent two distinct operating points on the size-quality tradeoff. Qwen3.5 9B offers stronger multilingual depth and larger capacity at the cost of higher VRAM consumption and slower inference. Gemma 4e 4B is lighter and faster, making it more suitable for deployment on constrained hardware. Fine-tuning both on the same dataset and evaluating them under identical conditions allows a direct comparison: whether the quality gain from the larger model justifies its inference cost in the on-premises context.

---

## 2.7 Training Data Synthesis

The structured JSON articles produced by Phase 4 of the RAG pipeline are the raw material for the fine-tuning dataset. Since no annotated Tunisian legal Q&A dataset exists publicly, the dataset is synthesized.

Describe:
- **Instruction-tuning format:** each example is a (system, user, assistant) triple
  - System: role definition, instruction to answer only from Tunisian law
  - User: a legal question in Arabic or French
  - Assistant: a grounded answer citing the relevant article number and law name
- **How pairs are generated:** seed questions written by a legal professional + GPT-4.1 expansion using the source legal codes as context
- **Language balance:** Arabic / French / mixed examples
- **Train / validation split:** e.g., 90% / 10%
- **Dataset statistics:** number of source laws covered, number of seed questions, total synthesized examples

---

## 2.8 Fine-Tuning Methodology

Explain why full fine-tuning is excluded: parameter count vs. available VRAM makes it infeasible.

Introduce QLoRA as the chosen approach:
- **Base quantization:** 4-bit NF4 (bitsandbytes) reduces the memory footprint of the frozen base weights
- **LoRA adapters:** low-rank weight matrices added to attention projection layers (q_proj, v_proj) and trained in bf16
- **PEFT framework:** Hugging Face PEFT library manages adapter injection and merging
- Key LoRA hyperparameters to document: rank r, alpha, dropout, target modules
- Approximate trainable parameters: ~1% of total model parameters

---

## 2.9 Training Configuration

Document the hardware and hyperparameters used for each training run:

| Hyperparameter | Value |
|---|---|
| Quantization | 4-bit NF4 (bitsandbytes) |
| LoRA rank (r) | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Learning rate | 2e-4 |
| Warmup ratio | 0.03 |
| Batch size | 4 + gradient accumulation x4 (effective 16) |
| Epochs | 3 |
| Max sequence length | 2048 tokens |
| Optimizer | paged_adamw_8bit |

Training platform: OVH AI Notebooks (confirm GPU specs from dashboard).
Framework: Hugging Face Transformers + PEFT + TRL (SFTTrainer).

---

## 2.10 Quantization and Deployment

After training:
- Merge the LoRA adapter back into the base model weights
- Export to GGUF format for compatibility with the local inference runtime
- Quantization level for inference: Q4_K_M (balance between model size and output quality)
- Justify the quantization level: Q4_K_M retains most of the fp16 quality while cutting memory usage by ~4x, making it deployable on the available hardware

---

## 2.11 Integration with the RAG System

The fine-tuned model slots into the query flow described in Part I (section 2.5.3) without modifying the retrieval layer.

Describe the prompt template structure:
1. **System prompt:** role definition + instruction to answer only from the provided legal articles
2. **Retrieved context block:** top-k reranked articles from Qdrant, each carrying law name, article number, source date, and content in the query language (Arabic or French)
3. **User query:** the original question as submitted
4. **Expected answer format:** grounded in the provided articles, with explicit citations (e.g., "Selon l'article 2 du Code des Obligations et des Contrats...")

If the confidence gate fires (best reranker score < 0.4), the model is not called and a bilingual fallback message is returned instead, preventing unsupported answers.
