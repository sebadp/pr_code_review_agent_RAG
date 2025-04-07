import shutil
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.core.config import EMBEDDING_MODEL, VECTOR_STORE_DIR


# Load vector store
embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding)


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
        str(repo_path), glob="**/*.py", loader_cls=TextLoader, show_progress=True
    )
    docs = loader.load()

    # Filter out __init__, tests
    filtered = []
    for doc in docs:
        source = doc.metadata["source"]
        if "__init__" in source or "test" in source.lower():
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
        separators=["\n\n", "\n", " ", ""],
    )

    all_chunks = []
    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        original_text = doc.page_content

        chunks = splitter.split_text(original_text)

        current_pos = 0
        for chunk_text in chunks:
            relative_pos = original_text.find(chunk_text, current_pos)
            if relative_pos == -1:
                start_line = "?"
            else:
                start_line = original_text[:relative_pos].count("\n") + 1
                current_pos = relative_pos + len(chunk_text)

            chunk_doc = Document(
                page_content=chunk_text,
                metadata={"source": source, "start_line": start_line},
            )
            all_chunks.append(chunk_doc)

    print(f"🔪 Created {len(all_chunks)} chunks after cleanup.")
    return all_chunks


def embed_and_store(chunks: List[Document]):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=str(VECTOR_STORE_DIR)
    )
    db.persist()
    print(f"✅ Stored vector store in {VECTOR_STORE_DIR}")


def retrieve_relevant_context(question: str, k: int) -> str:
    """
    Retrieve relevant context from the vector store based on the question.
    Args:
        question (str): The question to search for.
        k (int): The number of relevant documents to retrieve.
    """
    results = vectorstore.similarity_search(question, k=k)
    context = "\n\n".join([format_doc(doc) for doc in results])
    return context


def format_doc(doc):
    source = doc.metadata.get("source", "unknown")
    line = doc.metadata.get("start_line", "?")
    return f"// File: {source} - Line: {line}\n{doc.page_content.strip()}"
