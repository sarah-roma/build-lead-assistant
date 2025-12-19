from langchain_ibm import WatsonxLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import logging

load_dotenv()


def rewrite(question: str):
    llm = WatsonxLLM(
        model_id="meta-llama/llama-3-3-70b-instruct",
        url=os.environ.get("WATSONX_URL"),
        apikey=os.environ.get("WATSONX_APIKEY"),
        project_id=os.environ.get("WATSONX_PROJECT_ID"),
        params={
        "decoding_method": "greedy",
        "temperature": 0.2,
        "top_p": 1,
        "top_k": 1,
        "min_new_tokens": 5,
        "max_new_tokens": 50,
        "repetition_penalty": 1,
        "stop_sequences": [],
        "return_options": {
            "input_tokens": True,
            "generated_tokens": True,
            "token_logprobs": True,
            "token_ranks": True,
            }
        }
    )
    logging.info("Rewriting question for clarity and completeness")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """
         You are a helpful assistant that rewrites user questions to be clear, specific, and maximally useful for document retrieval.
         If the question is already clear, or if the rewritten question is essentially the same, return it unchanged.
         """),
        ("human", "Original question: {question}\n\nRewrite the question for clarity and completeness.")
    ])
    chain = prompt | llm | StrOutputParser()
    logging.info(f"Original question: {question}")
    rewritten = chain.invoke({"question": question})
    logging.info(f"Rewritten question: {rewritten}")
    return rewritten.strip()