# Optimization Audit Report
**Project:** COGNIFY  
**Team:** SYNTAX_SYNDICATE  
**Date:** December 11, 2025

## 1. Current State Analysis
**Baseline Metrics (Week 8 Data):**
- **Model:** `gpt-4o-mini` (Used for all quiz generations)
- **Avg Latency:** 2.8s per quiz generation
- **Avg Input Tokens:** ~4,500 (approx 10 pages of PDF text context)
- **Avg Output Tokens:** ~300 (JSON quiz structure)
- **Cost per Request:** ~$0.00085
- **Caching:** None. Every request hits the OpenAI API.

**Hotspots:**
1.  **Redundant Processing:** Students often study the same popular textbooks. Uploading the same PDF results in re-processing and re-generating identical quizzes.
2.  **Context Size:** Sending raw text includes unnecessary whitespace/formatting, inflating input token costs by ~15%.

---

## 2. Optimization Opportunities

| Opportunity | Description | Est. Savings | Priority |
|-------------|-------------|--------------|----------|
| **Result Caching** | Cache generated quizzes based on a hash of the (PDF Text + Topic). If User A and User B study the same PDF, User B gets a cached result. | 40-60% | **High** |
| **Context Optimization** | Strip whitespace and non-essential chars from PDF text before sending to LLM. | 10-15% | **Medium** |
| **Model Cascading** | Use a cheaper model/regex for simple "Flashcard" extraction vs `gpt-4o-mini` for "Deep Quiz". | <5% | Low |

---

## 3. Implementation Plan
We will implement **Result Caching** and **Cost Instrumentation**.

**Strategy:**
1.  **Instrumentation:** Create a structured logging utility to track every cent spent.
2.  **Caching:** Implement an in-memory LRU cache (simulating Redis).
    *   **Key:** `hash(pdf_content_snippet + topic + difficulty)`
    *   **TTL:** 24 hours (Study materials don't change often).
3.  **Success Metric:**
    *   Reduce latency for repeated queries to < 0.1s.
    *   Reduce costs by 30% in simulated multi-user test.

---

## 4. Cost Projection (Monthly)
*Based on 1,000 active students generating 5 quizzes/day.*

| Scenario | Monthly Queries | Cost/Query | Total Cost |
|----------|-----------------|------------|------------|
| **Baseline** | 150,000 | $0.00085 | **$127.50** |
| **Optimized** (30% Cache Hit) | 105,000 (API) | $0.00085 | $89.25 |
| | 45,000 (Cache) | $0.00000 | $0.00 |
| **Total Optimized** | | | **$89.25** |
| **Annual Savings** | | | **~$459.00** |
