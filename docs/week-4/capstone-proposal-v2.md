# Capstone Proposal v2 — Cognify
---

## 1. Problem Statement (Refined)

University and high-school students constantly face long, information-dense study materials — PDFs, lecture slides, or recorded lessons — but lack time to digest and extract key insights.  
A short survey of 6 KIU students showed:
- 100 % reread course PDFs multiple times before exams,
- 80 % skip at least one reading due to time pressure,
- 40 % said generic AI summarizers gave inaccurate or source-less answers.

**Cognify** addresses this problem by giving students a single place to upload their study material and automatically receive:
1. a cited summary,  
2. a short quiz,  
3. a glossary of important terms.  

This improves comprehension and active recall while reducing study preparation time from hours to minutes.

---

## 2. Solution Summary (Updated)

**Cognify** is an AI-powered study buddy that transforms uploaded content into concise, trustworthy study aids.

### Input Modalities
- Paste plain text  
- Upload PDF lecture slides  
- Upload short audio clips (lecture recordings)

### Outputs
- **Cited Summary:** paragraph-level citations to original text.  
- **Interactive Quiz:** MCQ + short-answer questions.  
- **Glossary:** extracted key terms with context sentences.  
- **Export:** optional PDF or Markdown study sheet.

### Tech Stack Overview
| Layer | Technology | Notes |
|-------|-------------|-------|
| **Frontend** | React (Vite + shadcn/ui) | Responsive SPA, uses REST calls |
| **Backend** | FastAPI (Python 3.11) | Handles uploads, RAG queries |
| **Worker** | Redis RQ | Long-running jobs (audio → text, exports) |
| **AI Core** | DistilBART / T5 / Whisper / spaCy | Summaries, quizzes, glossary, transcription |
| **Storage** | Local dev → S3 (prod) + Postgres | Docs, metrics, audit logs |
| **Deployment** | Render (API) + Vercel (frontend) | Free/student tiers only |

---

## 3. Week 3–4 Learnings

| Topic | Insight | Impact |
|--------|----------|--------|
| **Latency** | Summarization takes 4–6 s for 3-page PDFs | Added response streaming + caching |
| **Audio Inputs** | Noise caused recognition errors | Introduced Redis worker + noise-filtering |
| **User Preference** | Students valued glossary and citations more than quiz complexity | Prioritize glossary + citation accuracy |
| **Architecture** | Monolithic backend was hard to scale | Separated FastAPI API from AI worker |
| **Model Cost Awareness** | GPT models are costly for frequent use | Plan local models by default, remote optional |

---

## 4. Technical Decisions Log

| Area | Option A | Option B | Decision | Rationale |
|-------|-----------|-----------|-----------|------------|
| Summarizer | DistilBART | GPT-4o-mini | ✅ DistilBART | Free + local; good quality |
| Quiz Gen | T5-base QG | GPT-4o-mini | ✅ T5 | Fully open-source |
| Transcription | Whisper-small | Google STT | ✅ Whisper | No paid API |
| Embeddings | text-embedding-3-small | Sentence-BERT | ✅ OpenAI 3-small | Standard + low cost |
| Vector Store | FAISS local | Pinecone cloud | ✅ FAISS | Offline + free |
| Storage | Postgres + MinIO | Firebase | ✅ Postgres + MinIO | Structured logging |
| Deployment | Render + Vercel | Docker on GCP | ✅ Render/Vercel | Faster dev, no infra cost |

---

## 5. Updated Architecture Overview

Key Improvements Since Week 2:
- Added **Redis worker** for async audio and heavy model tasks  
- Defined **latency budgets** (< 3 s text, < 12 s audio)  
- Introduced **Postgres metrics table** for logging latency & cost  
- Clear **security boundaries** (JWT Auth → API → internal AI core)  
- Caching layer between FAISS and LLM requests  

---

## 6. Success Criteria (Measurable)

| Category | Metric | Target | Measurement |
|-----------|---------|---------|--------------|
| **Performance** | End-to-end latency | < 3 s (text), < 12 s (audio) | Logs + Grafana |
| **Accuracy** | Citation alignment | ≥ 90 % correct | Manual review |
| **User Satisfaction** | Usefulness rating | ≥ 4.0 / 5 avg (10 testers) | Survey |
| **Learning Effect** | Quiz score gain | ≥ 15 % improvement | A/B tests |
| **Reliability** | Uptime Week 15 | ≥ 99 % | Monitoring |
| **Cost Efficiency** | Avg cost per query | ≤ $0.05 (estimated) | Simulated pricing |

---

## 7. Risk Assessment (Revised)

| Risk | Likelihood | Impact | Mitigation |
|------|-------------|---------|-------------|
| Model Hallucination / Bad Citations | Medium | High | Restrict context to retrieved chunks + show sources |
| Slow Response Times | Medium | Medium | Streaming + Async Jobs + Caching |
| Team Bandwidth | Medium | Medium | Prioritize MVP features only |
| Cost Creep if using APIs | Low | Medium | Use free models first; simulate costs |
| Data Privacy | Low | High | Local storage + PII redaction |
| User Adoption | Medium | High | Run user testing Round 1 (Week 7) |

---

## 8. Updated Timeline (Realistic)

| Week | Milestone | Deliverable |
|------|------------|--------------|
| 2 | Proposal & Contract ✅ | docs + repo setup |
| 4 | Design Review ✅ | v2 proposal + architecture |
| 5–6 | RAG implementation | FAISS retrieval + summarizer integration |
| 7 | User Testing #1 | 3–5 participants + feedback forms |
| 8–10 | Iteration + Caching | Improved latency + UI polish |
| 11 | Safety Audit | Red-team + error taxonomy |
| 14 | User Testing #2 | Final UX round |
| 15 | Final Demo 🎯 | Working MVP + report |

---

## 9. Open Questions

1. Optimal chunk size for retrieval vs. context window length?  
2. Best way to evaluate quiz quality quantitatively?  
3. Should multi-document summaries be included in MVP or post-course roadmap?  
4. How to collect anonymous user feedback ethically without auth system?  

---

### References
- Hugging Face Transformers Docs  
- OpenAI API Pricing (https://openai.com/api/pricing)  
- FastAPI Documentation  
- OWASP AI Security Top 10  

---

**Prepared by:** Syntax Syndicate (Team Cognify)  
**Members:** Beka Tkhilaishvili · Daviti Matiashvili · Aleksandre Pluzhnikovi  
