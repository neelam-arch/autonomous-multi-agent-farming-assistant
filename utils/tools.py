import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DATA_GOV_IN_API_KEY = os.getenv("DATA_GOV_IN_API_KEY")

def get_weather(location: str):
    """Fetch real-time weather for a given location."""
    if not location:
        return "Please provide a location (city/village/district)."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            return {
                "description": weather_desc,
                "temperature": f"{temp}°C",
                "humidity": f"{humidity}%",
                "wind_speed": f"{wind_speed} m/s",
                "location": data['name']
            }
        else:
            return f"Error fetching weather: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Weather API Error: {str(e)}"

def get_market_prices_from_google(commodity: str, location: str):
    """Fetch agricultural market prices by searching Google via Serper API."""
    if not commodity or not location:
        return "Please provide both commodity name and location."
    
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    
    query = f"current market price of {commodity} in {location} mandi today"
    payload = {"q": query}
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Combine snippets from search results
            results = data.get('organic', [])
            if not results:
                return f"No Google search results found for {commodity} prices in {location}."
            
            snippets = [r.get('snippet', '') for r in results[:3]]
            combined_info = "\n".join(snippets)
            return {
                "search_results": combined_info,
                "source": "Google Search via Serper"
            }
        else:
            return f"Error searching Google: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Search API Error: {str(e)}"
