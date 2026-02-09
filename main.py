import os
import json

from dotenv import load_dotenv
from dataclasses import asdict

from resume_parser_framework.utils.constants import RESUME_DIR
from resume_parser_framework.extractor.extractor_simple import (
    EmailExtractor,
    NameExtractor,
    SkillsExtractorBased,
)

from resume_parser_framework.extractor.extractor_llm import (
    SkillsExtractorLLM,
)


from resume_parser_framework.framework.resume_extractor import ResumeExtractor
from resume_parser_framework.framework.framework import ResumeParserFramework

from resume_parser_framework.utils.logging_config import setup_logging

load_dotenv()
setup_logging()

def main():
    # Configure extractors (very flexible — swap / add strategies easily)
    extractors = {
        "name": NameExtractor(),     # ML/NER-based
        "email": EmailExtractor(),   # regex
        "skills_based": SkillsExtractorBased(), # rule-based
        "skills_llm": SkillsExtractorLLM(), # LLM
    }

    resume_extractor = ResumeExtractor(extractors)
    framework = ResumeParserFramework(resume_extractor)

    print("Word Resume:")
    result_docx = framework.parser_resume(os.path.join(RESUME_DIR, "resume.docx"))
    print(json.dumps(asdict(result_docx), indent=2))

    print("\nPDF Resume:")
    result_pdf = framework.parser_resume(os.path.join(RESUME_DIR, "resume.pdf"))
    print(json.dumps(asdict(result_pdf), indent=2))


if __name__ == "__main__":
    main()