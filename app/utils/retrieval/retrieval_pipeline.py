from retrieval.rewrite_question import rewrite
from retrieval.question_embedding import embed_question
from retrieval.vector_retrieval import retrieve_information
from retrieval.relevance_scoring import score_chunks
from retrieval.response_generator import answer_question

def crag_retrieval_flow(user_question: str, milvus_client: str, collection_name: str):
    rewritten_question = rewrite(user_question)
    question_vector = embed_question(rewritten_question)
    retrieved_information = retrieve_information(question_vector, milvus_client, collection_name)
    relevance_score = score_chunks(retrieved_information, rewritten_question)
    if not relevance_score:
        return {"No relevant information found."}
    response = answer_question(user_question, relevance_score)
    if not response or "No relevant information found." in response:
        return {"response": "I cannot answer that question based on the provided document."}
    return {"response": response}