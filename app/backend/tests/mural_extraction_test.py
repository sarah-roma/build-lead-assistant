import pytest
from unittest.mock import patch, MagicMock

from utils.ingestion.mural_extraction import (
    extract_mural_id,
    get_widget_text,
    list_mural_widgets,
)


# ----- extract_mural_id -----

def test_extract_mural_id_standard_url():
    assert extract_mural_id("https://app.mural.co/t/team/m/team/123/") == "team.123"


def test_extract_mural_id_with_trailing_slug():
    url = "https://app.mural.co/t/myteam/m/myteam/1234567890-abcd/board-name"
    assert extract_mural_id(url) == "myteam.1234567890-abcd"


def test_extract_mural_id_invalid_url():
    assert extract_mural_id("not-a-mural-url") is None
    assert extract_mural_id("https://example.com/foo") is None


# ----- list_mural_widgets -----

@pytest.fixture
def mock_get():
    with patch("utils.ingestion.mural_extraction.requests.get") as mock_get:
        yield mock_get


def test_list_mural_widgets_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"value": [{"id": "1"}], "next": None}
    mock_get.return_value = mock_response

    result = list_mural_widgets("https://app.mural.co/t/team/m/team/123/", "fake-token")

    mock_get.assert_called_once_with(
        "https://app.mural.co/api/public/v1/murals/team.123/widgets",
        headers={"Authorization": "Bearer fake-token"},
        params={"limit": 1000},
        timeout=30,
    )
    assert result == [{"id": "1"}]


def test_list_mural_widgets_paginates(mock_get):
    page1 = MagicMock()
    page1.status_code = 200
    page1.json.return_value = {"value": [{"id": "1"}], "next": "page2-token"}
    page2 = MagicMock()
    page2.status_code = 200
    page2.json.return_value = {"value": [{"id": "2"}, {"id": "3"}], "next": None}
    mock_get.side_effect = [page1, page2]

    result = list_mural_widgets("https://app.mural.co/t/team/m/team/123/", "tok")

    assert result == [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    assert mock_get.call_count == 2
    # Second call should include the next-page cursor
    second_call_params = mock_get.call_args_list[1].kwargs["params"]
    assert second_call_params["next"] == "page2-token"


def test_list_mural_widgets_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    with pytest.raises(ValueError) as exc:
        list_mural_widgets("https://app.mural.co/t/team/m/team/999/", "bad-token")

    assert "MURAL API error 404: Not Found" in str(exc.value)


def test_list_mural_widgets_unparseable_url(mock_get):
    with pytest.raises(ValueError, match="parse Mural board ID"):
        list_mural_widgets("not-a-url", "tok")
    mock_get.assert_not_called()


# ----- get_widget_text -----

@pytest.fixture
def mock_list():
    with patch("utils.ingestion.mural_extraction.list_mural_widgets") as mock_list:
        yield mock_list


def test_get_widget_text_extracts_from_sticky_notes(mock_list):
    mock_list.return_value = [
        {"htmlText": "<p>Hello <b>World</b></p>", "x": 0, "y": 0},
        {"htmlText": "<div>Another Note</div>", "x": 0, "y": 100},
    ]

    result = get_widget_text("https://app.mural.co/t/team/m/team/123/", "token123")

    assert len(result) == 2
    assert "Hello" in result[0] and "World" in result[0]
    assert "Another Note" in result[1]


def test_get_widget_text_extracts_from_non_sticky_widgets(mock_list):
    """Shapes, titles, captions etc. must all be picked up."""
    mock_list.return_value = [
        {"type": "title", "title": "Pain Points", "x": 0, "y": 0},
        {"type": "shape", "text": "Auth is broken", "x": 0, "y": 50},
        {"type": "image", "caption": "Architecture diagram", "x": 0, "y": 100},
        {"type": "file", "name": "notes.pdf", "x": 0, "y": 150},
    ]

    result = get_widget_text("https://app.mural.co/t/team/m/team/123/", "tok")

    assert result == [
        "Pain Points",
        "Auth is broken",
        "Architecture diagram",
        "notes.pdf",
    ]


def test_get_widget_text_orders_by_y_then_x(mock_list):
    """Top-down, left-to-right reading order keeps headers near their content."""
    mock_list.return_value = [
        {"text": "Bottom right", "x": 200, "y": 500},
        {"text": "Top",          "x": 100, "y": 0},
        {"text": "Middle left",  "x": 0,   "y": 250},
        {"text": "Middle right", "x": 300, "y": 250},
    ]

    result = get_widget_text("https://app.mural.co/t/team/m/team/123/", "tok")

    assert result == ["Top", "Middle left", "Middle right", "Bottom right"]


def test_get_widget_text_skips_widgets_with_no_text(mock_list):
    mock_list.return_value = [
        {"type": "connector"},
        {"htmlText": ""},
        {"text": "   "},
    ]

    result = get_widget_text("https://app.mural.co/t/team/m/team/123/", "tok")

    assert result == []


def test_get_widget_text_preserves_multiline_html(mock_list):
    """<p>Line 1</p><p>Line 2</p> must not collapse to 'Line 1Line 2'."""
    mock_list.return_value = [
        {"htmlText": "<p>Line 1</p><p>Line 2</p>", "x": 0, "y": 0},
    ]

    result = get_widget_text("https://app.mural.co/t/team/m/team/123/", "tok")

    assert result == ["Line 1\nLine 2"]


def test_get_widget_text_combines_multiple_fields_per_widget(mock_list):
    """A widget with both title and htmlText should yield both."""
    mock_list.return_value = [
        {"title": "Summary", "htmlText": "<p>Details here</p>", "x": 0, "y": 0},
    ]

    result = get_widget_text("https://app.mural.co/t/team/m/team/123/", "tok")

    assert result == ["Summary\nDetails here"]