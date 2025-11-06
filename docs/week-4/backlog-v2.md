# Backlog v2 — Cognify

This backlog defines all planned features for the Cognify MVP, organized by priority and milestone.  
Each task includes user story, acceptance criteria, dependencies, and definition of done.

---

## Priority 1 — Critical Path (Weeks 5–6)
Core infrastructure required for MVP and all downstream work.

### Issue #1: Project Skeleton & Environment Setup
**Priority:** P1  
**User Story:** As a developer, I want a clean repository with backend and frontend scaffolds so the team can collaborate efficiently.  
**Acceptance Criteria:**
- [ ] FastAPI backend with `/health` endpoint
- [ ] React frontend with placeholder upload form
- [ ] Shared `.env.example` and setup documentation
**Dependencies:** None  
**Definition of Done:** Project installs and runs locally; `GET /health` returns 200.

---

### Issue #2: PDF Upload & Text Extraction
**Priority:** P1  
**User Story:** As a user, I can upload a small PDF, and the system extracts plain text per page.  
**Acceptance Criteria:**
- [ ] Upload endpoint accepts PDFs up to 10 MB  
- [ ] Text extraction preserves page numbers  
- [ ] Errors handled gracefully  
**Dependencies:** #1  
**Definition of Done:** Example PDF returns structured text (page, text[]).

---

### Issue #3: Text Chunking & Preprocessing
**Priority:** P1  
**User Story:** As a developer, I can split extracted text into uniform chunks for later embedding and retrieval.  
**Acceptance Criteria:**
- [ ] Deterministic chunking (500 tokens ± 50 overlap)  
- [ ] Page and character metadata stored per chunk  
**Dependencies:** #2  
**Definition of Done:** Given same input, identical chunks are produced.

---

### Issue #4: Embedding & Local Vector Store
**Priority:** P1  
**User Story:** As a user, I can store and retrieve document content efficiently.  
**Acceptance Criteria:**
- [ ] Build FAISS index for stored chunks  
- [ ] Top-k retrieval (< 300 ms for small corpora)  
- [ ] Metadata mapping chunk → page preserved  
**Dependencies:** #3  
**Definition of Done:** Test query returns top-5 relevant chunk IDs.

---

### Issue #5: Summarization with Citations
**Priority:** P1  
**User Story:** As a student, I receive an AI-generated summary with citations pointing to source passages.  
**Acceptance Criteria:**
- [ ] Summary generated from retrieved chunks  
- [ ] Citations include page and span IDs  
- [ ] Output JSON: `{text, citations[]}`  
**Dependencies:** #4  
**Definition of Done:** Example document produces valid summary output.

---

### Issue #6: Quiz Generation
**Priority:** P1  
**User Story:** As a student, I can practice key concepts using auto-generated quizzes.  
**Acceptance Criteria:**
- [ ] Generates at least 5 MCQs + 2 SA questions  
- [ ] Each question has 1 correct answer and 3 distractors  
- [ ] JSON format matches schema (`question`, `choices[]`, `answer`)  
**Dependencies:** #4  
**Definition of Done:** Valid JSON returned for sample topic.

---

### Issue #7: Glossary Extraction
**Priority:** P1  
**User Story:** As a student, I can view a glossary of terms extracted from uploaded material.  
**Acceptance Criteria:**
- [ ] Extracts top 10 key terms with definitions  
- [ ] Each entry linked to source chunk  
- [ ] Glossary returned in JSON or table format  
**Dependencies:** #4  
**Definition of Done:** Glossary displays on frontend with 10+ entries.

---

## Priority 2 — High-Value Enhancements (Weeks 7–10)

### Issue #8: Frontend Integration
**Priority:** P2  
**User Story:** As a user, I can interact with the Cognify system through a modern interface.  
**Acceptance Criteria:**
- [ ] Upload → Progress indicator → Results view  
- [ ] Displays summary, quiz, glossary in tabs  
- [ ] Handles loading/error states  
**Dependencies:** #1, #5–7  
**Definition of Done:** Full front-to-back demo flow operational.

---

### Issue #9: Evaluation Pipeline Integration
**Priority:** P2  
**User Story:** As a team, we can automatically evaluate model outputs using our golden set.  
**Acceptance Criteria:**
- [ ] CLI test runner executes 10+ golden cases  
- [ ] Computes latency and Relevance@5 metrics  
- [ ] Outputs CSV results for dashboard import  
**Dependencies:** #4–5  
**Definition of Done:** Evaluation results visible in `/evaluation/results.csv`.

---

### Issue #10: Feedback Widget & Analytics
**Priority:** P2  
**User Story:** As a user, I can rate generated results to help improve quality.  
**Acceptance Criteria:**
- [ ] Simple 👍/👎 feedback with optional comment  
- [ ] Stored in Postgres table `feedback(task, rating, comment, ts)`  
- [ ] Aggregated analytics in dashboard  
**Dependencies:** #8  
**Definition of Done:** User feedback visible in analytics panel.

---

### Issue #11: Caching & Token Logging
**Priority:** P2  
**User Story:** As a developer, I can monitor token usage and cache repeated queries.  
**Acceptance Criteria:**
- [ ] Cache identical requests within 24 h  
- [ ] Log tokens_in/out, model, latency, cost estimate  
**Dependencies:** #5–6  
**Definition of Done:** Cache hit rate and logs visible in dashboard.

---

## Priority 3 — Nice-to-Have (Weeks 11–15)

### Issue #12: Audio Mode (Speech-to-Text + TTS)
**Priority:** P3  
**User Story:** As a user, I can upload short audio files to generate transcripts and summaries.  
**Acceptance Criteria:**
- [ ] Transcribe < 5 min audio clips  
- [ ] Summarize transcript and output TTS audio summary  
**Dependencies:** #5, #8  
**Definition of Done:** Audio round-trip demo successful.

---

### Issue #13: Export Options
**Priority:** P3  
**User Story:** As a student, I can export results for offline study.  
**Acceptance Criteria:**
- [ ] Export combined summary + quiz + glossary as PDF and Markdown  
- [ ] Include header, date, and source list  
**Dependencies:** #8  
**Definition of Done:** Exported file opens and displays properly.

---

### Issue #14: Personal Study History
**Priority:** P3  
**User Story:** As a user, I can revisit previously analyzed materials.  
**Acceptance Criteria:**
- [ ] Save processed results to account  
- [ ] List past uploads with timestamps  
- [ ] Delete option available  
**Dependencies:** #8  
**Definition of Done:** History page functions correctly.

---

## Milestone Overview

| Milestone | Week | Focus | Key Deliverables |
|---|---:|---|---|
| **M1: Setup & Pipeline Core** | 5–6 | Backend skeleton, ingestion, FAISS, summarizer | Issues #1–5 |
| **M2: Feature Completion** | 7–10 | Quiz, glossary, evaluation, analytics | Issues #6–11 |
| **M3: Polish & Expansion** | 11–15 | Audio mode, export, study history | Issues #12–14 |

---

**Prepared by:** Syntax Syndicate · Team Cognify
