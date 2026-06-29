import chromadb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_ROOT / "db" / "chroma"

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="mainframe_docs"
)

question = input("Ask a question: ")

results = collection.query(
    query_texts=[question],
    n_results=5
)

print("\n==========================")
print("TOP RESULTS")
print("==========================\n")

for i, doc in enumerate(results["documents"][0]):

    metadata = results["metadatas"][0][i]

    print(f"Result #{i+1}")
    print(f"Source: {metadata['source']}")
    print(f"Vendor: {metadata['vendor']}")
    print("-" * 60)

    print(doc[:1000])

    print("\n")
