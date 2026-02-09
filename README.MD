# 🧐 Pluggable Resume Parsing Framework

## Overview

Pluggable Resume Parsing Framework is a clean, extensible Python framework for extracting structured data (name, email, skills) from resumes in PDF and Word (.docx) formats.

The primary goal of this project is **architectural quality**, not parsing accuracy.  
It focuses on clean, testable, and production-oriented design, following Object-Oriented Design principles and modern software engineering practices.

This framework was intentionally designed to be:
- Easy to extend
- Easy to test
- Easy to reason about
- Ready for ML / LLM-powered strategies

## Architecture

The architecture is organized into three clearly separated layers:

1. **Parsing layer**
   - Responsible for converting files (PDF, DOCX) into raw text.
   - Uses a Factory pattern to select the correct parser based on file extension.

2. **Extraction layer**
   - Focuses on extracting specific fields (name, email, skills).
   - Each field extractor is isolated and independently testable.
   - Multiple strategies can coexist (rule-based, ML-based, LLM-based).

3. **Orchestration layer**
   - Coordinates the parsing and extraction steps.
   - Produces a structured `ResumeData` object as output.


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
├── samples_resume/
│   └── resume.pdf
├── main.py                    # Usage
├── requirements.txt
└── README.md

```

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/vivialves/resume-parser-framework.git
   cd resume-parser-framework

2. Create & activate virtual environment (recommended: conda or venv):

```bash
conda create -n resume_pf python=3.11
conda activate resume_pf
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. How to Run

```bash
python main.py
```

## Design Decisions

Key design decisions include:

- **Dependency Injection**  
  Field extractors are injected via a dictionary, allowing full control over strategies used at runtime and simplifying testing.

- **Strategy Pattern (implicit)**  
  Different extraction strategies (regex, ML, LLM) implement a common interface and can be swapped without modifying orchestration code.

- **Factory Pattern**  
  File parsers are selected dynamically based on file extension, enabling easy support for new formats.

- **Explicit Trade-offs**  
  The framework favors clarity and extensibility over premature optimization or overengineering.

- **Strategic Logging** 
  Basic logging is implemented at system boundaries (framework orchestration and external LLM calls) to improve observability and production readiness without overcomplicating the core extraction logic.



## Extensibility

The framework is designed to grow naturally with new requirements:

- Add a new file format → implement a parser and register it in the factory
- Add a new field → implement a new extractor and inject it
- Add a new extraction strategy → implement the extractor interface (e.g. LLM, ML model, API-based)

No changes are required in the orchestration logic when extending functionality.

## LLM Integration Strategy

LLM-based skills extraction is implemented using **Google Gemini (gemini-2.0-flash)**.

The LLM is treated as:
- A **pluggable strategy**, not a core dependency
- An optional, higher-precision layer that can coexist with rule-based extraction

Design considerations:
- Prompt logic is isolated inside the LLM extractor
- LLM calls are fully mockable in tests
- The framework can easily swap Gemini for another provider (OpenAI, Claude, local models)

This approach avoids tight coupling between business logic and LLM providers while still demonstrating practical LLM integration.


## Tests
The project uses **pytest**.

```bash
pytest -v
```

## Future Improvements

- Introduce confidence scores per extracted field
- Support multi-language resumes
- Add async LLM calls for scalability
- Implement caching for repeated LLM calls
- Expose the framework as a REST API
- Add structured logging and tracing

## 🧑‍💻 Author

**Viviane Alves de Oliveira**
AI Engineer | Python Developer | Medical AI Researcher
📧 [LinkedIn](https://www.linkedin.com/in/vivialves-developer)