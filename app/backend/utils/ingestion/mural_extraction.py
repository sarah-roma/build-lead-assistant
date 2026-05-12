import json
import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


MURAL_WIDGETS_URL = "https://app.mural.co/api/public/v1/murals/{mural_id}/widgets"

TEXT_FIELDS = ("title", "htmlText", "text", "caption", "name", "description")


def extract_mural_id(url: str) -> str | None:
    """
    Convert a Mural board URL to the API's "{workspace}.{boardId}" format.
    Handles trailing slugs and extra path segments without breaking.
    """
    try:
        parts = [p for p in urlparse(url).path.split("/") if p]
        t_idx = parts.index("t")
        m_idx = parts.index("m", t_idx + 1)
        workspace = parts[t_idx + 1]
        board_id = parts[m_idx + 2]
        return f"{workspace}.{board_id}"
    except (ValueError, IndexError):
        return None


def _parse_html_text(value: str) -> str:
    """Strip HTML tags while preserving line breaks between blocks."""
    soup = BeautifulSoup(value, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def _widget_text(widget: dict) -> str:
    """Concatenate every text-bearing field on a widget into one string."""
    pieces = []
    for field in TEXT_FIELDS:
        value = widget.get(field)
        if not isinstance(value, str) or not value.strip():
            continue
        text = _parse_html_text(value) if "<" in value and ">" in value else value.strip()
        if text:
            pieces.append(text)
    return "\n".join(pieces)


def list_mural_widgets(url: str, auth_token: str) -> list[dict]:
    """Fetch every widget on a Mural board, paging through all results."""
    mural_id = extract_mural_id(url)
    if not mural_id:
        raise ValueError(f"Could not parse Mural board ID from URL: {url}")

    endpoint = MURAL_WIDGETS_URL.format(mural_id=mural_id)
    headers = {"Authorization": f"Bearer {auth_token}"}
    params = {"limit": 1000}
    widgets: list[dict] = []

    while True:
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            raise ValueError(f"MURAL API error {response.status_code}: {response.text}")
        try:
            payload = response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON returned by MURAL API: {e}")

        widgets.extend(payload.get("value") or [])

        next_token = payload.get("next") or payload.get("nextToken")
        if not next_token:
            return widgets
        params = {"limit": 1000, "next": next_token}


def get_widget_text(url: str, auth_token: str) -> list[str]:
    """
    Return text from every widget on the board in top-down, left-to-right
    reading order. The spatial sort keeps a section header adjacent to the
    sticky notes underneath it, so concatenated + chunked text preserves
    that structural relationship.
    """
    widgets = list_mural_widgets(url, auth_token)

    def _sort_key(w: dict):
        y = w.get("y") if isinstance(w.get("y"), (int, float)) else 0
        x = w.get("x") if isinstance(w.get("x"), (int, float)) else 0
        return (y, x)

    widgets.sort(key=_sort_key)

    texts = []
    for widget in widgets:
        text = _widget_text(widget)
        if text:
            texts.append(text)

    if not texts:
        logging.warning("Mural board %s yielded no text content", url)
    return texts