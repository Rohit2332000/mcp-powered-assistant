import queue
import streamlit as st

from backend.graph import (
    chatbot,
    submit_async_task
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)

def stream_response(
    user_input,
    config
):

    status_holder = {
        "box": None
    }

    def ai_only_stream():

        event_queue = queue.Queue()

        async def run_stream():

            try:

                async for chunk, metadata in chatbot.astream(

                    {
                        "messages": [
                            HumanMessage(
                                content=user_input
                            )
                        ]
                    },

                    config=config,

                    stream_mode="messages"
                ):

                    event_queue.put(
                        (
                            chunk,
                            metadata
                        )
                    )

            finally:

                event_queue.put(None)

        submit_async_task(
            run_stream()
        )

        while True:

            item = event_queue.get()

            if item is None:
                break

            chunk, metadata = item

            if isinstance(
                chunk,
                ToolMessage
            ):

                tool_name = getattr(
                    chunk,
                    "name",
                    "tool"
                )

                if status_holder["box"] is None:

                    status_holder[
                        "box"
                    ] = st.status(
                        f"⚡ Executing Tool: {tool_name}"
                    )

            if isinstance(
                chunk,
                AIMessage
            ):
                yield chunk.content

    return st.write_stream(
        ai_only_stream()
    )