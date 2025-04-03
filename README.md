# 🧠 PR Insight Agent
This project is a RAG (Retrieval-Augmented Generation) based assistant that allows you to:
- Load the content of a GitHub Pull Request
- Analyze it within the complete context of the system
- Ask technical questions about the PR or the codebase
- Generate automatic code reviews with traceability via Langfuse
---
## 🚀 Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) running locally (`ollama run mistral`)
- A [Langfuse](https://cloud.langfuse.com/) account for traceability
---
## ⚙️ Installation
```bash
git clone https://github.com/your-username/pr-insight-agent.git
cd pr-insight-agent
# Install dependencies
pip install -r requirements.txt
# Configure credentials
cp .env.template .env  # and edit with your Langfuse keys
```

## 🧪 Usage
1. Start the backend
```bash
uvicorn chat_api:app --reload
```

2. Launch the client
```bash
python client.py
```

3. Available commands
- `load`: Load a Pull Request by number, user and repo
- `review`: Generate a technical review of the PR
- `exit`: Exit the client
- Type any technical question about the PR or the base system

## 📦 Project Structure
```
.
├── app/chat_api.py          # FastAPI backend with /ask, /load_pr, /review_pr endpoints
├── app/client.py            # CLI to interact with the agent
├── app/langfuse_config.py   # Global Langfuse configuration
├── app/prompting.py         # Base and review prompts
├── app/memory/              # Download and parsing of PRs from GitHub
├── cognition/           # Code ingestion and embedding
├── data/vectorstore/    # Persistent semantic base (auto-generated)
├── repos/               # Temporary PR files (auto-generated)
└── .env                 # Your private keys (do not upload)
```

## 📊 Langfuse
The project generates automatic traces of each model interaction at:
https://cloud.langfuse.com

You will see:
- Prompts sent
- Generated responses
- Execution time
- Errors and additional metadata

## 🛡️ Security
- Do not upload .env to Git.
- Do not share your vectorstore if it contains private code.