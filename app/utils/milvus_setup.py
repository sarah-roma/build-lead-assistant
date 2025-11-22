from pymilvus import connections, db, MilvusClient, DataType
import os


class MilvusSetup:
    """Milvus setup and connection management"""
    def __init__(
        self,
        host: str = os.environ.get("MILVUS_HOST"),
        port: str = os.environ.get("MILVUS_PORT"),
        uri: str = os.environ.get("MILVUS_URI"),
        token: str = os.environ.get("MILVUS_TOKEN")
    ):
        self.host = host
        self.port = port
        self.uri = uri
        self.token = token

    def setup_milvus_db(self):
        host = self.host
        port = self.port
        print(host, port)

        try:
            connections.connect(host=host, port=port)
        except Exception as e:
            raise Exception(f"Failed to connect to Milvus server: {e}")
        database_name = "prototype_db"
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
        host = self.host
        port = self.port
        print(f"Connecting to Milvus at {host}:{port}")

        try:
            conn = connections.connect(host=host, port=port)
            print(f"Connection object: {conn}")
            return conn
        except Exception as e:
            raise Exception(f"Failed to connect to Milvus server: {e}")

    def create_milvus_collection(self, client, collection_name: str):
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
