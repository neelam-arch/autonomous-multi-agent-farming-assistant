import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"), api_version="v1")

def identify_disease(image_path: str, user_query: str = ""):
    """Identify crop disease from an image using Gemini Vision API via LangChain."""
    try:
        prompt = """
        You are an expert Agricultural Pathologist. 
        Analyze the provided image of a crop and identify any disease or pest issues.
        Return the information in the following format:
        1. Disease/Issue Name
        2. Description & Causes
        3. Severity Level
        4. Treatment Suggestions (Pesticides, Fertilizers, Organic methods)
        5. Prevention Steps
        
        Be scientific yet easy for a farmer to understand.
        """
        if user_query:
            prompt += f"\nUser specifically asked: {user_query}"
            
        # For LangChain Google GenAI, we pass image content as part of the message
        import base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
            
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}"},
            ]
        )
        
        response = llm.invoke([message])
        return response.content
    except Exception as e:
        return f"Error in disease detection: {str(e)}"
