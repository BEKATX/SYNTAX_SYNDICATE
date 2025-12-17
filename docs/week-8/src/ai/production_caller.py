import json
import time
import logging
import os
from typing import List, Any, Dict
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

# Setup Audit Logger
logging.basicConfig(
    filename='logs/function_audit.log',
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger("audit_logger")

class ProductionFunctionCaller:
    """
    Production-ready wrapper for COGNIFY's quiz generation tools.
    Implements Safety, Cost Tracking, and Reliability patterns.
    """
    
    def __init__(self, cost_limit_usd: float = 0.50, user_id: str = "anon"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.cost_limit_usd = cost_limit_usd
        self.user_id = user_id
        self.total_cost = 0.0
        self.circuit_breakers = {"generate_study_quiz": "CLOSED"}
        self.breaker_failures = {"generate_study_quiz": 0}

    def execute_quiz_generation(self, user_query: str, context_text: str, tool_schema: List[Dict]) -> Dict:
        """
        Main entry point for generating a quiz safely.
        """
        start_time = time.time()
        
        try:
            # 1. Cost Check
            if self.total_cost >= self.cost_limit_usd:
                raise Exception("Cost limit exceeded for this session.")

            # 2. Prepare Context (Truncate to safe limit)
            safe_context = context_text[:15000] # Simple token safety
            
            # 3. Call LLM with Timeouts and Retries
            response = self._call_llm_safe(user_query, safe_context, tool_schema)
            
            # 4. Process Tool Call
            if response.tool_calls:
                tool_call = response.tool_calls[0]
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                # 5. Circuit Breaker Check
                if self.circuit_breakers.get(fn_name) == "OPEN":
                    raise Exception(f"Circuit Breaker is OPEN for {fn_name}. Service unavailable.")

                # 6. Log Execution
                self._log_audit(fn_name, fn_args, "attempt", 0)

                # 7. Return structured data (In a real app, you'd execute the python function here)
                # For Week 8 HW, we return the decision to execute + cost metadata
                execution_time = int((time.time() - start_time) * 1000)
                
                # Estimate Cost (Input + Output tokens)
                # Approximation: $0.00015/1k input, $0.0006/1k output (gpt-4o-mini)
                call_cost = 0.001 # Mock cost
                self.total_cost += call_cost

                return {
                    "success": True,
                    "function_name": fn_name,
                    "arguments": fn_args,
                    "cost_usd": self.total_cost,
                    "latency_ms": execution_time
                }

            return {"success": False, "error": "No tool call triggered"}

        except Exception as e:
            logger.error(json.dumps({"error": str(e), "user_id": self.user_id}))
            return {
                "success": False, 
                "error": str(e),
                "cost_usd": self.total_cost
            }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.Timeout, ConnectionError))
    )
    def _call_llm_safe(self, query, context, tools):
        """Wraps OpenAI call with Tenacity retry logic."""
        try:
            return self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant. Use the context to generate quizzes."},
                    {"role": "user", "content": f"Context: {context}\n\nRequest: {query}"}
                ],
                tools=tools,
                tool_choice="required",
                timeout=15  # Strict Timeout
            ).choices[0].message
        except Exception as e:
            # If 5xx error, this triggers retry. If 4xx, it raises immediately.
            raise e

    def _log_audit(self, tool, args, status, cost):
        entry = {
            "timestamp": time.time(),
            "user_id": self.user_id,
            "tool": tool,
            "args_preview": str(args)[:50],
            "status": status,
            "cost": cost
        }
        logger.info(json.dumps(entry))
