import pytest
from unittest.mock import patch, MagicMock

from utils.retrieval.rewrite_question import rewrite

def mock_chain(return_value="Rewritten question"):
    """Creates fake LCEL chain with invoke() method"""
    chain = MagicMock()
    chain.invoke.return_value = return_value
    return chain


@patch("utils.retrieval.rewrite_question.WatsonxLLM")
def test_rewrite_calls_llm_and_chain(mock_llm_class):
    """Ensures the LLM is instantiated and the chain pipeline is executed"""
    # Mock LLM instance returned by WatsonxLLM()
    mock_llm = MagicMock()
    mock_llm_class.return_value = mock_llm
    # Mock chain from: prompt | llm | StrOutputParser()
    chain = mock_chain("Rewritten question")
    # Mock piped chain: prompt | llm | StrOutputParser
    with patch("utils.retrieval.rewrite_question.ChatPromptTemplate.from_messages") as mock_prompt, \
         patch("utils.retrieval.rewrite_question.StrOutputParser"):
        # Make the OR operator chain return our fake chain
        mock_prompt.return_value.__or__.return_value.__or__.return_value = chain
        result = rewrite("original question")
    assert result == "Rewritten question"
    chain.invoke.assert_called_once_with({"question": "original question"})


@patch("utils.retrieval.rewrite_question.WatsonxLLM")
def test_rewrite_strips_output(mock_llm_class):
    mock_llm_class.return_value = MagicMock()
    # Mock chain returning padded spaces/newlines
    chain = mock_chain("\n  rewritten with spaces  \n")
    with patch("utils.retrieval.rewrite_question.ChatPromptTemplate.from_messages") as mock_prompt, \
         patch("utils.retrieval.rewrite_question.StrOutputParser"):
        mock_prompt.return_value.__or__.return_value.__or__.return_value = chain
        result = rewrite("hello")
    assert result == "rewritten with spaces"


@patch("utils.retrieval.rewrite_question.WatsonxLLM")
def test_rewrite_returns_question_when_llm_returns_same(mock_llm_class):
    mock_llm_class.return_value = MagicMock()
    chain = mock_chain("same question")
    with patch("utils.retrieval.rewrite_question.ChatPromptTemplate.from_messages") as mock_prompt, \
         patch("utils.retrieval.rewrite_question.StrOutputParser"):
        mock_prompt.return_value.__or__.return_value.__or__.return_value = chain
        result = rewrite("same question")
    assert result == "same question"


@patch("utils.retrieval.rewrite_question.WatsonxLLM")
def test_rewrite_handles_errors(mock_llm_class):
    """Verifies the function raises errors from chain.invoke"""
    mock_llm_class.return_value = MagicMock()
    # Mock chain raising an exception
    chain = MagicMock()
    chain.invoke.side_effect = RuntimeError("LLM failure")
    with patch("utils.retrieval.rewrite_question.ChatPromptTemplate.from_messages") as mock_prompt, \
         patch("utils.retrieval.rewrite_question.StrOutputParser"):
        mock_prompt.return_value.__or__.return_value.__or__.return_value = chain
        with pytest.raises(RuntimeError):
            rewrite("question")
