# Decision Models: Jev and Its Alternatives

A catalog of **decision models**: models that work like Jev and the OpenAI Decisions API.

**Retrieved and checked:** 2026-10-14. Jev launched on 2026-09-15, and the field changes weekly. Re-check names, prices and licenses before citing.

## Inclusion test

A model is listed only if its description meets all four criteria:

1. The caller sends a **state** plus **typed questions**: yes/no, choice, or ordered score.
2. The model returns a **probability for each option**. A single label or a free-form score doesn't count.
3. It generates **no text**: the answer is read from one forward pass, or a small number of internal passes.
4. It works on **general, caller-defined questions**, not a single fixed task.

**Verification levels:**
- **Primary:** I read the vendor's own docs, model card, or an independent evaluation directly.
- **Secondary:** the description comes from consistent news coverage, hub sites, or model listings. Treat performance and price figures as unverified.

---

## 1. Hosted decision-model APIs

| Model | Maker | Released | Yes/no · choice · score | Price (input; output free) | Open weights? | Independent eval? | Verification |
|---|---|---|---|---|---|---|---|
| **Jev** (jev-1.13) | TypeSafe AI | 2026-09-15 | noul · choice (≤255) · score | $0.042 / 1M | No | Yes (Vals, papers) | Primary ([docs](https://docs.typesafe.ai/introduction)) |
| **Decisions API** (gpt-6-luna) | OpenAI | Beta 2026-10-06 | predicate · choice · score | $0.10 / 1M | No | No (Luna was tested by Vals as a model, not through this endpoint) | Primary ([docs](https://developers.openai.com/api/docs/guides/decisions)) |
| **Decisions API** (pplx-decider-v1 / v1.1-27b) | Perplexity | 2026-10-01 | noul · choice (≤255) · score (≤10 levels); ≤128 questions per request | ~$0.04 / 1M (sources differ) | Yes (Apache-2.0) | No | Secondary |
| **Microsoft-Decision-1** | Microsoft Foundry | ~2026-10-09 | yes/no · choice · ordered scale | ~$0.04 / 1M (reported) | No | No | Secondary |
| **Mercury Decide** | Inception | 2026-09-30 | choice with a probability for every option | $0.021 / 1M | No | **Yes (Vals)** | Primary ([Vals](https://www.vals.ai/blogs/evaluation-of-mercury-decide)) |
| **d1** | Liquid AI | Late Sep 2026 | choices, judgments, scores | Free tier | Smaller open variants (below) | No | Secondary |
| **Clef / Clef-flash / Clef-omni** | Cloudflare | 2026-10-01 (omni 10-09) | typed questions; a "joint schema head" scores all options in one pass | ~$0.24 / $0.09 per 1M | Yes (Apache-2.0) | No | Secondary |
| **Solar Decide** (+ Flash) | Upstage | Beta 2026-09-22 | yes/no · choice · score, `/v1/systemone` schema; 512K context | $0.05–0.10 / 1M (sources differ) | No | No | Secondary |
| **GLiDE** | Fastino Labs | 2026-09-30 | choice: selected action, confidence, and a probability per option; adds internal reasoning passes when unsure | $0.30 / 1M | No | No | Secondary |

## 2. Open-weight decision models

### 2a. Encoder-based (small and fast, short context)

| Model | Maker | Size | License | Notes | Verification |
|---|---|---|---|---|---|
| **Laya** | Convai Innovations | 421M (English), 322M (multilingual) | Apache-2.0 | choice · score · noul heads. Publishes an RLCD-style recipe. Ships overconfident (temperature refit cuts ECE from 0.466 to 0.081). Hanzo's `kai-1-agent` is a Laya-family fine-tune. | Primary ([model card](https://huggingface.co/convaiinnovations/laya)) |
| **Von** | wfzyx | 395M | Apache-2.0 | Scores options independently; serves `/v1/systemone`. | Secondary |
| **GLiNER2.5-Decide** | Fastino Labs | 340M (also 1B, 287M multilingual) | Apache-2.0 | Takes label sets at call time. | Secondary |
| **open-jev-deberta-v3-large** | kotoba-lang | 434M | Apache-2.0 | Encoder reproduction of the Jev interface. | Secondary |
| **Anarkali** | ToufiqQureshi | 68M | Apache-2.0 | Smallest listed model. | Secondary |

### 2b. Decoder-based (fine-tuned LLM with a decision head or option readout)

| Model | Maker | Sizes | License | Notes | Verification |
|---|---|---|---|---|---|
| **pplx-decider** | Perplexity | 27B | Apache-2.0 | Same model as the hosted API. | Secondary |
| **Clef family** | Cloudflare | 27B, 9B, 30B-A3B | Apache-2.0 | Same models as the hosted API. | Secondary |
| **d1-3B, d1-omni-600M** | Liquid AI | 3.1B, 587M | LFM Open License (limits for large firms) | Released 2026-10-07. Single forward pass. | Secondary |
| **Strands Decider 2B** | AWS Strands Labs | ~2B | Apache-2.0 | Pointer head (~1M parameters). **Full training data and scripts released.** | Secondary |
| **H2O-Lightning-4B** | H2O.ai | 4.5B | Apache-2.0 | choice · yes/no · ordinal; images supported; one forward pass on vLLM. | Secondary |
| **Torchcast Decision 27B** | Torchcast AI | 27B | CC BY-NC 4.0 | choice · yes/no · ordinal. Fine-tune of StartLux-Decision-27B. | Secondary |
| **Xor-26B-A4B** | Juspay | 26B-A4B (Gemma-4) | — | noul · choice · score with full distributions. | Secondary |
| **Kev** | Jared Palmer | 0.8B, 4B, 9B, 27B | Apache-2.0 | Follows the TypeSafe contract; 2–255 options. | Secondary |
| **Tev1** | Together AI | 0.8B, 4B | MIT code; weights license pending | Option-letter readout, 2–24 options. Logprobs are not calibrated by default. | Secondary |
| **Nimble** | Bespoke Labs | 9B | Recipe open | Own API; served by Ollama's `/v1/systemone`. | Secondary |
| **Decider** | Mapika | 2B, 4B, 35B MoE (+ vision) | Apache-2.0 | A distribution over options per question in one pass; 2–255 options. | Secondary ([card](https://huggingface.co/Mapika/decider-2b)) |
| **OpenDecider** | Manjunath Shiva | ~400M, 4B, 30B MoE | Apache-2.0 | Distilled from two open teachers. | Secondary |
| **Jeeves** | PostHog | 9B | MIT code, Apache-2.0 weights | Reasons before deciding. | Secondary |
| **OpenJev-4B** | Junhao Shen | 4B | MIT | Option-set decision head; SFT, then REINFORCE. | Secondary |
| **Open-Jev** | Zefan Cai | 2B, 9B, 27B | Apache-2.0 | LoRA with a scalar decision head. | Secondary |
| **NanoJev** | TianyuCodings | 0.6B | MIT | Compact replica with a training pipeline. | Secondary |
| **Mica** | sky7350 | 4B | Apache-2.0 | `/v1/systemone`. Choice 2–255; score 2–10 levels. | Secondary |
| **MoJev** | MoLeMo-Lab | 0.85B | MIT | Text and image inputs; TypeSafe SDK-compatible. | Secondary |
| **Rizzo Flow** | Rizzo AI Academy | 1.7B, 4B | Apache-2.0 | Answer-letter probabilities, ≤26 options. Uncalibrated by default; runs on llama.cpp. | Secondary |
| **JevK5** | alibiserikbay | 4B | Apache-2.0 | Calibrated letter readout. | Secondary |
| **Jev-Style** | chaoliangUNSW | 0.8B, 2B | Apache-2.0 | GGUF; option probabilities from one token. | Secondary |
| **Jev-Omni** | akhilaaa3 | 12B (Gemma 4) | Apache-2.0 | Text, image, audio and video. | Secondary |
| **OpenThai-SystemOne** | iApp Technology | 0.8B | Apache-2.0 | Thai-focused. | Secondary |

### 2c. Training-free methods (turn an existing LLM into a decision model)

| Project | Maker | Notes |
|---|---|---|
| **AnyJev** | Nokia Applied Research | Library that reads option probabilities from existing LLMs (Apache-2.0). |
| **SemIf** (formerly OpenJev) | TheoLeeCJ | Reads option probabilities from a frozen LLM (MIT). |
| **djev** | mmastrac | Reads decisions from a diffusion LLM. |

These are methods rather than trained models. They inherit the label-wording and prompt-order biases of LLM token probabilities (Zhao et al. 2021, *Calibrate Before Use*).

---

## 3. Checked and excluded

| Name | Why it's not listed |
|---|---|
| Span-01 (Respan) | Specialized: scores whether behaviors appear in agent traces. Not general typed questions. |
| CLM-8B (Contrastive-LM) | Ranks candidate actions using embeddings. It has a Jev-like API, but its scores aren't calibrated option probabilities. |
| CyberJev, AgentJev | Task-specific classifiers (security; coding-task completion). |
| Kai 1 (Hanzo) | A Laya-family fine-tune; listed under Laya. |
| Celeris-1 Decision, meraGPT Decider 1, Surogate Rune, Quyet-1.0, Drex 1.5 | No source found that describes how they work. |

---

## 4. Shared interface and local serving

- **`/v1/systemone`** is a de facto shared schema. It's implemented by Upstage, Kev, Laya (`laya-serve`), Von and Mica.
- **Ollama 0.35** (2026-09-28) serves Tev1 and Nimble locally through `/v1/systemone`, with 2–26 options ([guide](https://sotaaz.com/post/ollama-decision-models-en)).
- A shared schema doesn't mean shared semantics:
  - Ollama's `confidence` is not the top probability.
  - OpenAI's `score` is a probability-weighted average.
  - Some readouts are uncalibrated by default.

## 5. Benchmarks that compare decision models

| Benchmark | Who runs it | What it shows | Caveat |
|---|---|---|---|
| [Vals: Mercury Decide](https://www.vals.ai/blogs/evaluation-of-mercury-decide) (2026-10-08) | Independent | **The only independent head-to-head between two decision models.** See below. | Mercury is unpinned; 33 items per LegalBench subtask |
| [Vals: Jev](https://www.vals.ai/blogs/independent-evaluation-of-jev) (2026-10-06) | Independent | Jev 0.975 on claim verification; last on LegalBench (0.730) | Two tasks; see `jev-benchmarks.md` |
| Jev Decision Index (Hugging Face) | Community leaderboard | 132,422 requests, 37 benchmarks, 19 scored; abstentions score zero | Most entries self-scored by vendors |
| JevBench | Community | H2O claims 72.5 vs Jev 71.5; AWS reports Strands 72.3% of 231 tasks | Vendor-reported |
| Vendor panels (Perplexity, Liquid, Fastino, Cloudflare, Torchcast) | Vendors | Each claims a lead over Jev of about 1–7 points | Self-run, unpinned |

**Vals: Mercury Decide vs Jev 1.13.0** (same items, prompts and scoring):

| | Mercury Decide | Jev |
|---|---|---|
| Claim verification accuracy | 0.978 | 0.975 |
| LegalBench class-balanced accuracy | 0.821 | 0.730 |
| ECE, claims | 0.011 | 0.011 |
| ECE, LegalBench | 0.058 | 0.108 |
| Cost per 1k claims | $0.006 | $0.025 |
| Median latency, 1 judgment | 0.16 s | ~0.10 s |
| Median latency, 64 judgments | 0.40 s | ~0.10 s |
| 1% error-budget run | 94% automated, 0.8% error (within budget) | 95% automated, 1.6% error (over budget) |
