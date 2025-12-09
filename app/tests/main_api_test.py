import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from main import app

client = TestClient(app)


@pytest.fixture
def mock_milvus_client():
    """Mock Milvus client returned from milvus_setup.get_milvus_client"""
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    return mock_client


# Test create milvus collection
@patch("main.milvus_setup.get_milvus_client")
@patch("main.milvus_setup.create_milvus_collection")
def test_create_collection(mock_create, mock_get_client):
    mock_get_client.return_value = MagicMock()
    mock_create.return_value = {"status": "ok"}

    response = client.post("/Create Collection/?collection_name=test_collection")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Collection 'test_collection' created successfully."
    mock_create.assert_called_once()



# Test mural authenticaiton
@patch("main.AuthenticateMural")
def test_get_mural_token(mock_auth):
    mock_auth().authenticate.return_value = {"access_token": "mock_token"}

    response = client.get("/Authenticate Mural/")
    assert response.status_code == 200
    assert response.json() == "mock_token"


# Test mural widget upload
@patch("main.milvus_setup.get_milvus_client")
@patch("main.get_widget_text")
@patch("main.IngestionPipeline.chunk_text")
@patch("main.IngestionPipeline.embed_chunks")
@patch("main.IngestionPipeline.create_milvus_payload")
def test_upload_mural_widgets(
    mock_payload, mock_embed, mock_chunk, mock_widgets, mock_get_client, mock_milvus_client
):
    mock_get_client.return_value = mock_milvus_client

    # Mural returns two widgets
    mock_widgets.return_value = ["Widget text A", "Widget text B"]

    # Chunking returns one chunk per widget
    mock_chunk.side_effect = lambda txt: [f"chunk_of_{txt}"]

    # Embedding & payload
    mock_embed.return_value = {"mock": "embeddings"}
    mock_payload.return_value = {"payload": "data"}

    response = client.get("/Upload Mural/?collection_name=existing_collection&mural_id=123")

    assert response.status_code == 200
    json = response.json()

    assert "chunks" in json
    assert "embeddings" in json
    assert "message" in json
    assert json["message"] == "Data successfully inserted into existing_collection"


