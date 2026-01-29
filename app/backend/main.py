from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Query, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv
from typing import Optional, List, Annotated
import logging
from enum import Enum
import time
from contextlib import asynccontextmanager

from utils.milvus_setup import MilvusSetup
from utils.ingestion.mural_authentication import AuthenticateMural
from utils.ingestion.mural_extraction import get_widget_text, extract_mural_id
from utils.ingestion.file_extraction import ExtractText
from models.workshop_context import WorkshopIngestionInput, workshop_form_dependency
from utils.ingestion.ingestion_pipeline import IngestionPipeline
from utils.retrieval_pipeline import crag_retrieval_flow
from utils.ingestion.url_extraction import extract_url_content


load_dotenv()


tags_metadata = [
    {
        "name": "info-ingestion",
        "description": "Multiple ways to ingest information into knowledge repositories",
    },
    {
        "name": "info-retrieval",
        "description": "Ask questions and retrieve the information from various knowledge repositories"
    },
]

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

milvus_setup = MilvusSetup()

# functionality for milvus collection dropdown
def create_dynamic_collection_enum():
    client = milvus_setup.get_milvus_client()
    collections = client.list_collections() or ["__no_collections__"]

    # dict of {member_name: member_value}
    namespace = {name: name for name in collections}

    # Correct dynamic Enum creation
    DynamicEnum = Enum(
        "MilvusCollections",
        namespace,
        type=str  # ensures it's a str-backed enum
    )
    return DynamicEnum

MilvusCollections = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global MilvusCollections

    logging.info("Starting application, waiting for Milvus...")

    milvus_setup.connect_with_retry()
    milvus_setup.setup_milvus_db()

    try:
        MilvusCollections = create_dynamic_collection_enum()
    except Exception as e:
        logging.warning(f"Skipping Milvus collection enum init: {e}")
        MilvusCollections = None

    logging.info("Milvus ready")
    yield




app = FastAPI(lifespan=lifespan)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # react dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/View Collections")
# def pick_collection(
#     collection_name: Annotated[MilvusCollections, Query(...)]
# ):
#     return {"selected": str(collection_name)}

@app.get("/List Collections/", tags=["info-ingestion"])
def list_collections():
    client = milvus_setup.get_milvus_client()
    collections = client.list_collections() or []
    return {"collections": collections}


# Create Milvus collection
@app.post("/Create a Collection/", tags=["info-ingestion"])
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


# # Mural authentication
# @app.get("/Authenticate Mural/", tags=["info-ingestion"])
# def get_mural_token():
#     token = getattr(app.state, "mural_token", None)
#     if token:
#         return token

#     # If not stored, auto-authenticate
#     auth = AuthenticateMural()
#     token_data = auth.authenticate()
#     token = token_data.get("access_token")
#     app.state.mural_token = token
#     return token


from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from utils.ingestion.mural_authentication import AuthenticateMural
import logging


@app.get("/oauth/mural/callback", tags=["oauth"])
def mural_oauth_callback(request: Request):
    """
    OAuth redirect endpoint called by Mural after user approves access.
    """

    auth = AuthenticateMural()

    # Exchange code for token
    token_data = auth.fetch_token(str(request.url))

    # Store the FULL token dict (access + refresh + expiry)
    app.state.mural_token = token_data

    # Close the popup window nicely
    return HTMLResponse("""
    <html>
      <body>
        <script>window.close();</script>
        <p>Mural authentication complete. You may close this window.</p>
      </body>
    </html>
    """)


