from unittest.mock import MagicMock, patch
from utils.retrieval.relevance_scoring import is_relevant, score_chunks


# Tests the yes response
def test_is_relevant_yes_response():
    with patch("utils.retrieval.relevance_scoring.llm") as mock_llm:
        mock_llm.invoke.return_value = "YES\n"
        result = is_relevant("doc text", "question?")
        assert result == "yes"
        mock_llm.invoke.assert_called_once()

# Tests the no response
def test_is_relevant_no_response():
    with patch("utils.retrieval.relevance_scoring.llm") as mock_llm:
        mock_llm.invoke.return_value = "No."
        result = is_relevant("doc text", "question?")
        assert result == "no"

# Tests variations in response format
def test_is_relevant_handles_whitespace_and_caps():
    with patch("utils.retrieval.relevance_scoring.llm") as mock_llm:
        mock_llm.invoke.return_value = " \n  YeS   "
        result = is_relevant("doc text", "question?")
        assert result == "yes"

def test_is_relevant_only_yes_matching():
    with patch("utils.retrieval.relevance_scoring.llm") as mock_llm:
        mock_llm.invoke.return_value = "yesterday"
        result = is_relevant("doc text", "question?")
        assert result == "no"

# Tests relevant chunk scoring
def test_score_chunks_returns_only_relevant():
    with patch("utils.retrieval.relevance_scoring.is_relevant") as mock_rel:
        mock_rel.side_effect = ["yes", "no", "yes"]
        retrieved = ["A", "B", "C"]
        question = "some question"
        result = score_chunks(retrieved, question)
        assert result == "A C"
        assert mock_rel.call_count == 3

# Test no relevant chunks found
def test_score_chunks_no_relevant_information():
    with patch("utils.retrieval.relevance_scoring.is_relevant") as mock_rel:
        mock_rel.return_value = "no"
        result = score_chunks(["chunk1", "chunk2"], "question")
        assert result == "No relevant information found."
        assert mock_rel.call_count == 2

# Tests empty list of chunks
def test_score_chunks_empty_input_list():
    result = score_chunks([], "question")
    assert result == "No relevant information found."

# Tests chunk order
def test_score_chunks_preserves_chunk_order():
    with patch("utils.retrieval.relevance_scoring.is_relevant") as mock_rel:
        mock_rel.side_effect = ["yes", "yes", "no"]
        chunks = ["first", "second", "third"]
        result = score_chunks(chunks, "question")
        assert result == "first second"
