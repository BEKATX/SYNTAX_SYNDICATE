import pytest
from unittest.mock import MagicMock, patch
from src.ai.production_caller import ProductionFunctionCaller

class TestCognifySafety:

    def test_cost_limit_enforcement(self):
        """Ensure execution stops if user is over budget."""
        caller = ProductionFunctionCaller(cost_limit_usd=0.01)
        caller.total_cost = 0.02 # Already over budget
        
        result = caller.execute_quiz_generation("Topic", "Context", [])
        
        assert result["success"] is False
        assert "Cost limit exceeded" in result["error"]

    @patch("src.ai.production_caller.OpenAI")
    def test_circuit_breaker_logic(self, mock_openai):
        """Ensure we don't call LLM if circuit is open."""
        caller = ProductionFunctionCaller()
        caller.circuit_breakers["generate_study_quiz"] = "OPEN"
        
        # Mocking tools schema
        tools = [{"type": "function", "function": {"name": "generate_study_quiz"}}]
        
        # Mock response to simulate a tool call attempt (though code shouldn't reach here)
        mock_msg = MagicMock()
        mock_msg.tool_calls = [MagicMock(function=MagicMock(name="generate_study_quiz", arguments='{}'))]
        caller._call_llm_safe = MagicMock(return_value=mock_msg)

        result = caller.execute_quiz_generation("Topic", "Context", tools)
        
        assert result["success"] is False
        assert "Circuit Breaker is OPEN" in result["error"]

    def test_audit_log_creation(self, tmp_path):
        """Verify logs are written."""
        # Setup temporary logger
        import logging
        log_file = tmp_path / "test_audit.log"
        logging.basicConfig(filename=str(log_file), level=logging.INFO)
        
        caller = ProductionFunctionCaller()
        caller._log_audit("test_tool", {}, "success", 0.0)
        
        assert log_file.exists()
        assert "test_tool" in log_file.read_text()
