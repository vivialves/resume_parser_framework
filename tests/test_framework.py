import pytest
from unittest.mock import MagicMock, patch
from resume_parser_framework.framework.framework import ResumeParserFramework
from resume_parser_framework.framework.resume_extractor import ResumeExtractor
from resume_parser_framework.framework.export import ResumeData


@pytest.mark.parametrize("file_path,ext", [
    ("fake.pdf", ".pdf"),
    ("fake.docx", ".docx")
])

def test_framework_orchestrates_correctly(resume_extractor,file_path, ext):
    mock_parser = MagicMock()
    mock_parser.extract_text.return_value = """
    Jane Doe
    jane.doe@example.com
    Python, Docker, AWS, LLM
    """
    with patch(
        "resume_parser_framework.framework.framework.ParserFactory.get_parser",
        return_value=mock_parser,
    ):

        framework = ResumeParserFramework(resume_extractor)
        result = framework.parser_resume(file_path=file_path)

    assert isinstance(result, ResumeData)
    assert result.name == "Jane Doe"
    assert result.email == "jane.doe@example.com"
    for skill in ["Python", "Docker", "AWS", "LLM"]:
        assert skill in result.skills_based


def test_framework_raises_if_file_has_no_extension(resume_extractor):
    framework = ResumeParserFramework(resume_extractor)

    with pytest.raises(ValueError, match="File has no extension"):
        framework.parser_resume("resume")


def test_framework_raises_for_unsupported_extension(resume_extractor):
    framework = ResumeParserFramework(resume_extractor)

    with patch(
        "resume_parser_framework.framework.framework.ParserFactory.get_parser",
        return_value=None,
    ):
        with pytest.raises(ValueError, match="Unsupported file format"):
            framework.parser_resume("resume.txt")


def test_framework_propagates_parser_error(resume_extractor):
    mock_parser = MagicMock()
    mock_parser.extract_text.side_effect = ValueError("parser exploded")

    with patch(
        "resume_parser_framework.framework.framework.ParserFactory.get_parser",
        return_value=mock_parser,
    ):
        framework = ResumeParserFramework(resume_extractor)

        with pytest.raises(ValueError, match="parser exploded"):
            framework.parser_resume("fake.pdf")