from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional

# --- Quiz Generation Models ---

class QuizRequest(BaseModel):
    topic: str = Field(..., description="The main topic or content summary to generate a quiz from.")
    difficulty: Literal["easy", "medium", "hard"] = Field(default="medium", description="The difficulty level of the quiz.")
    num_questions: int = Field(default=5, ge=1, le=10, description="Number of questions to generate (1-10).")

class QuizOption(BaseModel):
    text: str
    is_correct: bool

class QuizQuestion(BaseModel):
    question_text: str = Field(..., description="The actual question.")
    options: List[str] = Field(..., min_items=4, max_items=4, description="List of 4 possible answers.")
    correct_option_index: int = Field(..., ge=0, le=3, description="Index of the correct option (0-3).")
    explanation: str = Field(..., description="Explanation of why the answer is correct.")

class QuizResult(BaseModel):
    topic: str
    difficulty: str
    questions: List[QuizQuestion]

# --- Key Concept Extraction Models ---

class ConceptRequest(BaseModel):
    text_content: str = Field(..., description="The raw text from the PDF to analyze.")
    max_concepts: int = Field(default=5, description="Maximum number of concepts to extract.")

class ConceptDefinition(BaseModel):
    term: str = Field(..., description="The key term.")
    definition: str = Field(..., description="A concise definition based on the text.")
    category: Optional[str] = Field(None, description="Category (e.g., 'Formula', 'Definition', 'Date').")

class ConceptList(BaseModel):
    source_topic: str = Field(..., description="Inferred topic from the text.")
    concepts: List[ConceptDefinition]
