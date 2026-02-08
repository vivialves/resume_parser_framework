import pytest
from resume_parser_framework.extractor.extractor_simple import NameExtractor, EmailExtractor, SkillsExtractorBased


# ------------------------
# NameExtractor Tests
# ------------------------

@pytest.mark.parametrize(
    "text,expected_name",
    [
        ("Jane Doe\nLinkedIn | GitHub | jane.doe@example.com", "Jane Doe"),
        ("Jane Doe Williams\nLinkedIn | GitHub | jane.doe@example.com", "Jane Doe Williams"),
        ("José María García\nSoftware Engineer\nemail@example.com", "José María García"),
        ("mpf\nJohn Michael Smith\nSoftware Engineer\nno.person.entity.here@example.com", "John Michael Smith"),
        ("RESUME\nAna Paula Costa\nSkills Section", "Ana Paula Costa"),
    ]
)
def test_name_extractor_variety(text, expected_name):
    extractor = NameExtractor()
    result = extractor.extract(text)
    assert expected_name in result


def test_name_extractor_returns_none_for_empty_text():
    extractor = NameExtractor()
    result = extractor.extract("")
    assert result is None


# ------------------------
# EmailExtractor Tests
# ------------------------

def test_email_extractor_finds_valid_email():
    extractor = EmailExtractor()
    text = "Contact info: jane.doe@example.com"
    result = extractor.extract(text)
    assert result == "jane.doe@example.com"


def test_email_extractor_finds_first_email_when_multiple():
    extractor = EmailExtractor()
    text = "first@example.com or second@example.com"
    result = extractor.extract(text)
    assert result == "first@example.com"


def test_email_extractor_with_complex_email():
    extractor = EmailExtractor()
    text = "Email: john.doe+filter@company.co.uk"
    result = extractor.extract(text)
    assert result == "john.doe+filter@company.co.uk"


def test_email_extractor_returns_none_when_no_email():
    extractor = EmailExtractor()
    text = "No email here, only phone number"
    result = extractor.extract(text)
    assert result is None


# ------------------------
# SkillsExtractor Tests
# ------------------------

@pytest.mark.parametrize(
    "text,expected_skills",
    [
        ("Python, JavaScript, SQL", ["Python", "JavaScript", "SQL"]),
        ("python PYTHON Python aws AWS git", ["python", "aws", "git"]),
        ("No technical skills here", []),
        ("I use Python and JavaScript daily", ["Python", "JavaScript"]),
    ]
)
def test_skills_extractor_various(text, expected_skills):
    extractor = SkillsExtractorBased()
    result = extractor.extract(text)
    assert set(result) == set(expected_skills)