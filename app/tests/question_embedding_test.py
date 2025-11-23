import pytest
from unittest.mock import patch, MagicMock
from utils.retrieval.question_embedding import embed_question


# Test for embed_question
@patch("utils.retrieval.question_embedding.SentenceTransformer")
def test_embed_question_creates_embeddings(mock_model_class):
    """Ensures SentenceTransformer is instantiated and encode() is called."""
    
    # Mock SentenceTransformer instance
    mock_model = MagicMock()
    mock_model_class.return_value = mock_model

    # Mock encode() returning fake vector with .tolist()
    mock_encode_result = MagicMock()
    mock_encode_result.tolist.return_value = [0.1, 0.2, 0.3]
    mock_model.encode.return_value = mock_encode_result
    result = embed_question("test question")

    mock_model_class.assert_called_once_with('sentence-transformers/all-MiniLM-L6-v2')
    mock_model.encode.assert_called_once_with("test question")
    mock_encode_result.tolist.assert_called_once()

    assert result == [0.1, 0.2, 0.3]


@patch("utils.retrieval.question_embedding.SentenceTransformer")
def test_embed_question_handles_empty_string(mock_model_class):
    """Checks behavior when the question is empty."""
    mock_model = MagicMock()
    mock_model_class.return_value = mock_model

    mock_vector = MagicMock()
    mock_vector.tolist.return_value = [0.0]

    mock_model.encode.return_value = mock_vector

    result = embed_question("")

    assert result == [0.0]
    mock_model.encode.assert_called_once_with("")


@patch("utils.retrieval.question_embedding.SentenceTransformer")
def test_embed_question_raises_encode_error(mock_model_class):
    """Ensure exceptions from encode() are propagated."""
    mock_model = MagicMock()
    mock_model_class.return_value = mock_model
    mock_model.encode.side_effect = RuntimeError("Encoding failure")
    with pytest.raises(RuntimeError):
        embed_question("test failure")
