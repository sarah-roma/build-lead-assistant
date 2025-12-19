from unittest.mock import patch, MagicMock

from utils.ingestion.ingestion_pipeline import IngestionPipeline



# Test chunk_text
@patch("utils.ingestion.ingestion_pipeline.RecursiveCharacterTextSplitter")
def test_chunk_text(mock_splitter):
    # Mock the text splitter instance
    mock_instance = MagicMock()
    mock_instance.split_text.return_value = ["chunk1", "chunk2"]
    mock_splitter.return_value = mock_instance

    result = IngestionPipeline.chunk_text("raw text")

    mock_splitter.assert_called_once_with(chunk_size=500, chunk_overlap=50)
    mock_instance.split_text.assert_called_once_with("raw text")
    assert result == ["chunk1", "chunk2"]


# Test embed_chunks
@patch("utils.ingestion.ingestion_pipeline.SentenceTransformer")
def test_embed_chunks(mock_model_class):
    # Mock embedding model instance
    mock_model = MagicMock()
    # Create fake vector that supports .tolist()
    mock_vector = MagicMock()
    mock_vector.tolist.return_value = [0.1, 0.2, 0.3]
    # encode() should return a list with one embedding object
    mock_model.encode.return_value = [mock_vector]
    mock_model_class.return_value = mock_model
    all_chunks = {"file1": ["text A", "text B"]}
    result = IngestionPipeline.embed_chunks(all_chunks)

    assert "file1" in result
    assert len(result["file1"]) == 2
    assert result["file1"][0] == [0.1, 0.2, 0.3]
    assert result["file1"][1] == [0.1, 0.2, 0.3]

    # encode should be called once per chunk
    assert mock_model.encode.call_count == 2



# Test create_milvus_payload
def test_create_milvus_payload():
    embeddings = {
        "file1": [
            [0.1, 0.2],  
            [0.3, 0.4]
        ]
    }
    chunks = {
        "file1": [
            "chunk 1 text",
            "chunk 2 text"
        ]
    }

    result = IngestionPipeline.create_milvus_payload(embeddings, chunks)

    assert len(result) == 2
    assert result[0]["id"] == 0
    assert result[1]["id"] == 1

    assert result[0]["vector"] == [0.1, 0.2]
    assert result[0]["text"] == "chunk 1 text"
    assert result[0]["filename"] == "file1"

    assert result[1]["vector"] == [0.3, 0.4]
    assert result[1]["text"] == "chunk 2 text"
    assert result[1]["filename"] == "file1"
