# 🧐 Pluggable Resume Parsing Framework

A clean, extensible Python framework for extracting structured data (name, email, skills) from resumes in PDF and Word (.docx) formats.

The design prioritizes **Object-Oriented Design principles**:
- Abstraction & interfaces (ABC for parsers and extractors)
- Dependency injection / pluggability (field extractors passed via dict)
- Separation of concerns (parsing vs extraction vs orchestration)
- Extensibility (easy to add new formats, new field strategies, or swap LLMs)

Parsing accuracy is **not** the primary goal — the focus is on clean, testable, production-like architecture (per assignment instructions).

## Features

- Supports **PDF** and **.docx** files
- Pluggable field extractors for name, email, and skills
- Strategies implemented:
  - **Name**: spaCy NER (ML-based) + resume-specific heuristics
  - **Email**: reliable regex
  - **Skills**: 
    - Keyword-based (simple & fast fallback)
    - **LLM-based** using **Google Gemini** (gemini-2.5-flash) — satisfies ML/LLM requirement
- Output: structured `ResumeData` dataclass → easy JSON serialization
- Factory pattern for parser selection based on file extension
- Production-level practices: type hints, docstrings, unit tests, error handling

## 📁 Project Structure

```
resume_parser_framework/
├── extractor/                 # Field extractors (name, email, skills)
│   ├── extractor_base.py
│   ├── extractor_simple.py
│   └── extractor_llm.py       # Gemini LLM version for skills
├── parser/
│   └── parser_factory.py
├── framework/
│   ├── export.py              # ResumeData dataclass
│   ├── framework.py           # Main ResumeParserFramework
│   └── resume_extractor.py    # Orchestrates field extraction
├── tests/                     # pytest suite
│   ├── conftest.py
│   ├── test_parser_factory.py
│   ├── test_extractor_llm.py
│   ├── test_extractor_simple.py
│   ├── test_framework.py
│   └── test_resume_extractor.py
├── utils/
│   ├── constants.py 
├── main.py                    # Usage
├── requirements.txt
└── README.md

```

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/resume-parser-framework.git
   cd resume-parser-framework

2. Create & activate virtual environment (recommended: conda or venv):

```bash
conda create -n resume_pf python=3.11
conda activate resume_pf
```




