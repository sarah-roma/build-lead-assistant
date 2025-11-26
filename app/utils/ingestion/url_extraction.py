# from tavily import TavilyClient

# client = TavilyClient("tvly-dev-********************************")
# response = client.extract(
#     urls=[""]
# )
# print(response)

# from langchain_community.document_loaders import WebBaseLoader
# import logging

# def extract_url_content(url: str):
#     # Create a loader for web content
#     loader = WebBaseLoader(url)
#     logging.info(f"Loading content from URL: {url}")
#     documents = loader.load()
#     logging.info(f"Extracted {documents} documents from URL: {url}")
#     return documents

# Should I just be using bs4?


# import requests
# import logging

# def extract_url_content(url: str):
#     response = requests.get(url)
#     logging.info(f"Fetching URL: {url} - Status Code: {response.status_code}")
#     if response.status_code == 200:
#         logging.info(f"text scraped from {url}: {response.text[:500]}")
#         return response.text
#     else:
#         raise ValueError(f"Error fetching URL {url}: {response.status_code}")


from selenium import webdriver
from bs4 import BeautifulSoup

def extract_url_content(url):
    driver = webdriver.Safari()   # uses system Safari
    driver.get(url)

    print("Login in Safari using your passkey...")
    input("Press ENTER when done...")

    html = driver.page_source
    return html
