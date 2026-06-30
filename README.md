# AI Data Catalog Agent (PostgreSQL + MCP + Gemini + LangGraph)

An AI-powered Text-to-SQL agent capable of understanding natural language questions, generating SQL queries, executing them against a PostgreSQL database, and returning human-readable answers.

The project uses **Model Context Protocol (MCP)** for database interaction, **Gemini** as the LLM, and **LangGraph** for workflow orchestration.

---

# Features

- Natural language to SQL conversion
- Dynamic PostgreSQL schema discovery
- Read-only SQL execution
- SQL guardrails (blocks destructive queries)
- Human-readable responses
- LangGraph workflow orchestration
- MCP client-server architecture
- Schema validation before SQL generation
- Modular architecture for future Databricks migration

---

# Tech Stack

- Python 3.11+
- PostgreSQL
- FastMCP
- LangGraph
- Google Gemini
- Psycopg2

---

# Project Architecture

```
                    User
                      │
                      ▼
               LangGraph Workflow
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
Schema Node      SQL Generation   Answer Generation
      │               │                │
      ▼               ▼                ▼
 describe_schema()   Gemini        Gemini
      │
      ▼
 MCP Client
      │
      ▼
 MCP Server
      │
      ▼
 PostgreSQL
```

---

# Workflow

```
User Question
      │
      ▼
Retrieve Database Schema
      │
      ▼
Can the question be answered?
      │
      ├───────────────┐
      │               │
     Yes             No
      │               │
      ▼               ▼
Generate SQL      Return Error
      │
      ▼
Execute SQL
      │
      ▼
Generate Natural Language Response
      │
      ▼
Return Answer
```

---

# Folder Structure

```
.
├── database_server.py      # MCP Server
├── client.py               # MCP Client
├── graph.py                # LangGraph Workflow
├── LLM.py                  # Gemini Integration
├── main.py                 # Entry Point
├── requirements.txt
└── README.md
```

---

# Prerequisites

Install:

- Python 3.11+
- PostgreSQL
- Git

---

# Clone Repository

```bash
git clone https://github.com/Joell-Alex1/Agentic_LLM_Cyient

cd Agentic_LLM_Cyient
```

---

# Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Install PostgreSQL.

Create a database.

Example:

```
Northwind
```

Import the Northwind dataset.

Update the database credentials inside

```python
database_server.py
```

```python
DB_PARAMS = {
    "dbname": "Northwind",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": "5432"
}
```

---

# Gemini API Key

Create an API key from

https://aistudio.google.com/

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Install dotenv if required

```bash
pip install python-dotenv
```

Load it

```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
```

---

# Install MCP Dependencies

```bash
pip install fastmcp
```

---

# Start the MCP Server

Open a terminal

```bash
python database_server.py
```

This starts the MCP server exposing two tools:

- describe_schema()
- query_database()

---

# Run the Application

Open another terminal

Activate the virtual environment

Run

```bash
python main.py
```

---

# Example Questions

```
Which employee handled the most orders?

Top 10 customers by revenue

Which supplier generated the highest revenue?

What products were ordered the most?

Show all orders handled by employee 5.
```

---

# Security

The application only allows read-only queries.

Blocked SQL operations:

- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- TRUNCATE

---

# How Schema Discovery Works

The application dynamically discovers the schema by querying PostgreSQL's metadata.

Step 1

Retrieve all tables

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';
```

Step 2

For every table

```sql
SELECT column_name,
       data_type
FROM information_schema.columns
WHERE table_name=<table>;
```

The resulting schema dictionary is then passed to Gemini for SQL generation.

No table or column names are hardcoded.

---

# Current Capabilities

- Dynamic schema discovery
- PostgreSQL integration
- MCP client-server architecture
- LangGraph workflow
- Natural language to SQL
- SQL execution
- Human-readable answers
- Read-only SQL execution
- Schema validation
- Semantic understanding

---

# Current Limitations

- Entire schema is passed to the LLM.
- Large enterprise databases may exceed context limits.
- Metadata catalog is generated dynamically per request.
- No vector search.
- No metadata embeddings.
- No conversation memory.
- No SQL self-correction.

---

# Future Improvements

- Metadata catalog
- Vector database
- Semantic schema retrieval
- Databricks Delta Table support
- Database abstraction layer
- SQL retry/self-correction
- Conversation memory
- Streaming responses
- Metadata refresh scheduler
- Event-driven schema refresh

---

# Future Databricks Support

The project is designed so that PostgreSQL can later be replaced by Databricks with minimal changes.

Planned abstraction:

```
DatabaseAdapter
    │
    ├── PostgresAdapter
    └── DatabricksAdapter
```

Business logic remains unchanged while only the adapter implementation changes.

---

# Author

Joell Alex
