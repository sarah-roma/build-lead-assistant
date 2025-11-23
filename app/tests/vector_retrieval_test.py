import pytest
from unittest.mock import MagicMock, patch

from utils.retrieval.vector_retrieval import retrieve_information

# Test collection missing
def test_retrieve_information_collection_missing():
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["other_collection"]
    result = retrieve_information([0.1, 0.2], mock_client, "missing_collection")
    assert result == "Error: Collection does not exist."
    mock_client.list_collections.assert_called_once()

# Test successful retrieval
def test_retrieve_information_successful_retrieval():
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["my_collection"]
    # Fake Milvus search result structure
    mock_client.search.return_value = [[
        {"entity": {"text": "Document 1"}},
        {"entity": {"text": "Document 2"}},
        {"entity": {"text": "Document 3"}},
    ]]
    result = retrieve_information([0.5, 0.6], mock_client, "my_collection")
    assert result == ["Document 1", "Document 2", "Document 3"]
    # Validate Milvus search call
    mock_client.search.assert_called_once_with(
        collection_name="my_collection",
        data=[[0.5, 0.6]],
        anns_field="vector",
        limit=3,
        search_params={
            "metric_type": "COSINE",
            "params": {"nprobe": 10},
        },
        output_fields=["text"]
    )

# Test bad hits handling
def test_retrieve_information_handles_missing_text_fields():
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["col"]
    mock_client.search.return_value = [[
        {"entity": {"text": "Valid text"}},
        {"entity": {}},                  # Missing "text"
        {},                              # Missing "entity"
        {"entity": {"other": "x"}},      # Wrong field
    ]]
    result = retrieve_information([1, 2, 3], mock_client, "col")
    assert result == ["Valid text"]

# Test empty results
def test_retrieve_information_empty_results():
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["col"]
    mock_client.search.return_value = [[]]  # No hits
    result = retrieve_information([1, 2], mock_client, "col")
    assert result == []

# Test collection missing logging
def test_retrieve_information_logs_error_when_collection_missing(caplog):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []
    with caplog.at_level("ERROR"):
        retrieve_information([0.1], mock_client, "missing")
    assert "Collection 'missing' does not exist" in caplog.text
