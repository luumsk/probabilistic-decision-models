# Jev Benchmarks: Curated Reference

Benchmarks and evaluations of TypeSafe's **Jev** (System One decision model), grouped by source type.

**Retrieved and checked:** 2026-10-13. Jev launched in September 2026, so treat all of this as early evidence. Numbers are taken from each source as reported; none were reproduced here. Re-check before citing.

## How to read this list

Before trusting a number, ask four questions:

1. **What were the labels?** Ground truth (human or rule-based) vs. agreement with a reference model.
2. **How many cases were there?** With n < 500, differences of a few points are usually noise.
3. **Who were the comparators, and in what settings?** Reasoning mode, prompt format, and whether they had training data.
4. **Who ran it?** Vendor, independent organization, academic preprint, or a community repo.

## Overview

| # | Source | Type | Date | Labels | Scale | Main finding |
|---|---|---|---|---|---|---|
| 1 | Vals AI | Independent org | 2026-10-06 | Ground truth | 400 + 396 items, 12 systems | Matches frontier models on claim verification; last on LegalBench |
| 2 | Deußer et al. (arXiv 2609.37647) | Preprint | 2026-09-29 | Ground truth | 37 datasets, 346k requests | Beats Qwen3.8-27B on 27/37 datasets; choice probabilities well calibrated |
| 3 | Rafe & Das (arXiv 2609.24052) | Preprint | 2026-09-21 | Human labels | 195,857 narratives coded | F1 0.908; recalibration cuts calibration error 3.3× |
| 4 | Huang et al. (arXiv 2609.27607) | Preprint | 2026-09-23 | Expert error counts | RadEvalX, RadEvalExpert | Kendall 0.573 / 0.398; AUROC 0.977 for false negation |
| 5 | dhruvmehra/jevbench | Community repo | 2026-09-22 | Ground truth | 3 datasets × 500 | Competitive zero-shot; fine-tuned DistilBERT still wins on AG News and Banking77 |
| 6 | 4esv/jev-eval | Community repo | 2026 | Ground truth | 5 tasks × 300 | Strong on CLINC (151 options); latency flat as options grow |
| 7 | stern9/jev-bench | Community repo | 2026-09-24 | Hand labels | 72 decisions | 94.4% vs Opus 5 at 98.6%, about 14× faster |
| 8 | TypeSafe workflow evals | Vendor | 2026 | **Reference models** | 4 workflows | 67.8% at $0.0004 and 0.4 s per case |
| 9 | TypeSafe launch post | Vendor | 2026-10-12 | **Reference models** | — | Claims 193.6× faster and 444.6× cheaper |

---

## 1. Independent evaluations

### 1.1 Vals AI: *An Independent Evaluation of TypeSafe's Jev*
- **Link:** https://www.vals.ai/blogs/independent-evaluation-of-jev
- **Author and date:** Connor Frank, 2026-10-06
- **Setup:** 12 systems, Jev 1.13.0. Preregistered. Native structured output for every system, no retries. Bootstrap confidence intervals with Bonferroni correction.

**Claim verification** (400 items from 10-K filings; labels set by construction rule and audited by humans):
- Jev accuracy is **0.975**, tied with GPT-6 Astra, GPT-6.1 Sol and GPT-6 Luna. The top system is Claude Sonnet 5.5 at 0.995.
- Jev's ECE is **0.011**, the best of the 12 systems.
- Cost: $0.02 per 1,000 cases, about 1/498 of GPT-6 Astra.

**LegalBench** (12 subtasks × 33 = 396 items):
- Jev is **last**, with class-balanced accuracy 0.730. The leader is GPT-5.6 Terra at 0.932.
- Jev's ECE is **0.108**, the worst of the 12.
- Failure mode: it answered "Yes" to all 33 items of `contract_nli_permissible_copy`.

**Selective prediction** (1% error budget, held-out set of 265 items):
- Jev reached 95% coverage with a realized error of 1.6%, so it exceeded the budget.

**Latency:**
- About 0.10 s median.
- At 32 judgments, Jev is 194× faster than GPT-6 Astra.

**Takeaway:** calibration doesn't transfer between tasks. Jev was the best-calibrated system on one benchmark and the worst-calibrated on the other.

**Caveats:**
- Some claim-verification items were written with an LLM.
- The LegalBench slice is small and may overlap with training data.
- Latency was measured from a single residential machine.

### 1.2 Vals AI: *Evaluation of Mercury Decide* (Jev as comparator)
- **Link:** https://www.vals.ai/blogs/evaluation-of-mercury-decide
- **Author and date:** Connor Frank, 2026-10-08
- **Why it matters:** this is the only independent head-to-head between two decision models so far. It uses the same items, prompts and scoring as 1.1.

