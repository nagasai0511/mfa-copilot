from pathlib import Path
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parent.parent

IBM_DIR = PROJECT_ROOT / "docs" / "ibm"
ROCKET_DIR = PROJECT_ROOT / "docs" / "rocket"


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


all_chunks = []

for folder in [IBM_DIR, ROCKET_DIR]:

    for pdf_file in folder.glob("*.pdf"):

        print(f"\nChunking {pdf_file.name}")

        text = extract_text(pdf_file)

        chunks = splitter.split_text(text)

        print(f"Chunks Created: {len(chunks)}")

        for idx, chunk in enumerate(chunks):

            all_chunks.append(
                {
                    "source": pdf_file.name,
                    "chunk_id": idx,
                    "text": chunk
                }
            )

print("\n===================")
print(f"TOTAL CHUNKS: {len(all_chunks)}")
