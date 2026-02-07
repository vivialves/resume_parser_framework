from typing import Dict

from resume_parser_framework.framework.export import ResumeData
from resume_parser_framework.extractor.extractor import FieldExtractor


class ResumeExtractor:
    """
    Orchestrates field extraction using provided FieldExtractor instances.
    Returns a ResumeData object.
    """
    def __init__(self, extractors: Dict[str, FieldExtractor]):
        self.extractors = extractors

    def extract(self, text: str) -> ResumeData:
        return ResumeData(
            name=self.extractors["name"].extract(text),
            email=self.extractors["email"].extract(text),
            skills=self.extractors["skills"].extract(text),
        )