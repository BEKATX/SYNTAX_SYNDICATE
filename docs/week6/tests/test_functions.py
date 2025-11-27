import pytest
from pydantic import ValidationError
from src.models.function_models import QuizRequest, ConceptRequest
from src.functions.tools import generate_study_quiz, extract_key_concepts

def test_quiz_generation_valid():
    """Test that quiz generation returns correct structure."""
    req = QuizRequest(topic="Python Basics", difficulty="easy", num_questions=3)
    result = generate_study_quiz(req)
    
    assert result.topic == "Python Basics"
    assert len(result.questions) == 3
    assert result.questions[0].correct_option_index == 0

def test_concept_extraction_valid():
    """Test that concept extraction works."""
    req = ConceptRequest(text_content="AI is cool.", max_concepts=2)
    result = extract_key_concepts(req)
    
    assert len(result.concepts) <= 2
    assert result.concepts[0].term == "Artificial Intelligence"

def test_quiz_validation_error():
    """Test that Pydantic raises error for invalid inputs (questions > 10)."""
    with pytest.raises(ValidationError):
        QuizRequest(topic="Math", num_questions=20) # Limit is 10

def test_concept_validation_error():
    """Test failure on missing required field."""
    with pytest.raises(ValidationError):
        ConceptRequest(max_concepts=5) # text_content is missing
