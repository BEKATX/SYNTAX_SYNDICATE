
# Event Schemas Documentation
**Project:** COGNIFY  
**Team:** SYNTAX_SYNDICATE  
**Last Updated:** November 27, 2025

This document defines the JSON schemas for the core events in the COGNIFY study assistant.

---

## 1. User Quiz Request Event
**Purpose:** Triggered when a student requests a quiz from uploaded content.

```json
{
  "event_type": "quiz_generation_request",
  "timestamp": "2025-11-27T10:30:00Z",
  "request_id": "req_882910",
  "user_id": "user_123",
  "payload": {
    "topic": "Python Introduction",
    "difficulty": "medium",
    "num_questions": 5,
    "source_text_length": 1500
  }
}

## 2. LLM Tool Call Event (Week 6 Integration)
**Purpose:** The specific JSON structure when GPT-4o calls our Python function.

```json
{
  "event_type": "tool_call",
  "timestamp": "2025-11-27T10:30:02Z",
  "tool_name": "generate_study_quiz",
  "arguments": {
    "topic": "Python Introduction",
    "difficulty": "medium",
    "num_questions": 5
  }
}

## 3. Quiz Result Event (Structured Output)
**Purpose:** The validated Pydantic output returned to the frontend.

```json
{
  "event_type": "quiz_result_generated",
  "timestamp": "2025-11-27T10:30:05Z",
  "success": true,
  "data": {
    "topic": "Python Introduction",
    "difficulty": "medium",
    "questions": [
      {
        "question_text": "What keyword is used to define a function in Python?",
        "options": ["func", "def", "define", "function"],
        "correct_option_index": 1,
        "explanation": "'def' is the keyword for function definition."
      }
    ]
  }
}

## 4. Error Event
**Purpose:** Standard error format when PDF parsing or AI generation fails.

```json
{
  "event_type": "error",
  "error_code": "TOKEN_LIMIT_EXCEEDED",
  "message": "The PDF content is too long for a single quiz generation.",
  "component": "llm_service",
  "user_visible": true
}
