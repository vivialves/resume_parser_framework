import logging
from pathlib import Path

from resume_parser_framework.parser.parser_factory import ParserFactory
from resume_parser_framework.framework.resume_extractor import ResumeExtractor
from resume_parser_framework.framework.export import ResumeData

logger = logging.getLogger(__name__)


class ResumeParserFramework:
    """Main entry point: combines parser + extractor logic."""

    def __init__(self, extractor: ResumeExtractor):
        self.extractor = extractor


    def parser_resume(self, file_path: str) -> ResumeData:
        """Parse a resume file and return structured data."""

        ext = Path(file_path).suffix.lower()
        logger.info("Starting resume parsing", extra={"file": file_path, "ext": ext})

        if not ext:
            raise ValueError(f"File has no extension")
        
        try:
            parser = ParserFactory.get_parser(ext)
            if not parser:
                raise ValueError(f"Unsupported file format: {ext}. Supported: .pdf, .docx")

            text = parser.extract_text(file_path)
            logger.info("Resume parsed successfully", extra={"file": file_path})
            return self.extractor.extract(text)
        except Exception:
            logger.exception("Resume parsing failed")
            raise