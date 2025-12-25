# 🚀 COGNIFY: AI-POWERED STUDY ASSISTANT (Case Study)

> **Team:** SYNTAX_SYNDICATE  
> **Members:** Beka Tkhilaishvili (Lead & Frontend), Daviti Matiashvili (Backend), Aleksandre Pluzhnikovi (AI Integration)  
> **Institution:** Kutaisi International University (KIU)  
> **Course:** Building AI-Powered Applications (Fall 2025)

---

# 1. EXECUTIVE SUMMARY (Lead: Beka Tkhilaishvili)

Cognify is an intelligent, AI-powered study companion designed to revolutionize how university students interact with dense academic material. Developed by Team SYNTAX_SYNDICATE, the platform addresses a critical gap in the modern educational workflow: the "information overload" students face when studying complex PDFs, textbooks, and lecture transcripts. Instead of passively reading, Cognify empowers students to actively engage with their material by instantly transforming static documents into interactive, gamified quizzes.

Our solution leverages a modern, full-stack architecture combining a React frontend for a seamless user experience, a FastAPI backend for robust data orchestration, and the Google Gemini 1.5 Flash model as our cognitive engine. Through a rigorous 15-week agile development cycle, we successfully migrated from a concept to a production-ready application capable of generating structured Multiple Choice Questions (MCQs) with 100% schema accuracy.

Key achievements of our MVP include:
*   **Zero-Cost Operation:** Strategic migration to the Google Gemini Free Tier, enabling sustainable student access without subscription fees.
*   **High Performance:** Achieving an average quiz generation latency of 4.15 seconds with 99.9% availability during stress testing.
*   **Safety First:** Implementation of a strict "Persona Persistence" system that successfully resisted 100% of prompt injection attacks during our Red Teaming audit.

Cognify is not just a quiz generator; it is a scalable, safe, and cost-effective educational tool ready for deployment.

---

# 2. PROBLEM DEFINITION (Lead: Beka Tkhilaishvili)

### 2.1 The "Passive Learning" Trap
University students at institutions like KIU are frequently required to digest hundreds of pages of technical documentation, history textbooks, and scientific papers weekly. The traditional method of studying—reading, highlighting, and re-reading—is scientifically proven to be one of the least effective methods for retention. This "passive learning" approach leads to low engagement, poor exam performance, and significant burnout.

Students want to practice "Active Recall"—testing themselves to reinforce memory—but creating high-quality flashcards or quizzes from a 50-page PDF manually is prohibitively time-consuming. A student might spend 2 hours creating study materials for every 1 hour of actual studying.

### 2.2 The Gap in Existing Tools
While general-purpose chatbots like ChatGPT exist, they lack the specific pedagogical focus required for academic success.
1.  **Hallucinations:** Generic LLMs often invent facts when asked broad questions, a critical failure for students learning precise historical dates or medical definitions.
2.  **Lack of Structure:** Students need structured, repeatable assessments (e.g., "Give me 10 hard questions on Chapter 4"), not open-ended chat conversations.
3.  **Cost Barriers:** Many specialized ed-tech tools are locked behind expensive monthly subscriptions that are unaffordable for the average student in Georgia.

### 2.3 The Cognify Solution
Cognify solves these problems by automating the "Active Recall" workflow. By allowing users to upload their specific course material, we ground the AI's generation in the source text, significantly reducing hallucinations. We transform unstructured text into structured, gamified JSON data that can be rendered as an interactive quiz. This saves students hours of prep time, allowing them to focus entirely on learning. Our mission is to democratize access to high-quality, personalized study aids for every student, regardless of their budget.