@app.get("/Upload a Mural Board/", tags=["info-ingestion"])
async def upload_mural_board(
    collection_name: str,
    url: str,
):
    auth = AuthenticateMural()

    # Try to get token immediately
    token = getattr(app.state, "mural_token", None)

    # If token missing, give OAuth a short chance to complete
    if not token:
        for _ in range(6):  # ~3 seconds total
            time.sleep(0.5)
            token = getattr(app.state, "mural_token", None)
            if token:
                break

    # Still no token → start OAuth
    if not token:
        authorization_url, state = auth.get_authorization_url()
        app.state.mural_oauth_state = state

        return JSONResponse(
            status_code=401,
            content={
                "error": "Mural authentication required",
                "authorization_url": authorization_url,
            },
        )

    # Ensure token is valid / refreshed
    try:
        token = auth.get_valid_access_token(token)
        app.state.mural_token = token
        access_token = token["access_token"]
    except Exception:
        authorization_url, state = auth.get_authorization_url()
        app.state.mural_oauth_state = state

        return JSONResponse(
            status_code=401,
            content={
                "error": "Mural authentication required",
                "authorization_url": authorization_url,
            },
        )

    try:
        # Call Mural API using valid token
        widget_text = get_widget_text(url, access_token)
        logging.info(f"Extracted text from mural '{url}'")

        chunks = []
        for widget in widget_text:
            chunks.extend(IngestionPipeline.chunk_text(widget))

        mural_id = extract_mural_id(url)
        mural_chunks = {mural_id: chunks}

        embeddings = IngestionPipeline.embed_chunks(mural_chunks)
        payload = IngestionPipeline.create_milvus_payload(
            embeddings, mural_chunks
        )

        client = milvus_setup.get_milvus_client()

        if collection_name not in client.list_collections():
            raise HTTPException(
                status_code=400,
                detail=f"Collection '{collection_name}' does not exist",
            )

        client.insert(collection_name, payload)

        return {
            "status": "success",
            "title": "Mural board ingested",
            "message": f"Mural board saved to '{collection_name}'",
            "details": {
                "chunks_created": len(chunks),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Mural upload failed")
        raise HTTPException(status_code=500, detail=str(e))


# # Uploading files
# @app.post("/Upload Files/", tags=["info-ingestion"])
# async def create_upload_file(
#     collection_name: str,
#     file: Optional[List[UploadFile]] = File(None)
# ):
@app.post("/Upload Files/", tags=["info-ingestion"])
async def create_upload_file(
    collection_name: str = Form(...),
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


@app.post("/Upload a URL/", tags=["info-ingestion"])
async def upload_url(
    collection_name: str = Form(...),
    url: str = Form(...)
):
    try:
        url_text = extract_url_content(url)

        if not isinstance(url_text, str):
            raise ValueError("extract_url_content must return a string")

        chunks = IngestionPipeline.chunk_text(url_text)

        url_chunks = {url: chunks}
        embeddings = IngestionPipeline.embed_chunks(url_chunks)
        payload = IngestionPipeline.create_milvus_payload(embeddings, url_chunks)

        client = milvus_setup.get_milvus_client()

        if collection_name not in client.list_collections():
            return {"error": f"Collection '{collection_name}' does not exist."}

        client.insert(collection_name, payload)

        return {
            "status": "success",
            "title": "URL content ingested",
            "message": (
                f"Information from the URL has been successfully saved to the "
                f"'{collection_name}' collection."
            ),
            "details": {
                "content_type": "url input",
                "chunks_created": len(url_chunks),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/Upload Text/", tags=["info-ingestion"])
async def upload_text(
        collection_name: str,
        information: str
    ):
    try:
        logging.info(f"Information entered into tool: {information}")
        information_chunks = {}
        information_chunks_list = []

        information_chunks_list.extend(IngestionPipeline.chunk_text(information))

        information_chunks[information] = information_chunks_list
        file_embeddings: dict = IngestionPipeline.embed_chunks(information_chunks)  # Create embeddings from the chunks
        payload = IngestionPipeline.create_milvus_payload(file_embeddings, information_chunks)  # Create Milvus payload

        client = milvus_setup.get_milvus_client()  # Get the client object

        if collection_name not in client.list_collections():
            logging.error("Collection doesn't exist") # If the collection doesn't exist
            return {"error": f"Collection '{collection_name}' does not exist. Please create it first."}

        client.insert(collection_name, payload)
        return {
            "status": "success",
            "title": "Text ingested",
            "message": (
                f"Your text has been successfully saved to the "
                f"'{collection_name}' collection."
            ),
            "details": {
                "content_type": "manual text input",
                "chunks_created": len(information_chunks_list),
            }
        }

    except Exception as e:
        logging.exception("Error occurred while uploading url content")
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/Upload Workshop Information/", tags=["info-ingestion"])
# async def upload_workshop_info(
#     collection_name: str,
#     user_input: WorkshopIngestionInput = Depends(workshop_form_dependency),
#     workshop_files: Optional[UploadFile] = File(
#         None,
#         description="Upload any workshop files (PDF, DOCX etc)"
#     )
# ):

@app.post("/Upload Workshop Information/", include_in_schema=False, tags=["info-ingestion"])
async def upload_workshop_info(
    collection_name: str = Form(...),
    user_input: WorkshopIngestionInput = Depends(workshop_form_dependency),
    workshop_files: Optional[UploadFile] = File(None),
):
    try:
        contextual_sections = []

        # 1. Workshop date
        if user_input.workshop_date:
            contextual_sections.append(
                "Prompt: When was the workshop held?\n"
                f"User Answer: {user_input.workshop_date}\n"
            )

        # 2. Attendees
        if user_input.attendees:
            for attendee in user_input.attendees:
                attendee_text = (
                    "Prompt: Who attended the workshop and what were their job title, team, and company?\n"
                    f"User Answer: {attendee.name}, "
                    f"Job Title: {attendee.job_title or 'N/A'}, "
                    f"Team: {attendee.team or 'N/A'}, "
                    f"Company: {attendee.company or 'N/A'}\n"
                )
                contextual_sections.append(attendee_text)

        # 3. Mural URL
        if user_input.mural_url:
            contextual_sections.append(
                "Prompt: Provide any Mural board links used during the workshop.\n"
                f"User Answer: {user_input.mural_url}\n"
            )

        # # 4. File Upload
        # file_text = None
        # if workshop_files:
        #     file_contents = (await workshop_files.read()).decode("utf-8", errors="ignore")
        #     contextual_sections.append(
        #         f"Prompt: Uploaded file '{workshop_files.filename}' contents.\n"
        #         f"User Answer:\n{file_contents}\n"
        #     )

        # Combine
        contextual_text = "\n".join(contextual_sections)

        # Pipeline call
        chunks = IngestionPipeline.chunk_text(contextual_text)
        chunk_map = {contextual_text: chunks}
        embeddings = IngestionPipeline.embed_chunks(chunk_map)
        payload = IngestionPipeline.create_milvus_payload(embeddings, chunk_map)

        # Milvus
        client = milvus_setup.get_milvus_client()

        if collection_name not in client.list_collections():
            return {"error": f"Collection '{collection_name}' does not exist. Please create it first."}

        client.insert(collection_name, payload)

        return {
            "status": "success",
            "title": "Workshop ingested",
            "message": (
                f"Your workshop information has been successfully saved to the "
                f"'{collection_name}' collection."
            ),
            "details": {
                "content_type": "manual workshop text input",
                "chunks_created": len(chunk_map),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/Ask a Question/", tags=["info-retrieval"])
async def ask_your_question(collection_name: str, question: str):
    try:
        milvus_client = milvus_setup.get_milvus_client()
        response = crag_retrieval_flow(question, milvus_client, collection_name)
        answer_text = response.get("response", "No answer available.")
        return {
            "collection": collection_name,
            "question": question,
            "answer": answer_text
        }
    except Exception as e:
        logging.exception("Error occurred while processing the question")
        raise HTTPException(status_code=500, detail=str(e))