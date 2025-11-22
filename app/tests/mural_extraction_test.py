import pytest
from unittest.mock import patch, MagicMock
from utils.mural_extraction import list_mural_widgets, get_widget_text

@pytest.fixture
def mock_request():
    with patch("utils.mural_extraction.requests.request") as mock_request:
        yield mock_request

# Test widget extraction
def test_list_mural_widgets_success(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"value": [{"id": "1"}]}'
    mock_request.return_value = mock_response

    result = list_mural_widgets("123", "fake-token")

    mock_request.assert_called_once_with(
        "GET",
        "https://app.mural.co/api/public/v1/murals/123/widgets",
        headers={"Authorization": "Bearer fake-token"},
        data={}
    )

    assert result == {"value": [{"id": "1"}]}

def test_list_mural_widgets_error(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_request.return_value = mock_response

    with pytest.raises(ValueError) as exc:
        list_mural_widgets("999", "bad-token")

    assert "MURAL API error 404: Not Found" in str(exc.value)


# Test text extraction
@pytest.fixture
def mock_list():
    with patch("utils.mural_extraction.list_mural_widgets") as mock_list:
        yield mock_list

def test_get_widget_text_extracts_html(mock_list):
    mock_list.return_value = {
        "value": [
            {"htmlText": "<p>Hello <b>World</b></p>"},
            {"htmlText": "<div>Another Note</div>"}
        ]
    }

    result = get_widget_text("123", "token123")

    assert result == ["Hello World", "Another Note"]

def test_get_widget_text_missing_html(mock_list):
    mock_list.return_value = {
        "value": [
            {},  # no htmlText
            {"htmlText": ""},  # empty htmlText
        ]
    }

    result = get_widget_text("123", "token123")

    assert result == []  # nothing extracted

def test_get_widget_text_invalid_response(mock_list):
    mock_list.return_value = {}  # no "value" key

    result = get_widget_text("123", "token123")

    assert result == []
