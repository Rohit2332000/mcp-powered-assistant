import streamlit as st

from frontend.helpers import (
    reset_chat,
    get_thread_title,
    load_conversation
)

from langchain_core.messages import (
    HumanMessage,
)


def render_sidebar():

    st.sidebar.markdown(
        "# 🤖 MCP Assistant"
    )

    if st.sidebar.button(
        "➕ New Chat",
        use_container_width=True
    ):
        reset_chat()

    st.sidebar.markdown("---")

    st.sidebar.subheader(
        f"Conversations ({len(st.session_state['chat_threads'])})"
    )

    for thread_id in st.session_state[
        "chat_threads"
    ][::-1]:

        title = get_thread_title(
            thread_id
        )

        if st.sidebar.button(
            f"💬 {title}",
            key=f"thread_{thread_id}",
            use_container_width=True
        ):

            st.session_state[
                "thread_id"
            ] = thread_id

            messages = load_conversation(
                thread_id
            )

            temp = []

            for msg in messages:

                role = (
                    "user"
                    if isinstance(
                        msg,
                        HumanMessage
                    )
                    else "assistant"
                )

                temp.append(
                    {
                        "role": role,
                        "content": msg.content
                    }
                )

            st.session_state[
                "message_history"
            ] = temp