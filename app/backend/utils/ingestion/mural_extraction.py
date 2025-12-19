import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse


MURAL_URL = "https://app.mural.co/api/public/v1/murals/{mural_id}/widgets"


def extract_mural_id(url: str) -> str | None:
    try:
        path_parts = [p for p in urlparse(url).path.split("/") if p]
        # Expected: ["t", "<team>", "m", "<team>", "<boardId>", ...]
        team = path_parts[1]
        board_id = path_parts[4]

        return f"{team}.{board_id}"
    except Exception:
        return None


def list_mural_widgets(url: str, auth_token: str):
    """ List widgets in a Mural board"""
    mural_id = extract_mural_id(url)
    auth_url = MURAL_URL.format(mural_id=mural_id)
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.request("GET", auth_url, headers=headers, data={})

    # Check error BEFORE parsing JSON
    if response.status_code != 200:
        raise ValueError(f"MURAL API error {response.status_code}: {response.text}")

    try:
        response_json = json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by MURAL API: {e}")

    return response_json



def get_widget_text(url: str, auth_token: str):
    """ Extract text from Mural widgets """
    response_json = list_mural_widgets(url, auth_token)
    all_extracted_text = []
    
    if response_json and 'value' in response_json:
        for sticky_note in response_json['value']:
            html_text = sticky_note.get('htmlText', '') # Extract the html text
            
            if html_text: # Use BeautifulSoup to parse the HTML and extract the text
                soup = BeautifulSoup(html_text, 'html.parser')
                extracted_text = soup.get_text()
                all_extracted_text.append(extracted_text)
                print(extracted_text)
            else:
                print("No htmlText found for this sticky note.")
    else:
        print("No sticky notes found or invalid response.")
    return all_extracted_text