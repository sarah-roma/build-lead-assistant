import pytest
from unittest.mock import patch, MagicMock

from utils.retrieval_pipeline import crag_retrieval_flow


@pytest.fixture
def mock_flow():
    """Patch all retrieval steps for isolated orchestration testing."""
    with patch("utils.retrieval_pipeline.rewrite") as mock_rewrite, \
         patch("utils.retrieval_pipeline.embed_question") as mock_embed, \
         patch("utils.retrieval_pipeline.retrieve_information") as mock_retrieve, \
         patch("utils.retrieval_pipeline.score_chunks") as mock_score, \
         patch("utils.retrieval_pipeline.answer_question") as mock_answer:

        yield {
            "rewrite": mock_rewrite,
            "embed": mock_embed,
            "retrieve": mock_retrieve,
            "score": mock_score,
            "answer": mock_answer,
        }


def test_full_success_flow(mock_flow):
    """Pipeline returns final LLM answer when all steps succeed."""

    mock_flow["rewrite"].return_value = "rewritten"
    mock_flow["embed"].return_value = [0.1, 0.2, 0.3]
    mock_flow["retrieve"].return_value = ["doc1", "doc2"]
    mock_flow["score"].return_value = "relevant summary"
    mock_flow["answer"].return_value = "final answer"

    result = crag_retrieval_flow("original question", "client", "collection")

    assert result == {"response": "final answer"}
    mock_flow["rewrite"].assert_called_once_with("original question")
    mock_flow["embed"].assert_called_once_with("rewritten")
    mock_flow["retrieve"].assert_called_once()
    mock_flow["score"].assert_called_once_with(["doc1", "doc2"], "rewritten")
    mock_flow["answer"].assert_called_once()


def test_no_relevance_found(mock_flow):
    """If no relevant chunks, pipeline returns fallback message."""

    mock_flow["rewrite"].return_value = "rewritten"
    mock_flow["embed"].return_value = [0.1, 0.2]
    mock_flow["retrieve"].return_value = ["doc1"]
    mock_flow["score"].return_value = "No relevant information found."

    result = crag_retrieval_flow("question", "client", "collection")

    assert result == {"response": "I cannot answer that question based on the provided document."}
    mock_flow["answer"].assert_not_called()


def test_answer_returns_invalid(mock_flow):
    """If LLM fails or returns no answer, pipeline returns fallback."""

    mock_flow["rewrite"].return_value = "rewritten"
    mock_flow["embed"].return_value = [0.1, 0.2]
    mock_flow["retrieve"].return_value = ["doc1"]
    mock_flow["score"].return_value = "summary"
    mock_flow["answer"].return_value = ""

    result = crag_retrieval_flow("question", "client", "collection")

    assert result == {"response": "I cannot answer that question based on the provided document."}


def test_retrieve_returns_empty_list(mock_flow):
    """If retrieval returns empty results, score_chunks likely returns fallback."""

    mock_flow["rewrite"].return_value = "rewritten"
    mock_flow["embed"].return_value = [0.1, 0.2]
    mock_flow["retrieve"].return_value = []
    mock_flow["score"].return_value = "No relevant information found."

    result = crag_retrieval_flow("q", "client", "collection")

    assert result == {"response": "I cannot answer that question based on the provided document."}
    mock_flow["answer"].assert_not_called()


def test_rewrite_exception_bubbles(mock_flow):
    """If rewrite throws an error, pipeline should not swallow it."""

    mock_flow["rewrite"].side_effect = RuntimeError("rewrite failed")

    with pytest.raises(RuntimeError):
        crag_retrieval_flow("q", "client", "collection")


def test_score_none(mock_flow):
    """If score returns None instead of a string, treat it as no relevance."""

    mock_flow["rewrite"].return_value = "rewritten"
    mock_flow["embed"].return_value = [0.1]
    mock_flow["retrieve"].return_value = ["doc"]
    mock_flow["score"].return_value = None

    result = crag_retrieval_flow("q", "client", "collection")

    assert result == {"response": "I cannot answer that question based on the provided document."}
