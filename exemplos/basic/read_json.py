import json

try:
    with open('source/data/example.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Access specific data fields
    print(data)
    print(f"Tile set: {data['layers'][0]['map']}")

except FileNotFoundError:
    print("Error: The file 'data.json' was not found.")
except json.JSONDecodeError:
    print("Error: The file is not a valid JSON format.")