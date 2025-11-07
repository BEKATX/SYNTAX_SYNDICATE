# Feature Roadmap — Cognify
---

## 1. Methodology

This roadmap was created using two AI design frameworks:

1. **20-Pillar Design System** → broad exploration of potential product functions.  
2. **Feature Prioritization Framework** → selection of high-impact, feasible features for the MVP.

The resulting plan covers **6 strategic design pillars**, **60 feature ideas**, and **a prioritized MVP set of 15 core features** to be implemented by Week 15.

---

## 2. Selected Strategic Design Pillars

| Pillar # | Name | Relevance |
|-----------|------|------------|
| 1 | **User-Centered Experience** | Ensures accessibility and simplicity for students. |
| 2 | **Retrieval & Citation Integrity** | Guarantees that every summary and quiz item links to verifiable source text. |
| 3 | **Cost Optimization & Caching** | Keeps token usage minimal for free/educational tiers. |
| 4 | **Evaluation & Analytics** | Enables performance tracking and golden-set benchmarking. |
| 5 | **Accessibility & Export** | Provides universal access and offline study options. |
| 6 | **Reliability & Error Recovery** | Maintains stability and transparency when models or APIs fail. |

---

## 3. Feature Matrix (60 Ideas)

### 🧩 Pillar 1 – User-Centered Experience
1. Drag-and-drop PDF upload  
2. Audio record and upload button  
3. Step-by-step upload wizard  
4. Progress indicator and loading animation  
5. Streaming summary updates in real time  
6. Hover-to-view citations in summary  
7. Quiz practice mode with score feedback  
8. Glossary side panel with source links  
9. Dark/light mode toggle  
10. Keyboard-only navigation

---

### 📚 Pillar 2 – Retrieval & Citation Integrity
1. Document chunking (500 tokens + 50 overlap)  
2. FAISS vector store with embeddings  
3. Source-span storage for citations  
4. Citation confidence scores  
5. Citation consistency checker  
6. Duplicate-sentence filtering  
7. Re-ranking retrieved chunks by semantic similarity  
8. Snippet preview on hover  
9. “View source in context” button  
10. Audit log of retrieved chunks per query

---

### 💰 Pillar 3 – Cost Optimization & Caching
1. Response cache for identical prompts  
2. Embedding cache by chunk hash  
3. Tiered model routing (mini → pro)  
4. Token-usage logger per request  
5. Prompt compression heuristics  
6. Batched requests for similar jobs  
7. Partial result reuse across sessions  
8. Local model fallback if API fails  
9. Dashboard of average token cost per user  
10. Monthly cost summary in admin panel (optional)

---

### 📊 Pillar 4 – Evaluation & Analytics
1. Golden-set test runner (50 cases)  
2. Dashboard for latency, accuracy, and cost  
3. Prompt variant A/B testing hooks  
4. Feedback widget (👍 / 👎 + comment)  
5. Regression tests before deployments  
6. User-satisfaction survey integration  
7. Automatic metric export to CSV  
8. Heatmap of most retrieved topics  
9. Error taxonomy categorization  
10. Notification if accuracy drops > 10 %

---

### ♿ Pillar 5 – Accessibility & Export
1. High-contrast theme  
2. Dyslexia-friendly font toggle  
3. Screen-reader ARIA labels  
4. Adjustable text size slider  
5. Offline study pack download (PDF/MD)  
6. Export selected sections only  
7. QR code to share study sheet  
8. Mobile responsive layout  
9. Localization (en → ka later)  
10. Print-ready format preview

---

### 🛡 Pillar 6 – Reliability & Error Recovery
1. Queue with automatic retries (Redis RQ)  
2. Dead-letter queue for failed jobs  
3. Circuit breaker for external API calls  
4. Graceful fallback to cached outputs  
5. Error report popup with trace ID  
6. “Report an issue” link auto-filling logs  
7. Status page for backend health  
8. Retry counter displayed in logs  
9. Job timeout monitoring and alert  
10. Auto-restart stuck jobs after 2 min

---

## 4. MVP Features (Week 15 Target)

| # | Feature | Pillar | Reason for Inclusion |
|---|----------|---------|----------------------|
| 1 | Cited Summary Generator | Retrieval & Citation | Core value — trustworthy summaries |
| 2 | Quiz Generator (MCQ + Short) | User Experience | Supports active learning |
| 3 | Glossary Extractor + Definitions | User Experience | Key for concept recall |
| 4 | FAISS Vector Search | Retrieval & Citation | Enables RAG accuracy |
| 5 | PDF Upload + Parsing | User Experience | Primary input path |
| 6 | Audio Transcription (Whisper) | Reliability | Multimodal support |
| 7 | Real-Time Streaming Summaries | UX / Reliability | Fixes latency perception |
| 8 | Response & Embedding Cache | Cost Optimization | 40 % cost reduction target |
| 9 | Feedback Widget (👍 / 👎) | Evaluation | Data for metric tracking |
| 10 | Golden-Set Test Runner | Evaluation | Quantitative benchmarking |
| 11 | Token Usage Logger | Cost Optimization | Required for cost model |
| 12 | Error Popup + Trace Logs | Reliability | Debug visibility |
| 13 | Export to PDF/Markdown | Accessibility | Offline study option |
| 14 | Dark/Light Mode + Font Toggle | Accessibility | Improves usability |
| 15 | Dashboard for Latency & Cost | Evaluation | Presentation / metrics visualization |

---

## 5. Future Roadmap (Post-Course)

| Phase | Features |
|-------|-----------|
| **Phase 2 (After Week 15)** | Multi-document summaries · User accounts · Team folders · Personalization (learning style profiles) |
| **Phase 3 (Extended)** | Mobile app · Collaborative study rooms · Gamified quiz leaderboards · AI coach chatbot |

---

## 6. Prioritization Rationale

The MVP focuses on:
- **Educational impact** → summaries + quizzes + glossaries cover learning cycle (comprehend → test → recall).  
- **Feasibility under free resources** → all core features use open-source models.  
- **Reliability** → caching and queueing mitigate slow models.  
- **Evaluation alignment** → feedback widget and golden set enable Week 7 testing and Week 11 audit.

Future phases add social and enterprise-scale features only after academic MVP is stable.

---

## 7. Implementation Timeline (Excerpt)

| Week | Deliverable | Key Features Implemented |
|------|--------------|--------------------------|
| 5 – 6 | RAG Integration | Vector search + citations + summary refinement |
| 7 | User Testing #1 | Quiz + feedback widget + dashboard (MVP subset) |
| 8 – 10 | Optimization | Caching + token logging + error handling |
| 11 | Safety Audit | Golden set + PII redaction tests |
| 14 – 15 | Final Demo | Export features + UI polish + report |

---

**Prepared by:** Syntax Syndicate · Team Cognify  
