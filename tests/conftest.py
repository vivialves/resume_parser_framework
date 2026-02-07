import pytest
from resume_parser_framework.framework.export import ResumeData
from resume_parser_framework.extractor.extractor import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser_framework.framework.resume_extractor import ResumeExtractor

# ------------------------
# Sample Resume Texts
# ------------------------

@pytest.fixture
def sample_text() -> str:
    """Sample resume with single surname."""
    return """
    Jane Doe
    linkedIn | gitHub | jane.doe@example.com
    SUMMARY
    AI Engineer with experience in Python, Machine Learning, LLM, NLP, Docker, AWS.
    PROFESSIONAL EXPERIENCE
    ...
    SKILLS
    Python, JavaScript, SQL, TensorFlow, PyTorch
    """.strip()


@pytest.fixture
def multi_surname_text() -> str:
    """Sample resume with two surnames."""
    return """
    Jane Doe Williams
    LinkedIn | GitHub | jane.doe@example.com
    SUMMARY
    AI Engineer with experience in Python, Machine Learning, LLM, NLP, Docker, AWS.
    SKILLS
    Python, JavaScript, SQL, TensorFlow, PyTorch
    """.strip()


@pytest.fixture
def special_chars_text() -> str:
    """Sample resume with accented characters."""
    return """
    José María García
    LinkedIn | GitHub | jose.garcia@example.com
    SUMMARY
    AI Engineer with Python, Machine Learning, LLM.
    SKILLS
    Python, JavaScript, SQL
    """.strip()


@pytest.fixture
def no_email_text() -> str:
    """Sample resume without any email."""
    return """
    Ana Paula Costa
    LinkedIn | GitHub
    SUMMARY
    AI Engineer with Python, Machine Learning
    SKILLS
    Python, JavaScript
    """.strip()


# ------------------------
# Extractors
# ------------------------

@pytest.fixture
def extractors_dict():
    """Dictionary of all field extractors."""
    return {
        "name": NameExtractor(),
        "email": EmailExtractor(),
        "skills": SkillsExtractor(),
    }


@pytest.fixture
def resume_extractor(extractors_dict):
    """ResumeExtractor instance using all extractors."""
    return ResumeExtractor(extractors_dict)


# ------------------------
# Expected ResumeData outputs
# ------------------------

@pytest.fixture
def sample_resume_data() -> ResumeData:
    """Expected ResumeData for sample_text"""
    return ResumeData(
        name="Jane Doe",
        email="jane.doe@example.com",
        skills=["Python", "JavaScript", "SQL", "Machine Learning", "LLM", "NLP", "Docker", "AWS", "TensorFlow", "PyTorch"]
    )


@pytest.fixture
def multi_surname_resume_data() -> ResumeData:
    """Expected ResumeData for multi_surname_text"""
    return ResumeData(
        name="Jane Doe Williams",
        email="jane.doe@example.com",
        skills=["Python", "JavaScript", "SQL", "Machine Learning", "LLM", "NLP", "Docker", "AWS", "TensorFlow", "PyTorch"]
    )


@pytest.fixture
def special_chars_resume_data() -> ResumeData:
    """Expected ResumeData for special_chars_text"""
    return ResumeData(
        name="José María García",
        email="jose.garcia@example.com",
        skills=["Python", "JavaScript", "SQL", "Machine Learning", "LLM"]
    )


@pytest.fixture
def no_email_resume_data() -> ResumeData:
    """Expected ResumeData for no_email_text"""
    return ResumeData(
        name="Ana Paula Costa",
        email=None,
        skills=["Python", "JavaScript", "Machine Learning"]
    )