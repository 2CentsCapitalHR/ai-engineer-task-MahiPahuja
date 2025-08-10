import os
import chromadb
from chromadb.utils import embedding_functions
from src.tools.doc_parser import parse_raw_folder, read_docx_text, read_pdf_text
from src.tools.checklist import check_required_documents

# Path to ChromaDB storage
CHROMA_PATH = os.path.join("data", "chroma_db")

# ✅ Use the new Chroma PersistentClient
client = chromadb.PersistentClient(path=CHROMA_PATH)

# SentenceTransformer embedding function
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create / get Chroma collection
collection = client.get_or_create_collection(
    name="adgm_docs",
    embedding_function=embedding_fn
)

def ingest_documents(raw_folder):
    """Reads documents from raw folder and stores embeddings in Chroma."""
    detected_docs = parse_raw_folder(raw_folder)

    for filename, doc_type in detected_docs.items():
        file_path = os.path.join(raw_folder, filename)

        if filename.lower().endswith(".docx"):
            content = read_docx_text(file_path)
        elif filename.lower().endswith(".pdf"):
            content = read_pdf_text(file_path)
        else:
            continue  # Skip unsupported formats

        if content.strip():
            collection.add(
                ids=[filename],
                documents=[content],
                metadatas=[{"type": doc_type}],
            )

    print("✅ Ingestion complete.")
    return detected_docs

if __name__ == "__main__":
    RAW_FOLDER = os.path.join("data", "raw")

    # Step 1 — Ingest into Chroma
    ingest_documents(RAW_FOLDER)

    # Step 2 — Run checklist
    result = check_required_documents(RAW_FOLDER)

    print("\n📄 Found document types:")
    for doc in result["found"]:
        print(f"  - {doc}")

    print("\n❌ Missing document types:")
    for doc in result["missing"]:
        print(f"  - {doc}")
