# RAG Strategy — Cognify
 
This document specifies Cognify’s Retrieval-Augmented Generation (RAG) approach: sources, architecture, implementation choices, metadata schema, quality evaluation, and rollout plan.

---

## 1) Knowledge Sources

### 1.1 Primary inputs (student-provided)
| Source type | Examples | Format | Expected size | Update cadence |
|---|---|---|---:|---|
| Lecture PDFs | course slides, handouts | PDF | 5–50 pages/file | Weekly |
| Text exports | notes, transcripts | TXT/MD | 1–100 KB | Ad hoc |
| Audio lectures (optional) | recorded talks | MP3/WAV | ≤ 5 min/clip | Ad hoc |

### 1.2 Internal materials (team-provided)
| Source type | Examples | Format | Expected size | Use |
|---|---|---|---:|---|
| Golden set | labeled questions, citation spans | JSONL | 50–100 cases | Eval |
| System prompts | summarization/quiz/glossary templates | MD/TXT | < 20 KB | Generation |

> Scope rule: Only **user-authorized** files are indexed. No web crawling.

---

## 2) Architecture Choice

We adopt **Traditional RAG with optional Hybrid re-ranking**.

```text
User query → Embed query → Vector search (FAISS) → Retrieve top-k chunks
→ (optional) Cross-encoder rerank → Build prompt with citations → LLM output
```

Why:
- Simple, reproducible, and low-latency for MVP.
- FAISS local index keeps cost near zero.
- Optional rerank gives quality headroom for dense/long PDFs.

---

## 3) System Diagram (RAG Path)

```mermaid
flowchart LR
    U["User Question"] --> QEmbed["Embed Query"]
    QEmbed --> VS["FAISS Vector Search — k = 5"]
    VS -->|top-k| ReRank{"Rerank"}
    ReRank -- Yes --> XR["Cross-Encoder Rerank — k to m"]
    ReRank -- No --> Prompt["Prompt Builder — with citations"]
    XR --> Prompt
    Prompt --> LLM["LLM — GPT-4o mini / GPT-4o"]
    LLM --> Resp["Answer + Citations"]
```

---

## 4) Technical Implementation

### 4.1 Embeddings
- **Model:** `text-embedding-3-small`
- **Dims:** 1536  
- **Granularity:** embed at **chunk** level (not page/document)
- **Normalization:** L2-normalize vectors
- **Dedup:** SHA-256 hash of cleaned chunk text (avoid re-embedding)

### 4.2 Vector Store
- **Engine:** **FAISS** (FlatIP initially; HNSW if corpus > 200k chunks)
- **Metric:** cosine similarity
- **Sharding:** single index per user workspace
- **Persistence:** `data/faiss/{workspace_id}/index.faiss` + `meta.parquet`

### 4.3 Chunking Strategy
- **Splitter:** token-aware (tiktoken) with sentence bias
- **Chunk size:** **900 tokens**
- **Overlap:** **180 tokens**
- **Max page span per chunk:** 2 pages
- **Section hints:** prefer headings to start new chunks (regex on PDF text)

### 4.4 Retrieval Parameters
- **k (initial):** **5**
- **Similarity threshold:** **0.70**
- **Reranker (optional):** cross-encoder `ms-marco-MiniLM-L-6-v2` on top-k → top-m (**m=3**)
- **Diversity:** MMR λ = 0.5 (enabled only when top-k > 10)

### 4.5 Prompt Assembly
- **Context budget:** ≤ **1,200 input tokens** total
- **Template:**  
  - “Instructions” (concise)  
  - **Cited context** = concatenation of `m` chunks: `[CHUNK i]\n{content}\n(Source: file, page, span)`  
  - User question  
- **Citation format:** inline `[#i]` with footnotes at end.

---

## 5) Metadata & Storage Schema

### 5.1 Chunk metadata (Parquet/JSONL)
```json
{
  "chunk_id": "wksp_12:doc_abc:p9:100-820",
  "workspace_id": "wksp_12",
  "doc_id": "doc_abc",
  "file_name": "Lecture-04-Transformers.pdf",
  "page_start": 9,
  "page_end": 10,
  "char_start": 100,
  "char_end": 820,
  "text": "...chunk text...",
  "hash": "sha256:3c6e0b8a9c...",
  "tokens": 892,
  "created_at": "2025-11-07T15:21:11Z",
  "embedding": "[1536 floats]"  // stored in FAISS; reference here is optional
}
```

### 5.2 Document registry
```json
{
  "doc_id": "doc_abc",
  "workspace_id": "wksp_12",
  "title": "Lecture 04 - Transformers",
  "source_path": "/uploads/wksp_12/Lecture-04.pdf",
  "num_pages": 28,
  "lang": "en",
  "status": "indexed",
  "chunks": 146,
  "last_indexed_at": "2025-11-07T15:19:02Z"
}
```

