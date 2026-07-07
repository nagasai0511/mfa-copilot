import os
from pathlib import Path

import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_ROOT / "db" / "chroma"

# -------------------------
# Chroma
# -------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="mainframe_docs"
)

# -------------------------
# Embedding Model
# -------------------------

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# -------------------------
# Groq
# -------------------------

groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

# -------------------------
# Question
# -------------------------

question = input("Ask a question: ")

query_embedding = embedding_model.encode(
    question
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=8
)

context = "\n\n".join(
    results["documents"][0]
)

sources = []

for m in results["metadatas"][0]:
    sources.append(m["source"])

prompt = f"""
You are a Mainframe Migration SME Assistant.

Answer only using the supplied context.

If information is not available in the context,
say so.

CONTEXT:

{context}

QUESTION:

{question}
"""

response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print("\n========================")
print("ANSWER")
print("========================\n")

print(
    response.choices[0].message.content
)

print("\n========================")
print("SOURCES")
print("========================")

for source in set(sources):
    print(source)