import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHUNKS_FILE = PROJECT_ROOT / "db" / "chunks.json"

CHROMA_DIR = PROJECT_ROOT / "db" / "chroma"

print("Loading embedding model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="mainframe_docs"
)

BATCH_SIZE = 100

for start in range(0, len(chunks), BATCH_SIZE):

    batch = chunks[start:start + BATCH_SIZE]

    texts = [c["text"] for c in batch]

    embeddings = model.encode(
        texts,
        show_progress_bar=False
    )

    collection.add(
        ids=[
            f"{c['vendor']}_{c['chunk_id']}_{start+i}"
            for i, c in enumerate(batch)
        ],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "source": c["source"],
                "vendor": c["vendor"]
            }
            for c in batch
        ]
    )

    print(
        f"Processed {start + len(batch)} / {len(chunks)}"
    )

print("\nEmbeddings Complete")
