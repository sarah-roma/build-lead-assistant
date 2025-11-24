# from tavily import TavilyClient

# client = TavilyClient("tvly-dev-********************************")
# response = client.extract(
#     urls=[""]
# )
# print(response)

from langchain_community.document_loaders import WebBaseLoader
import logging

def extract_url_content(url: str):
    # Create a loader for web content
    loader = WebBaseLoader(url)
    logging.info(f"Loading content from URL: {url}")
    documents = loader.load()
    logging.info(f"Extracted {documents} documents from URL: {url}")
    return documents

# Should I just be using bs4?