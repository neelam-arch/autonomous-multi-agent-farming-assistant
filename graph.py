from typing import TypedDict, Optional, List, Dict
from langgraph.graph import StateGraph, END
from agents.supervisor import supervisor_agent
from agents.disease_agent import identify_disease
from agents.weather_agent import weather_agent
from agents.market_agent import market_agent
from agents.knowledge_agent import knowledge_agent

class AgentState(TypedDict):
    query: str
    image_path: Optional[str]
    history: Optional[List[Dict[str, str]]]
    response: str
    next_agent: str

def supervisor_node(state: AgentState):
    has_image = True if state.get("image_path") else False
    history = state.get("history", [])
    next_agent = supervisor_agent(state["query"], has_image, history=history)
    return {"next_agent": next_agent}

def disease_node(state: AgentState):
    response = identify_disease(state["image_path"], state["query"])
    return {"response": response}

def weather_node(state: AgentState):
    history = state.get("history", [])
    response = weather_agent(state["query"], history=history)
    return {"response": response}

def market_node(state: AgentState):
    history = state.get("history", [])
    response = market_agent(state["query"], history=history)
    return {"response": response}

def knowledge_node(state: AgentState):
    history = state.get("history", [])
    response = knowledge_agent(state["query"], history=history)
    return {"response": response}

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("disease_agent", disease_node)
workflow.add_node("weather_agent", weather_node)
workflow.add_node("market_agent", market_node)
workflow.add_node("knowledge_agent", knowledge_node)

# Define edges
workflow.set_entry_point("supervisor")

def router(state: AgentState):
    return state["next_agent"]

workflow.add_conditional_edges(
    "supervisor",
    router,
    {
        "disease_agent": "disease_agent",
        "weather_agent": "weather_agent",
        "market_agent": "market_agent",
        "knowledge_agent": "knowledge_agent"
    }
)

workflow.add_edge("disease_agent", END)
workflow.add_edge("weather_agent", END)
workflow.add_edge("market_agent", END)
workflow.add_edge("knowledge_agent", END)

# Compile
app = workflow.compile()

def run_agriculture_assistant(query: str, image_path: str = None, history: list = None):
    initial_state = {
        "query": query,
        "image_path": image_path,
        "history": history or [],
        "response": "",
        "next_agent": ""
    }
    result = app.invoke(initial_state)
    return result["response"]
