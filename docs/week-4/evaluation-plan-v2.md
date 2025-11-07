# Evaluation Plan v2 — Cognify

Cognify turns course materials (text/PDF/audio) into a **cited summary**, **quiz**, and **glossary**. This plan defines **metrics**, **methods**, a **golden set**, a **user testing protocol**, and a **timeline** to evaluate quality, speed, safety, and usability — aligned with Week 7 user testing, Week 11 safety audit, and Week 15 demo.

---

## 1) Success Metrics (Quantitative & Verifiable)

| Category | Metric | Target | Why it matters | Measurement Source |
|---|---|---|---|---|
| **Performance** | p50 / p95 end-to-end latency (text) | ≤ 1.8s / ≤ 3.0s | Feels instant for short text | API logs (ts start/finish) |
|  | p50 / p95 end-to-end latency (10-min audio) | ≤ 7s / ≤ 12s | Usable for short lectures | Worker logs + job duration |
| **Retrieval Quality** | Relevance@5 | ≥ 85% | Good top-k chunks | Golden set judgments |
| **Citation Integrity** | Correct-citation rate | ≥ 90% | Trustworthiness | Span match vs ground truth |
| **Summary Quality** | Human usefulness rating | ≥ 4.0 / 5.0 (n≥10) | Study value | Post-task survey |
| **Quiz Utility** | Learning uplift on repeat | ≥ +15% | Efficacy | Pre/post short quiz |
| **Reliability** | Uptime (Week 15 demo week) | ≥ 99% | Stability | Uptime ping/health checks |
| **Cost Efficiency** | Est. cost/query (simulated) | ≤ $0.05 | Feasible at scale (sim) | Token logger × price sheet |
| **Adoption (internal)** | Sessions/day (testers) | ≥ 10 | Usage proxy | App analytics |
| **Feedback** | Widget response rate | ≥ 30% of sessions | Signal for iteration | Postgres feedback table |

**Operational definitions**
- **Relevance@5**: fraction of test prompts where ≥1 of the top-5 retrieved chunks is labeled “relevant”.
- **Correct-citation**: generated citation spans point to ground-truth source ranges (page + char offsets) with ≥80% overlap.

---

## 2) Evaluation Methods

### 2.1 Golden Set (50+ cases by Week 6)

**Purpose:** Standardized, repeatable tests to track quality and regressions.

**Composition (target distribution):**
- **Typical (70%)**: clean PDFs, lecture notes, short articles.
- **Edge (20%)**: scanned PDFs, math/LaTeX, code-heavy notes, mixed languages (en/ka).
- **Adversarial (10%)**: random text, irrelevant uploads, repeated pages, empty sections.

**Labeling schema (per case)**
```json
{
  "id": "gs_lectures_023",
  "input_type": "pdf|text|audio",
  "source_meta": {"title": "Lecture 5 - Trees", "pages": 18},
  "prompts": [
    {"task": "summary", "ask": "Summarize key ideas"},
    {"task": "quiz", "ask": "Create 5 MCQs"},
    {"task": "glossary", "ask": "Extract 10 key terms"}
  ],
  "ground_truth": {
    "key_points": ["BST ops", "Traversal orders", "Balancing idea"],
    "citation_spans": [
      {"page": 6, "start": 120, "end": 260},
      {"page": 9, "start": 30, "end": 210}
    ],
    "expected_terms": ["BST", "AVL", "Rotation", "Inorder"],
    "relevant_chunks": ["p6:100-320", "p9:0-240"]
  }
}
```

**Storage & access**
- Repo path: `docs/golden-set/`
- Files: `*.json` metadata + original assets (PDF/audio) stored locally; keep small.
- Review: two-pass light labeling; disagreements resolved by 2/3 vote.

**Automation**
- CLI runner `scripts/eval_runner.py` computes latency, Relevance@5, and correct-citation rate; outputs `evaluation/results.csv`.

---

### 2.2 User Testing Protocol (Week 7 & Week 14)

**Participants**
- n = 5–7 KIU students (CS/DS).
- Inclusion: familiar with PDFs/lecture notes.
- Consent: IRB-light checklist; anonymize feedback.

