from pathlib import Path

from app.services.vectorstore.chroma import reset_vectorstore, load_source_files, split_documents, embed_and_store

# Configuration
REPO_DIR = Path("repos/")

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
