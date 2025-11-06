# Cognify — Function Specifications

This document defines Cognify’s core AI function interfaces and schemas for use with LLM function calling and structured outputs.  
Each function has a clear **purpose**, **parameters**, **JSON schema**, and **safety rules**.

---

## 1️⃣ Function: `generate_summary`

**Purpose:**  
Create a structured, concise summary from uploaded text, PDF content, or transcribed audio.

**When AI should call this:**  
- User uploads a new file and requests “summarize”  
- A quiz or glossary needs summary context first  
- Periodic re-summarization after document updates

**Parameters:**
| Name | Type | Required | Description |
|------|------|-----------|-------------|
| `document_id` | string | ✅ | Unique file ID |
| `content` | string | ✅ | Raw or cleaned text to summarize |
| `max_words` | integer | ❌ | Length limit (default: 300) |
| `style` | string | ❌ | “concise”, “academic”, “study-notes” (default: concise) |

**Returns:**  
Structured summary text with metadata (JSON).

```json
{
  "document_id": "doc_001",
  "summary": "This lecture introduces RAG architectures and discusses embeddings...",
  "word_count": 284,
  "style_used": "concise",
  "sources": [
    {"file": "Lecture-04.pdf", "page_range": "2–8"}
  ]
}
```

**JSON Schema:**
```json
{
  "name": "generate_summary",
  "description": "Generate a structured text summary from document content.",
  "parameters": {
    "type": "object",
    "properties": {
      "document_id": {"type": "string"},
      "content": {"type": "string"},
      "max_words": {"type": "integer", "default": 300, "minimum": 50, "maximum": 1000},
      "style": {
        "type": "string",
        "enum": ["concise", "academic", "study-notes"],
        "default": "concise"
      }
    },
    "required": ["document_id", "content"]
  }
}
```

**Safety Considerations:**
- Sanitize text before passing to LLM (remove PII).
- Limit `max_words` to prevent runaway token usage.
- Validate `document_id` pattern.
- Redact source text before logging.

---

## 2️⃣ Function: `generate_quiz`

**Purpose:**  
Produce 5–10 comprehension questions from a document or summary for active recall learning.

**When AI should call this:**  
- After summary generation.  
- When user explicitly asks “make me a quiz.”  

**Parameters:**
| Name | Type | Required | Description |
|------|------|-----------|-------------|
| `topic` | string | ✅ | The subject or summary title |
| `content` | string | ✅ | Input text (from summary) |
| `num_questions` | integer | ❌ | Default 5 |
| `difficulty` | string | ❌ | “easy”, “medium”, “hard” (default: medium) |

**Returns:**  
A structured quiz object with questions, answers, and difficulty levels.

```json
{
  "topic": "RAG Architecture",
  "questions": [
    {
      "id": 1,
      "question": "What problem does Retrieval-Augmented Generation solve?",
      "options": [
        "A) Low model accuracy",
        "B) Hallucination and missing context",
        "C) Cost of embeddings",
        "D) Audio-to-text conversion"
      ],
      "answer": "B",
      "difficulty": "medium"
    }
  ],
  "total": 5
}
```

**JSON Schema:**
```json
{
  "name": "generate_quiz",
  "description": "Generate quiz questions and answers from document content.",
  "parameters": {
    "type": "object",
    "properties": {
      "topic": {"type": "string"},
      "content": {"type": "string"},
      "num_questions": {"type": "integer", "default": 5, "minimum": 3, "maximum": 15},
      "difficulty": {
        "type": "string",
        "enum": ["easy", "medium", "hard"],
        "default": "medium"
      }
    },
    "required": ["topic", "content"]
  }
}
```

**Safety Considerations:**
- Ensure questions are based strictly on provided text (no hallucinations).  
- Reject requests with empty or irrelevant text.  
- Log generation metadata, not content.  

---

## 3️⃣ Function: `extract_glossary`

**Purpose:**  
Extract 10–15 key terms and definitions from a document to help learners review terminology.

**When AI should call this:**  
- After summarization or on explicit “make glossary” request.

**Parameters:**
| Name | Type | Required | Description |
|------|------|-----------|-------------|
| `content` | string | ✅ | Cleaned text from document |
| `max_terms` | integer | ❌ | Default 15 |

**Returns:**  
A list of key terms with short definitions.

```json
{
  "glossary": [
    {"term": "Embedding", "definition": "Numeric vector representation of text meaning"},
    {"term": "FAISS", "definition": "A library for fast vector similarity search"}
  ],
  "total": 12
}
```

**JSON Schema:**
```json
{
  "name": "extract_glossary",
  "description": "Identify and define important terms from input text.",
  "parameters": {
    "type": "object",
    "properties": {
      "content": {"type": "string"},
      "max_terms": {"type": "integer", "default": 15, "minimum": 5, "maximum": 25}
    },
    "required": ["content"]
  }
}
```

**Safety Considerations:**
- Detect and avoid including personal names or PII as terms.  
- Ensure definitions are factual and concise (≤ 20 words each).  
- Validate JSON structure before display.

---

## 4️⃣ Function Calling Flow (Shared)

```text
1️⃣ User uploads file → system stores `document_id`.
2️⃣ User requests summary or quiz → AI determines which function to call.
3️⃣ LLM emits function call JSON:
    {"name": "generate_summary", "arguments": {"document_id": "...", "content": "..."}}
4️⃣ Backend executes real code (later, Week 6) to perform that function.
5️⃣ Result returned as JSON → LLM uses it to craft a natural language response.
6️⃣ Final answer (summary, quiz, or glossary) displayed to the user with citations.
```

---

## 5️⃣ Safety & Compliance Summary

| Risk | Mitigation |
|------|-------------|
| Hallucinated facts | Restrict LLM answers to retrieved context only |
| Prompt injection | Sanitize all text before embedding / passing to model |
| Cost blowout | Limit max_tokens, enforce word caps |
| Data leakage | Never store raw uploaded text in logs |
| Abuse | Rate-limit: 10 calls/min per user |

---

**End of file**
