from graph import app

query = input(
    "Enter your query: "
)

result = app.invoke(
    {
        "question": query
    }
)

# debugging
print("\nGenerated SQL:")
print(result.get("sql"))

print("\nRows:")
print(result.get("rows"))

print("\nAnswer:")
print(result.get("answer"))