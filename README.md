# 🤖 LangGraph MCP Assistant

An AI-powered conversational assistant built using LangGraph, MCP (Model Context Protocol), Groq LLMs, and Streamlit.

The assistant intelligently routes user requests to specialized tools, supports persistent chat memory, tool execution, and multi-conversation management.

<img width="1908" height="920" alt="Screenshot_17-10-2026_13017_drive google com" src="https://github.com/user-attachments/assets/8d1e58d8-03fa-40dc-8469-1791d075bab7" />



<img width="1912" height="916" alt="Screenshot_17-10-2026_1318_drive google com" src="https://github.com/user-attachments/assets/34619b4a-bb93-4ec8-969a-61f5ea894fd8" />



<img width="1910" height="911" alt="Screenshot_17-10-2026_13143_drive google com" src="https://github.com/user-attachments/assets/18a48ff0-8d2b-4893-9cb5-30cea12ba34b" />



---

## 🚀 Features

### 💬 Conversational AI

* Powered by Groq LLMs
* Multi-turn conversations
* Persistent memory using SQLite

### 🔧 Tool Calling

* DuckDuckGo Web Search
* Stock Price Lookup
* Weather Information
* Local Events Finder
* MCP-based External Tools

### 🧠 Agentic Workflow

* LangGraph State Management
* Conditional Tool Routing
* Dynamic Tool Invocation
* Memory-Aware Conversations

### 📂 Multi-Thread Chat

* Multiple conversation threads
* Automatic chat history persistence
* Thread switching support

### ⚡ Streaming Responses

* Real-time token streaming
* Tool execution status updates
* Interactive user experience

---

## 🏗️ Architecture

User
↓
Streamlit Frontend
↓
LangGraph Workflow
↓
LLM Router
├── Direct Response
└── Tool Calling
├── Search Tool
├── Weather Tool
├── Stock Tool
├── Events Tool
└── MCP Tools
↓
SQLite Memory

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* LangGraph
* LangChain

### LLMs

* Groq

  * llama-3.1-8b-instant
  * gpt-oss-120b

### Memory

* SQLite
* LangGraph Checkpointer

### Tools

* DuckDuckGo Search
* OpenWeather API
* Alpha Vantage API
* SerpAPI Events
* MCP Servers

---

## 📁 Project Structure

project/

├── app.py

├── backend/

│ ├── config.py

│ ├── graph.py

│ ├── state.py

│ ├── tools.py

│ └── **init**.py

├── frontend/

│ ├── chat.py

│ ├── sidebar.py

│ ├── helpers.py

│ ├── styles.py

│ ├── ui.py

│ └── **init**.py

├── data/

│ └── chatbot.db

├── requirements.txt

├── .env.example

└── README.md

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/langgraph-mcp-assistant.git

cd langgraph-mcp-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=

ALPHA_VANTAGE_API_KEY=

OPENWEATHER_API_KEY=

SERPAPI_API_KEY=

UVX_PATH=

MATH_MCP_PATH=

EXPENSE_MCP_PATH=

MANIM_MCP_PATH=
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

Add screenshots of:

* Main Chat Interface
* Tool Execution Status
* Multiple Conversations
* MCP Tool Usage

Example:

```markdown
![Chat UI](screenshots/chat_ui.png)
```

---

## 🎯 Future Improvements

* RAG Integration
* Voice Assistant
* Multi-Agent Collaboration
* Authentication
* Docker Deployment
* Cloud Deployment
* Observability & Tracing

---

## 👨‍💻 Author

Rohit Kumar Yadav

AI Engineer | Generative AI | Agentic AI | Machine Learning

LinkedIn: https://linkedin.com/in/your-profile

GitHub: https://github.com/your-username
