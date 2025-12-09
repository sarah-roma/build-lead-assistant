from pymilvus import connections, db, MilvusClient, DataType
import os
import logging


_SENTINEL = object()

class MilvusSetup:
    """Milvus setup and connection management"""
    # def __init__(self, host=None, port=None, uri=None, token=None):
    #     self.host = host or os.environ.get("MILVUS_HOST")
    #     self.port = port or os.environ.get("MILVUS_PORT")
    #     self.uri = uri or os.environ.get("MILVUS_URI")
    #     self.token = token or os.environ.get("MILVUS_TOKEN")

    # Sentinal pattern to distinguish between None and not provided for unit testing
    def __init__(self, host=_SENTINEL, port=_SENTINEL, uri=_SENTINEL, token=_SENTINEL):
        self.host = os.environ.get("MILVUS_HOST") if host is _SENTINEL else host
        self.port = os.environ.get("MILVUS_PORT") if port is _SENTINEL else port
        self.uri  = os.environ.get("MILVUS_URI")  if uri  is _SENTINEL else uri
        self.token = os.environ.get("MILVUS_TOKEN") if token is _SENTINEL else token

    def setup_milvus_db(self):
        try:
            logging.info("Connecting to Milvus server...")
            connections.connect(host=self.host, port=self.port)
        except Exception as e:
            logging.exception("Failed to connect to Milvus server")
            raise Exception(f"Failed to connect to Milvus server: {e}")
        database_name = "build_lead_assistant_db_v1"
        existing_databases = db.list_database()
        if database_name not in existing_databases:
            database = db.create_database(database_name)
            print(f"Database '{database_name}' created.")
            return database
        else:
            print(f"Database '{database_name}' already exists.")

        print(f"Current databases:{db.list_database()}")

    def get_milvus_client(self) -> MilvusClient:
        if self.uri is None:
            raise ValueError("Milvus URI is not set.")
        if self.token is None:
            raise ValueError("Milvus token is not set.")

        client = MilvusClient(uri=self.uri, token=self.token)
        print(f"Client object: {client}")
        return client

    def connect_to_milvus(self):

        logging.info(f"Connecting to Milvus at {self.host}:{self.port}")
        try:
            conn = connections.connect(host=self.host, port=self.port)
            print(f"Connection object: {conn}")
            return conn
        except Exception as e:
            logging.exception("Failed to connect to Milvus server")
            raise Exception(f"Failed to connect to Milvus server: {e}")

    def create_milvus_collection(self, client, collection_name: str):
        # build_lead_knowledge
        schema = client.create_schema(
            auto_id=False,
            enable_dynamic_field=True,
        )
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=384)
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=2000)
        index_params = client.prepare_index_params()
        index_params.add_index(
            field_name="id",
            index_type="STL_SORT"
        )
        index_params.add_index(
            field_name="vector", 
            index_type="AUTOINDEX",
            metric_type="COSINE"
        )
        client.create_collection(
            collection_name=collection_name,
            schema=schema,
            index_params=index_params
        )
        res = client.get_load_state(
            collection_name=collection_name
        )

        return res
