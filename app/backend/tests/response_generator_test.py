import pytest
from unittest.mock import patch, MagicMock

from utils.retrieval.response_generator import answer_question

LLM_PATH = "utils.retrieval.response_generator.llm"

# Tests passing of question + context to LLM and output handling
def test_answer_question_calls_llm_with_correct_prompt():
    with patch(LLM_PATH) as mock_llm:
        mock_llm.invoke.return_value = " Final Answer "

        question = "What is AI?"
        context = "AI stands for artificial intelligence."

        result = answer_question(question, context)
        sent_prompt = mock_llm.invoke.call_args[0][0]  # Extract the actual prompt sent

        assert question in sent_prompt
        assert context in sent_prompt
        assert result == "Final Answer"  # must be stripped

# Tests stripping of output
def test_answer_question_strips_output():
    with patch(LLM_PATH) as mock_llm:
        mock_llm.invoke.return_value = "\n   answer with spaces   \n"
        result = answer_question("q?", "ctx")
        assert result == "answer with spaces"

# Tests LLM exception propagation
def test_answer_question_llm_error_propagates():
    with patch(LLM_PATH) as mock_llm:
        mock_llm.invoke.side_effect = RuntimeError("LLM failure")
        with pytest.raises(RuntimeError):
            answer_question("q", "ctx")

# Tests prompt tag formatting
def test_prompt_formatting_contains_template_markers():
    with patch(LLM_PATH) as mock_llm:
        mock_llm.invoke.return_value = "ok"
        answer_question("hello?", "ctx")
        prompt = mock_llm.invoke.call_args[0][0]
        # Check LLM prompt structure markers
        assert "<|begin_of_text|>" in prompt
        assert "<|start_header_id|>system" in prompt
        assert "<|start_header_id|>user" in prompt
        assert "<|start_header_id|>assistant" in prompt
