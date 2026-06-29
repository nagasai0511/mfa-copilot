from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_ROOT / "db" / "chroma"

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="mainframe_docs"
)

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

question = input("Ask a question: ")

query_embedding = model.encode(
    question
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

for i, doc in enumerate(results["documents"][0]):

    metadata = results["metadatas"][0][i]

    print("\n===================")

    print(f"Source: {metadata['source']}")
    print(f"Vendor: {metadata['vendor']}")

    print("===================")

    print(doc[:1200])
