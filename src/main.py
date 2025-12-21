"""
Cognify FastAPI Application
Main routes for integrating ProductionFunctionCaller (Week 10/11)
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Ensure logs directory exists BEFORE importing modules that use it
# cost_tracking.py creates a FileHandler on import, so directory must exist
project_root = Path(__file__).parent.parent
src_logs = Path(__file__).parent / "logs"
project_logs = project_root / "logs"
src_logs.mkdir(exist_ok=True)
project_logs.mkdir(exist_ok=True)

# Add docs/week-9 paths for imports
# production_caller.py expects to import from src.utils, so we need both paths
week9_base = Path(__file__).parent.parent / "docs" / "week-9"
week9_src = week9_base / "src"
sys.path.insert(0, str(week9_src))  # For: from ai.production_caller import ...
sys.path.insert(0, str(week9_base))  # For: from src.utils.cost_tracking import ... (inside production_caller)

# Import ProductionFunctionCaller from the week-9 AI engine
try:
    from ai.production_caller import ProductionFunctionCaller
except ImportError as e:
    raise ImportError(
        f"Failed to import ProductionFunctionCaller. Ensure docs/week-9/src/ai/production_caller.py exists. Error: {e}"
    )

# Initialize FastAPI app
app = FastAPI(
    title="Cognify API",
    description="AI-Powered Study Assistant - Quiz Generation API",
    version="1.0.0"
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
        # Verify GOOGLE_API_KEY is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables. "
                "Please set it in your .env file or production environment."
            )
        _ai_engine = ProductionFunctionCaller()
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


# =====================================================
# API Routes
# =====================================================

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Cognify API - AI-Powered Study Assistant",
        "status": "running",
        "version": "1.0.0"
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
            "model": "gemini-flash-latest"
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


if __name__ == "__main__":
    import uvicorn
    
    # Use 127.0.0.1 for local development (accessible via localhost)
    # Change to "0.0.0.0" for production to accept connections from all interfaces
    uvicorn.run(app, host="127.0.0.1", port=8000)

