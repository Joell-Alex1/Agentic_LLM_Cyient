from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv()
client = genai.Client()

print("Uploading PDF to Gemini Files API...")
uploaded_file = client.files.upload(file=r"C:\Users\ja89847\ai_agent\documents_to_parse\pdfcoffee.com_saep-381-project-quality-issues-escalation-process-pdf-pdf-free.pdf")

prompt = """
Convert this document into structured Markdown for a RAG tree.
Use clear headers (#, ##), paragraphs, and list items (-).
Skip footers, page numbers, and repeating license text.
"""

# Call the ultra-budget Lite model
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",  # <--- Forces the lowest cost tier
    contents=[uploaded_file, prompt],
    config=types.GenerateContentConfig(
     
    )
)

print("\n===== PARSED OUTPUT =====\n")
print(response.text)

# Clean up storage
client.files.delete(name=uploaded_file.name)