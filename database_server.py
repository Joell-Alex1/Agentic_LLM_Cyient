import psycopg2
from psycopg2.extras import RealDictCursor
import re
# 1. FROM THE DOCS: Import FastMCP directly
from fastmcp import FastMCP

# 2. FROM THE IDENTITY DOCS: Initialize with clear system instructions
# This acts as our macro-level vectorless RAG metadata helper.
mcp = FastMCP(
    "Northwind-PostgreSQL-Engine",
    instructions=(
        "You are a PostgreSQL data assistant for the Northwind database. "
        "Step 1: ALWAYS call describe_schema() first to see available tables. "
        "Step 2: Synthesize a standard read-only SQL SELECT string natively. "
        "Step 3: Pass that string to query_database() to get active records."
    ),
    version="1.0.0",
    # FROM THE BEHAVIOR DOCS: Lock down input matching to prevent LLM hallucination types
    strict_input_validation=True,
    mask_error_details=True # Keeps database internal system codes clean
)

DB_PARAMS = {
    "dbname": "Northwind",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": "5432"
}

# 3. FROM THE COMPONENTS DOCS: Register Tool 1 using the standard decorator
@mcp.tool
def describe_schema() -> dict:
    """
    Scans the PostgreSQL system catalogs to map out all public tables and column types.
    Run this tool first to understand the data schema before trying to write SQL queries.
    """
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [row['table_name'] for row in cur.fetchall()]
    
    schema = {}
    for table in tables:
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s;
        """, (table,))
        schema[table] = {r['column_name']: r['data_type'] for r in cur.fetchall()}
        
    cur.close()
    conn.close()
    return schema

# 4. FROM THE COMPONENTS DOCS: Register Tool 2 with input parameters
@mcp.tool
def query_database(sql: str) -> list:
    """
    Executes a read-only SQL SELECT query against the Northwind database.
    
    Args:
        sql: A syntactically valid SQL SELECT statement string.
    """
    # OUR SYSTEM DESIGN GUARDRAIL (Runs locally before database access)
    sql_upper = sql.upper()
    banned_keywords = [r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b", r"\bDROP\b", r"\bALTER\b", r"\bTRUNCATE\b"]
    
    for pattern in banned_keywords:
        if re.search(pattern, sql_upper):
            return [{"error": "Security Access Denied: Destructive or data-modifying queries are strictly prohibited."}]
            
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        return [{"error": f"SQL Error encountered: {str(e)}"}]

# 5. FROM THE RUNNING THE SERVER DOCS: The default STDIO transport pipeline entry
if __name__ == "__main__":
    mcp.run()