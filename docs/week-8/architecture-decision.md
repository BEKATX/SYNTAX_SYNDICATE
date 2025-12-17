# Architecture Decision: Direct Function Calling

**Project:** COGNIFY  
**Team:** SYNTAX_SYNDICATE  
**Date:** December 17, 2025  

**Decision:** Path B - Direct Function Calling

**Rationale:**
COGNIFY is a study aid that performs specific, deterministic tasks based on user input (PDFs). We do not require an autonomous agent loop.

**Justification:**
1.  **Predictable Workflow:** The user journey is linear: Upload -> Parse -> Generate. An agent reasoning loop (ReAct) adds unnecessary latency.
2.  **Cost Efficiency:** Direct function calling uses significantly fewer tokens than an agent loop that "thinks" before acting. Since students are price-sensitive, cost control is a priority.
3.  **Accuracy:** We want strict adherence to the Pydantic models defined in Week 6, without the LLM trying to "improvise" new steps.

**Trade-offs Considered:**
- **Advantages:** 5-10x lower cost, <2s latency, strict type safety.
- **Disadvantages:** Less flexible if a user asks complex, multi-step questions (e.g., "Compare this PDF to a Wikipedia article").

**Future Considerations:**
If we add a "Research Assistant" feature that searches the web to supplement the PDF content, we will upgrade to an Agent architecture for that specific feature.
