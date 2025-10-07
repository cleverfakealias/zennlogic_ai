from __future__ import annotations

"""LangGraph definition for the local RAG-enabled agent."""

from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import RunnableConfig

from app.agents.llm import get_chat_model
from app.tools import rag


class AgentState(TypedDict):
    """State definition for the LangGraph agent."""

    messages: Annotated[list[BaseMessage], add_messages]


@tool
def rag_tool(query: str) -> str:
    """Search the local document index for passages related to the query."""

    return rag.search(query)


def _call_model(state: AgentState, config: RunnableConfig | None = None) -> AgentState:
    """Invoke the chat model with tool support and append the response."""

    model = get_chat_model().bind_tools([rag_tool])
    response = model.invoke(state.get("messages", []), config=config)
    return {"messages": [response]}


def build_graph() -> StateGraph:
    """Build and compile the single-step LangGraph agent."""

    graph = StateGraph(AgentState)
    graph.add_node("model", _call_model)
    graph.add_edge(START, "model")
    graph.add_edge("model", END)
    return graph


_GRAPH = build_graph().compile()


def run_agent(messages: Sequence[BaseMessage | str], *, config: RunnableConfig | None = None) -> list[BaseMessage]:
    """Execute the compiled LangGraph agent with the provided messages."""

    normalized_messages = _normalize_messages(messages)
    output = _GRAPH.invoke({"messages": normalized_messages}, config=config)
    return list(output["messages"])


def _normalize_messages(messages: Sequence[BaseMessage | str]) -> list[BaseMessage]:
    """Ensure all provided messages conform to LangChain message objects."""

    normalized: list[BaseMessage] = []
    for item in messages:
        if isinstance(item, BaseMessage):
            normalized.append(item)
        else:
            normalized.append(HumanMessage(content=str(item)))
    return normalized
