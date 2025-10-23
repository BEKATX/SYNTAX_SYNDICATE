# Capstone Proposal

**Course:** Building AI-Powered Applications
**Team Name:** SYNTAX SYNDICATE
**Project Title:** Cognify
**Date:** October 21, 2025

---

## 1. Problem Statement

### The Problem

Many university and high school students struggle with the overwhelming volume of information they need to process for their courses. They are faced with dense textbook chapters, lengthy academic articles, and hours of recorded lectures. The critical process of converting this raw material into effective study aids—such as summaries, practice questions, and glossaries—is a manual, time-consuming, and cognitively demanding task that often gets skipped due to time constraints.

Currently, students use a patchwork of inadequate solutions. They might manually re-write notes, a process that is slow and doesn't guarantee comprehension. Others use multiple, disconnected online tools: a website for summarizing, another for making flashcards, and perhaps a general-purpose chatbot for asking questions. This approach is fragmented, inefficient, and fails to create a cohesive study experience for a specific piece of content.

This problem matters because ineffective studying leads directly to lower comprehension, higher stress levels, and ultimately, poorer academic outcomes. It's a significant barrier to learning. An AI-powered solution is perfectly suited to address this by automating the most laborious parts of study preparation. AI can analyze large volumes of text to synthesize key ideas, identify important terminology, and generate relevant questions, freeing students to focus on what truly matters: active learning and self-assessment.

---

### Scope

**What's In Scope:**
- **Feature/capability 1:** Ingestion of user content via three methods: pasted text, PDF document upload, and audio file upload (for lecture transcription).
- **Feature/capability 2:** Generation of three core AI-powered study aids: a concise summary, an interactive practice quiz, and a glossary of key terms with definitions.
- **Feature/capability 3:** A complete, single-page web application that provides a seamless user experience, including a tabbed interface to view generated content and the ability to export the full study guide to a formatted PDF.

**What's Out of Scope (but maybe future work):**
- **Thing you won't do 1:** User accounts and cloud-based storage. Session data will only be saved in the user's local browser storage.
- **Thing you won't do 2:** Real-time collaboration, sharing features, or support for video file inputs.

**Why This Scope Makes Sense:**
This scope is designed to deliver a complete and valuable end-to-end user journey within a single semester. It prioritizes perfecting the core AI-driven workflow over peripheral features like authentication, which can be added in the future.

---

## 2. Target Users

### Primary User Persona

**User Type:** University and High School Students

**Demographics:**
- **Age range:** 18-24
- **Technical proficiency:** High. Comfortable with modern web apps, but not developers.
- **Context of use:** Late-night study sessions on a laptop; quick reviews on a mobile device between classes.

**User Needs:**
1.  **Need #1:** To quickly understand the main points of a long document or lecture.
    - **Why it matters:** It saves critical study time and reduces anxiety before an exam.
    - **Current workaround:** Manually skimming chapters, re-reading paragraphs multiple times, or giving up and not reading the material at all.

2.  **Need #2:** To actively test their knowledge of the material, not just passively review it.
    - **Why it matters:** Active recall is a scientifically proven method for stronger memory retention.
    - **Current workaround:** Manually creating their own flashcards (which is tedious), or searching for generic online quizzes that don't match their specific course content.

3.  **Need #3:** To have all study materials for a specific topic organized in one accessible place.
    - **Why it matters:** It reduces the mental clutter of managing multiple files and links, making final exam review far more efficient.
    - **Current workaround:** A disorganized collection of downloaded PDFs, Google Docs for notes, and browser bookmarks.

**User Pain Points:**
- "I have a 30-page PDF to read for tomorrow and no time to get through it all."
- "I don't know what's important enough to be on the exam."
- "Making my own flashcards and practice questions takes forever."

---

### Secondary Users (Optional)
- **Lifelong Learners & Professionals:** Individuals studying for professional certifications who need to digest dense technical manuals and self-test their understanding.

---

## 3. Success Criteria

### Product Success Metrics

**How we'll know our solution works:**

