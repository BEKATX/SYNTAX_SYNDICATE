"""
Cognify FastAPI Application
Full Study Suite - Quiz, Summary, and Glossary Generation (Week 10/11)
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import fitz  # PyMuPDF

# Load environment variables first
load_dotenv()

# Ensure logs directory exists BEFORE importing modules that use it
# cost_tracking.py creates a FileHandler on import, so directory must exist
project_root = Path(__file__).parent.parent
src_logs = Path(__file__).parent / "logs"
project_logs = project_root / "logs"
src_logs.mkdir(exist_ok=True)
project_logs.mkdir(exist_ok=True)

# Add paths for imports - try src/ai first (newer version), then fallback to docs/week-9
src_ai_path = Path(__file__).parent / "ai"
week9_base = Path(__file__).parent.parent / "docs" / "week-9"
week9_src = week9_base / "src"

# Try to import from src/ai first (if it exists with providers)
if (src_ai_path / "production_caller.py").exists():
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from ai.production_caller import ProductionFunctionCaller
        print("✅ Using ProductionFunctionCaller from src/ai/")
    except ImportError:
        # Fallback to docs/week-9 version
        sys.path.insert(0, str(week9_src))
        sys.path.insert(0, str(week9_base))
        from ai.production_caller import ProductionFunctionCaller
        print("✅ Using ProductionFunctionCaller from docs/week-9/src/ai/")
else:
    # Use docs/week-9 version
    sys.path.insert(0, str(week9_src))
    sys.path.insert(0, str(week9_base))
    from ai.production_caller import ProductionFunctionCaller
    print("✅ Using ProductionFunctionCaller from docs/week-9/src/ai/")

# Initialize FastAPI app
app = FastAPI(
    title="Cognify API",
    description="AI-Powered Study Assistant - Full Study Suite (Quiz, Summary, Glossary)",
    version="2.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ProductionFunctionCaller (singleton pattern)
_ai_engine: Optional[ProductionFunctionCaller] = None


def get_ai_engine() -> ProductionFunctionCaller:
    """Get or create the AI engine instance."""
    global _ai_engine
    if _ai_engine is None:
        # ProductionFunctionCaller now handles API key validation internally
        # and has fallback to MockProvider if Gemini fails
        try:
            _ai_engine = ProductionFunctionCaller()
        except Exception as e:
            raise ValueError(
                f"Failed to initialize AI engine: {str(e)}. "
                "Please check your GOOGLE_API_KEY in .env file or production environment."
            )
    return _ai_engine


# =====================================================
# Request/Response Models
# =====================================================

class QuizGenerationRequest(BaseModel):
    """Request model for quiz generation."""
    context_text: str = Field(..., description="The text content to generate quiz questions from.")
    topic: str = Field(..., description="The topic or subject of the quiz.")
    difficulty: str = Field(default="medium", description="Difficulty level: easy, medium, or hard")
    num_questions: int = Field(default=5, ge=1, le=15, description="Number of questions to generate (1-15)")


class QuizQuestionResponse(BaseModel):
    """Single quiz question response model."""
    id: int
    question: str
    options: list[str]
    answer: str
    explanation: str


class QuizGenerationResponse(BaseModel):
    """Response model for quiz generation."""
    success: bool
    topic: str
    questions: list[QuizQuestionResponse]
    total: int
    message: Optional[str] = None


class SummaryGenerationRequest(BaseModel):
    """Request model for summary generation."""
    context_text: str = Field(..., description="The text content to summarize.")
    topic: str = Field(..., description="The topic or subject of the content.")


class SummaryGenerationResponse(BaseModel):
    """Response model for summary generation."""
    success: bool
    topic: str
    summary: str
    message: Optional[str] = None


class GlossaryGenerationRequest(BaseModel):
    """Request model for glossary generation."""
    context_text: str = Field(..., description="The text content to extract glossary terms from.")
    topic: str = Field(..., description="The topic or subject of the content.")


class GlossaryTerm(BaseModel):
    """Single glossary term model."""
    term: str
    definition: str


class GlossaryGenerationResponse(BaseModel):
    """Response model for glossary generation."""
    success: bool
    topic: str
    terms: List[GlossaryTerm]
    total: int
    message: Optional[str] = None


class PDFUploadResponse(BaseModel):
    """Response model for PDF upload."""
    success: bool
    extracted_text: str
    page_count: int
    message: Optional[str] = None


# =====================================================
# API Routes
# =====================================================

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Cognify API - AI-Powered Study Assistant (Full Study Suite)",
        "status": "running",
        "version": "2.0.0",
        "features": ["quiz", "summary", "glossary", "pdf_upload"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if AI engine can be initialized
        engine = get_ai_engine()
        return {
            "status": "healthy",
            "ai_engine": "initialized",
            "model": "gemini-flash-latest (with fallback)",
            "features": ["quiz", "summary", "glossary"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/api/generate-quiz", response_model=QuizGenerationResponse)
async def generate_quiz(request: QuizGenerationRequest):
    """
    Generate a quiz from the provided context text.
    
    This endpoint uses the ProductionFunctionCaller (Google Gemini Flash) to generate
    multiple-choice quiz questions based on the provided context.
    """
    try:
        # Get AI engine instance
        engine = get_ai_engine()
        
        # Call the production function caller
        result = engine.generate_quiz(
            context_text=request.context_text,
            topic=request.topic,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate quiz. AI engine returned None."
            )
        
        # Extract quiz data from the response wrapper
        quiz_data = result.data
        
        # Debug: Log the structure we received (remove in production if needed)
        print(f"DEBUG: Received quiz_data type: {type(quiz_data)}")
        if isinstance(quiz_data, (dict, list)):
            print(f"DEBUG: quiz_data preview: {json.dumps(quiz_data, indent=2)[:500]}")
        
        # Transform the data to match our response model
        # Handle different possible response structures from the AI
        questions_data = []
        topic = request.topic
        
        if isinstance(quiz_data, list):
            # AI returned a list of questions directly
            questions_data = quiz_data
        elif isinstance(quiz_data, dict):
            # AI returned a dictionary - check for questions key
            if 'questions' in quiz_data:
                questions_data = quiz_data['questions']
            elif 'question' in quiz_data or 'id' in quiz_data:
                # Single question wrapped in dict, or questions at root level
                # Check if it's a single question or a list structure
                if isinstance(quiz_data.get('questions'), list):
                    questions_data = quiz_data['questions']
                else:
                    # Might be a single question dict, wrap it in a list
                    questions_data = [quiz_data]
            else:
                # Try to find any list-like structure
                for key, value in quiz_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        # Check if it looks like questions
                        if isinstance(value[0], dict) and ('question' in value[0] or 'id' in value[0]):
                            questions_data = value
                            break
                
                # If still no questions found, try to use the dict itself as a single question
                if not questions_data and ('question' in quiz_data or 'id' in quiz_data):
                    questions_data = [quiz_data]
            
            # Extract topic if available
            topic = quiz_data.get('topic', request.topic)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected response format from AI engine: {type(quiz_data)}. Expected dict or list."
            )
        
        # Transform questions to match our response model
        questions = []
        for idx, q in enumerate(questions_data):
            # Handle both dict and object-like structures
            if isinstance(q, dict):
                questions.append(QuizQuestionResponse(
                    id=q.get('id', idx + 1),
                    question=q.get('question', ''),
                    options=q.get('options', []),
                    answer=q.get('answer', ''),
                    explanation=q.get('explanation', '')
                ))
            else:
                # Handle object-like structures
                questions.append(QuizQuestionResponse(
                    id=getattr(q, 'id', idx + 1),
                    question=getattr(q, 'question', ''),
                    options=getattr(q, 'options', []),
                    answer=getattr(q, 'answer', ''),
                    explanation=getattr(q, 'explanation', '')
                ))
        
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No questions found in AI response. The AI may not have generated valid quiz questions."
            )
        
        return QuizGenerationResponse(
            success=True,
            topic=topic,
            questions=questions,
            total=len(questions),
            message="Quiz generated successfully"
        )
            
    except ValueError as e:
        # Handle missing API key or configuration errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating quiz: {str(e)}"
        )


@app.post("/api/generate-summary", response_model=SummaryGenerationResponse)
async def generate_summary(request: SummaryGenerationRequest):
    """
    Generate a summary from the provided context text.
    
    This endpoint uses the ProductionFunctionCaller (Google Gemini Flash) to generate
    a concise summary of the provided content.
    """
    try:
        engine = get_ai_engine()
        
        result = engine.generate_summary(
            context_text=request.context_text,
            topic=request.topic
        )
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate summary. AI engine returned None."
            )
        
        summary_data = result.data
        
        # Extract summary text
        if isinstance(summary_data, dict):
            summary_text = summary_data.get('summary', '')
            topic = summary_data.get('topic', request.topic)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected response format from AI engine: {type(summary_data)}"
            )
        
        if not summary_text:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No summary found in AI response."
            )
        
        return SummaryGenerationResponse(
            success=True,
            topic=topic,
            summary=summary_text,
            message="Summary generated successfully"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating summary: {str(e)}"
        )


@app.post("/api/generate-glossary", response_model=GlossaryGenerationResponse)
async def generate_glossary(request: GlossaryGenerationRequest):
    """
    Generate a glossary from the provided context text.
    
    This endpoint uses the ProductionFunctionCaller (Google Gemini Flash) to extract
    key terms and definitions from the provided content.
    """
    try:
        engine = get_ai_engine()
        
        result = engine.generate_glossary(
            context_text=request.context_text,
            topic=request.topic
        )
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate glossary. AI engine returned None."
            )
        
        glossary_data = result.data
        
        # Extract glossary terms
        if isinstance(glossary_data, dict):
            terms_data = glossary_data.get('terms', [])
            topic = glossary_data.get('topic', request.topic)
        elif isinstance(glossary_data, list):
            terms_data = glossary_data
            topic = request.topic
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected response format from AI engine: {type(glossary_data)}"
            )
        
        # Transform terms to match our response model
        terms = []
        for term_item in terms_data:
            if isinstance(term_item, dict):
                terms.append(GlossaryTerm(
                    term=term_item.get('term', ''),
                    definition=term_item.get('definition', '')
                ))
            else:
                # Handle object-like structures
                terms.append(GlossaryTerm(
                    term=getattr(term_item, 'term', ''),
                    definition=getattr(term_item, 'definition', '')
                ))
        
        if not terms:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No terms found in AI response."
            )
        
        return GlossaryGenerationResponse(
            success=True,
            topic=topic,
            terms=terms,
            total=len(terms),
            message="Glossary generated successfully"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating glossary: {str(e)}"
        )


@app.post("/api/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and extract text from a PDF file.
    
    This endpoint accepts a PDF file, extracts its text content using PyMuPDF,
    and returns the extracted text for use with other endpoints.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a PDF (.pdf)"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Extract text using PyMuPDF
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            extracted_text = ""
            page_count = len(doc)
            
            for page_num in range(page_count):
                page = doc[page_num]
                extracted_text += page.get_text()
                if page_num < page_count - 1:
                    extracted_text += "\n\n"  # Add spacing between pages
            
            doc.close()
            
            if not extracted_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="PDF appears to be empty or contains no extractable text."
                )
            
            return PDFUploadResponse(
                success=True,
                extracted_text=extracted_text,
                page_count=page_count,
                message=f"Successfully extracted text from {page_count} page(s)"
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error extracting text from PDF: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF upload: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    # Use 127.0.0.1 for local development (accessible via localhost)
    # Change to "0.0.0.0" for production to accept connections from all interfaces
    uvicorn.run(app, host="127.0.0.1", port=8000)