---

## 6) Indexing Pipeline

### 6.1 Steps
1. **Ingest** file → extract text/page structure (PyPDF + fallback OCR if needed).  
2. **Clean** text → normalize whitespace, remove headers/footers.  
3. **Chunk** with 900/180 strategy + heading-aware splits.  
4. **Embed** each chunk (`text-embedding-3-small`).  
5. **Upsert** vectors into FAISS; write metadata to Parquet.  
6. **Verify** counts, sample neighbors for sanity, persist.

### 6.2 CLI (dev utility)
```bash
# Index a PDF into a workspace
python -m tools.index --workspace wksp_12 --file "./uploads/Lecture-04.pdf"

# Rebuild FAISS from metadata (safety)
python -m tools.rebuild_faiss --workspace wksp_12
```

### 6.3 Re-indexing policy
- Re-index if **file hash changes** or chunker version changes.
- Maintain `index_version` for migrations.

---

## 7) Query Flow (detailed)

```text
1) Receive user question
2) Build query embedding
3) Vector search (k=5, thr=0.70)
4) (optional) Cross-encoder rerank → top-3
5) Assemble prompt with cited chunks ≤ 1,200 tokens
6) Call LLM (GPT-4o mini; escalate to GPT-4o for complex cases)
7) Return final answer with [#i] inline refs + footnotes
8) Log: tokens_in/out, latency, chosen chunks, scores
```

**Escalation heuristic:** escalate to GPT-4o when:
- No chunk surpasses sim **0.78**, or
- Question detected as **multi-part** (≥ 2 intents), or
- Answer requires synthesis across **≥ 4 chunks**.

---

## 8) Quality & Evaluation

### 8.1 Metrics
- **Answer faithfulness** (citation-grounded) — manual + LLM judge  
- **Context precision@k** (relevant chunk ratio) — target **≥ 0.8**  
- **Latency** (vector search) — **< 300 ms** on dev laptop  
- **ASR → RAG** path (if audio) — WER (< 12%) before indexing

### 8.2 Golden Set (from Week-4 plan)
- 50+ labeled Q→{relevant_chunks[], expected_terms[]}  
- Evaluate nightly via CLI; output `evaluation/metrics.csv`.

### 8.3 Failure Taxonomy
- **Miss:** no relevant chunk retrieved → raise k or relax threshold.  
- **Hallucination:** low sim + missing citations → enforce “answer only from context.”  
- **Duplicate context:** chunk overlap returns near-duplicates → enable MMR.

---

## 9) Privacy, Security, & Access Control

- **Per-workspace isolation:** separate FAISS index + metadata file space.  
- **Access control:** only workspace members can query or export.  
- **PII handling:** redact PII **before** embedding; keep raw uploads encrypted at rest (MinIO SSE).  
- **Deletion:** hard-delete vectors + metadata on file removal (verify by hash).  
- **Audit:** log query, top-k doc ids, but not raw content in logs.

---

## 10) Performance & Cost

- **Local FAISS** keeps retrieval cost $0.  
- Embedding cost minimal (see `cost-model-v2.md`).  
- **Context budget** caps LLM spend (≤ 1,200 in / 500 out).  
- Cache the most common queries per workspace for 24h.

---

## 11) Rollout Plan

| Phase | Goal | Switches |
|---|---|---|
| **Alpha** | pure FAISS (k=5), no rerank | FlatIP |
| **Beta** | add optional rerank for dense docs | Cross-encoder top-3 |
| **RC** | HNSW for large corpora | efSearch tuned for P95 < 150ms |

---

## 12) Acceptance Criteria

- Uploading a 20-page PDF results in:  
  - ≥ 95% pages produce chunks  
  - Index build ≤ 15s on dev machine  
  - Query “What is X?” returns ≥ 3 relevant chunks with correct citations  
- End-to-end: summary includes **[#1][#2]** citations that match footnotes.  
- CLI eval on golden set achieves **precision@5 ≥ 0.8**.

---

## 13) Open Questions

- Add OCR step for image-only PDFs (tesseract vs. paddleocr)?  
- Multi-language support (embedding model swap on language detect)?  
- Per-user vs. per-team workspace indexes in UI?

---

## 14) Appendix — Prompt Skeleton

```text
SYSTEM: You are a study assistant. Answer **only** with the cited context.
If a fact is missing in the context, say you don't know.

CONTEXT (≤1200 tokens):
[#1] {chunk_1_text}
Source: {file_1}, p{page_start}–{page_end}, chars {char_start}-{char_end}

[#2] {chunk_2_text}
Source: {file_2}, p{...}

USER QUESTION:
{question}

ASSISTANT:
- Short, precise answer.
- Use [#i] inline markers and add footnotes:
[1] {file_1}, p{page_start}
[2] {file_2}, p{...}
```

---