1.  **Metric #1:** Task completion time
    - **Target:** A first-time user can successfully generate at least one study aid in under 3 minutes.
    - **Measurement method:** Time users from landing on the page to seeing their first generated output during usability testing.

2.  **Metric #2:** Output Quality
    - **Target:** At least 80% of users in a study rate the generated Quiz and Summary as a 4 or 5 on a 5-point usefulness scale.
    - **Measurement method:** Post-task survey administered during user testing sessions.

3.  **Metric #3:** Feature Engagement
    - **Target:** At least 60% of test users voluntarily use more than one of the core AI features (e.g., Summary and Quiz) on a single document.
    - **Measurement method:** Observation during user testing sessions.

4.  **Metric #4:** Performance
    - **Target:** The average end-to-end processing time for a standard 5-page PDF or 5-minute audio file is under 90 seconds.
    - **Measurement method:** Logging the time from API request to response on the backend.

### Technical Success Criteria

**Minimum viable performance:**
- **Response latency:** p95 latency for AI generation endpoints under 15 seconds for standard inputs.
- **Availability:** 99% uptime during the final two weeks of the semester.
- **Error rate:** <5% of API requests fail during user testing sessions.

### Learning Goals

**What each team member wants to learn:**

**Beka Tkhilaishvili:**
- Master state management in complex React applications using hooks.
- Learn best practices for building responsive, mobile-first web designs with CSS.
**Daviti Matiashvili:**
- Gain proficiency in designing and deploying RESTful APIs with FastAPI.
- Understand the full lifecycle of a full-stack application from development to deployment.
**Aleksandre Pluzhnikovi:**
- Learn to effectively integrate and manage multiple Hugging Face models within a single application.
- Understand the performance trade-offs (speed vs. quality) of different AI models.

---

## 4. Technical Architecture

### System Overview
Cognify is a full-stack web application with a decoupled architecture. The frontend is a single-page application built in React.js that handles all user interactions. It communicates via a REST API with a Python-based backend powered by FastAPI. The backend is responsible for all business logic, file processing, and orchestrating calls to our AI Core, which is a collection of pre-trained NLP models from libraries like Hugging Face Transformers and spaCy.

### Architecture Diagram
+------------------+ +----------------------+ +---------------------------+
| User's Browser   | | Backend Server | | AI Model Services |
| (React Frontend) | | (FastAPI)      | | (Python) |
+------------------+ +----------------------+ +---------------------------+
| | |
| 1. Upload PDF/Audio | |
|-------------------------> | POST /api/upload/... |
| | |
| | 2. Extract/Transcribe Text |
| <-------------------------| 200 OK { text: "..." } |
| | |
| 3. Click "Quiz Me" | |
|-------------------------> | POST /api/generate-quiz |
| | |
| | 4. Call AI Core Quizzer |
| |--------------------------------> | [Question Gen Model] |
| | |
| <-------------------------| 200 OK { quiz: [...] } |
| | |
| 5. Display Quiz in UI | |

### Technology Stack

**Frontend:**
- **Framework:** React.js (with Hooks)
- **Key libraries:** JavaScript (ES6+), CSS3
- **Hosting:** Vercel

**Backend:**
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Hosting:** Render

**AI/ML Services:**
- **Primary model(s):** Hugging Face Transformers for Summarization (`distilbart-cnn-12-6`) and Question Generation (`t5-base-qg-hl`).
- **Other AI services:** OpenAI Whisper for transcription, spaCy for Named Entity Recognition.

**Data Storage:**
- **Database:** None for V1.0.
- **Vector store:** None for V1.0.
- **Session Storage:** Browser Local Storage.

### Data Flow

**Flow: User Uploads PDF -> Generates Quiz**

1.  User clicks "Upload PDF" on the React frontend.
2.  Frontend sends the file via a `POST` request to the `/api/upload-pdf` endpoint.
3.  FastAPI backend receives the file, uses `PyMuPDF` to extract text.
4.  Backend sends the extracted text back to the frontend in a JSON response.
5.  Frontend displays the text in a textarea for user review.
6.  User clicks "Quiz Me".
7.  Frontend sends the reviewed text in a `POST` request to `/api/generate-quiz`.
8.  Backend calls the AI Core's `generate_questions` function.
9.  The function loads the T5 model and generates a list of questions.
10. Backend returns the list of questions to the frontend.
11. Frontend displays the interactive quiz in the UI.

