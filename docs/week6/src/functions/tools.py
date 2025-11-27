import random
from typing import List
from ..models.function_models import (
    QuizRequest, QuizResult, QuizQuestion, 
    ConceptRequest, ConceptList, ConceptDefinition
)

def generate_study_quiz(params: QuizRequest) -> QuizResult:
    """
    Generates a multiple-choice quiz based on a study topic.
    Used when a student wants to test their knowledge after reading a PDF.
    """
    # MOCK DATA for Week 6 Demo
    # In production, this would call OpenAI with the specific context
    
    mock_questions = []
    
    for i in range(params.num_questions):
        q = QuizQuestion(
            question_text=f"Test Question {i+1} about {params.topic}",
            options=[
                f"Correct Answer for {params.topic}", 
                "Wrong Answer A", 
                "Wrong Answer B", 
                "Wrong Answer C"
            ],
            correct_option_index=0,
            explanation=f"This is the correct answer because it defines {params.topic} accurately."
        )
        mock_questions.append(q)

    return QuizResult(
        topic=params.topic,
        difficulty=params.difficulty,
        questions=mock_questions
    )

def extract_key_concepts(params: ConceptRequest) -> ConceptList:
    """
    Analyzes text content (from a PDF) and extracts key definitions.
    Used to create flashcards or summaries.
    """
    # MOCK DATA for Week 6 Demo
    
    # Simulate processing text
    inferred_topic = params.text_content[:20] + "..."
    
    concepts = [
        ConceptDefinition(
            term="Artificial Intelligence",
            definition="Simulation of human intelligence by machines.",
            category="Definition"
        ),
        ConceptDefinition(
            term="Neural Networks",
            definition="Computing systems inspired by biological neural networks.",
            category="Algorithm"
        )
    ]
    
    # Limit to requested amount
    return ConceptList(
        source_topic=inferred_topic,
        concepts=concepts[:params.max_concepts]
    )
