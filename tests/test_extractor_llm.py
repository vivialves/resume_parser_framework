from unittest.mock import MagicMock, patch
from resume_parser_framework.extractor.extractor_llm import SkillsExtractorLLM


@patch("resume_parser_framework.extractor.extractor_llm.genai.Client")
def test_skills_extractor_llm_happy_path(mock_client):
    mock_response = MagicMock()
    mock_response.parsed.skills = ["Python", "Docker"]

    mock_client.return_value.models.generate_content.return_value = mock_response

    extractor = SkillsExtractorLLM(api_key="fake-key")
    result = extractor.extract("Some resume text")

    assert result == ["Docker", "Python"]