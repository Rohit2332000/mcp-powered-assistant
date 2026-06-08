import streamlit as st

from frontend.styles import CSS
from frontend.ui import render_header
from frontend.sidebar import render_sidebar
from frontend.chat import stream_response
from frontend.helpers import (
    generate_thread_id,
    add_thread
)

from backend.graph import retrieve_all_threads

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="LangGraph MCP Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# STYLES
# ==================================================

st.markdown(
    CSS,
    unsafe_allow_html=True
)

# ==================================================
# SESSION STATE
# ==================================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "thread_titles" not in st.session_state:
    st.session_state["thread_titles"] = {}

add_thread(st.session_state["thread_id"])

# ==================================================
# SIDEBAR
# ==================================================

render_sidebar()

# ==================================================
# HEADER
# ==================================================

render_header()

# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state["message_history"]:

    avatar = (
        "🧑‍💻"
        if message["role"] == "user"
        else "🤖"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

# ==================================================
# USER INPUT
# ==================================================

user_input = st.chat_input(
    "Ask me anything..."
)

if user_input:

    # Show user message
    with st.chat_message(
        "user",
        avatar="🧑‍💻"
    ):
        st.markdown(user_input)

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Thread title for first message
    current_thread = st.session_state["thread_id"]

    if current_thread not in st.session_state["thread_titles"]:

        title = user_input[:35]

        if len(user_input) > 35:
            title += "..."

        st.session_state["thread_titles"][
            current_thread
        ] = title

    config = {
        "configurable": {
            "thread_id":
            st.session_state["thread_id"]
        }
    }

    # Assistant response
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        response = stream_response(
            user_input,
            config
        )

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": response
        }
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Powered by LangGraph • MCP • Streamlit • Tool Calling"
)