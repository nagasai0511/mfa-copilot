from pathlib import Path
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCS_DIR = PROJECT_ROOT / "docs"

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
            print(f"Error reading {pdf_path.name}: {e}")

    return text


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

all_chunks = []


def detect_vendor(folder_name):

    folder = folder_name.lower()

    if folder == "ibm":
        return "IBM"

    if folder == "rocket":
        return "ROCKET"

    if folder == "redbooks":
        return "IBM REDBOOK"

    if folder == "ibm_redbooks":
        return "IBM REDBOOK"

    if folder == "incidents":
        return "INTERNAL"

    if folder == "internal":
        return "INTERNAL"

    if folder == "github_docs":
        return "COMMUNITY"

    return "OTHER"


pdf_files = sorted(DOCS_DIR.rglob("*.pdf"))

print(f"\nFound {len(pdf_files)} PDF documents\n")

for pdf_file in pdf_files:

    category = pdf_file.parent.name

    vendor = detect_vendor(category)

    print("=" * 60)
    print(f"Processing : {pdf_file.name}")
    print(f"Category   : {category}")
    print(f"Vendor     : {vendor}")

    text = extract_text(pdf_file)

    print(f"Characters : {len(text)}")

    chunks = splitter.split_text(text)

    print(f"Chunks     : {len(chunks)}")

    for idx, chunk in enumerate(chunks):

        all_chunks.append({

            "source": pdf_file.name,

            "vendor": vendor,

            "category": category,

            "chunk_id": idx,

            "text": chunk

        })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\n" + "=" * 60)
print("Chunk Generation Completed")
print("=" * 60)
print(f"Documents : {len(pdf_files)}")
print(f"Chunks    : {len(all_chunks)}")
print(f"Saved To  : {OUTPUT_FILE}")