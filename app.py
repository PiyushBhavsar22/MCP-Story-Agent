import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

load_dotenv()

# Configure APIs
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
TavilyClient = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Select the model
