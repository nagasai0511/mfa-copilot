from pathlib import Path
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent

IBM_DIR = PROJECT_ROOT / "docs" / "ibm"
ROCKET_DIR = PROJECT_ROOT / "docs" / "rocket"


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page_num, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        except Exception as e:
            print(f"Error on page {page_num}: {e}")

    return text


def process_folder(folder_path):

    results = []

    for pdf_file in folder_path.glob("*.pdf"):

        print(f"\nProcessing: {pdf_file.name}")

        text = extract_pdf_text(pdf_file)

        char_count = len(text)

        print(f"Characters Extracted: {char_count}")

        results.append(
            {
                "file_name": pdf_file.name,
                "characters": char_count,
            }
        )

    return results


if __name__ == "__main__":

    print("\n=== IBM DOCUMENTS ===")

    ibm_docs = process_folder(IBM_DIR)

    print("\n=== ROCKET DOCUMENTS ===")

    rocket_docs = process_folder(ROCKET_DIR)

    print("\nSUMMARY")

    print(f"IBM Documents: {len(ibm_docs)}")
    print(f"Rocket Documents: {len(rocket_docs)}")
