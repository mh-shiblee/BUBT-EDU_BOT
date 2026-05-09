from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


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
    chunks = splitter.split_text(text)
    return chunks


# ─── Save chunks to a file so you can inspect them ───────────────────────────

def save_chunks(chunks, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- CHUNK {i+1} ---\n")
            f.write(chunk)
            f.write("\n\n")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    text = load_text("data/bubt_clean_text.txt")
    chunks = split_into_chunks(text)
    save_chunks(chunks, "data/bubt_chunks.txt")
