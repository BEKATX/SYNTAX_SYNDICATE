# Cognify - Your AI-Powered Study Buddy 🚀

**Cognify is a web application built by Syntax Syndicate to help students study smarter, not harder.**  
It takes your messy notes, dense readings, and long lectures and automatically transforms them into concise summaries, interactive quizzes, and key-term glossaries.

---

### 🌟 Key Features

* **Multi-Format Input:** Upload PDFs, paste text, or drop in recorded audio lectures.
* **AI Summaries:** Generate concise, citation-linked summaries from any document.
* **Interactive Quizzes:** Get 5–10 comprehension questions directly from your material.
* **Automatic Glossary:** Extract 10–15 key terms and definitions.
* **Export Study Packs:** Download formatted summaries + quizzes + glossaries as PDFs.
* **RAG Architecture:** Context-aware retrieval ensures accuracy and grounding in source material.

---

### 🧭 Week 5 Progress Report

#### ✅ Major Deliverables
| Component | Description | Status |
|------------|--------------|--------|
| **Project Requirements Document (PRD)** | Complete system requirements, architecture, and latency goals finalized. | ✅ |
| **Function Specifications** | Defined JSON schemas for core AI calls (`generate_summary`, `generate_quiz`, `extract_glossary`). | ✅ |
| **Pydantic Models** | Implemented validated output schemas for all AI functions and logs. | ✅ |
| **RAG Strategy** | Designed full Retrieval-Augmented Generation pipeline (FAISS + reranker). | ✅ |
| **Metadata Schema** | Created chunk and document registries with timestamped entries. | ✅ |
| **Evaluation Setup** | Golden set defined for automated weekly precision testing. | 🟡 (in progress) |

#### 🧩 Technical Highlights
* Implemented **FAISS-based local vector search** for cost-free retrieval.
* Added **cross-encoder reranking** option for dense corpora.
* Defined **JSON-based structured outputs** compatible with LLM function-calling.
* Added **Pydantic validation** for AI outputs and logs.
* Ensured compliance with **PII redaction and access control** rules.
* Drafted **CLI tools** for indexing, reindexing, and evaluation metrics.

#### 📁 Related Files
- [`prd-full.md`](./docs/week-5/prd-full.md) → Complete PRD & architecture.
- [`functions-spec.md`](./docs/week-5/functions-spec.md) → Function-level JSON schemas.
- [`pydantic-models.py`](./docs/week-5/pydantic-models.py) → Validated Pydantic models.
- [`rag-strategy.md`](./docs/week-5/rag-strategy.md) → RAG architecture, retrieval pipeline, evaluation metrics.

---

### 🛠️ Tech Stack

* **Frontend:** React.js (Hooks, Vite)
* **Backend:** FastAPI (Python 3.11 + Redis RQ)
* **Database:** PostgreSQL (via Supabase)
* **Storage:** MinIO / S3 (encrypted at rest)
* **AI Models:** GPT-4o / GPT-4o-mini, text-embedding-3-small
* **Libraries:** spaCy, PyPDF2, FAISS, Whisper
* **CI/CD:** GitHub Actions + Docker Compose
* **Monitoring:** Prometheus + Grafana

---

## ⚡ Performance & Optimization (Week 9)

COGNIFY is optimized for cost and speed using **Result Caching**.

### Performance Metrics
- **Cache Hit Latency:** < 2ms
- **Cache Miss Latency:** ~2.5s
- **Cost Reduction:** Estimated 40% savings on repeated study sessions.

### Architecture
We use a **Direct Function Calling** approach (Path B) combined with an LRU Cache to minimize redundant LLM calls. All costs are tracked in `logs/cost_audit.jsonl`.

### 🚀 Getting Started

➡️ **[Development Setup Guide](./docs/setup.md)**

### 👥 Team: Syntax Syndicate

| Name | Role | GitHub |
| :--- | :--- | :--- |
| Beka Tkhilaishvili | Frontend Lead | [@BEKATX](https://github.com/BEKATX) |
| Daviti Matiashvili | Backend Lead | [@mato08](https://github.com/mato08) |
| Aleksandre Pluzhnikovi| AI Integration Lead| [@sTreLeCa](https://github.com/sTreLeCa) |

---

This project was created for the "Building AI-Powered Applications" course at KIU (Fall 2025). See our full project plan in the [Capstone Proposal](./docs/capstone-proposal.md).
