import requests

url = "https://openlibrary.org/search.json"
params ={"author": "Andy Weir", "limit": 5}

response = requests.get(url, params=params, timeout=10)
print(f"Status code: {response.status_code}")

data = response.json()
print(f"Total reults found: {data['numFound']}")

for doc in data["docs"]:
    title = doc.get("title")
    author = doc.get("author_name", ["Unknown"])[0]
    year = doc.get("first_publish_year", "Unknown")
    print(f"{title} by {author} ({year})")