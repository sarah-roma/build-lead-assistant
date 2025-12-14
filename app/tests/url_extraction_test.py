import pytest
from unittest.mock import patch, MagicMock
import requests
from utils.ingestion.url_extraction import extract_url_content


# Test successful URL extraction
@patch("utils.ingestion.url_extraction.requests.get")
def test_extract_url_content_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Hello world"
    mock_get.return_value = mock_response

    result = extract_url_content("https://example.com")

    assert result == "Hello world"
    mock_get.assert_called_once_with('https://example.com', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}, timeout=15)


# Test URL extraction with non-200 status code
@patch("utils.ingestion.url_extraction.requests.get")
def test_extract_url_content_non_200(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    with pytest.raises(ValueError) as exc:
        extract_url_content("https://example.com/missing")

    assert "Error fetching URL" in str(exc.value)
    assert "404" in str(exc.value)


# Test URL extraction with network error
@patch("utils.ingestion.url_extraction.requests.get")
def test_extract_url_content_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    with pytest.raises(requests.exceptions.RequestException):
        extract_url_content("https://broken-url.com")

    mock_get.assert_called_once()


# Test URL extraction with empty URL
@patch("utils.ingestion.url_extraction.requests.get")
def test_extract_url_content_empty_url(mock_get):
    mock_get.side_effect = requests.exceptions.MissingSchema("Invalid URL")

    with pytest.raises(requests.exceptions.RequestException):
        extract_url_content("")

    mock_get.assert_called_once_with('', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}, timeout=15)