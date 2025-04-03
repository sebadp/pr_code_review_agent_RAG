import os
import shutil
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from tqdm import tqdm

# Configuration
REPO_DIR = Path("repos/")
VECTOR_STORE_DIR = Path("data/vectorstore/")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def reset_vectorstore():
    if VECTOR_STORE_DIR.exists():
        print(f"⚠️ Deleting old vector store at {VECTOR_STORE_DIR}")
        shutil.rmtree(VECTOR_STORE_DIR)
    else:
        print("✅ Vector store already clean.")

def load_source_files(repo_path: Path) -> List[Document]:
    loader = DirectoryLoader(
        str(repo_path),
        glob="**/*.py",
        loader_cls=TextLoader,
        show_progress=True
    )
    docs = loader.load()

    # Filter out __init__, tests, and very small files
    filtered = []
    for doc in docs:
        source = doc.metadata["source"]
        if "__init__" in source or "test" in source.lower():
            continue
        if len(doc.page_content.strip()) < 50:
            continue
        filtered.append(doc)

    print(f"📄 Loaded {len(filtered)} source files after filtering:")
    for d in filtered:
        print("   •", d.metadata["source"])
    return filtered

def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)

    # Remove empty or semantically irrelevant chunks
    clean_chunks = [
        c for c in chunks
        if len(c.page_content.strip()) > 50 and any(char.isalpha() for char in c.page_content)
    ]
    print(f"🔪 Created {len(clean_chunks)} chunks after cleanup.")
    return clean_chunks

def embed_and_store(chunks: List[Document]):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_STORE_DIR)
    )
    db.persist()
    print(f"✅ Stored vector store in {VECTOR_STORE_DIR}")

def main():
    if not REPO_DIR.exists():
        print(f"❌ Repo directory not found at {REPO_DIR}")
        return

    reset_vectorstore()

    print("📥 Loading source code files...")
    docs = load_source_files(REPO_DIR)

    print("🧠 Splitting and cleaning chunks...")
    chunks = split_documents(docs)

    print("📦 Embedding and storing chunks...")
    embed_and_store(chunks)

    print("🎉 Completed successfully!")

if __name__ == "__main__":
    main()