---

## 5. Risk Assessment

### Technical Risks

- **Risk #1: Low-quality AI outputs** (e.g., inaccurate summaries, nonsensical questions)
  - **Likelihood:** Medium, **Impact:** High
  - **Mitigation:** 1. Research and benchmark multiple pre-trained models before selection. 2. Always allow the user to review and edit all generated content.
- **Risk #2: High latency from AI models**
  - **Likelihood:** High, **Impact:** Medium
  - **Mitigation:** 1. Enforce strict input size limits to manage processing time. 2. Implement clear loading indicators in the UI to manage user expectations.

### Product Risks

- **Risk #1: Users don't find the tool significantly better than their current methods.**
  - **Likelihood:** Medium, **Impact:** High
  - **Mitigation:** 1. Conduct early user interviews (Week 3-4) to validate pain points. 2. Focus on a seamless, integrated workflow, which is our key differentiator.

### Team Risks

- **Risk #1: Unequal workload distribution.**
  - **Likelihood:** Medium, **Impact:** Medium
  - **Mitigation:** 1. Use GitHub Issues to make work visible and track progress. 2. Review task distribution at each weekly meeting.

### Safety & Ethical Risks

- **Risk #1: Misinformation from AI outputs.**
  - **Likelihood:** Medium, **Impact:** Medium
  - **Mitigation:** 1. Add a clear disclaimer in the UI stating that AI-generated content may contain errors and should be verified. 2. Use reputable, well-documented models.

---

## 6. Research Plan

### What We Need to Learn

**Technical Questions:**
1.  **Question:** What are the best pre-trained models on Hugging Face that balance quality and inference speed for our summarization and quiz generation tasks?
    - **Resources:** Hugging Face Hub, academic papers on text generation.
    - **Timeline:** Weeks 3-4

2.  **Question:** How can we reliably access word-level confidence scores from the Whisper transcription model to implement the review feature?
    - **Resources:** Whisper model documentation, open-source projects using Whisper.
    - **Timeline:** Week 4

**Product Questions:**
1.  **Question:** Do students prefer more multiple-choice questions or more open-ended questions in their practice quizzes?
    - **Method:** A/B test during user studies.
    - **Timeline:** Week 7

### Experiments & Prototypes

- **Weeks 3-4: AI Core Proof-of-Concept:** Build standalone Python scripts for each AI feature to validate model choices and performance before building the API.
- **Weeks 7-8: User Testing Round 1:** Test a prototype of the complete end-to-end workflow with 3-5 users to identify major UX flaws and validate the core value proposition.

---

## 7. User Study Plan

### Research Ethics

**Do we need IRB approval?**
- [x] No - but we've completed the IRB Light Checklist. Our study collects anonymous usability feedback, does not involve sensitive data, and poses minimal risk to participants.

**Data we'll collect:**
- Observer notes, anonymous survey responses on usefulness, task completion times.
- Data will be stored in a team-shared, password-protected folder and deleted at the end of the semester.

**User consent:**
- We have adapted the course consent template. Users will be informed that participation is voluntary and they can withdraw at any time.

### Testing Protocol

**Session Structure (30 minutes):**
1.  **Introduction (5 min):** Explain the purpose and get consent.
2.  **Task (20 min):** Provide the user with a 3-4 page PDF article and ask them to use Cognify to create a study guide they would use for an exam. We will observe using a "think-aloud" protocol.
3.  **Debrief (5 min):** Ask follow-up questions about their experience and have them complete a short survey on usefulness.

---

## 8. Project Timeline & Milestones

