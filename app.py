import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

load_dotenv()

# Configure APIs
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Select the model
MODEL_INFO = "gemini-2.0-flash"
MODEL_SCRIPT = "gemini-2.5-flash"

st.set_page_config(
    page_title="MCP Story Agent",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Theme
st.markdown("""
    <style>
        :root {
            --black-1: #0f2027;
            --black-2: #203a43;
            --black-3: #2c5364;
            --blue-1: #06b6d4;
            --blue-2: #3b82f6;
            --blue-3: #2563eb;
        }
        .stApp {
            background: linear-gradient(135deg, var(--black-1), var(--black-2), var(--black-3));
            color: #f5f5f5;
        }
        h1, h2, h3 {
            text-align: center;
            color: #F9FAFB !important;
        }
        .stTextInput>div>div>input {
            border: 1px solid #6EE7B7 !important;
            border-radius: 10px;
            padding: 12px;
            background-color: #111827;
            color: white !important;
        }
        div.stButton > button {
            background: linear-gradient(90deg, var(--blue-1), var(--blue-2));
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            border: none;
            transition: 0.3s ease-in-out;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, var(--blue-3), var(--blue-1));
        }
        .card {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            margin-top: 20px;
        }
        .stRadio > div {
            justify-content: center;
        }
        footer, .stCaption {
            text-align: center;
            color: #9CA3AF;
        }
    </style>
""", unsafe_allow_html=True)

def get_realtime_info(query):
    try:
        resp = tavily_client.search(
            query = query,
            max_results = 3,
            topic = "general"
        )

        if resp and resp.get("results"):
            summaries = []
            for r in resp["results"]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")
                summaries.append(f"**{title}**\n\n{snippet}\n\n {url}")
            source_info = "\n\n---\n\n".join(summaries)
        else:
            source_info = f"No recent updates found on '{query}'."
    except Exception as e:
        st.error(f"Error fetching info: {e}")
        return None    
    
    # Refine & Summarize the content via Gemini
    prompt = f"""
You are a professional researcher and content creator with expertise in multiple fields.
Using the following real-time information, write an accurate, engaging, and human-like summary
for the topic: '{query}'.

Requirements:
- Keep it factual, insightful, and concise (around 200 words).
- Maintain a smooth, natural tone.
- Highlight key takeaways or trends.
- Avoid greetings or self-references.

Source information:
{source_info}

Output only the refined, human-readable content.
"""
    try:
        model = genai.GenerativeModel(MODEL_INFO)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else source_info

    except Exception as e:
        st.error(f"Error fetching info: {e}")
        return None

def main():
    st.markdown("<h1>🌐MCP Story Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#D1D5DB;'>Search any topic from world news to research trends and get AI-powered insights & video scripts instantly </p>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
