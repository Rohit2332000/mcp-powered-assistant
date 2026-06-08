import asyncio
import threading
import aiosqlite

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)

from langgraph.checkpoint.sqlite.aio import (
    AsyncSqliteSaver
)

from langchain_core.messages import (
    HumanMessage
)

from langchain_mcp_adapters.client import (
    MultiServerMCPClient
)

from backend.state import ChatState

from backend.config import (
    chat_llm,
    tool_llm,
    UVX_PATH,
    MATH_MCP_PATH,
    EXPENSE_MCP_PATH,
    MANIM_MCP_PATH
)

from backend.tools import (
    search_tool,
    get_stock_price,
    get_weather,
    find_local_events
)

# ==================================================
# ASYNC LOOP
# ==================================================

_ASYNC_LOOP = asyncio.new_event_loop()

_ASYNC_THREAD = threading.Thread(
    target=_ASYNC_LOOP.run_forever,
    daemon=True
)

_ASYNC_THREAD.start()


def _submit_async(coro):
    return asyncio.run_coroutine_threadsafe(
        coro,
        _ASYNC_LOOP
    )


def run_async(coro):
    return _submit_async(coro).result()


def submit_async_task(coro):
    return _submit_async(coro)

# ==================================================
# MCP CLIENT
# ==================================================

client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": UVX_PATH,
            "args": [
                "--with",
                "fastmcp",
                "fastmcp",
                "run",
                MATH_MCP_PATH
            ]
        },

        "Expense": {
            "transport": "stdio",
            "command": UVX_PATH,
            "args": [
                "--with",
                "fastmcp",
                "fastmcp",
                "run",
                EXPENSE_MCP_PATH
            ]
        },

        "manim-server": {
            "transport": "stdio",
            "command": "python",
            "args": [
                MANIM_MCP_PATH
            ]
        }
    }
)

# ==================================================
# LOAD MCP TOOLS
# ==================================================

def load_mcp_tools():

    try:
        return run_async(
            client.get_tools()
        )

    except Exception:
        return []


mcp_tools = load_mcp_tools()

# ==================================================
# TOOL REGISTRATION
# ==================================================

tools = [
    search_tool,
    get_stock_price,
    get_weather,
    find_local_events,
    *mcp_tools
]

llm_with_tools = (
    tool_llm.bind_tools(tools)
    if tools
    else tool_llm
)

# ==================================================
# TOOL DETECTION
# ==================================================

def needs_tool(user_text: str):

    text = user_text.lower()

    tool_keywords = [
        "search",
        "find",
        "lookup",
        "latest",
        "current",
        "news",
        "today",
        "stock",
        "share",
        "price",
        "expense",
        "add expense",
        "delete expense",
        "update expense",
        "list expense",
        "calculate",
        "math",
        "multiply",
        "divide",
        "subtract",
        "addition",
        "manim",
        "animation",
        "render"
    ]

    return any(
        keyword in text
        for keyword in tool_keywords
    )

# ==================================================
# CHAT NODE
# ==================================================

async def chat_node(state: ChatState):

    messages = state["messages"]

    last_message = messages[-1]

    if isinstance(
        last_message,
        HumanMessage
    ):

        if not needs_tool(
            last_message.content
        ):

            response = await (
                chat_llm.ainvoke(messages)
            )

            return {
                "messages": [response]
            }

    response = await (
        llm_with_tools.ainvoke(messages)
    )

    return {
        "messages": [response]
    }

# ==================================================
# TOOL NODE
# ==================================================

tool_node = ToolNode(tools)

# ==================================================
# CHECKPOINTER
# ==================================================

async def init_checkpointer():

    conn = await aiosqlite.connect(
        "data/chatbot.db"
    )

    return AsyncSqliteSaver(conn)


checkpointer = run_async(
    init_checkpointer()
)

# ==================================================
# LANGGRAPH
# ==================================================

graph = StateGraph(ChatState)

graph.add_node(
    "chat_node",
    chat_node
)

graph.add_node(
    "tools",
    tool_node
)

graph.add_edge(
    START,
    "chat_node"
)

graph.add_conditional_edges(
    "chat_node",
    tools_condition
)

graph.add_edge(
    "tools",
    "chat_node"
)

chatbot = graph.compile(
    checkpointer=checkpointer
)

# ==================================================
# THREAD HISTORY
# ==================================================

async def _alist_threads():

    all_threads = set()

    async for checkpoint in checkpointer.alist(None):

        all_threads.add(
            checkpoint.config[
                "configurable"
            ]["thread_id"]
        )

    return list(all_threads)


def retrieve_all_threads():

    return run_async(
        _alist_threads()
    )