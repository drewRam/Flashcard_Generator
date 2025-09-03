import os
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter

load_dotenv()

# Configuration
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            text += reader.pages[i].extract_text() or ""
    
    return text

# Generate flashcards
def generate_flashcards(text):
    amount_of_cards = 10
    response = client.responses.create(
        model="gpt-4o",  # or "gpt-3.5-turbo"
        instructions=f"You are a helpful assistant. Based on the following study material, generate {amount_of_cards} flashcards in Q&A format:",
        input=f"Study Material: {text} Return in this format: \nQ1: ... \nA1: ... \nQ2: ... \nA2: ... "
    )
    return response.output_text

def save_flashcards_to_txt_file(flashcards, filename="flashcards.txt"):
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(flashcards)