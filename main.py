from flashcards import extract_text_from_pdf, generate_flashcards, save_flashcards_to_txt_file

pdf_path = "./AP_Psychology_Review.pdf"

if __name__ == "__main__":
    text = extract_text_from_pdf(pdf_path)
    flashcards = generate_flashcards(text)
    save_flashcards_to_txt_file(flashcards)
    print("\nGenerated flashcards\n")
