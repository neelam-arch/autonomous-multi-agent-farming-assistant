# 🌱 AgriGPT – Autonomous Multi-Agent Farming Assistant

AgriGPT is an AI-powered agricultural assistant that helps farmers with crop disease analysis, weather updates, mandi prices, and farming advice using AI agents.

## 🚀 Features

- 🔬 **Crop Disease Detection:** Analyze crop leaf images using Google Gemini Vision.
- 🌦️ **Weather Updates:** Get weather information using OpenWeatherMap API.
- 📊 **Mandi Prices:** Search agricultural market prices using Serper API.
- 🌾 **Farming Advice:** Get guidance on fertilizers, soil health, irrigation, and crop management.
- 🤖 **Multi-Agent System:** Uses LangGraph to route queries to specialized AI agents.
- 💬 **Interactive Chat Interface:** Built using Streamlit.
- ⚡ **REST API:** Built with FastAPI for backend communication.

## 🛠️ Technologies Used

- Python
- LangChain
- LangGraph
- Groq API
- Google Gemini Vision
- FastAPI
- Streamlit
- OpenWeatherMap API
- Serper Search API

## 📂 Project Structure

```text
AgriGPT/
├── agents/
│   ├── disease_agent.py
│   ├── knowledge_agent.py
│   ├── market_agent.py
│   ├── supervisor.py
│   └── weather_agent.py
├── utils/
│   └── tools.py
├── graph.py
├── main.py
├── streamlit_app.py
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/agrigpt.git
cd agrigpt
```

**2. Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure API keys**

Create a `.env` file and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
OPENWEATHER_API_KEY=your_weather_api_key
SERPER_API_KEY=your_serper_api_key
```

Never upload your actual API keys to GitHub.

## ▶️ Run the Project

**Start the FastAPI backend:**

```bash
python main.py
```

**Start the Streamlit frontend in another terminal:**

```bash
streamlit run streamlit_app.py
```

Open the application at:

`http://localhost:8501`

API documentation:

`http://localhost:8000/docs`

## 💡 Example Queries

- Identify a disease from a crop leaf image.
- What is the weather in my location?
- What are the current mandi prices for wheat?
- Which fertilizer is suitable for my crop?
- How can I improve soil health?

## 🎯 Project Objective

The goal of AgriGPT is to explore how multi-agent AI systems can make agricultural information more accessible and help farmers make informed farming decisions.

## 👩‍💻 Author

**Neelam Makode**

AI/ML Enthusiast | Generative AI | Agentic AI

---

⭐ If you find this project interesting, feel free to explore the repository!
