import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="qwen/qwen3.8-27b", groq_api_key=os.getenv("GROQ_API_KEY"))

def supervisor_agent(query: str, has_image: bool = False, history: list = None):
    """Determines the user intent and routes to the correct agent considering conversation history."""
    if has_image:
        return "disease_agent"
    
    context_str = ""
    if history:
        recent = history[-4:]
        context_str = "Recent Chat History:\n" + "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in recent]) + "\n\n"
    
    prompt = f"""
    You are an Agriculture Assistant Coordinator. 
    Based on the user query and chat history, identify the most suitable agent:
    - 'weather_agent': Current weather, rain, humidity, suitability for farming activities.
    - 'market_agent': Crop prices, market recommendations, mandi prices.
    - 'knowledge_agent': General farming advice, fertilizers, soil, pests, irrigation instructions.
    
    {context_str}Current User Query: '{query}'
    
    Reply with ONLY the agent name.
    """
    
    response = llm.invoke(prompt)
    intent = response.content.strip().lower()
    
    if "weather" in intent: return "weather_agent"
    if "market" in intent or "price" in intent: return "market_agent"
    if "disease" in intent or "identify" in intent: return "disease_agent"
    
    return "knowledge_agent"
