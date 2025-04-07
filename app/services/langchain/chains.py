from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from app.services.langchain.prompts import chat_prompt, review_prompt
from app.services.ollama.call_ollama import call_ollama
from app.services.vectorstore.chroma import retrieve_relevant_context


def create_rag_graph(prompt_template: ChatPromptTemplate):
    async def call_model(state: MessagesState):
        messages = state["messages"]
        last_question = messages[-1].content

        context = retrieve_relevant_context(question=last_question, k=5)

        prompt = prompt_template.invoke({"messages": messages, "context": context})

        response = await call_ollama(prompt)
        return {"messages": [AIMessage(content=response)]}

    builder = StateGraph(MessagesState)
    builder.add_node("model", call_model)
    builder.add_edge(START, "model")

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


ask_graph = create_rag_graph(chat_prompt)
review_graph = create_rag_graph(review_prompt)
