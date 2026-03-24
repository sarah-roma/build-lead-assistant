from sentence_transformers import SentenceTransformer
import logging

def embed_question(question):
    logging.info(f"Creating embeddings for question: {question}")
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    vector = embedding_model.encode(question).tolist()
    logging.info(f"Generated vector: {vector}")
    return vector