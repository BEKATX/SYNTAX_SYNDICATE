"""
Cognify – Pydantic Data Models
Last updated: 2025-11-07

This module defines structured output models that align with the core Cognify functions:
- generate_summary
- generate_quiz
- extract_glossary

These models ensure consistent, validated outputs and are designed for later integration with
LLM function-calling workflows and backend FastAPI endpoints.
"""

from pydantic import BaseModel, Field, constr, conint
from typing import List, Literal, Optional
from datetime import datetime


# =====================================================
# 1️⃣ Summary Generation Models
# =====================================================

class SourceReference(BaseModel):
    """Metadata reference for a summarized document section."""
    file: str = Field(..., description="File name or source document ID.")
    page_range: str = Field(..., description="Page numbers or span in the original file.")


class SummaryResult(BaseModel):
    """Model for the generate_summary function output."""
    document_id: str = Field(..., description="Unique identifier of the summarized document.")
    summary: constr(min_length=50, max_length=5000) = Field(
        ..., description="Generated summary text.")
    word_count: conint(ge=50, le=1000) = Field(..., description="Word count of the summary.")
    style_used: Literal["concise", "academic", "study-notes"] = Field(
        "concise", description="Summary style applied.")
    sources: List[SourceReference] = Field(
        default_factory=list, description="List of referenced file sources.")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of creation.")


# =====================================================
# 2️⃣ Quiz Generation Models
# =====================================================

class QuizQuestion(BaseModel):
    """Single quiz question with options and correct answer."""
    id: int = Field(..., ge=1, description="Question ID number.")
    question: str = Field(..., description="Question text.")
    options: List[str] = Field(..., min_items=2, max_items=5, description="List of answer options.")
    answer: str = Field(..., description="Correct answer (letter or text).")
    difficulty: Literal["easy", "medium", "hard"] = Field("medium", description="Difficulty level.")


class QuizResult(BaseModel):
    """Model for the generate_quiz function output."""
    topic: str = Field(..., description="Topic or title of the quiz.")
    questions: List[QuizQuestion] = Field(..., description="List of generated quiz questions.")
    total: conint(ge=1, le=20) = Field(..., description="Total number of quiz questions.")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of creation.")


# =====================================================
# 3️⃣ Glossary Extraction Models
# =====================================================

class GlossaryEntry(BaseModel):
    """Single glossary term and its concise definition."""
    term: str = Field(..., description="Key term or concept.")
    definition: constr(min_length=5, max_length=200) = Field(
        ..., description="Short definition of the term (≤ 20 words).")


class GlossaryResult(BaseModel):
    """Model for the extract_glossary function output."""
    glossary: List[GlossaryEntry] = Field(..., description="List of glossary entries.")
    total: conint(ge=1, le=30) = Field(..., description="Total number of terms extracted.")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of creation.")


# =====================================================
# 4️⃣ Error & Logging Models (shared utility)
# =====================================================

class ErrorResponse(BaseModel):
    """Standardized error response model."""
    error_code: str = Field(..., description="Unique error code identifier.")
    error_message: str = Field(..., description="Human-readable message describing the error.")
    details: Optional[dict] = Field(None, description="Additional structured details if available.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error occurrence time.")


class ProcessingLog(BaseModel):
    """Metadata log entry for evaluation, debugging, or analytics."""
    document_id: Optional[str] = Field(None, description="Associated document ID, if relevant.")
    function_name: Literal["generate_summary", "generate_quiz", "extract_glossary"] = Field(
        ..., description="Function that produced this log entry.")
    tokens_in: int = Field(0, description="Number of input tokens used.")
    tokens_out: int = Field(0, description="Number of output tokens used.")
    latency_ms: int = Field(0, description="Processing time in milliseconds.")
    cost_usd: float = Field(0.0, description="Estimated processing cost in USD.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Time of log record.")


# =====================================================
# 5️⃣ Example Usage (for AI-assisted development tools)
# =====================================================

if __name__ == "__main__":
    # Example 1: Summary object
    example_summary = SummaryResult(
        document_id="doc_123",
        summary="This document introduces the concept of RAG and explains how embeddings connect context with LLM reasoning.",
        word_count=72,
        style_used="concise",
        sources=[SourceReference(file="Lecture-04.pdf", page_range="2–8")]
    )
    print(example_summary.model_dump_json(indent=2))

    # Example 2: Quiz result
    example_quiz = QuizResult(
        topic="RAG Architecture",
        questions=[
            QuizQuestion(
                id=1,
                question="What does Retrieval-Augmented Generation primarily solve?",
                options=["A) Hallucination", "B) Latency", "C) Token cost", "D) Audio noise"],
                answer="A",
                difficulty="medium"
            )
        ],
        total=1
    )
    print(example_quiz.model_dump_json(indent=2))

    # Example 3: Glossary
    example_glossary = GlossaryResult(
        glossary=[
            GlossaryEntry(term="Embedding", definition="Vector representation of text meaning."),
            GlossaryEntry(term="FAISS", definition="Library for efficient similarity search.")
        ],
        total=2
    )
    print(example_glossary.model_dump_json(indent=2))
