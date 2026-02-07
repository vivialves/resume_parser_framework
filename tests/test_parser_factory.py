import pytest
from unittest.mock import MagicMock, patch

from resume_parser_framework.parser.parser_factory import (
    ParserFactory,
    PDFParser,
    WordParser,
    FileParser
)


# ------------------------
# Parser Factory Tests
# ------------------------


def test_factory_returns_usable_parser_instance():
    parser = ParserFactory.get_parser(".pdf")
    assert hasattr(parser, "extract_text")
    assert callable(parser.extract_text)


def test_factory_raises_for_unsupported_extension():
    with pytest.raises(ValueError, match="No parser available"):
        ParserFactory.get_parser(".txt")


def test_factory_is_static_and_does_not_require_instantiation():
    parser = ParserFactory.get_parser(".pdf")
    assert isinstance(parser, PDFParser)


# ------------------------
# PDF Parser and WORD Parser Tests
# ------------------------


@patch("resume_parser_framework.parser.parser_factory.PdfReader", side_effect=PermissionError("access denied"))
@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
def test_pdf_parser_raises_value_error_with_cause(mock_exists, mock_pdfreader):
    parser = PDFParser()
    with pytest.raises(ValueError, match="Failed to parse PDF") as exc_info:
        parser.extract_text("fake.pdf")
    
    assert exc_info.value.__cause__ is not None
    assert "access denied" in str(exc_info.value.__cause__)


@patch("resume_parser_framework.parser.parser_factory.Document", side_effect=PermissionError("docx access denied"))
@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
def test_word_parser_raises_value_error_with_cause(mock_exists, mock_document):
    parser = WordParser()
    with pytest.raises(ValueError, match="Failed to parse WORD document") as exc_info:
        parser.extract_text("fake.docx")

    assert exc_info.value.__cause__ is not None
    assert "access denied" in str(exc_info.value.__cause__)


@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
@patch("resume_parser_framework.parser.parser_factory.PdfReader")
def test_pdf_parser_handles_empty_or_corrupt_file(mock_pdfreader, mock_exists):
    mock_pdfreader.return_value.pages = []
    parser = PDFParser()
    text = parser.extract_text("empty.pdf")
    assert text == ""


@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
@patch("resume_parser_framework.parser.parser_factory.Document")
def test_word_parser_handles_empty_or_corrupt_document(mock_document, mock_exists):
    mock_document.return_value.paragraphs = []
    parser = WordParser()
    text = parser.extract_text("empty.docx")
    assert text == ""


@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
@patch("resume_parser_framework.parser.parser_factory.PdfReader")
def test_pdf_parser_extracts_text(mock_pdfreader, mock_exists):
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Page 1 content"

    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Page 2 content"

    mock_pdfreader.return_value.pages = [mock_page1, mock_page2]

    parser = PDFParser()
    text = parser.extract_text("fake.pdf")

    assert "Page 1 content" in text
    assert "Page 2 content" in text


@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
@patch("resume_parser_framework.parser.parser_factory.Document")
def test_word_parser_extracts_text(mock_document, mock_exists):
    mock_doc = mock_document.return_value
    mock_doc.paragraphs = [
        type('Para', (), {'text': 'Line one'}),
        type('Para', (), {'text': ''}),
        type('Para', (), {'text': 'Line two'}),
    ]

    parser = WordParser()
    text = parser.extract_text("fake.docx")

    assert text == "Line one\nLine two"

# ------------------------
# Parametrize Tests
# ------------------------

@pytest.mark.parametrize(
    "parser_cls, file_path, patch_target, error_message",
    [
        (
            PDFParser,
            "fake.pdf",
            "resume_parser_framework.parser.parser_factory.PdfReader",
            "Failed to parse PDF",
        ),
        (
            WordParser,
            "fake.docx",
            "resume_parser_framework.parser.parser_factory.Document",
            "Failed to parse WORD document",
        ),
    ],
    ids=["pdf", "docx"],
)

@patch("resume_parser_framework.parser.parser_factory.pathlib.Path.exists", return_value=True)
def test_parsers_raise_value_error_on_fail(
    mock_exists, parser_cls, file_path, patch_target, error_message
):
    with patch(patch_target, side_effect=Exception("parse error")):
        parser = parser_cls()
        with pytest.raises(ValueError, match=error_message):
            parser.extract_text(file_path)


@pytest.mark.parametrize("ext,expected_class", [
    (".pdf", PDFParser),
    (".docx", WordParser)
    ],
    ids=["pdf", "docx"]
)

def test_factory_returns_correct_parser(ext, expected_class):
    parser = ParserFactory.get_parser(ext)
    assert isinstance(parser, expected_class)
    assert isinstance(parser, FileParser)


@pytest.mark.parametrize("extension, parser_class", [
    (".pdf", PDFParser), 
    (".docx", WordParser)
    ],
    ids=["pdf", "docx"]
)

def test_parser_raise_file_not_found(extension, parser_class):
    parser = parser_class()
    with pytest.raises(FileNotFoundError, match="File not found"):
        parser.extract_text("this_file_does_not_exist" + extension)
