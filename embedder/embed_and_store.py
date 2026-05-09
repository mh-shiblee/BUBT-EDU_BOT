import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_PATH = os.path.join(BASE_DIR, "..", "data", "bubt_clean_text.txt")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "..", "vector_store")
FAISS_INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_STORE_DIR, "index.pkl")

# ─── Load clean text ──────────────────────────────────────────────────────────


def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# ─── Split into chunks ────────────────────────────────────────────────────────


def split_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)

# ─── Load embedding model ─────────────────────────────────────────────────────


def load_embedding_model():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded!")
    return model

# ─── Embed and store in FAISS ─────────────────────────────────────────────────


def embed_and_store(chunks, model):
    print(f"Embedding {len(chunks)} chunks...")

    # Convert chunks to vectors
    embeddings = model.encode(chunks, show_progress_bar=True)

    # Convert to float32 — FAISS requires this
    embeddings = np.array(embeddings).astype("float32")

    # Get vector dimension size
    dimension = embeddings.shape[1]

    # Create FAISS index
    # IndexFlatL2 = exact search using L2 (euclidean) distance
    index = faiss.IndexFlatL2(dimension)

    # Add all vectors to the index
    index.add(embeddings)

    # Save FAISS index to file
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Save original chunks separately as pickle
    # FAISS only stores vectors, not the original text
    # So we save chunks in a .pkl file and match by position
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"Successfully stored {len(chunks)} chunks!")
    print(f"FAISS index saved to: {FAISS_INDEX_PATH}")
    print(f"Chunks saved to: {CHUNKS_PATH}")

# ─── Run ──────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    text = load_text(TEXT_PATH)
    chunks = split_into_chunks(text)
    model = load_embedding_model()
    embed_and_store(chunks, model)
    print("Done! Your knowledge base is ready.")
