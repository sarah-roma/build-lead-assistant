from langchain_ibm import WatsonxLLM
import os

llm = WatsonxLLM(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url=os.environ["WATSONX_URL"],
    api_key=os.environ["WATSONX_APIKEY"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    params={
        "max_new_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.95,
        "stop_sequences": ["<|eot_id|>"]
    }
)

def answer_question(question, context):
    # prompt = f"""
    # <|begin_of_text|><|start_header_id|>system<|end_header_id|>

    # Given the retrieved information, your task is as follows: answer any user query by using only the retrieved information and context only.
        
    # If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.<|eot_id|><|start_header_id|>user<|end_header_id|>

    # {context}<|eot_id|><|start_header_id|>user<|end_header_id|>

    # {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

    # """
    prompt = f"""
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        Given the retrieved information, answer the user's question using ONLY the provided context. 
        If you do not know, say so. Avoid hallucinations.
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Context:
        {context}

        Question:
        {question}
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
        """

#     """
# You are a helpful assistant. Use ONLY the provided context to answer.

# Question:
# {question}

# Context:
# {context}

# Answer the question clearly and concisely.
# """
    return llm.invoke(prompt).strip()
