import pytest
from unittest.mock import MagicMock

from resume_parser_framework.framework.resume_extractor import ResumeExtractor


def test_coordinator_extracts_all_fields(resume_extractor, sample_text, sample_resume_data):
    result = resume_extractor.extract(sample_text)

    assert result.name == sample_resume_data.name or "Jane Doe" in (result.name or "")
    assert result.email == sample_resume_data.email
    assert len(result.skills_based) >= 5


def test_resume_extractor_extracts_all_fields(resume_extractor, sample_text):
    result = resume_extractor.extract(sample_text)

    assert result.name == "Jane Doe"
    assert result.email == "jane.doe@example.com"

    expected_skills = {"Python", "Docker", "AWS", "LLM"}
    assert expected_skills.issubset(set(result.skills_based))


def test_resume_extractor_raises_when_extractor_missing(sample_text):
    extractors = {
        "name": MagicMock(),
        "email": MagicMock(),
        # "skills_based" missing
    }
    extractor = ResumeExtractor(extractors)

    with pytest.raises(KeyError):
        extractor.extract(sample_text)

