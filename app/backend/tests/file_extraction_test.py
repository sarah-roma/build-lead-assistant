import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path

from utils.ingestion.file_extraction import ExtractText



#  Test text cleaning
def test_clean_text():
    raw = "Hello\n\n\nWorld\n\nTest\n"
    cleaned = ExtractText._clean_text(raw)
    assert cleaned == "Hello\nWorld\nTest"

#  Test text extraction
@patch("utils.ingestion.file_extraction.DocumentConverter")
def test_extract_any_format(mock_converter_cls, tmp_path):
    # Create fake docling converter
    mock_converter = MagicMock()
    mock_result = MagicMock()
    mock_document = MagicMock()

    mock_document.export_to_text.return_value = "Some raw text"
    mock_result.document = mock_document
    mock_converter.convert.return_value = mock_result
    mock_converter_cls.return_value = mock_converter

    # Create fake temporary file path
    temp_file = tmp_path / "sample.docx"
    temp_file.write_text("dummy")

    result = ExtractText._extract_any_format(temp_file)
    assert result == "Some raw text"
    assert mock_converter.convert.called


#  Test async extract
@pytest.mark.asyncio
@patch("utils.ingestion.file_extraction.run_in_threadpool")
@patch("utils.ingestion.file_extraction.DocumentConverter")
async def test_extract(mock_converter_cls, mock_run_threadpool, tmp_path):
    # Create fake upload file
    file_bytes = b"hello world"
    upload = AsyncMock()
    upload.filename = "file.txt"
    upload.read = AsyncMock(return_value=file_bytes)

    # Mock DocumentConverter → returns object with export_to_text()
    mock_converter = MagicMock()
    mock_result = MagicMock()
    mock_document = MagicMock()
    mock_document.export_to_text.return_value = "raw extracted text"
    mock_result.document = mock_document
    mock_converter.convert.return_value = mock_result
    mock_converter_cls.return_value = mock_converter

    # run_in_threadpool returns cleaned text
    mock_run_threadpool.return_value = "raw extracted text"

    result = await ExtractText.extract(upload)
    assert result == "raw extracted text"

    # Temporary file must be deleted
    temp_path = Path("./temp_file.txt")
    assert not temp_path.exists()


#  Test file parsing success
@pytest.mark.asyncio
@patch("utils.ingestion.file_extraction.ExtractText.extract")
async def test_file_parser_success(mock_extract):
    # mock ExtractText.extract to return text
    mock_extract.return_value = "parsed text"

    file1 = AsyncMock()
    file1.filename = "doc1.pdf"
    file2 = AsyncMock()
    file2.filename = "doc2.docx"

    result = await ExtractText.file_parser([file1, file2])

    assert result == {
        "doc1.pdf": "parsed text",
        "doc2.docx": "parsed text",
    }

# Test file parsing with extraction error
@pytest.mark.asyncio
@patch("utils.ingestion.file_extraction.ExtractText.extract")
async def test_file_parser_error(mock_extract):
    # Make extract() raise an exception
    mock_extract.side_effect = Exception("Boom!")

    file1 = AsyncMock()
    file1.filename = "badfile.pdf"

    result = await ExtractText.file_parser([file1])

    assert "error" in result["badfile.pdf"]
    assert result["badfile.pdf"]["error"] == "Boom!"
