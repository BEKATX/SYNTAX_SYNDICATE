# Architecture Explanation — Cognify
---

## 1. Diagram Reference
See `architecture-v2.png`. It shows three main zones:
- **User Zone:** browser (UI) with file upload and real-time feedback.
- **Application Zone:** FastAPI gateway + Redis queue + Postgres DB.
- **AI Core Zone:** local/remote models + FAISS vector store + MinIO storage.

---

## 2. Component Purpose Summary

| # | Component | Purpose |
|---|------------|----------|
| 1 | **React SPA** | Single-page app for uploading content and viewing results. |
| 2 | **FastAPI Server** | Auth, API routing, logging, metrics collection. |
| 3 | **Redis RQ Worker** | Executes CPU/GPU-intensive jobs asynchronously. |
| 4 | **AI Models (LLM Core)** | Generates summaries, quizzes, glossaries. |
| 5 | **FAISS Index** | Retrieves relevant chunks for RAG. |
| 6 | **Postgres DB** | Stores metrics, feedback, golden-set data. |
| 7 | **MinIO/S3** | Keeps user uploads and exports. |
| 8 | **Grafana Dashboard** | Visualizes latency, accuracy, cost metrics. |

---

## 3. Design Trade-Offs

| Decision | Pros | Cons | Mitigation |
|-----------|------|------|-------------|
| Use local models instead of remote APIs | $0 cost, offline capable | Slower on CPU | Redis queue + streaming |
| FastAPI monolith vs microservices | Simpler deploy, less overhead | Harder to scale | Add worker tier only for AI |
| FAISS (local) vs Pinecone | Free and fast for small sets | Not managed | Persist index daily backup |
| MinIO vs S3 | Local testing | Need manual bucket setup | Use S3 in prod with same API |
| Postgres vs MongoDB | Structured analytics | Schema rigidity | ORM migrations for evolution |

---

## 4. Potential Bottlenecks

1. **LLM Inference Speed** → mitigated by queue + batching.  
2. **Large PDF Extraction** → chunk page-by-page with progress updates.  
3. **Redis Queue Overflow** → auto-scaling worker processes planned.  
4. **Front-end streaming disconnects** → resumable event streams via retry tokens.  
5. **Vector Store growth** → prune old indices periodically.

---

## 5. Architecture Goals

- ⚡ **Low Latency:** Target < 3 s for text, < 12 s for audio.  
- 🔒 **Privacy:** Local processing + PII redaction.  
- 💰 **Zero Cost Ops:** Run entirely on free tiers.  
- 🧠 **Transparency:** Display citations + model metadata to user.  
- 🧩 **Extensibility:** Add RAG + multi-doc support easily later.

---

**Authors:** Syntax Syndicate (Team Cognify)
