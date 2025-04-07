import sys
from pathlib import Path
from app.services.vectorstore.ingest_db_scripts.ingest_repo import load_source_files, split_documents, embed_and_store


def ingest_repo_from_path(repo_path: str):
    print("📥 Loading files from:", repo_path)
    docs = load_source_files(Path(repo_path))

    print("🔪 Splitting and cleaning...")
    chunks = split_documents(docs)

    print("📦 Embedding and storing...")
    embed_and_store(chunks)

    print("✅ Done ingesting repo.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a path to the repo.")
        sys.exit(1)

    path = sys.argv[1]
    ingest_repo_from_path(path)
