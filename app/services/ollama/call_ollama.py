from langchain_core.prompt_values import PromptValue
from langchain_ollama import ChatOllama
import asyncio

from fastapi import HTTPException

from app.core.config import OLLAMA_MODEL, logger, OLLAMA_URL
from app.core.langfuse_config import langfuse


async def call_ollama(
    prompt: PromptValue, retries: int = 3, backoff: float = 1.5
) -> str:
    """Call Ollama with retry logic using LangChain's OllamaLLM."""
    trace = langfuse.trace(name="ollama_call", input=prompt)
    span = trace.span(name="ollama_request")

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL,
        timeout=600,
    )

    for attempt in range(retries):
        try:
            logger.info(f"[Ollama] Sending prompt (attempt {attempt + 1})...")
            result = await llm.ainvoke(prompt)
            span.end(output=result)
            logger.info("[Ollama] Response received successfully")
            return result.content
        except Exception as e:
            logger.warning(f"[Ollama] Error: {e}")
            if attempt < retries - 1:
                logger.info(
                    f"[Ollama] Retrying in {backoff * (attempt + 1)} seconds..."
                )
                await asyncio.sleep(backoff * (attempt + 1))
            else:
                span.end(output="FAILED", metadata={"error": str(e)})
                raise HTTPException(
                    status_code=502,
                    detail="Ollama is not responding after multiple attempts.",
                )