**Tasks (≤ 15 minutes total)**
1. **Upload & Summary:** Upload a 3–8 page PDF; view cited summary.  
   - Success: completes unaided ≤ 5 min; finds at least 2 useful points.  
2. **Quiz:** Generate 5 MCQs; answer them.  
   - Success: completes ≤ 6 min; post-task clarity ≥ 4/5.  
3. **Export:** Export PDF/MD study sheet.  
   - Success: completes ≤ 2 min; file opens correctly.

**Measured signals**
- Time-on-task, errors, help requests.  
- SUS (System Usability Scale) + 4 custom questions (usefulness, trust in citations, quiz helpfulness, willingness to reuse).  
- Open comments.

**Instrumentation**
- Frontend event log (start/finish per task).  
- Feedback widget (👍/👎 + comment).  
- Survey form (anonymous link).

---

### 2.3 A/B & Prompt Experiments (as time allows)
- **A/B**: Prompt A (concise) vs Prompt B (verbose) for summaries.  
- Metrics: usefulness rating, citation correctness, tokens used.  
- Rollout: dev only; 50/50 split; random by session id.

---

### 2.4 Regression Testing (CI)
- Run golden set on each PR that touches retrieval/generation code.  
- **Fail build if**: Relevance@5 drops by >5% absolute, citation correctness < 85%, or p95 latency rises by >20% vs baseline.  
- Export results → `evaluation/history/`.

---

## 3) Tools & Infrastructure

- **Logging**: JSON structured logs (ts, user_session, task, tokens_in/out, latency_ms).  
- **Metrics Store**: Postgres table `metrics(request_id, task, latency_ms, tokens_in, tokens_out, cost_usd_est, ts)`.  
- **Dashboards**: Grafana panels for latency p50/p95, cost/query, feedback trend.  
- **Test Runner**: Python CLI (`scripts/eval_runner.py`) to run the golden set and emit CSV.  
- **Repro seeds**: fixed random seeds for model sampling when feasible.

---

## 4) Data Governance & Safety

- **PII Handling**: no real user data in golden set; transcripts sanitized; logs strip emails/phones.  
- **Storage**: small local files; MinIO/S3 only if needed; delete test uploads weekly.  
- **Access**: restrict evaluation assets to team; don’t publish lecture PDFs without permission.  
- **Ethics**: informed consent for testers; allow withdrawal; anonymize results.

---

## 5) Schedule & Milestones

| Week | Activity | Metric | Target |
|---|---|---|---|
| **4** | Baseline capture on 10 cases | Initial Relevance@5 / latency | Document current |
| **5** | RAG integration smoke test | Relevance@5 | ≥ 70% |
| **6** | Golden set finalized (50+) | Test coverage | ≥ 50 cases |
| **7** | **User testing round 1** | Task completion | ≥ 70% |
| **8–10** | Iteration & caching | p95 latency | −25% vs W4 |
| **11** | **Safety audit** | Red-team pass rate | ≥ 90% blocked |
| **14** | User testing round 2 | Satisfaction | ≥ 4.0/5 |
| **15** | Final evaluation & report | All metrics | Hit targets |

---

## 6) Reporting

- **Weekly** mini-report in `docs/evaluation/weekly.md`: key metrics, issues, actions.  
- **Release** notes include golden-set delta table.  
- **Final** evaluation appendix includes raw CSV + plots and lessons learned.

---

## 7) Risks & Mitigations (Evaluation-Specific)

| Risk | Impact | Mitigation |
|---|---|---|
| Labeling inconsistency in golden set | Noisy metrics | Two-pass labeling; adjudication |
| Tiny n in user testing | Low statistical power | Focus on qualitative + task success |
| Latency spikes on shared machines | Unfair comparisons | Repeat runs; report medians + p95 |
| Overfitting to golden set | Inflated metrics | Hold-out cases; periodic refresh |

---

## 8) Zero-Cost Operation Note

All evaluation activities are designed to **avoid spending money**:
- Prefer **local** models: DistilBART/T5/Whisper/spaCy.  
- If remote LLMs are tested, **simulate cost** via token logger × **published price sheets** (OpenAI pricing page).  
- All metrics (latency, quality, feedback) are collected locally with no paid services.

---

**Prepared by:** Syntax Syndicate · Team Cognify