| | Mercury Decide | Jev 1.13.0 |
|---|---|---|
| Claim verification accuracy | 0.978 | 0.975 |
| LegalBench class-balanced accuracy | 0.821 | 0.730 |
| ECE, LegalBench | 0.058 | 0.108 |
| Cost per 1k claims | $0.006 | $0.025 |
| Median latency, 64 judgments | 0.40 s | ~0.10 s |
| 1% error-budget run | 94% automated, 0.8% error | 95% automated, 1.6% error (over budget) |

- **Takeaway:** neither model dominates. Mercury is more accurate on legal entailment and cheaper per claim. Jev is faster and scales better with many questions about one long document.
- **Caveats:** Mercury Decide is unpinned. LegalBench subtasks have only 33 items each.

---

## 2. Academic preprints (not peer-reviewed)

### 2.1 *Evaluating and Benchmarking the System One Model Jev*
- **Link:** https://arxiv.org/abs/2609.37647
- **Authors and date:** Tobias Deußer, Lorenz Sparrenberg, Rafet Sifa. Submitted 2026-09-29.
- **Setup:** 37 datasets covering classification, routing, NLI, reading comprehension, commonsense, moderation, legal clauses and rubric scoring. 346,009 requests, zero-shot, one fixed template per dataset, full evaluation splits. Comparators are Qwen3.8-27B and Gemma-4-E4B.

**Results:**
- Accuracy of 95–99% on IMDB, SST-2, HellaSwag and ARC, and 86.7% on Belebele across 122 languages.
- Beats Qwen on 27 of 37 datasets. None of Qwen's 9 leads is significant.
- Beats Gemma on all 37 datasets.
- Choice probabilities are well calibrated and support selective prediction.
- Binary probabilities **rank well but sit poorly against a fixed 0.5 threshold**. On UNFAIR-ToS, tuning the threshold raised micro-F1 from 0.50 to 0.75.
- Rotating the answer options doesn't change accuracy. Withholding the question drops accuracy to near chance.

**Limitations:**
- Closed model.
- Only one template per dataset.
- Memorized question–answer pairs are not ruled out.
- Only two open-model comparators.

### 2.2 *Calibrated Decisions at Scale: Converting Police Crash Narratives into Probabilistic Crash Variables with a System One Model (Jev)*
- **Link:** https://arxiv.org/abs/2609.24052
- **Authors and date:** Amir Rafe, Subasish Das. Submitted 2026-09-21.
- **Setup:** 499,500 Texas crash narratives screened. 195,857 coded with a 27-question gated schema. 2,416 blinded human judgments.

**Results:**
- F1 of **0.908** against human labels.
- Recalibration reduced calibration error by **3.3×**.
- One frontier LLM scored 0.059 higher; the other was indistinguishable from Jev.
- Authors' conclusion: *"calibration varies by model rather than by paradigm"*, so each model has to be audited.

**Limitations:** Texas data only. Probabilities come on a discrete grid, which limits resolution.

### 2.3 *Can Jev Judge Radiology Reports? Evaluating a System One Model for Clinical Factuality*
- **Link:** https://arxiv.org/abs/2609.27607
- **Authors and date:** Jiaju Huang et al. Submitted 2026-09-23.
- **Setup:** Jev judges whether statements in a generated radiology report agree with a reference report, checking in both directions. Datasets are RadEvalX, RadEvalExpert, and a controlled-error test.

**Results:**
- Kendall τ of **0.573** (RadEvalX) and **0.398** (RadEvalExpert) against expert error counts.
- AUROC of **0.977** for detecting false negations.
- Costs under $0.03 per 100 report pairs.
- Beats an open NLI judge under a matched setup.
- RadMatch, a local method, does better on clinically significant errors.

**Note:** a search snippet credited this paper with Brier and recalibration numbers (raw Brier 0.1269). I couldn't verify them from the abstract, so check the PDF before citing them.

### 2.4 *Calibrated Decision Models for Autonomous Penetration-Testing Harnesses* (position paper, low evidential weight)
- **Link:** https://arxiv.org/abs/2609.28940
- **Author and date:** Joas Antonio dos Santos Barbosa. Submitted 2026-09-24.
- **Content:** An exploratory case study with one run per configuration. It reports no statistically significant results. It's useful as an architecture idea (four decision points in a pentest agent), not as benchmark evidence.

---

## 3. Community benchmarks (reproducible code)

### 3.1 dhruvmehra/jevbench
- **Link:** https://github.com/dhruvmehra/jevbench
- **Results file:** `docs/results/2026-09-22-n500-summary.md` (dated 2026-09-22)
- **Setup:** 500 seeded examples per dataset. Jev 1.13 was called through OpenRouter.
- **Comparators:**
  - Laya (421M parameters, open weights)
  - GPT-5-mini
  - Claude Sonnet 5
  - DistilBERT fine-tuned on up to 10k examples
  - BART-MNLI zero-shot

| Dataset | Jev acc | Jev ECE | Best other (acc) | Jev p50 latency | Jev $/1k |
|---|---|---|---|---|---|
| SST-2 (2 labels) | 95.4 | 0.026 | Sonnet 5: 95.6 | 376 ms | $0.015 |
| AG News (4 labels) | 84.3 | 0.112 | DistilBERT-ft: 91.0 | 381 ms | $0.018 |
| Banking77 (77 labels) | 76.4 | 0.125 | DistilBERT-ft: 88.0 | 389 ms | $0.083 |

