from difflib import SequenceMatcher
import re
import unicodedata

import requests


def normalize(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def similarity(typed_name, candidate_name):
    typed = normalize(typed_name)
    candidate = normalize(candidate_name)
    direct_score = SequenceMatcher(None, typed, candidate).ratio()
    typed_words = typed.split()
    candidate_words = candidate.split()
    word_scores = [
        max(SequenceMatcher(None, word, other).ratio() for other in candidate_words)
        for word in typed_words
    ]
    return (direct_score + sum(word_scores) / len(word_scores)) / 2


def find_author(name):
    # Searching individual words as well as the full name makes misspellings such
    # as "Yuval Herari" discoverable, then the closest full name is selected.
    queries = [name, *normalize(name).split()]
    candidates = {}
    for query in queries:
        response = requests.get(
            "https://openlibrary.org/search/authors.json",
            params={"q": query, "limit": 100},
            timeout=10,
        )
        response.raise_for_status()
        for author in response.json().get("docs", []):
            if author.get("key") and author.get("name"):
                candidates[author["key"]] = author

    if not candidates:
        return None
    return max(candidates.values(), key=lambda author: similarity(name, author["name"]))


def get_titles(author_key):
    titles = set()
    offset = 0
    while True:
        response = requests.get(
            f"https://openlibrary.org/authors/{author_key}/works.json",
            params={"limit": 100, "offset": offset},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        entries = data.get("entries", [])
        titles.update(entry["title"] for entry in entries if entry.get("title"))
        offset += len(entries)
        if not entries or offset >= data.get("size", 0):
            return sorted(titles, key=str.casefold)


try:
    typed_name = input("Enter an author's name: ").strip()
    if not typed_name:
        raise ValueError("Please enter an author's name.")

    author = find_author(typed_name)
    if author is None:
        print("No matching author found.")
    else:
        titles = get_titles(author["key"])
        print(f"\nClosest match: {author['name']}")
        print(f"Titles found: {len(titles)}\n")
        for title in titles:
            print(title)
except (requests.RequestException, ValueError) as error:
    print(f"Error: {error}")