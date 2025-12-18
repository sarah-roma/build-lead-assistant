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

    response = client.post("/Create a Collection/?collection_name=test_collection")
    
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

    response = client.get("/Upload a Mural Board/?collection_name=existing_collection&url=https://app.mural.co/t/x/m/x/123/")

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["title"] == "Mural board ingested"
    assert body["details"]["chunks_created"] == 2


# Test mural widget upload: collection missing
@patch("main.milvus_setup.get_milvus_client")
@patch("main.get_widget_text")
def test_upload_mural_missing_collection(mock_widgets, mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []  # No collections exist
    mock_get_client.return_value = mock_client

    mock_widgets.return_value = ["test"]

    response = client.get("/Upload a Mural Board/?collection_name=missing&url=https://app.mural.co/t/x/m/x/1/")

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
        "/Upload Files/",
        data={"collection_name": "existing_collection"},
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

    response = client.post(
        "/Upload Files/",
        data={"collection_name": "existing_collection"},
        files=files
    )

    assert "error" in response.json()
    assert "does not exist" in response.json()["error"]

@patch("main.extract_url_content", new_callable=MagicMock)
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

    # Extractor returns string (endpoint expects string)
    mock_extract_url.return_value = "URL content text"

    # Chunk → embeddings → payload
    mock_chunk.return_value = ["chunk1"]
    mock_embed.return_value = {"url": "embedding"}
    mock_payload.return_value = {"payload": "test"}

    response = client.post(
        "/Upload a URL/",
        data={
            "collection_name": "existing_collection",
            "url": "https://example.com"
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert "URL" in body["title"]
    assert body["details"]["chunks_created"] == 1



# Test URL upload with missing url
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_missing_url_param(mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    response = client.post(
        "/Upload a URL/",
        data={
            "collection_name": "existing_collection"
        }
    )

    # FastAPI validates missing parameters -> 422
    assert response.status_code == 422


# Test URL upload with empty string
@patch("main.extract_url_content", new_callable=MagicMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_empty_string(mock_get_client, mock_extract_url):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    # Extractor returns empty str
    mock_extract_url.return_value = ""

    response = client.post(
        "/Upload a URL/",
        data={
            "collection_name": "existing_collection",
            "url": "https://example.com"
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert "message" in body


# Test URL upload with unreachable URL
@patch("main.extract_url_content", new_callable=MagicMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_unreachable(mock_get_client, mock_extract_url):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    mock_extract_url.side_effect = Exception("URL fetch failed")

    response = client.post(
        "/Upload a URL/",
        data={
            "collection_name": "existing_collection",
            "url": "https://bad-url.com"
        }
    )

    assert response.status_code == 500
    assert "URL fetch failed" in response.json()["detail"]


# Test URL upload with no usable text
@patch("main.extract_url_content", new_callable=MagicMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_returns_no_text(mock_get_client, mock_extract_url):
    """Test: URL extraction succeeds but returns no usable text."""
    mock_client = MagicMock()
    mock_client.list_collections.return_value = ["existing_collection"]
    mock_get_client.return_value = mock_client

    # URL returns empty list → no content to chunk
    mock_extract_url.return_value = ""

    response = client.post(
        "/Upload a URL/",
        data={
            "collection_name": "existing_collection",
            "url": "https://example.com"
        }
    )

    assert response.status_code == 200
    body = response.json()

    # assert "chunks" in body
    # assert isinstance(body["chunks"], dict)
    # assert all(isinstance(v, list) for v in body["chunks"].values())


# Test URL upload with missing collection
@patch("main.extract_url_content", new_callable=MagicMock)
@patch("main.milvus_setup.get_milvus_client")
def test_upload_url_missing_collection(mock_get_client, mock_extract_url):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []
    mock_get_client.return_value = mock_client

    mock_extract_url.return_value = "content"

    response = client.post(
        "/Upload a URL/",
        data={
            "collection_name": "missing_collection",
            "url": "https://example.com"
        }
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

    assert body["status"] == "success"
    assert body["title"] == "Text ingested"
    assert body["details"]["chunks_created"] == 1


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

    assert body["status"] == "success"
    assert body["details"]["chunks_created"] == 0


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

# # Test upload workshop with no file provided
# @patch("main.milvus_setup.get_milvus_client")
# @patch("main.IngestionPipeline.chunk_text")
# @patch("main.IngestionPipeline.embed_chunks")
# @patch("main.IngestionPipeline.create_milvus_payload")
# def test_upload_workshop_no_file(
#     mock_payload, mock_embed, mock_chunk, mock_get_client, mock_milvus_client
# ):
#     mock_get_client.return_value = mock_milvus_client

#     mock_chunk.return_value = ["chunk1"]
#     mock_embed.return_value = {"chunk1": [0.1, 0.2]}
#     mock_payload.return_value = {"payload": "mock"}

#     response = client.post(
#         "/Upload Workshop Information/?collection_name=existing_collection",
#         data={
#             "workshop_date": "2025-12-11",
#             "mural_url": "https://mural.co/test",
#             "attendee_names": "Alice",
#             "attendee_job_titles": "Designer",
#             "attendee_teams": "UX",
#             "attendee_companies": "Meta",
#         }
#     )

#     assert response.status_code == 200
#     body = response.json()
#     assert "combined_text" in body
#     assert "Alice" in body["combined_text"]
#     assert "chunks" in body
#     assert "embeddings" in body
#     assert body["message"] == "Workshop data successfully inserted into existing_collection"


# # Test upload workshop with file upload
# @patch("main.milvus_setup.get_milvus_client")
# @patch("main.ExtractText.file_parser", new_callable=AsyncMock)
# @patch("main.IngestionPipeline.chunk_text")
# @patch("main.IngestionPipeline.embed_chunks")
# @patch("main.IngestionPipeline.create_milvus_payload")
# def test_upload_workshop_with_file(
#     mock_payload, mock_embed, mock_chunk, mock_file_parser, mock_get_client, mock_milvus_client
# ):
#     mock_get_client.return_value = mock_milvus_client

#     mock_file_parser.return_value = {"testfile.txt": "Some workshop notes"}
#     mock_chunk.return_value = ["chunk1"]
#     mock_embed.return_value = {"chunk1": [0.1, 0.2]}
#     mock_payload.return_value = {"payload": "mock"}

#     response = client.post(
#         "/Upload Workshop Information/?collection_name=existing_collection",
#         data={
#             "workshop_date": "2025-12-11",
#             "attendee_names": "Bob"
#         },
#         files={
#             "workshop_files": ("testfile.txt", b"dummy content", "text/plain")
#         }
#     )

#     assert response.status_code == 200
#     body = response.json()
#     assert "dummy content" in body["combined_text"]
#     assert "Bob" in body["combined_text"]
#     assert body["message"] == "Workshop data successfully inserted into existing_collection"


# Test multiple attendees
@patch("main.milvus_setup.get_milvus_client")
@patch("main.IngestionPipeline.chunk_text")
@patch("main.IngestionPipeline.embed_chunks")
@patch("main.IngestionPipeline.create_milvus_payload")
def test_upload_workshop_multiple_attendees(
    mock_payload, mock_embed, mock_chunk, mock_get_client, mock_milvus_client
):
    mock_get_client.return_value = mock_milvus_client

    mock_chunk.return_value = ["chunk1"]
    mock_embed.return_value = {"chunk1": [0.1, 0.2]}
    mock_payload.return_value = {"payload": "mock"}

    response = client.post(
        "/Upload Workshop Information/?collection_name=existing_collection",
        data={
            "collection_name": "existing_collection",
            "workshop_date": "2025-12-11",
            "attendee_names": ["Alice", "Bob"],
            "attendee_job_titles": ["Designer", "Engineer"],
            "attendee_teams": ["UX", "Platform"],
            "attendee_companies": ["Meta", "IBM"],
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["title"] == "Workshop ingested"
    assert body["details"]["content_type"] == "manual workshop text input"
    assert body["details"]["chunks_created"] > 0



# Test collection missing
@patch("main.milvus_setup.get_milvus_client")
def test_upload_workshop_missing_collection(mock_get_client):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []  # No collection found
    mock_get_client.return_value = mock_client

    response = client.post(
        "/Upload Workshop Information/",
        data={"collection_name": "missing_collection", "workshop_date": "2025-12-11"}
    )

    assert response.status_code == 200
    assert "error" in response.json()
    assert "does not exist" in response.json()["error"]


# Test invalid URL (FastAPI validation)
def test_upload_workshop_invalid_url():
    response = client.post(
        "/Upload Workshop Information/?collection_name=existing_collection",
        data={
            "collection_name": "existing_collection",
            "workshop_date": "2025-12-11",
            "mural_url": "not-a-url"
        }
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"][-1] == "mural_url"
    assert detail[0]["type"] == "url_parsing"


# Test minimal submission (only date + name)
@patch("main.milvus_setup.get_milvus_client")
@patch("main.IngestionPipeline.chunk_text")
@patch("main.IngestionPipeline.embed_chunks")
@patch("main.IngestionPipeline.create_milvus_payload")
def test_upload_workshop_minimal(
    mock_payload, mock_embed, mock_chunk, mock_get_client, mock_milvus_client
):
    mock_get_client.return_value = mock_milvus_client

    mock_chunk.return_value = ["chunk1"]
    mock_embed.return_value = {"chunk1": [0.1, 0.2]}
    mock_payload.return_value = {"payload": "mock"}

    response = client.post(
        "/Upload Workshop Information/?collection_name=existing_collection",
        data={
            "collection_name": "existing_collection",
            "workshop_date": "2025-12-11",
            "attendee_names": "Alice"
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["title"] == "Workshop ingested"
    assert body["details"]["chunks_created"] >= 1