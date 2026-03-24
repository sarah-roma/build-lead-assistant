from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

class IngestionPipeline:

    def chunk_text(raw_extracted_text: str):
        logging.info("Starting text chunking...")
        text_chunker = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_chunker.split_text(raw_extracted_text)
        logging.info(f"Completed text chunking into {len(text_chunks)} chunks.")
        return text_chunks

    def embed_chunks(all_file_chunks):
        logging.info("Starting embedding creation for text chunks...")
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = {}
        for key, chunks in all_file_chunks.items():
            embeddings[key] = [embedding_model.encode([chunk])[0].tolist() for chunk in chunks]
            logging.info(f"Created {len(embeddings[key])} embeddings for file '{key}'")
        return embeddings

    def create_milvus_payload(embeddings, all_file_chunks):
        data_payload = []
        record_id = 0  # Unique identifier
        
        for filename, chunks in all_file_chunks.items():
            logging.debug(f"Processing file '{filename}' for Milvus payload...")
            for chunk, embedding in zip(chunks, embeddings[filename]):  # Correctly pair chunks with embeddings
                logging.debug(f"Adding payload record {record_id} for file '{filename}'")
                data_payload.append(
                    {
                        "id": record_id,  # Use a unique integer ID
                        "vector": embedding,  # Embedding vector
                        "text": chunk,  # The actual text chunk
                        "filename": filename  # Store filename as metadata
                    }
                )
                record_id += 1  # Increment unique ID
        logging.debug(f"Final Milvus payload: {data_payload[:2]}... (total {len(data_payload)})")
        return data_payload