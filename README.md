# 🧠 Local AI Code Reviewer
An intelligent code review assistant that runs locally using LangChain, Ollama, and ChromaDB — optimized for real pull requests and real codebases.

![screenshot or demo gif here]

---

## 🚀 Features
- 🔍 **Semantic code search** with line-level references (file + line number)
- 💬 **Local inference** using [Ollama](https://ollama.com/) + Mistral or Qwen
- 📦 **RAG-powered insights** using LangChain + ChromaDB
- 🧠 **Memory support** via LangGraph for contextual conversations
- ✅ **PR-aware architecture** ready for GitHub integration
- 🧼 **Clean codebase** following service-oriented architecture

---

## 🏗️ Architecture Overview
```
LocalRAG/
├── .env
├── .venv/
├── .gitignore
├── Makefile
├── README.md
├── requirements.txt
├── client.py
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── github.py
│   │   └── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github/
│   │   │   ├── __init__.py
│   │   │   └── pr_loader.py
│   │   ├── langchain/
│   │   │   ├── __init__.py
│   │   │   ├── chains.py
│   │   │   └── prompts.py
│   │   └── vectorstore/
│   │       ├── __init__.py
│   │       └── chroma.py
│   └── models/
│       ├── __init__.py
│       └── schemas.py
├── data/
│   └── vectorstore/

```

### Services
- VectorStoreService: Handles indexing and retrieval
- OllamaService: Local LLM client
- GitHubService: Pull request integration
- Memory: LangGraph nodes to manage chat history

---

## 🛠️ Tech Stack
- **LangChain** — RAG, memory, embedding abstraction
- **ChromaDB** — Vector database
- **Ollama** — Local LLM inference (Mistral, Qwen, etc.)
- **LangGraph** — Memory-aware multi-step conversations
- **FastAPI** — Lightweight API server
- **Python 3.10+**

---

## 📥 Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/local-ai-code-reviewer.git
cd local-ai-code-reviewer
pip install -r requirements.txt
```

### 2. Start Ollama
```bash
ollama run mistral
```
Or use:
```bash
ollama run qwen:7b
```

### 3. Embed Your Repo
```bash
python ingest_repo.py
```
*(Make sure your repo is inside the `repos/` folder)*

### 4. Launch the API
```bash
uvicorn chat_api:app --reload
```

### 5. Ask Questions
```bash
python client.py
```

## 📍 Referencing Code with File + Line
Each code chunk is enriched with metadata during ingestion:
```
// File: chat_api.py - Line: 47
@app.post("/ask")
async def ask_question(request: QuestionRequest):
```
This allows the agent to ground its feedback to the exact place in the code.

## 🔮 Coming Soon
* Web frontend (Streamlit or FastAPI + React)
* Auto-suggested review comments
* LLM self-evaluation for feedback quality
* Multi-agent code review (naming, perf, security, etc.)

## 🤝 Contributing
Contributions welcome! Feel free to open issues, PRs, or reach out on LinkedIn.

## 📜 License
This project is licensed under the MIT License.

## 📧 Contact
[linkedin](https://www.linkedin.com/in/sebastiandavila/)