### Weekly Breakdown
| Week | Focus | Key Deliverable(s) |
| :--- | :--- | :--- |
| 2 | **Planning** | **This Proposal, Team Contract, Repo Setup** |
| 3-4 | **Core Functionality** | Headless AI scripts work; basic end-to-end summarize feature |
| 5-6 | **Full Feature Integration**| All AI features (Quiz, Glossary) and inputs (PDF, Audio) integrated |
| 7-8 | **User Testing & Iteration**| Conduct first round of user testing; implement key feedback |
| 9-10 | **Polish & UX** | Implement loading states, error handling, and session persistence |
| 11-12| **Final Features** | Implement PDF export; conduct second round of user testing |
| 13-14| **Final Polish & Deployment**| Final bug fixes, deploy to Vercel/Render, prepare demo |
| 15 | **Final Demo** | Present the final project |

### Major Milestones

**✅ Milestone 1: Proposal (Week 2)** - YOU ARE HERE
- **Submission:** October 24, 2025
- **Points:** 10

**🎯 Milestone 2: Design Review (Week 4)**
- **Submission:** November 7, 2025
- **Points:** 5
- **What's due:** Updated architecture, evaluation plan, backlog, token usage plan

**🎯 Milestone 3: Safety & Evaluation Audit (Week 11)**
- **Submission:** January 9, 2026
- **Points:** 3
- **What's due:** Red team results, bias checks, golden set, error taxonomy, telemetry plan

**🎯 Milestone 4: Final Demo (Week 15)**
- **Submission:** February 6, 2026
- **Points:** 7
- **What's due:** Working product, CI/CD, public README, demo video, case study

### Dependency Map
- ⚠️ Basic API integration (Week 4) blocks Full Feature Integration (Week 5).
- ⚠️ A working core user flow (Week 6) is required before the first round of User Testing (Week 7).
- ⚠️ The User Study Plan (Week 2) must be complete before recruiting users (Week 6).

### Backup Plan

**If we fall behind, we'll cut (in this order):**
1.  **Audio File Input:** This is the most complex input type to process.
2.  **Interactive Quiz Answer-Checking:** The feature will degrade to a simpler "Show Answer" button.
3.  **PDF Export:** The core value is in the interactive web app; the export is a nice-to-have.

**Core features we won't cut:**
- Text and PDF input processing.
- AI generation of Summaries, Quizzes, and Glossaries.
- The core web interface for viewing and interacting with the results.

---

## 9. Budget & Resources

### Cost Estimates

**AI API Costs:**
- The selected models (Distilbart, T5, Whisper) can all be run locally on a standard developer machine or on free-tier cloud services like Hugging Face Spaces or Google Colab. Therefore, we anticipate $0 in direct API or compute costs.
- **Total AI costs: $0**

### Resource Constraints

**Time:**
- **Total:** ~15 weeks
- **Accounting for midterms, finals:** ~12 effective weeks
- **Team capacity:** ~5 hours/week × 3 team members = **15 total hours/week**

**Compute:**
- **Development machines:** Team laptops are sufficient for running the frontend, backend, and most AI models.
- **GPU needs:** May be required for faster Whisper transcription. We will use free services like Google Colab for initial testing if needed.

**Access:**
- **API keys:** No paid API keys are required for the core V1.0 feature set. A Hugging Face account token may be needed and will be stored in the `.env` file.

---

## 10. Appendix

### Team Contract Summary
Our team contract outlines member roles (Frontend, Backend, AI Integration), communication protocols (Discord, twice-weekly meetings), and a conflict resolution process. See [docs/team-contract.md](./team-contract.md) for full details.

### References
- Hugging Face Transformers Documentation
- FastAPI Documentation
- React Documentation
- OpenAI Whisper Paper/Repository

### Revision History
| Date | Author | Changes |
|------|--------|---------|
| 10/21/2025 | Beka Tkhilaishvili | Initial draft of the capstone proposal |
| 10/22/2025 | All | Team review, added budget, risks, and detailed timeline |

---

## Instructor Use Only

**Grade: _____ / 10**

| Component | Points | Feedback |
|-----------|--------|----------|
| Problem Clarity | __/2 | |
| Technical Feasibility | __/2 | |
| Success Criteria | __/1 | |
| Risk Assessment | __/1 | |
| Research & User Plan | __/1.5 | |
| Team Contract | __/1.5 | |
| Presentation Quality | __/1 | |

**Overall Feedback:**