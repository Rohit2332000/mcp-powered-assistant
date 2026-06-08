import uuid
import streamlit as st

from backend.graph import chatbot
from langchain_core.messages import HumanMessage


def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):

    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():

    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id

    add_thread(thread_id)

    st.session_state["message_history"] = []


def load_conversation(thread_id):

    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get(
        "messages",
        []
    )


def get_thread_title(thread_id):

    try:

        if (
            thread_id
            in st.session_state["thread_titles"]
        ):
            return st.session_state["thread_titles"][thread_id]

        messages = load_conversation(
            thread_id
        )

        for msg in messages:

            if isinstance(msg, HumanMessage):

                title = msg.content[:35]

                st.session_state[
                    "thread_titles"
                ][thread_id] = title

                return title

        return "New Chat"

    except Exception:
        return "New Chat"