# Test mural widget upload: collection missing
@patch("main.milvus_setup.get_milvus_client")
@patch("main.get_widget_text")
def test_upload_mural_missing_collection(mock_widgets, mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []  # No collections exist
    mock_get_client.return_value = mock_client

    mock_widgets.return_value = ["test"]

    response = client.get("/Upload Mural/?collection_name=missing&mural_id=1")

    assert "error" in response.json()
    assert "does not exist" in response.json()["error"]


# Test file upload
@patch("main.ExtractText.file_parser", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
@patch("main.IngestionPipeline.chunk_text")
@patch("main.IngestionPipeline.embed_chunks")
@patch("main.IngestionPipeline.create_milvus_payload")
def test_file_upload(
    mock_payload, mock_embed, mock_chunk, mock_get_client, mock_file_parser, mock_milvus_client
):
    mock_get_client.return_value = mock_milvus_client

    # Mock file parsing
    mock_file_parser.return_value = {"file1.txt": "Hello world"}

    # Mock chunking
    mock_chunk.return_value = ["chunk1", "chunk2"]

    # Mock embedding + payload
    mock_embed.return_value = {"file1": "embedding"}
    mock_payload.return_value = {"payload": "test"}

    files = {
        "file": ("file1.txt", b"Fake content", "text/plain")
    }

    response = client.post(
        "/File Upload/?collection_name=existing_collection",
        files=files
    )

    assert response.status_code == 200
    body = response.json()
    assert "chunks" in body
    assert "embeddings" in body
    assert body["message"] == "Data successfully inserted into existing_collection"


# Test file upload: missing collection
@patch("main.ExtractText.file_parser", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
def test_file_upload_missing_collection(mock_get_client, mock_file_parser):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []  # No collections
    mock_get_client.return_value = mock_client

    mock_file_parser.return_value = {"file.txt": "content"}

    files = {"file": ("file.txt", b"Hey", "text/plain")}

    response = client.post("/File Upload/?collection_name=missing_collection", files=files)

    assert "error" in response.json()
    assert "does not exist" in response.json()["error"]

# Test URL upload success
@patch("main.extract_url_content", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
@patch("main.IngestionPipeline.chunk_text")
@patch("main.IngestionPipeline.embed_chunks")
@patch("main.IngestionPipeline.create_milvus_payload")
def test_upload_url_success(
    mock_payload,
    mock_embed,
    mock_chunk,
    mock_get_client,
    mock_extract_url,
    mock_milvus_client
):
    mock_get_client.return_value = mock_milvus_client

    # URL extractor returns list of strings (your code expects this)
    mock_extract_url.return_value = ["URL content text"]

    # chunk → embeddings → payload
    mock_chunk.return_value = ["chunk1"]
    mock_embed.return_value = {"url": "embedding"}
    mock_payload.return_value = {"payload": "test"}

    response = client.get(
        "/Upload a URL/?collection_name=existing_collection&url=https://example.com"
    )

    assert response.status_code == 200
    body = response.json()

    assert "message" in body
    assert body["message"] == "Data successfully inserted into existing_collection"
    assert "chunks" in body
    assert "embeddings" in body
    mock_extract_url.assert_awaited()


# Test URL upload with missing url
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_missing_url_param(mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    response = client.get("/Upload a URL/?collection_name=existing_collection")

    # FastAPI validates missing parameters -> 422
    assert response.status_code == 422


# Test URL upload with empty string
@patch("main.extract_url_content", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_empty_string(mock_get_client, mock_extract_url):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    # Extractor returns empty content list
    mock_extract_url.return_value = []

    response = client.get("/Upload a URL/?collection_name=existing_collection&url=")

    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "chunks" in body

# Test URL upload with unreachable URL
@patch("main.extract_url_content", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_unreachable(mock_get_client, mock_extract_url):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    # Simulate failure when fetching URL
    mock_extract_url.side_effect = Exception("URL fetch failed")

    response = client.get("/Upload a URL/?collection_name=existing_collection&url=https://bad-url.com")

    # Should return a 500 because your endpoint catches and rethrows exception
    assert response.status_code == 500
    assert "URL fetch failed" in response.json()["detail"]


# Test URL upload with no usable text
@patch("main.extract_url_content", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_returns_no_text(mock_get_client, mock_extract_url):
    """Test: URL extraction succeeds but returns no usable text."""
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    # URL returns empty list → no content to chunk
    mock_extract_url.return_value = []

    response = client.get("/Upload a URL/?collection_name=existing_collection&url=https://example.com")

    assert response.status_code == 200
    body = response.json()

    assert "chunks" in body
    assert isinstance(body["chunks"], dict)
    assert all(isinstance(v, list) for v in body["chunks"].values())


# Test URL upload with missing collection
@patch("main.extract_url_content", new_callable=AsyncMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_missing_collection(mock_get_client, mock_extract_url):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []
    mock_get_client.return_value = mock_client

    mock_extract_url.return_value = ["content"]

    response = client.get(
        "/Upload a URL/?collection_name=missing_collection&url=https://example.com"
    )

    assert response.status_code == 200
    body = response.json()
    assert "error" in body
    assert "does not exist" in body["error"]


# Test text upload success
@patch("main.milvus_setup.get_milvus_client")
@patch("main.IngestionPipeline.chunk_text")
@patch("main.IngestionPipeline.embed_chunks")
@patch("main.IngestionPipeline.create_milvus_payload")
def test_upload_text_success(
    mock_payload, mock_embed, mock_chunk, mock_get_client, mock_milvus_client
):
    mock_get_client.return_value = mock_milvus_client

    mock_chunk.return_value = ["chunk1"]
    mock_embed.return_value = {"text": "embedding"}
    mock_payload.return_value = {"payload": "test"}

    response = client.get(
        "/Upload Text/?collection_name=existing_collection&information=Hello+World"
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == "Data successfully inserted into existing_collection"
    assert "chunks" in body
    assert "embeddings" in body

# Test text upload with no text
@patch("main.milvus_setup.get_milvus_client")
def test_upload_text_missing_information(mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    # No 'information' query param
    response = client.get("/Upload Text/?collection_name=existing_collection")

    # FastAPI will return 422 for missing required parameters
    assert response.status_code == 422

# Test text upload with empty string
@patch("main.milvus_setup.get_milvus_client")
def test_upload_text_empty_string(mock_get_client):
    """Test: information='' should still process but will chunk empty text."""
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    response = client.get("/Upload Text/?collection_name=existing_collection&information=")

    # Your code does not explicitly block empty text, so it should still succeed.
    # Validate the structure.
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "chunks" in body
    assert "embeddings" in body


# Test text upload with missing collection
@patch("main.milvus_setup.get_milvus_client")
def test_upload_text_missing_collection(mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []
    mock_get_client.return_value = mock_client

    response = client.get(
        "/Upload Text/?collection_name=missing&information=hello"
    )

    assert response.status_code == 200
    assert response.json() == {
        "error": "Collection 'missing' does not exist. Please create it first."
    }

