from sentence_transformers import SentenceTransformer

def embed_question(question):
    print(f"[DEBUG] Creating embeddings for question: {question}")
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    vector = embedding_model.encode(question).tolist()
    return vector