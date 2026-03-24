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



# This is really interesting
# I got this error: UploadURL failed: Error: {"detail":"Error fetching URL https://en.wikipedia.org/wiki/Border_Terrier: 403"}
# because its a bare request without a user-agent header so wikipedia rejects it as it thinks its a bot
# old code:


import requests
import logging

# def extract_url_content(url: str):
#     response = requests.get(url)
#     logging.info(f"Fetching URL: {url} - Status Code: {response.status_code}")
#     if response.status_code == 200:
#         logging.info(f"text scraped from {url}: {response.text[:500]}")
#         return response.text
#     else:
#         raise ValueError(f"Error fetching URL {url}: {response.status_code}")

# new code:

from bs4 import BeautifulSoup

def extract_url_content(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    logging.info(f"Fetching URL: {url} - Status Code: {response.status_code}")

    if response.status_code == 200:
        logging.info(f"Text scraped from {url}: {response.text[:500]}")
        return response.text
    else:
        raise ValueError(
            f"Error fetching URL {url}: {response.status_code}"
        )
# This will need cleaning up later to remove HTML tags but its fine for now

# from selenium import webdriver
# from bs4 import BeautifulSoup

# def extract_url_content(url):
#     driver = webdriver.Safari()   # uses system Safari
#     driver.get(url)

#     print("Login in Safari using your passkey...")
#     input("Press ENTER when done...") # this still doesn't work

#     html = driver.page_source
#     return html
