book = {
    "title": "Project Hail Mary",
    "author": "Andy Weir",
    "year": 2021,
    "genre": "Science Fiction",
}

print(book["title"])
print(book["year"])

books = [
    {"title": "The Martian", "author": "Andy Weir", "year": 2014},
    {"title": "Educated", "author": "Tara Westover", "year": 2018},
    {"title": "Project Hail Mary", "author": "Andy Weir", "year": 2021},
]

for b in books:
    print(f"{b['title']} by {b['author']} ({b['year']})")

def format_book(b):
    return f"{b['title']} by {b['author']} ({b['year']})"

def books_by_author(book_list, author_name):
    matches = []
    for b in book_list:
        if b["author"] == author_name:
            matches.append(b)
    return matches

print("---Andy Wier Books---")
weir_books = books_by_author(books, "Stephen King")
for b in weir_books:
    print(format_book(b))