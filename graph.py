from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from client import get_schema, run_query
from LLM import can_answer, generate_sql, generate_answer
import asyncio
# from IPython.display import Image

class AgentState(TypedDict):
    question: str
    schema: str
    sql: str
    rows: str
    answer: str

def get_schema_node(state):

    schema = asyncio.run(
        get_schema()
    )

    return {
        "schema": schema
    }
def generate_sql_node(state):

    sql = generate_sql(
        state["question"],
        state["schema"]
    )

    return {
        "sql": sql
    }
def run_query_node(state):

    rows = asyncio.run(
        run_query(
            state["sql"]
        )
    )

    return {
        "rows": str(rows)
    }
def generate_answer_node(state):

    answer = generate_answer(
        state["question"],
        state["rows"]
    )

    return {
        "answer": answer
    }

def should_continue(state):

    if can_answer(
        state["question"],
        state["schema"]
    ):
        return "generate_sql"

    return "cannot_answer"
# rejection node
def cannot_answer_node(state):
    return {
        "answer":
        "I'm unable to answer that question using the available information."
    }

builder = StateGraph(AgentState)
builder.add_node(
    "get_schema",
    get_schema_node
)

builder.add_node(
    "generate_sql",
    generate_sql_node
)

builder.add_node(
    "run_query",
    run_query_node
)

builder.add_node(
    "generate_answer",
    generate_answer_node
)
builder.add_node(
    "cannot_answer",
    cannot_answer_node
)

builder.add_edge(
    "cannot_answer",
    END
)

builder.add_edge(
    START,
    "get_schema"
)

builder.add_conditional_edges(
    "get_schema",
    should_continue,
    {
        "generate_sql": "generate_sql",
        "cannot_answer": "cannot_answer"
    }
)

builder.add_edge(
    "generate_sql",
    "run_query"
)

builder.add_edge(
    "run_query",
    "generate_answer"
)

builder.add_edge(
    "generate_answer",
    END
)

app = builder.compile()
print(app.get_graph().draw_ascii())