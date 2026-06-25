import asyncio
from fastmcp import Client

client = Client("database_server.py")


async def get_schema():
    async with client:
        schema = await client.call_tool(
            "describe_schema",
            {}
        )

        return schema.content[0].text


async def run_query(sql: str):
    async with client:
        rows = await client.call_tool(
            "query_database",
            {
                "sql": sql
            }
        )

        return rows.content[0].text