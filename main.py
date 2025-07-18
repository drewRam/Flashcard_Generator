import os
from openai import OpenAI
import PyPDF2

# Configuration
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

pdf_path = "PDF_FILE_PATH_HERE"

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            text += reader.pages[i].extract_text() or ""
    
    return text

# Generate flashcards
def generate_flashcards(text):
    response = client.responses.create(
        model="gpt-4o",  # or "gpt-3.5-turbo"
        instructions="You are a helpful assistant. Based on the following study material, generate flashcards in Q&A format:",
        input=f"Study Material: {text} Return in this format: \nQ1: ... \nA1: ... \nQ2: ... \nA2: ... "
    )
    return response.output_text

def save_flashcards_to_txt_file(flashcards, filename="flashcards.txt"):
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(flashcards)

if __name__ == "__main__":
    text = extract_text_from_pdf(pdf_path)
    flashcards = generate_flashcards(text)
    save_flashcards_to_txt_file(flashcards)
    print("\nGenerated flashcards\n")