- **Takeaway:** a cheap fine-tuned classifier still beats zero-shot Jev when labelled data exists.
- **Caveats:** at n=500 the 95% CI is about ±2.5 points. SST-2 and AG News are probably in pretraining data.

### 3.2 4esv/jev-eval
- **Link:** https://github.com/4esv/jev-eval
- **What it is:** a harness for comparing Jev with any OpenRouter model or local checkpoint on your own data.
- **Setup:** 300 items per task, Jev 1.13.0.

| Task | Jev | GPT-5.6 Terra | open-jev (435M) |
|---|---|---|---|
| CLINC (151 options) | **0.897** | — | 0.610 |
| Banking77 (77 options) | 0.780 | 0.847 | **0.873** |
| SST-5 (5 options) | 0.570 | **0.593** | 0.560 |
| IMDB polarity | **0.970** | **0.970** | 0.957 |

- Jev has the lowest ECE on CLINC (0.039).
- open-jev is the best-calibrated model on 4 of the 5 tasks.
- Jev's p50 latency barely moves between 2 and 151 options (0.17–0.20 s).
- **Caveat:** the author treats differences under about 5 points as noise.

### 3.3 stern9/jev-bench
- **Link:** https://github.com/stern9/jev-bench
- **Date:** results dated 2026-09-24.
- **Setup:** 72 hand-labelled decisions across three tasks: support routing (5-way choice), phishing (yes/no), and incident severity (score 0–3). Comparators are Claude Haiku 4.5 and Opus 5.

| | Jev | Haiku 4.5 | Opus 5 |
|---|---|---|---|
| Accuracy | 94.4% | 91.7% | 98.6% |
| p50 latency | ~185 ms | ~1.2 s | ~2.6 s |
| $/1k decisions | ~$0.02 | ~$0.82 | ~$6.40 |

- Jev's routing ECE is 0.025, the best of the three.
- Jev's misses were adjacent severity levels.
- **Caveat:** very small set, a single run, so the results are directional only.
- **Teaching use:** this is closest to the lecture's ticket-routing example.

---

## 4. Vendor sources (TypeSafe), treated as claims

### 4.1 Workflow evals
- **Link:** https://evals.typesafe.ai
- **Labels:** averaged answers from GPT-6 Astra and Claude Fable 5.1 at high thinking. **This is not ground truth.** It measures agreement with those models.
- **Workflows:** security incidents, agent trace review, invoice processing, customer service.
- **Mean across the 4 workflows:**
  - Jev: 67.8% at $0.0004 and 0.4 s per case.
  - GPT-6.1 Sol: 74.1% at $0.084 and 23 s.
  - Opus 5: 73.1% at $0.176 and 38 s.
### 4.2 Launch post: *Introducing System One Models & Jev*
- **Link:** https://typesafe.ai/blog/introducing-system-one-models-and-jev
- **Claims:**
  - 193.6× faster and 444.6× cheaper on workflows.
  - 70–500 ms latency.
  - $0.042 per million input tokens, with output free.
  - 0% hallucination.
- **Caveats:**
  - The 0% figure is guaranteed by the schema, not measured.
  - The workflows were written by TypeSafe's own team.
  - The authors acknowledge the pricing may be subsidized.

---

## Not included
- *Medium: "TypeSafe's Jev beyond the hype"* (https://medium.com/@pravvich/typesafes-jev-beyond-the-hype-an-independent-benchmark-8bdc1c99d000): the page was blocked, so I couldn't verify it.
- SEO, aggregator and explainer sites (jevai.tools, Wikipedia, and similar) contain no original measurements.

---

## Cross-cutting lessons (for the lecture)

1. **Calibration is task-dependent.** Jev's ECE is about 0.01 on one benchmark and about 0.11 on another (Vals). Audit calibration per task; don't assume it carries over.
2. **Ranking is not thresholding.** Binary probabilities can rank well and still sit poorly against 0.5 (Deußer et al.). Tune thresholds on held-out data (lecture slides 3 and 30).
3. **Recalibration helps.** Error dropped 3.3× in the crash-narrative study. This links to lecture slide 14 on temperature scaling and isotonic regression.
4. **Cost and latency claims hold up independently.** Vals confirms roughly 194× faster and about 1/500 the cost. Accuracy claims depend much more on the task.
5. **Labelled data still wins.** Fine-tuned DistilBERT beats zero-shot Jev on AG News and Banking77 (jevbench).
6. **Check what the labels are.** Vendor workflow evals measure agreement with reference models, not correctness. That is the point of lecture slide 29.
7. **Decision models differ from each other.** Mercury Decide beats Jev on LegalBench accuracy and calibration, while Jev is faster (Vals, 1.2). Evaluate alternatives on your own task; see `decision-models.md`.
