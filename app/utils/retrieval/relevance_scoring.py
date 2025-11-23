import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

load_dotenv()

# Initialise once
llm = WatsonxLLM(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url=os.environ["WATSONX_URL"],
    apikey=os.environ["WATSONX_APIKEY"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    params={
        "decoding_method": "greedy",
        "temperature": 0.0,
        "max_new_tokens": 3,
    }
)


def is_relevant(document: str, question: str) -> str:
    """
    Returns "yes" or "no" depending on whether the document is relevant.
    No chains, no complexity.
    """

    prompt = (
        "Answer only 'yes' or 'no'.\n\n"
        f"Question: {question}\n\n"
        f"Document:\n{document}\n\n"
        "Is this document relevant?"
    )

    response = llm.invoke(prompt)

    answer = response.strip().lower()

    if "yes" in answer:
        return "yes"
    return "no"


def score_chunks(retrieved_texts, rewritten_question):
    relevant_chunks = []

    for chunk in retrieved_texts:
        score = is_relevant(chunk, rewritten_question)
        print(f"[DEBUG] Relevance check -> {score}")
        
        if score == "yes":
            relevant_chunks.append(chunk)

    if not relevant_chunks:
        return "No relevant information found."

    return " ".join(relevant_chunks)