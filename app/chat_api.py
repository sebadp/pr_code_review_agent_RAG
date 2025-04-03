from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.models.schemas import LoadPRRequest, ReviewPRRequest
from app.prompting import ask_prompt, review_prompt
from .memory.github_pr_loader import download_pr_files
from .cognition.ingest_one_repo import ingest_repo_from_path

import httpx
import asyncio
import logging
from .langfuse_config import langfuse

app = FastAPI()

# Config
VECTOR_STORE_DIR = "data/vectorstore"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load vector store
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embedding)


class QuestionRequest(BaseModel):
    question: str

# Retry helper
async def call_ollama(prompt: str, retries: int = 3, backoff: float = 1.5) -> str:
    trace = langfuse.trace(name="ollama_call", input=prompt)
    span = trace.span(name="ollama_request")

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                logger.info(f"[Ollama] Sending prompt (attempt {attempt + 1})...")
                response = await client.post(OLLAMA_URL, json=payload, timeout=600.0)
                logger.info(f"[Ollama] Response status: {response.status_code}")
                response.raise_for_status()
                result = response.json()["response"]
                span.end(output=result)
                return result
            except Exception as e:
                logger.warning(f"[Ollama] Error: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(backoff * (attempt + 1))
                else:
                    span.end(output="FAILED", metadata={"error": str(e)})
                    trace.end()
                    raise HTTPException(status_code=502, detail="Ollama is not responding.")
        span.end(output="FAILED", metadata={"error": "Max retries exceeded"})
        raise HTTPException(status_code=502, detail="Ollama is not responding.")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    trace = langfuse.trace(name="ask_question", input=request.model_dump())
    span = trace.span(name="ask_request")
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"[User] Question: {question}")

    # Semantic search
    try:
        results = vectorstore.similarity_search(question, k=5)
        context = "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        logger.error(f"[Vectorstore] Search failed: {e}")
        raise HTTPException(status_code=500, detail="Vector store failed")

    prompt = ask_prompt.format(context=context, question=question)

    # Call Ollama with retries
    answer = await call_ollama(prompt)
    span.end(output=answer)

    return {"answer": answer}

@app.post("/load_pr")
async def load_pull_request(req: LoadPRRequest):
    logger.info(f"[Load PR] Loading PR #{req.pr_number} from {req.owner}/{req.repo}")
    try:
        repo_path = download_pr_files(req.owner, req.repo, req.pr_number)
        ingest_repo_from_path(repo_path)
        return {"status": "ok", "repo_path": repo_path}
    except Exception as e:
        logger.error(f"[Load PR] Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/review_pr")
async def review_pr(request: ReviewPRRequest):
    trace = langfuse.trace(name="review_pr", input=request.model_dump())
    span = trace.span(name="review_request")
    logger.info("[User] Code review requested")

    try:
        results = vectorstore.similarity_search(request.question, k=10)
        context = "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        logger.error(f"[Vectorstore] Search failed: {e}")
        raise HTTPException(status_code=500, detail="Vector store failed")

    prompt = review_prompt.format(context=context, question=request.question)
    answer = await call_ollama(prompt)
    span.end(output=answer)
    return {"review": answer}
