
# Fine-Tuning Qwen3.5 9B on OVHcloud — Full Summary

## Project Overview

**Goal:** Fine-tune Qwen3.5 9B to create a Tunisian legal assistant for the E-Tafakna platform.

**Model:** `unsloth/Qwen3.5-9B` — 9 billion parameters.

**Method:** QLoRA (4-bit NF4 quantization) — fp16 loading of the 9B base exceeded the 32 GiB V100S ceiling, so the base weights were loaded in 4-bit NF4 and the LoRA adapters trained in fp16.

**Dataset:** 1,619 cleaned examples of Tunisian law Q&A in French, in chat format (system / user / assistant). 49 multi-turn conversations, 1,571 single-turn.

**Result:** LoRA adapter successfully trained and pushed to Hugging Face at `L0uu/qwen3.5-9b-etafakna-lora`.

---

## OVHcloud Setup

### Platform: AI Notebooks

- **GPU:** Ai1-Le-1-Gpu — NVIDIA Tesla V100S, 32 GiB VRAM
- **Cost:** TND 3.08/hour (ex. VAT)
- **Framework:** PyTorch 2.10.0 with Python 3.12 and CUDA 12.8
- **Editor:** JupyterLab
- **Region:** Gravelines (France)

### OVHcloud Startup Program

- 10,000€ credit voucher for 12 months
- Only V100S GPUs are covered by the voucher (H100, A100 are excluded)
- Check voucher: OVHcloud Manager → Payment methods → My Vouchers
- Billing is per-minute, only while notebook is in RUNNING state
- **Always stop the notebook when done** — closing the tab does NOT stop billing

### Known Issues / Notes

- V100S does **not** support bf16 — fp16 used for adapter weights
- fp16 loading of the 9B base model exceeds the 32 GiB VRAM ceiling — QLoRA (4-bit NF4) required
- Qwen3.5 uses custom Mamba Triton kernels — initial compilation is slow on V100S
- GGUF export filled workspace disk; intermediate files had to be deleted manually before re-attempting
- **JupyterLab login:** Requires an AI user created under Project Management → Users & Roles (not your OVHcloud Manager credentials)

---

## Model Details

### Qwen3.5 9B Architecture

- 9 billion parameters
- Gated Delta Networks + sparse MoE architecture
- 201 languages supported
- Context window: 32K tokens
- Apache 2.0 license

### VRAM Usage (QLoRA 4-bit)

| Stage | VRAM Used |
|-------|-----------|
| Model loaded (4-bit NF4) | ~8 GiB |
| With LoRA adapters (fp16) | ~9–10 GiB |
| Peak during training | 11.2 GiB |

---

## Training Configuration

### LoRA / QLoRA Parameters

- **Quantization:** 4-bit NF4 (base weights); adapters in fp16
- **Rank (r):** 16
- **Alpha:** 32
- **Dropout:** 0 (Unsloth optimized)
- **Target modules:** q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- **Trainable parameters:** 29,097,984 / 9,438,911,728 (0.31%)
- **Gradient checkpointing:** Unsloth mode

### Training Hyperparameters

- **Batch size:** 1
- **Gradient accumulation steps:** 8 (effective batch size = 8)
- **Epochs:** 3
- **Learning rate:** 2e-4 with cosine scheduler
- **Warmup ratio:** 0.05
- **Optimizer:** AdamW 8-bit
- **Max sequence length:** 2048
- **Packing:** disabled

### Dataset Preparation

- `train_on_responses_only` applied — only assistant responses are trained on, system/user prompts are masked

---

## Training Results

- **Training time:** 15,223 seconds (~253 minutes / ~4.2 hours)
- **Final loss:** 0.8208
- **GPU peak memory:** 11.2 GiB / 32 GiB
- **Steps:** 609 (3 epochs × 1,619 examples ÷ effective batch 8)
- **Loss note:** Higher than Gemma 4 E4B (0.0586) due to QLoRA 4-bit quantization and the Gated Delta Network / sparse MoE architecture, which is harder to adapt with LoRA on a narrow domain dataset. Training took ~4.5× longer than Gemma despite fewer trainable parameters.

---

## Outputs & Deployment

### What Was Saved

| Output | Location | Size |
|--------|----------|------|
| LoRA adapter | Hugging Face: `L0uu/qwen3.5-9b-etafakna-lora` | 130.1 MB (adapter_model.safetensors: 111.0 MB) |
| GGUF (q4_k_m) | Hugging Face: `L0uu/qwen3.5-9b-etafakna-gguf` | — |
| Merged 16-bit model | `/workspace/qwen35-9b-etafakna-gguf` (OVHcloud) | ~18 GB |

### GGUF Export

GGUF conversion ran directly on OVHcloud. llama.cpp was already present in the system, so the full pipeline (merge → F16 → q4_k_m) completed successfully. Intermediate files were deleted to free workspace disk before the final push to Hugging Face.

---

## Cost Summary

| Item | Duration | Cost (est.) |
|------|----------|-------------|
| Training run (Ai1-Le-1-Gpu) | ~253 min | ~TND 13.0 |
| Failed attempts / setup | ~20 min | ~TND 1.0 |
| **Total estimated** | **~273 min** | **~TND 14.0** |
