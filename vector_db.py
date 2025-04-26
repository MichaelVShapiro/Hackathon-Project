import os
import faiss
import fitz
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

DOCUMENTS_DIR = "./documents/"
DB_DIR = "./db/"
DB_INDEX_FILE = "vector_index.faiss"
DOCS_PKL_FILE = "documents_metadata.pkl"
os.makedirs(DB_DIR, exist_ok=True)


def _extract_pdf_text(chunk_size=300):
    all_chunks = []
    metadata = []

    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            doc = fitz.open(filepath)
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()

            words = pdf_text.split()
            chunks = [
                ' '.join(words[i:i+chunk_size])
                for i in range(0, len(words), chunk_size)
            ]

            for chunk in chunks:
                all_chunks.append(chunk)
                metadata.append({
                    'source': filename,
                    'chunk_text': chunk
                })

    return all_chunks, metadata


def _build_db(text_chunks, metadata):
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedder.encode(text_chunks, batch_size=8, show_progress_bar=True).astype('float32')

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, os.path.join(DB_DIR, DB_INDEX_FILE))

    with open(os.path.join(DB_DIR, DOCS_PKL_FILE), "wb") as f:
        pickle.dump(metadata, f)

    print(f"Database saved with {len(text_chunks)} chunks")


def load_db():
    index = faiss.read_index(os.path.join(DB_DIR, DB_INDEX_FILE))
    with open(os.path.join(DB_DIR, DOCS_PKL_FILE), "rb") as f:
        metadata = pickle.load(f)
    return index, metadata


if __name__ == "__main__":
    chunks, metadata = _extract_pdf_text()
    _build_db(chunks, metadata)
