from pathlib import Path
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

IBM_DIR = PROJECT_ROOT / "docs" / "ibm"
ROCKET_DIR = PROJECT_ROOT / "docs" / "rocket"

OUTPUT_FILE = PROJECT_ROOT / "db" / "chunks.json"


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        try:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        except Exception as e:
            print(f"Error reading page: {e}")

    return text


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

all_chunks = []


def process_directory(directory, vendor):

    for pdf_file in directory.glob("*.pdf"):

        print(f"Processing {pdf_file.name}")

        text = extract_text(pdf_file)

        chunks = splitter.split_text(text)

        print(f"Chunks Created: {len(chunks)}")

        for idx, chunk in enumerate(chunks):

            all_chunks.append({
                "source": pdf_file.name,
                "vendor": vendor,
                "chunk_id": idx,
                "text": chunk
            })


# Process IBM Documents
process_directory(IBM_DIR, "IBM")

# Process Rocket Documents
process_directory(ROCKET_DIR, "ROCKET")

# Save chunks
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print("\n====================")
print(f"Total Chunks Saved: {len(all_chunks)}")
print(f"Output File: {OUTPUT_FILE}")
