import os
from langchain_groq import ChatGroq
from utils.tools import get_market_prices_from_google
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="qwen/qwen3.8-27b", groq_api_key=os.getenv("GROQ_API_KEY"))

def market_agent(query: str, commodity: str = None, location: str = None, history: list = None):
    """Handles market price queries with history awareness."""
    if not commodity or not location:
        ctx = ""
        if history:
            recent = history[-4:]
            ctx = "Recent Conversation Context:\n" + "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in recent]) + "\n\n"
        
        prompt = f"{ctx}Extract the commodity name and district/location from this query and conversation history: '{query}'. Format as 'Commodity: [name], Location: [location]'. If either is missing and cannot be found in history, say 'MISSING_INFO'."
        response = llm.invoke(prompt)
        info = response.content.strip()
        
        if "MISSING_INFO" in info or "Commodity: " not in info:
            return "Please provide both the crop name and your district/location to get market prices."
        
        # Simple parsing logic
        try:
            parts = info.split(",")
            commodity = parts[0].split(": ")[1].strip()
            location = parts[1].split(": ")[1].strip()
        except:
            return "Could not understand the crop or location. Please specify them clearly."

    price_data = get_market_prices_from_google(commodity, location)
    
    if isinstance(price_data, str):
        return price_data
    
    # Format response using LLM
    report_prompt = f"The Google Search results for {commodity} market prices in {location} are: {price_data['search_results']}. Extract the most relevant price information (min, max, or modal if mentioned) and provide a clear summary for the farmer. Mention that this data is sourced via Google Search."
    summary = llm.invoke(report_prompt)
    
    return summary.content
