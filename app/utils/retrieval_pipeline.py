import logging
from utils.retrieval.rewrite_question import rewrite
from utils.retrieval.question_embedding import embed_question
from utils.retrieval.vector_retrieval import retrieve_information
from utils.retrieval.relevance_scoring import score_chunks
from utils.retrieval.response_generator import answer_question

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def crag_retrieval_flow(user_question: str, milvus_client: str, collection_name: str):
    logging.info(f"Starting CRAG retrieval flow for question: {user_question}")
    rewritten_question = rewrite(user_question)
    logging.info(f"Rewritten question: {rewritten_question}")
    question_vector = embed_question(rewritten_question)
    logging.info(f"Generated question vector: {question_vector}")
    retrieved_information = retrieve_information(question_vector, milvus_client, collection_name)
    logging.info(f"Retrieved information: {retrieved_information}")
    relevance_score = score_chunks(retrieved_information, rewritten_question)
    logging.info(f"Relevance score: {relevance_score}")
    if not relevance_score or relevance_score == "No relevant information found.":
        logging.warning("No relevant information found.")
        return {"response": "I cannot answer that question based on the provided document."}
    response = answer_question(user_question, relevance_score)
    if not response or "No relevant information found." in response:
        logging.warning("LLM could not generate a valid response.")
        return {"response": "I cannot answer that question based on the provided document."}
    return {"response": response}