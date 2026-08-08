import csv
with open("flashcards.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    cards = list(reader)

print(f"Loaded {len(cards)} cards")
print(cards[0]["question"])
print(cards[0]["answer"])

tier1 = []
for c in cards:
    if c["tier"] == "1":
        tier1.append(c)

print(f"Tier1 1 cards: {len(tier1)}")

