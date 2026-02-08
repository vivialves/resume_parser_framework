from typing import Dict

from resume_parser_framework.framework.export import ResumeData
from resume_parser_framework.extractor.extractor_base import FieldExtractor


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
            skills_based=self.extractors["skills_based"].extract(text),
            skills_llm=self.extractors["skills_llm"].extract(text)
        )