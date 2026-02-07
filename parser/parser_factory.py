import pathlib

from pypdf import PdfReader
from docx import Document
from abc import ABC, abstractmethod
     

class FileParser(ABC):
    """Abstract base class for file parsers."""

    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract raw text from the file."""
        pass


class PDFParser(FileParser):
    """Parser for PDF files using pypdf."""

    def extract_text(self, file_path: str) -> str:
        if not pathlib.Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError("Failed to parse PDF") from e


class WordParser(FileParser):
    """Parser for .docx files using python-docx."""

    def extract_text(self, file_path: str) -> str:
        if not pathlib.Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            doc = Document(file_path)
            text = "\n".join(
                para.text for para in doc.paragraphs if para.text.strip()
            )
            return text.strip()
        except Exception as e:
            raise ValueError("Failed to parse WORD document") from e
        
class ParserFactory:
    """The Factory that decides which parser to use."""
    
    _parsers = {
        ".pdf": PDFParser,
        ".docx": WordParser,
    }
    
    @staticmethod
    def get_parser(extension: str) -> FileParser:
        parser_class = ParserFactory._parsers.get(extension)
        if not parser_class:
            raise ValueError(f"No parser available for extension: {extension}")
            
        return parser_class()