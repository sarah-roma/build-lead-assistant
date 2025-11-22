from pathlib import Path
from fastapi.concurrency import run_in_threadpool
from fastapi import UploadFile
from docling.document_converter import DocumentConverter
import re
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

class ExtractText:
    @staticmethod
    def _clean_text(text: str) -> str:
        """ Removes newlines + whitespace """
        text = "\n".join([line for line in text.splitlines() if line.strip()])
        text = re.sub(r"\n{3,}", "\n\n", text)
        logging.info("Cleaned extracted text")
        return text.strip()

    @staticmethod
    def _extract_any_format(temp_path: Path) -> str:
        """ Extract text from any file format using DocumentConverter """
        converter = DocumentConverter()
        result = converter.convert(str(temp_path))
        raw_text = result.document.export_to_text()
        logging.info(f"Extracted raw text from file: {temp_path.name}")
        return ExtractText._clean_text(raw_text)

    @staticmethod
    async def extract(upload_file: UploadFile) -> str:
        """ Extract text from an uploaded file """
        temp_path = Path(f"./temp_{upload_file.filename}")
        file_bytes = await upload_file.read()
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
        try:
            logging.info(f"Extracting text from uploaded file: {upload_file.filename}")
            text = await run_in_threadpool(
                ExtractText._extract_any_format, temp_path
            )
        finally:
            logging.info(f"Deleting temporary file: {temp_path.name}")
            temp_path.unlink(missing_ok=True)
        return text

    @staticmethod
    async def file_parser(uploaded_files):
        """ Parse multiple uploaded files and extract their text """
        results = {}
        for file in uploaded_files:
            try:
                results[file.filename] = await ExtractText.extract(file)
            except Exception as e:
                logging.exception(f"Error extracting text from file: {file.filename}")
                results[file.filename] = {"error": str(e)}
        return results
