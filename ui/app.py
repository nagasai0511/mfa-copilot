import os
from pathlib import Path

import chromadb
import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer

# --------------------------------
# Page Config
# --------------------------------

st.set_page_config(
    page_title="Mainframe Migration SME Copilot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------
# Paths
# --------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_ROOT / "db" / "chroma"

# --------------------------------
# Cached Models
# --------------------------------

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

@st.cache_resource
def load_chroma():
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    return client.get_collection(
        name="mainframe_docs"
    )

@st.cache_resource
def load_groq():
    return Groq(
        api_key=os.environ["GROQ_API_KEY"]
    )

embedding_model = load_embedding_model()
collection = load_chroma()
groq_client = load_groq()

# --------------------------------
# Header
# --------------------------------

st.title("Mainframe Migration SME Copilot")

st.markdown(
    """
Search IBM COBOL, Rocket Software and Migration Documentation.
"""
)

# --------------------------------
# User Input
# --------------------------------

question = st.text_input(
    "Ask a question",
    placeholder="What is ADDRESS OF in COBOL?"
)

# --------------------------------
# Search
# --------------------------------

if st.button("Search"):

    with st.spinner("Searching knowledge base..."):

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

        prompt = f"""
You are an expert Mainframe Migration SME.

Answer only from the supplied context.

Provide:

1. Explanation
2. Important considerations
3. References

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

        answer = response.choices[0].message.content

    st.subheader("Answer")

    st.write(answer)

    st.subheader("Sources")

    unique_sources = sorted(
        set(
            meta["source"]
            for meta in results["metadatas"][0]
        )
    )

    for source in unique_sources:
        st.write(f"• {source}")
