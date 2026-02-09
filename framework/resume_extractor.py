import logging

from typing import Dict

from resume_parser_framework.framework.export import ResumeData
from resume_parser_framework.extractor.extractor_base import FieldExtractor

logger = logging.getLogger(__name__)

class ResumeExtractor:
    """
    Orchestrates field extraction using provided FieldExtractor instances.
    Returns a ResumeData object.
    """
    def __init__(self, extractors: Dict[str, FieldExtractor]):
        self.extractors = extractors

    def extract(self, text: str) -> ResumeData:
        logger.info("Starting field extraction")

        result = ResumeData(
            name=self.extractors["name"].extract(text),
            email=self.extractors["email"].extract(text),
            skills_based=self.extractors["skills_based"].extract(text),
            skills_llm=self.extractors["skills_llm"].extract(text)
        )

        logger.info(
            "Field extraction completed",
            extra={
                "has_name": bool(result.name),
                "has_email": bool(result.email),
                "skills_based_count": len(result.skills_based),
                "skills_llm_count": len(result.skills_llm),
            },
        )

        return result