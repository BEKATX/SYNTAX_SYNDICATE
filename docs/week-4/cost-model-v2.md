# Token Usage & Cost Model v2 — Cognify

This document defines pricing baselines, per-feature cost formulas, example per-query calculations, and monthly scenarios for Cognify’s MVP.  
All prices are in USD and sourced from the official provider pricing pages.

---

## 1) Models & Unit Prices

### 1.1 Language Models (Text)
| Model | Unit | Price |
|---|---:|---:|
| **GPT-4o mini** | Input tokens | **$0.15 / 1M** (= $0.00015 / 1K) |
|  | Output tokens | **$0.60 / 1M** (= $0.00060 / 1K) |
| **GPT-4o** | Input tokens | **$2.50 / 1M** (= $0.0025 / 1K) |
|  | Output tokens | **$10.00 / 1M** (= $0.0100 / 1K) |

### 1.2 Embeddings
| Model | Unit | Price |
|---|---:|---:|
| **text-embedding-3-small** | Embedding tokens | **$0.02 / 1M** (= $0.00002 / 1K) |

### 1.3 Speech (Optional)
| Service | Unit | Price |
|---|---:|---:|
| **Google Cloud Speech-to-Text V2 (Standard)** | per minute | **$0.016 / min** |
| **Google Cloud Text-to-Speech (WaveNet / Standard)** | after free tier | **$4 / 1M characters** (= $0.000004 / char) |

> Prices exclude taxes and temporary free-tier promotions.

---

## 2) Baseline Token Profiles

| Flow | Avg Input Tokens | Avg Output Tokens | Notes |
|---|---:|---:|---|
| **Cited Summary** | 1 200 | 500 | 3–8 page PDF |
| **Quiz (5 MCQ + 2 SA)** | 900 | 450 | facts + distractors |
| **Glossary (10 items)** | 600 | 350 | term + definition |
| **Embeddings per new doc** | 3 000 | — | ≈ 6 chunks × 500 |
| **TTS summary** | — | ≈ 600 chars | short output |
| **STT audio** | — | ≈ 1 min | short segment |

---

## 3) Per-Query Cost Formulas

```text
LLM_in   = (Cin  / 1_000_000) * Pin
LLM_out  = (Cout / 1_000_000) * Pout
EmbCost  = (E    / 1_000_000) * Pe
STT      = M * Pstt
TTS      = (Chars / 1_000_000) * Ptts
QueryCost = LLM_in + LLM_out + EmbCost + STT + TTS
```

Where:  
- `Cin`, `Cout` = token counts  `Pin`, `Pout` = token rates  
- `E`, `Pe` = embedding tokens / price  `M`, `Pstt` = audio minutes / price  
- `Chars`, `Ptts` = TTS characters / price  

---

## 4) Worked Examples (GPT-4o mini unless stated)

### 4.1 Cited Summary (new doc + embedding)
- `Cin = 1200`, `Cout = 500`, `E = 3000`  
- LLM_in = 1200 × $0.15 / 1M = **$0.00018**  
- LLM_out = 500 × $0.60 / 1M = **$0.00030**  
- Embeddings = 3000 × $0.02 / 1M = **$0.00006**  
**→ Total = $0.00054 (≈ 0.054¢)**  

### 4.2 Quiz (5 MCQ + 2 SA)
`Cin = 900`, `Cout = 450`  
→ (900 × $0.15 + 450 × $0.60)/1M = **$0.00041 (≈ 0.04¢)**  

### 4.3 Glossary (10 items)
`Cin = 600`, `Cout = 350`  
→ **$0.00030 (≈ 0.03¢)**  

### 4.4 Voice Task (STT + summary + TTS)
- STT 1 min = $0.01600  
- LLM summary = $0.00048  
- TTS 600 chars = 600 × $4 / 1M = $0.00240  
**→ Total = $0.01888 (≈ 1.89¢)**  

### 4.5 Heavy Case (GPT-4o, 10 % traffic)
`Cin = 2000`, `Cout = 1000` on GPT-4o  
→ LLM_in = 2000 × $2.50 / 1M = $0.00500  
→ LLM_out = 1000 × $10.00 / 1M = $0.01000  
**→ Total = $0.01500 (1.5¢)**  

---

## 5) Month-Level Scenarios

| Scenario | Queries / Month | Mix | Est. Cost / Query | Est. Total Cost |
|---|---:|---:|---:|---:|
| **S1 Testing** | 3 000 | 100 % mini | $0.00040 | **$1.20** |
| **S2 Class Pilot** | 9 000 | 90 % mini / 10 % GPT-4o | — | **$17.40** |
| **S3 Heavy Week** | 18 000 | 80 % mini / 20 % GPT-4o | — | **$60.97** |

Voice features add ≈ $0.0189 per 1-minute task.

---

## 6) Cost Optimization Guidelines

1. **Model routing** – use GPT-4o mini by default; escalate only for complex cases.  
2. **Prompt discipline** – ≤ 1 200 input / 500 output tokens; deduplicate context.  
3. **Embed once / reuse** – hash chunks to avoid re-embedding.  
4. **Response caching** – cache identical requests (short TTL).  
5. **Batching** – group background jobs (quiz + glossary).  
6. **Latency budget** – warm indices to avoid retries (wasted tokens).  

---

## 7) Operational Logging Schema

| Field | Example | Purpose |
|---|---|---|
| request_id | `req_20251106_153012` | traceability |
| task | `summary | quiz | glossary` | segmentation |
| model | `gpt-4o-mini` | routing |
| tokens_in / out | `1200 / 500` | token audit |
| embedding_tokens | `3000` | vector cost |
| latency_ms | `2450` | performance |
| cost_usd_est | `0.00054` | cost tracking |
| ts | ISO 8601 | time series |
