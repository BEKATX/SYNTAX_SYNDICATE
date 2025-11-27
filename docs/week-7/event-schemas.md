
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
