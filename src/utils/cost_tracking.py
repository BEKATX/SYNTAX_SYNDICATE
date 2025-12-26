import logging
import json
import time
from datetime import datetime
from functools import wraps

# Setup specialized logger for costs
cost_logger = logging.getLogger("cost_tracker")
cost_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/cost_audit.jsonl")
handler.setFormatter(logging.Formatter('%(message)s'))
cost_logger.addHandler(handler)

# 2025 Pricing Constants (gpt-4o-mini)
PRICE_INPUT_1M = 0.15
PRICE_OUTPUT_1M = 0.60

def calculate_cost(model, input_tokens, output_tokens):
    """Calculate cost based on OpenAI 2025 pricing."""
    if "mini" in model:
        in_cost = (input_tokens / 1_000_000) * PRICE_INPUT_1M
        out_cost = (output_tokens / 1_000_000) * PRICE_OUTPUT_1M
        return in_cost + out_cost
    # Fallback for standard GPT-4o
    return (input_tokens / 1_000_000) * 2.50 + (output_tokens / 1_000_000) * 10.00

def track_cost(query_type="unknown"):
    """Decorator to track cost and latency of LLM calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = None
            error = None
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise e
            finally:
                latency = time.time() - start
                
                # Extract usage stats if available
                usage = getattr(result, 'usage', None) if result else None
                input_tok = usage.prompt_tokens if usage else 0
                output_tok = usage.completion_tokens if usage else 0
                model = getattr(result, 'model', 'unknown') if result else 'unknown'
                
                cost = calculate_cost(model, input_tok, output_tok)
                
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "query_type": query_type,
                    "model": model,
                    "latency_ms": round(latency * 1000, 2),
                    "input_tokens": input_tok,
                    "output_tokens": output_tok,
                    "cost_usd": round(cost, 6),
                    "status": "error" if error else "success"
                }
                
                # If cached (custom flag we will add in caller), cost is 0
                if hasattr(result, 'cached') and result.cached:
                    log_entry['cost_usd'] = 0.0
                    log_entry['status'] = "cache_hit"

                cost_logger.info(json.dumps(log_entry))
                
        return wrapper
    return decorator
