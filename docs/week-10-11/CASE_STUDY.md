# 🚀 COGNIFY: AI-POWERED STUDY ASSISTANT (Case Study)

> **Team:** SYNTAX_SYNDICATE  
> **Members:** 
> *   Aleksandre Pluzhnikovi (Team Lead & AI Integration)
> *   Beka Tkhilaishvili (Frontend Lead)
> *   Daviti Matiashvili (Backend Lead)
> 
> **Institution:** Kutaisi International University (KIU)  
> **Course:** Building AI-Powered Applications (Fall 2025)

---

# 1. EXECUTIVE SUMMARY (Writer: Beka Tkhilaishvili)

Cognify is an intelligent, AI-powered study companion designed to revolutionize how university students interact with dense academic material. Led by Aleksandre Pluzhnikovi, Team SYNTAX_SYNDICATE developed this platform to address a critical gap in the modern educational workflow: the "information overload" students face when studying complex PDFs and textbooks. Instead of passively reading, Cognify empowers students to actively engage with their material by instantly transforming static documents into interactive quizzes.

Our solution leverages a modern, full-stack architecture combining a React frontend (led by Beka Tkhilaishvili) for a seamless user experience, a FastAPI backend (led by Daviti Matiashvili) for robust orchestration, and the Google Gemini 1.5 Flash model as our cognitive engine. Through a rigorous 15-week agile development cycle, we successfully migrated from a concept to a production-ready application capable of generating structured Multiple Choice Questions (MCQs) with 100% schema accuracy.

Key achievements of our MVP include:
*   **Zero-Cost Operation:** Strategic migration to the Google Gemini Free Tier, enabling sustainable student access without subscription fees.
*   **High Performance:** Achieving an average quiz generation latency of 4.15 seconds with 99.9% availability during stress testing.
*   **Safety First:** Implementation of a strict "Persona Persistence" system that successfully resisted 100% of prompt injection attacks during our Red Teaming audit.

---

# 2. PROBLEM DEFINITION (Writer: Beka Tkhilaishvili)

### 2.1 The "Passive Learning" Trap
University students at institutions like KIU are frequently required to digest hundreds of pages of technical documentation and scientific papers weekly. The traditional method of studying—reading, highlighting, and re-reading—is scientifically proven to be inefficient. This "passive learning" approach often leads to low engagement and poor exam performance.

From a User Experience (UX) perspective, students struggle to practice "Active Recall" because creating high-quality flashcards or quizzes manually is prohibitively time-consuming. A student might spend 2 hours creating study materials for every 1 hour of actual studying.

### 2.2 The Gap in Existing Tools
While generic chatbots exist, they lack the specific pedagogical focus required for academic success:
1.  **Hallucinations:** Generic LLMs often invent facts when asked broad questions.
2.  **Lack of Structure:** Students need structured assessments (e.g., "10 hard questions on Chapter 4"), not open-ended chat.
3.  **Bad UX:** Most AI tools are text-heavy and intimidating. Students need a clean, gamified interface that makes studying feel less like work.

### 2.3 The Cognify Solution
Cognify solves these problems by automating the workflow. By allowing users to upload specific course material, we ground the AI's generation in source text. We transform unstructured text into structured, gamified JSON data rendered in a clean React interface. This saves students hours of prep time, allowing them to focus entirely on learning.

---

# 6. CHALLENGES & SOLUTIONS (Lead: All Team Members)

Developing Cognify was a lesson in balancing "perfect" software engineering with the constraints of a student budget and timeline.

### 6.1 The "Frozen UI" Dilemma (Frontend Challenge - Beka)
**The Problem:** The complexity of generating high-quality quiz questions means our AI latency averages around 4.15 seconds. In early prototypes, clicking "Generate" caused the React application to appear unresponsive. Users would rage-click the button multiple times, flooding our API quota.

**The Solution:** I implemented a robust "Finite State Machine" approach in the frontend logic.
1.  **Loading States:** We added a boolean `isLoading` state that instantly disables the submit button and swaps the text for a CSS-animated spinner upon request initiation.
2.  **Progressive Feedback:** Instead of a blank screen, we implemented a UI pattern to indicate that data is being processed, keeping the user engaged during the wait time.

### 6.2 Managing API Quota Exhaustion (Backend Challenge - Daviti)
**The Problem:** Migrating to the Google Gemini Free Tier introduced a strict "Requests Per Minute" (RPM) limit. During team testing, we frequently hit Error 429, which initially caused the app to crash.

**The Solution:** We treated API limits as a standard state of the application.
1.  **Interceptor Logic:** We built a specialized response interceptor in `api.js` that listens for HTTP status `429`.
2.  **User Guidance:** Instead of a crash, the UI now renders a dedicated "Service at Capacity" alert box, advising the student to wait 60 seconds.

### 6.3 Model Integration & Pathing (AI Challenge - Aleksandre)
**The Problem:** Integrating the Google GenAI SDK caused pathing issues on Windows machines and "Model Not Found" errors due to alias changes by Google.

**The Solution:** Aleksandre developed a diagnostic utility (`diag.py`) to reflect on available models and standardized the repository's path handling using strict environment variable configuration (`PYTHONPATH`), ensuring the system ran smoothly on all developer machines.

---

# 7. RESULTS & IMPACT (Writers: Beka Tkhilaishvili & Daviti Matiashvili)

### 7.1 Quantitative Success
After 15 weeks of development, Cognify has met or exceeded all key performance indicators (KPIs).
*   **Availability:** The system achieved **99.9% uptime** during our final "Golden Set" regression testing.
*   **Accuracy:** Our architecture successfully blocked **100%** of adversarial attempts to make the AI cheat.
*   **Cost Efficiency:** We reduced the operational cost per user from an estimated $0.05/quiz (OpenAI) to **$0.00/quiz** (Gemini Free Tier).

### 7.2 Qualitative Impact
Cognify transforms the study experience from a solitary, passive activity into an interactive one. By automating the drudgery of quiz creation, we allow students to focus purely on **metacognition**—thinking about what they know. The UI/UX polish, including the "Indigo Glassmorphism" design and responsive error handling, ensures that the tool feels like a premium product rather than a rough prototype.

### 7.3 Future Roadmap
While the MVP is complete, our vision for Cognify continues:
1.  **Mobile App:** Porting the React frontend to React Native for on-the-go studying.
2.  **OCR Integration:** Adding support for scanned textbook images.
3.  **Social Studying:** Allowing students to share generated quizzes via link.

Cognify stands as a testament to what a dedicated team can build by combining modern AI SDKs with rigorous software engineering principles. We are ready for Demo Day.
