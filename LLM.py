from google import genai

client = genai.Client()

def generate_sql(
    question: str,
    schema: str
) -> str:

    prompt = f"""
    You are a PostgreSQL SQL generator.

    Database Schema:
    {schema}

    Rules:
    - Return ONLY SQL.
    - No explanations.
    - No markdown.
    - PostgreSQL column names are CASE SENSITIVE.
    - ALL column names MUST be wrapped in double quotes.
    - ALL mixed-case identifiers MUST be wrapped in double quotes.
    - Use the schema exactly as provided.
    - Example:
    SELECT e."EmployeeID"
    FROM employees e

    User Question:
    {question}
    """

    interaction = client.interactions.create(
        model="gemini-2.5-flash-lite",
        input=prompt
    )

    return interaction.output_text


def can_answer(
    question: str,
    schema: str
) -> bool:

    prompt = f"""
Database Schema:
{schema}

User Question:
{question}

Can this question be answered using ONLY the tables and columns in the schema?

Rules:
- Do not guess.
- Do not infer missing columns.
- Do not invent tables.
- Return ONLY YES or NO.
"""

    interaction = client.interactions.create(
        model="gemini-2.5-flash-lite",
        input=prompt
    )

    return interaction.output_text.strip() == "YES"

def generate_answer(
    question: str,
    rows: str
) -> str:

    prompt = f"""
You are a database assistant.

User Question:
{question}

Database Result:
{rows}

Answer the user's question naturally using the database result.

If the result is empty, say no matching records were found.
"""

    interaction = client.interactions.create(
        model="gemini-2.5-flash-lite",
        input=prompt
    )

    return interaction.output_text