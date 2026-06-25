import asyncio

from client import get_schema, run_query
from LLM import can_answer, generate_sql, generate_answer

query = input("Enter your query: ")

schema = asyncio.run(
    get_schema()
)
if not can_answer(query, schema):
    print(
        "I'm unable to answer that question using the available information."
    )
    exit()

sql = generate_sql(
    query,
    schema
)

print("\nGenerated SQL:")
print(sql)


if sql == "CANNOT_ANSWER":
    print(
        "I'm unable to answer that question using the available information."
    )
    exit()

rows = asyncio.run(
    run_query(sql)
)

print("\nRows:")
print(rows)

answer = generate_answer(
    query,
    str(rows)
)

print("\nAnswer:")
print(answer)