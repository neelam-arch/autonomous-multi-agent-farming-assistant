import streamlit as st
import requests
import os
import json
from PIL import Image

# Set Page Config
st.set_page_config(
    page_title="AgriGPT",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide standard Streamlit header & footer */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Top Bar Header */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.5rem;
        background: #171717;
        border-bottom: 1px solid #2f2f2f;
        margin-top: -3.8rem;
        margin-left: -4rem;
        margin-right: -4rem;
        margin-bottom: 2rem;
    }

    .top-nav-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .top-nav-badge {
        background-color: #2f2f2f;
        color: #10a37f;
        border: 1px solid #10a37f44;
        padding: 3px 10px;
        border-radius: 16px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Chat Messages container */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 1.2rem 1.5rem !important;
        max-width: 52rem;
        margin: 0 auto;
    }

    /* Distinct background for Assistant */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #262626 !important;
        border-radius: 14px !important;
    }

    div[data-testid="stChatMessageContent"] {
        color: #ececec !important;
        font-size: 1rem;
        line-height: 1.65;
    }

    /* Primary Buttons */
    .stButton > button {
        width: 100%;
        background-color: #2f2f2f !important;
        color: #ececec !important;
        border: 1px solid #424242 !important;
        border-radius: 12px !important;
        padding: 0.65rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #383838 !important;
        border-color: #666666 !important;
        color: #ffffff !important;
    }

    /* Hero Page Title */
    .hero-container {
        text-align: center;
        max-width: 48rem;
        margin: 3.5rem auto 2rem auto;
    }

    .hero-icon {
        font-size: 3.2rem;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #9e9e9e;
        margin-bottom: 2rem;
    }

    /* Input box container styling */
    .stChatInputContainer {
        max-width: 52rem;
        margin: 0 auto;
    }

    .stChatInput > div {
        background-color: #2f2f2f !important;
        border: 1px solid #424242 !important;
        border-radius: 24px !important;
    }

    .stChatInput input {
        color: #ffffff !important;
    }

    /* Dark File Uploader Container */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #262626 !important;
        border: 1px dashed #424242 !important;
        border-radius: 10px !important;
    }

    .disclaimer-text {
        text-align: center;
        font-size: 0.75rem;
        color: #707070;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Tables & Code in dark mode */
    table {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border-collapse: collapse !important;
        border-radius: 8px !important;
    }
    th, td {
        border: 1px solid #333333 !important;
        padding: 8px 12px !important;
    }
    th {
        background-color: #2a2a2a !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Header
st.markdown("""
<div class="top-nav">
    <div class="top-nav-title">
        🌱 <span>AgriGPT</span>
        <span class="top-nav-badge">v4.0 • Qwen 3.8 & Gemini</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Sidebar Controls
with st.sidebar:
    st.markdown("### 💬 AgriGPT")
    
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("---")
    st.markdown("##### 📷 Crop Image Analysis")
    uploaded_file = st.file_uploader("Attach crop photo for disease check", type=["jpg", "jpeg", "png"], key="crop_uploader")
    
    if uploaded_file:
        st.image(uploaded_file, caption="📷 Attached Crop Photo", use_container_width=True)
        st.success("Photo attached! Ask any question about it.")

    st.markdown("---")
    st.markdown("##### ⚡ Capabilities")
    st.caption("• 🌿 Plant Disease Identification\n• 🌦️ Weather & Farming Forecasts\n• 📊 Mandi Crop Market Prices\n• 🧪 Soil & Fertilizer Guidance")
    
    st.markdown("---")
    st.caption("Powered by LangGraph & Groq API")

# Main Container
main_container = st.container()

# Check if prompt came from quick action button
user_prompt = st.chat_input("Message AgriGPT...")

if st.session_state.pending_prompt:
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# Render Welcome Hero Screen when chat is empty
if len(st.session_state.messages) == 0 and not user_prompt:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icon">🌱</div>
        <div class="hero-title">What can I help with today?</div>
        <div class="hero-subtitle">Ask anything about crop care, market prices, disease diagnosis, or weather alerts.</div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Quick Prompt Cards Grid
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌾 Best Fertilizer for Wheat\nRecommended NPK schedule & timing"):
            st.session_state.pending_prompt = "What is the best fertilizer program for wheat?"
            st.rerun()
        if st.button("🌦️ Weather Forecast & Irrigation\nCheck weather suitability for spraying"):
            st.session_state.pending_prompt = "What's the current weather in Delhi and is it good for irrigation?"
            st.rerun()

    with col2:
        if st.button("📊 Wheat Mandi Prices\nCheck latest market prices in Punjab"):
            st.session_state.pending_prompt = "Find the latest wheat mandi prices in Punjab."
            st.rerun()
        if st.button("🔬 Identify Crop Disease\nUpload leaf photo or describe symptoms"):
            st.session_state.pending_prompt = "How do I identify yellow rust in wheat crops?"
            st.rerun()

# Display Chat History
for msg in st.session_state.messages:
    avatar = "🌱" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=300)

# Process New User Message
if user_prompt:
    # Append user message
    user_msg_entry = {"role": "user", "content": user_prompt}
    if uploaded_file:
        user_msg_entry["image"] = uploaded_file

    st.session_state.messages.append(user_msg_entry)
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    # Fetch Assistant Response
    with st.chat_message("assistant", avatar="🌱"):
        with st.spinner("Thinking..."):
            try:
                files = None
                if uploaded_file:
                    files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                history_payload = []
                for m in st.session_state.messages[:-1]:
                    history_payload.append({"role": m["role"], "content": m["content"]})

                res = requests.post(
                    "http://localhost:8000/chat",
                    data={
                        "message": user_prompt,
                        "history": json.dumps(history_payload)
                    },
                    files=files
                )

                if res.status_code == 200:
                    answer = res.json().get("response", "No response received.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend Error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to AgriGPT backend: {str(e)}")

st.markdown('<div class="disclaimer-text">AgriGPT can make mistakes. Verify important agricultural advice.</div>', unsafe_allow_html=True)
