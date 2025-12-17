import json
import time
import hashlib
import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
# Import the new tracker
from src.utils.cost_tracking import track_cost

class ProductionFunctionCaller:
    """
    COGNIFY AI Caller with Caching & Cost Tracking.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Simple In-Memory Cache (Dictionary)
        # In production, swap this for Redis
        self._cache = {} 

    def _generate_cache_key(self, text: str, topic: str, difficulty: str) -> str:
        """Create a unique hash for the request."""
        raw = f"{text[:100]}-{len(text)}-{topic}-{difficulty}"
        return hashlib.md5(raw.encode()).hexdigest()

    @track_cost(query_type="generate_quiz")
    def generate_quiz(self, context_text: str, topic: str, difficulty: str):
        """
        Generates a quiz. Checks cache first.
        """
        # 1. Check Cache
        cache_key = self._generate_cache_key(context_text, topic, difficulty)
        if cache_key in self._cache:
            # Return cached response structure
            print("⚡ CACHE HIT! Serving instant quiz.")
            
            # Create a mock object to satisfy the decorator's expectation of 'usage'
            class CachedResult:
                cached = True
                model = "gpt-4o-mini-cache"
                usage = None # No tokens used
                content = None # Placeholder
            
            result_obj = CachedResult()
            result_obj.content = self._cache[cache_key]
            return result_obj

        # 2. API Call (Cache Miss)
        print("🐢 CACHE MISS. Calling OpenAI...")
        
        # Optimize Context (Strip excessive whitespace)
        optimized_context = " ".join(context_text.split())
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Generate a JSON quiz based on the context."},
                {"role": "user", "content": f"Context: {optimized_context}\nTopic: {topic}\nDifficulty: {difficulty}"}
            ],
            response_format={"type": "json_object"}
        )
        
        # 3. Save to Cache
        content = response.choices[0].message.content
        self._cache[cache_key] = content
        
        return response

# --- Simulation for Homework Submission ---
if __name__ == "__main__":
    caller = ProductionFunctionCaller()
    
    pdf_text = "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability."
    
    print("\n--- Request 1 (Fresh) ---")
    res1 = caller.generate_quiz(pdf_text, "Python Intro", "easy")
    
    print("\n--- Request 2 (Cached) ---")
    res2 = caller.generate_quiz(pdf_text, "Python Intro", "easy")
