import pytest
from pymilvus import DataType
from unittest.mock import patch, MagicMock
from utils.milvus_setup import MilvusSetup


#  Test __init__
def test_init_uses_env_vars(monkeypatch):
    monkeypatch.setenv("MILVUS_HOST", "env_host")
    monkeypatch.setenv("MILVUS_PORT", "19530")
    monkeypatch.setenv("MILVUS_URI", "env_uri")
    monkeypatch.setenv("MILVUS_TOKEN", "env_token")

    setup = MilvusSetup()
    assert setup.host == "env_host"
    assert setup.port == "19530"
    assert setup.uri == "env_uri"
    assert setup.token == "env_token"


#  Test get_milvus_client
def test_get_milvus_client_success():
    with patch("utils.milvus_setup.MilvusClient") as MockClient:
        setup = MilvusSetup(uri="mock_uri", token="mock_token")
        client = setup.get_milvus_client()

        MockClient.assert_called_once_with(uri="mock_uri", token="mock_token")
        assert client == MockClient.return_value


def test_get_milvus_client_missing_uri():
    setup = MilvusSetup(uri=None, token="token")
    with pytest.raises(ValueError):
        setup.get_milvus_client()


def test_get_milvus_client_missing_token():
    setup = MilvusSetup(uri="uri", token=None)
    with pytest.raises(ValueError):
        setup.get_milvus_client()


#  Test connect_to_milvus
def test_connect_to_milvus_success():
    with patch("utils.milvus_setup.connections.connect") as mock_connect:
        mock_connect.return_value = "connection_ok"
        setup = MilvusSetup(host="localhost", port="19530")

        conn = setup.connect_to_milvus()

        mock_connect.assert_called_once_with(host="localhost", port="19530")
        assert conn == "connection_ok"


def test_connect_to_milvus_failure():
    with patch("utils.milvus_setup.connections.connect", side_effect=Exception("boom")):
        setup = MilvusSetup(host="localhost", port="19530")

        with pytest.raises(Exception):
            setup.connect_to_milvus()


#  Test setup_milvus_db
def test_setup_milvus_db_creates_new_db():
    with (
        patch("utils.milvus_setup.connections.connect") as mock_conn,
        patch("utils.milvus_setup.db.list_database", return_value=[]),
        patch("utils.milvus_setup.db.create_database") as mock_create,
    ):
        setup = MilvusSetup(host="localhost", port="19530")
        result = setup.setup_milvus_db()
        mock_conn.assert_called_once()
        mock_create.assert_called_once_with("build_lead_assistant_db_v1")
        assert result == mock_create.return_value


def test_setup_milvus_db_existing_db():
    with (
        patch("utils.milvus_setup.connections.connect"),
        patch("utils.milvus_setup.db.list_database", return_value=["build_lead_assistant_db_v1"]),
        patch("utils.milvus_setup.db.create_database") as mock_create,
    ):
        setup = MilvusSetup(host="localhost", port="19530")

        result = setup.setup_milvus_db()

        mock_create.assert_not_called()
        assert result is None  # function prints but returns nothing


#  Test create_milvus_collection
def test_create_milvus_collection():
    mock_client = MagicMock()
    mock_schema = MagicMock()
    mock_client.create_schema.return_value = mock_schema
    mock_index_params = MagicMock()
    mock_client.prepare_index_params.return_value = mock_index_params
    mock_client.get_load_state.return_value = "load_state_ok"
    setup = MilvusSetup()
    res = setup.create_milvus_collection(mock_client, "test_collection")

    # check schema creation
    mock_client.create_schema.assert_called_once()

    # Check fields added to schema
    mock_schema.add_field.assert_any_call(field_name="id", datatype=DataType.INT64, is_primary=True)
    mock_schema.add_field.assert_any_call(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=384)
    mock_schema.add_field.assert_any_call(field_name="text", datatype=DataType.VARCHAR, max_length=2000)

    # check indexes and collection creation
    mock_client.create_collection.assert_called_once()
    assert res == "load_state_ok"
