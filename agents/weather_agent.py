import os
from langchain_groq import ChatGroq
from utils.tools import get_weather
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="qwen/qwen3.8-27b", groq_api_key=os.getenv("GROQ_API_KEY"))

def weather_agent(query: str, location: str = None, history: list = None):
    """Handles weather-related queries with context memory."""
    if not location:
        ctx = ""
        if history:
            recent = history[-4:]
            ctx = "Recent Conversation Context:\n" + "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in recent]) + "\n\n"
        
        prompt = f"{ctx}Extract the city or location from this query/conversation: '{query}'. If no location is mentioned anywhere, reply exactly with 'LOCATION_REQUIRED'."
        response = llm.invoke(prompt)
        extracted_location = response.content.strip()
        
        if "LOCATION_REQUIRED" in extracted_location:
            return "Could you please specify your city, village, or district for the weather report?"
        location = extracted_location

    weather_data = get_weather(location)
    
    if isinstance(weather_data, str):
        return weather_data
    
    report_prompt = f"The weather data for {location} is: {weather_data}. Query: '{query}'. Provide helpful agricultural advice based on this weather (e.g., is it a good time for irrigation or pesticides?)."
    advice = llm.invoke(report_prompt)
    
    return f"Weather in {location}: {weather_data['description']}, {weather_data['temperature']}. \n\nAdvice: {advice.content}"
    
if __name__ == "__main__":
    print(weather_agent("What's the weather like?", "Delhi"))
