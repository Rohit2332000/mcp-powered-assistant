import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

chat_llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

tool_llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

ALPHA_VANTAGE_API_KEY = os.getenv(
    "ALPHA_VANTAGE_API_KEY"
)

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

SERPAPI_API_KEY = os.getenv(
    "SERPAPI_API_KEY"
)

UVX_PATH = os.getenv("UVX_PATH")

MATH_MCP_PATH = os.getenv(
    "MATH_MCP_PATH"
)

EXPENSE_MCP_PATH = os.getenv(
    "EXPENSE_MCP_PATH"
)

MANIM_MCP_PATH = os.getenv(
    "MANIM_MCP_PATH"
)