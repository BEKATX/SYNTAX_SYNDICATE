"""
Quick test script to verify backend is working properly
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from ai.production_caller import ProductionFunctionCaller

def test_quiz_generation():
    print("\n" + "="*60)
    print("TESTING QUIZ GENERATION")
    print("="*60)

    engine = ProductionFunctionCaller()

    test_text = """
    Python is a high-level, interpreted programming language created by Guido van Rossum.
    It was first released in 1991. Python emphasizes code readability with its notable use
    of significant indentation. It supports multiple programming paradigms including
    procedural, object-oriented, and functional programming.
    """

    result = engine.generate_quiz(
        context_text=test_text,
        topic="Python Programming",
        difficulty="medium",
        num_questions=3
    )

    if result:
        print("\n[SUCCESS] Quiz generation completed")
        print(f"Data type: {type(result.data)}")
        print(f"Data keys: {result.data.keys() if isinstance(result.data, dict) else 'N/A'}")
        if isinstance(result.data, dict) and 'questions' in result.data:
            print(f"Number of questions: {len(result.data['questions'])}")
            print(f"First question: {result.data['questions'][0].get('question', 'N/A')}")
        else:
            print("[WARNING] No 'questions' key found in data!")
            print(f"Full data: {result.data}")
    else:
        print("\n[FAILED] Quiz generation returned None")

    return result

def test_summary_generation():
    print("\n" + "="*60)
    print("TESTING SUMMARY GENERATION")
    print("="*60)

    engine = ProductionFunctionCaller()

    test_text = """
    Python is a high-level, interpreted programming language created by Guido van Rossum.
    It was first released in 1991. Python emphasizes code readability.
    """

    result = engine.generate_summary(
        context_text=test_text,
        topic="Python Programming"
    )

    if result:
        print("\n[SUCCESS] Summary generation completed")
        print(f"Summary: {result.data.get('summary', 'N/A')[:100]}...")
    else:
        print("\n[FAILED] Summary generation returned None")

    return result

def test_glossary_generation():
    print("\n" + "="*60)
    print("TESTING GLOSSARY GENERATION")
    print("="*60)

    engine = ProductionFunctionCaller()

    test_text = """
    Python is a high-level, interpreted programming language.
    Variables in Python are dynamically typed. Functions are first-class objects.
    """

    result = engine.generate_glossary(
        context_text=test_text,
        topic="Python Programming"
    )

    if result:
        print("\n[SUCCESS] Glossary generation completed")
        print(f"Number of terms: {len(result.data.get('terms', []))}")
    else:
        print("\n[FAILED] Glossary generation returned None")

    return result

if __name__ == "__main__":
    print("\nCOGNIFY BACKEND TEST SUITE")
    print("="*60)

    # Test all three functions
    quiz_result = test_quiz_generation()
    summary_result = test_summary_generation()
    glossary_result = test_glossary_generation()

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Quiz:     {'PASS' if quiz_result else 'FAIL'}")
    print(f"Summary:  {'PASS' if summary_result else 'FAIL'}")
    print(f"Glossary: {'PASS' if glossary_result else 'FAIL'}")
    print("="*60)
