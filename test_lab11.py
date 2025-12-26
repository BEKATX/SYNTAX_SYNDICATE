import os
import json
from src.ai.production_caller import ProductionFunctionCaller

# Step 1: LIVE AI TEST
print("--- TEST 1: LIVE AI ---")
try:
    engine = ProductionFunctionCaller()
    res1 = engine.generate_quiz("Python is a high-level programming language.", "Python", "easy")
    if res1:
        # Use .get() to avoid KeyError
        topic = res1.data.get('topic', 'Key missing')
        print(f"✅ Success! Topic found: {topic}")
        print(f"Generated {len(res1.data.get('questions', []))} questions.")
    else:
        print("❌ Test 1 failed: No response.")
except Exception as e:
    print(f"❌ Test 1 crashed: {e}")

# Step 2: FALLBACK TEST
print("\n--- TEST 2: FALLBACK CHECK ---")
# Hide the key to force fallback
original_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = "invalid_key_for_testing"

try:
    # Re-init to trigger key check logic
    engine_fallback = ProductionFunctionCaller()
    res2 = engine_fallback.generate_quiz("Math basics.", "Math", "hard")
    if res2:
        print(f"✅ Fallback Success! Topic found: {res2.data.get('topic')}")
    else:
        print("❌ Test 2 failed.")
finally:
    # Restore key
    if original_key: os.environ["GOOGLE_API_KEY"] = original_key