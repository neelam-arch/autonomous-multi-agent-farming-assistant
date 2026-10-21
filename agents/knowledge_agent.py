import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="qwen/qwen3.8-27b", groq_api_key=os.getenv("GROQ_API_KEY"))

def knowledge_agent(query: str, history: list = None):
    """Handles general agriculture questions with conversation memory."""
    system_prompt = """
    You are an expert Agricultural Advisor with deep knowledge of:
    - Fertilizer and soil health
    - Irrigation techniques
    - Crop rotation and variety selection
    - Pest and disease prevention (general)
    - Sustainable farming practices
    Provide detailed, practical, and easy-to-follow advice.
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        for m in history:
            role = "assistant" if m.get("role") == "assistant" else "user"
            messages.append({"role": role, "content": m.get("content", "")})
    else:
        messages.append({"role": "user", "content": query})
        
    response = llm.invoke(messages)
    return response.content
