from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from ..models.schemas import QuestionRequest, LoadPRRequest, ReviewPRRequest
from ...core.config import logger
from ...core.langfuse_config import langfuse
from ...services.github.github_pr_loader import download_pr_files
from ...services.langchain.chains import ask_graph, review_graph

from ...services.vectorstore.ingest_db_scripts.ingest_one_repo import (
    ingest_repo_from_path,
)

router = APIRouter()


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    trace = langfuse.trace(name="ask_question", input=request.model_dump())
    span = trace.span(name="ask_request")
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"[User] Question: {question}")
    config = {"configurable": {"thread_id": "ask-user-1"}}
    messages = [HumanMessage(content=request.question)]
    output = await ask_graph.ainvoke({"messages": messages}, config)

    span.end(output=output)

    return {"answer": output["messages"][-1].content}


@router.post("/load_pr")
async def load_pull_request(req: LoadPRRequest):
    logger.info(f"[Load PR] Loading PR #{req.pr_number} from {req.owner}/{req.repo}")
    try:
        repo_path = download_pr_files(req.owner, req.repo, req.pr_number)
        ingest_repo_from_path(repo_path)
        return {"status": "ok", "repo_path": repo_path}
    except Exception as e:
        logger.error(f"[Load PR] Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review_pr")
async def review_pr(request: ReviewPRRequest):
    trace = langfuse.trace(name="review_pr", input=request.model_dump())
    span = trace.span(name="review_request")
    logger.info("[User] Code review requested")

    config = {"configurable": {"thread_id": "ask-user-1"}}
    messages = [HumanMessage(content=request.question)]
    output = await review_graph.ainvoke({"messages": messages}, config)

    span.end(output=output)
    return {"review": output}
