from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from dotenv import load_dotenv
from typing import Optional, List
import logging

from utils.milvus_setup import MilvusSetup
from utils.ingestion.mural_authentication import AuthenticateMural
from utils.ingestion.mural_extraction import get_widget_text
from utils.ingestion.file_extraction import ExtractText
from utils.ingestion.ingestion_pipeline import IngestionPipeline


load_dotenv()
app = FastAPI()

milvus_setup = MilvusSetup()
milvus_setup.connect_to_milvus()
milvus_setup.setup_milvus_db()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)


# Create Milvus collection
@app.post("/Create Collection/")
async def create_collection(collection_name: str):
    """ Endpoint to create a Milvus collection """
    try:
        # Get the Milvus client
        logging.debug("Getting Milvus client...")
        client = milvus_setup.get_milvus_client()
        # Create the collection
        logging.debug(f"Creating Milvus collection: {collection_name}")
        load_state = milvus_setup.create_milvus_collection(client, collection_name)
        logging.info(f"Milvus collection '{collection_name}' created successfully.")
        return {"message": f"Collection '{collection_name}' created successfully.", "load_state": load_state}
    except Exception as e:
        logging.exception("Error occurred while creating Milvus collection")
        raise HTTPException(status_code=500, detail=str(e))


# Mural authentication
@app.get("/Authenticate Mural/")
def get_mural_token():
    token = getattr(app.state, "mural_token", None)
    if token:
        return token

    # If not stored, auto-authenticate
    auth = AuthenticateMural()
    token_data = auth.authenticate()
    token = token_data.get("access_token")
    app.state.mural_token = token
    return token


# Uploading Mural widgets
@app.get("/Upload Mural/")
async def get_widgets(
    collection_name: str,
    mural_id: str, 
    auth_token: str = Depends(get_mural_token)
):
    """ Endpoint to get widgets from a Mural board and process their text content """
    try:
        widget_text = get_widget_text(mural_id, auth_token)  # Extracts the text from the widgets
        logging.info(f"Extracted text from mural '{mural_id}': {widget_text}")
        mural_chunks = {}
        chunks_list = []

        for widget in widget_text:
            text = widget  # widget is a string
            chunks_list.extend(IngestionPipeline.chunk_text(text))

        mural_chunks[mural_id] = chunks_list
        file_embeddings: dict = IngestionPipeline.embed_chunks(mural_chunks)  # Create embeddings from the chunks
        payload = IngestionPipeline.create_milvus_payload(file_embeddings, mural_chunks)  # Create Milvus payload

        client = milvus_setup.get_milvus_client()  # Get the client object

        if collection_name not in client.list_collections():
            logging.error("Collection doesn't exist") # If the collection doesn't exist
            return {"error": f"Collection '{collection_name}' does not exist. Please create it first."}

        client.insert(collection_name, payload)
        return {
                    "message": f"Data successfully inserted into {collection_name}",
                    "chunks": mural_chunks,
                    "embeddings": file_embeddings
                }
    except Exception as e:
        logging.exception("Error occurred while uploading mural widgets")
        raise HTTPException(status_code=500, detail=str(e))


# Uploading files
@app.post("/File Upload/")
async def create_upload_file(
    collection_name: str,
    file: Optional[List[UploadFile]] = File(None)
):
    """ Endpoint to upload files and process their text content """
    try:
        extracted_text: dict = await ExtractText.file_parser(file)

        all_file_chunks = {}
        for key, value in extracted_text.items():
            if isinstance(value, str):
                all_file_chunks[key] = IngestionPipeline.chunk_text(value)

            elif isinstance(value, dict) and "error" in value:
                print(f"Skipping {key}: {value['error']}")
                continue

            else:
                raise ValueError(f"Unexpected extracted value type: {type(value)} for {key}")

        file_embeddings: dict = IngestionPipeline.embed_chunks(all_file_chunks)
        payload = IngestionPipeline.create_milvus_payload(file_embeddings, all_file_chunks)

        client = milvus_setup.get_milvus_client()

        if collection_name not in client.list_collections():
            return {"error": f"Collection '{collection_name}' does not exist."}

        client.insert(collection_name, payload)

        return {
            "message": f"Data successfully inserted into {collection_name}",
            "chunks": all_file_chunks,
            "embeddings": file_embeddings
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
