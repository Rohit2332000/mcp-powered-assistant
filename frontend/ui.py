import streamlit as st


def render_header():

    st.markdown(
        """
        <div class="main-header">
        <h1>🤖 LangGraph MCP Assistant</h1>
        <p>
        LangGraph • MCP • Tool Calling
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )