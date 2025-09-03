# test_flashcards.py
import pytest
import pathlib
from unittest.mock import MagicMock
from pypdf import PdfWriter
from flashcards import (
    extract_text_from_pdf,
    generate_flashcards,
    save_flashcards_to_txt_file,
)


PDF_FILE = pathlib.Path("AP_Psychology_Review.pdf")
OUTPUT_DIR = pathlib.Path("tests/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Fixture: Create a sample PDF
# ---------------------------
@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return pdf_path


# ---------------------------
# Test: PDF extraction
# ---------------------------
def test_extract_text_from_pdf(sample_pdf):
    text = extract_text_from_pdf(sample_pdf)
    assert isinstance(text, str)
    assert text == "" or isinstance(text, str)  # pypdf may return empty


# ---------------------------
# Test: Flashcard generation (mocked OpenAI)
# ---------------------------
def test_generate_flashcards(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.output_text = "Q1: What is AI?\nA1: Artificial Intelligence"
    mock_client.responses.create.return_value = mock_response

    # Patch client inside your_module
    monkeypatch.setattr("flashcards.client", mock_client)

    result = generate_flashcards("Some study text")
    assert "Q1:" in result
    assert "A1:" in result


# ---------------------------
# Test: Saving flashcards to file
# ---------------------------
def test_save_flashcards_to_txt_file(tmp_path):
    file_path = tmp_path / "flashcards.txt"
    content = "Q1: Sample\nA1: Answer"

    save_flashcards_to_txt_file(content, filename=file_path)

    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    assert "Q1:" in data
    assert "A1:" in data


# ---------------------------
# Test: Full pipeline regression (mocked)
# ---------------------------
def test_full_pipeline(monkeypatch, tmp_path):
    # Extract text from real PDF
    text = extract_text_from_pdf(PDF_FILE)
    assert text, "PDF extraction failed or returned empty text"

    # Generate real flashcards
    flashcards = generate_flashcards(text)

    # Save output to persistent folder
    file_path = OUTPUT_DIR / "flashcards_test_results.txt"
    save_flashcards_to_txt_file(flashcards, filename=file_path)

    # Quick sanity check
    assert "Q1:" in flashcards
    assert "A1:" in flashcards

    print("\nFlashcards saved to:", file_path)
