import csv
import random
def load_cards(path):
    try:
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Could not find {path}. Is it in this folder?")
        return []

cards = load_cards("flashcards.csv")
tier1 = [c for c in cards if c["tier"] == "1"]
print(f"Quizzing from {len(tier1)} Tier 1 cards")

random.shuffle(tier1)
score = 0

for i, card in enumerate(tier1[:10], start=1):
    print(f"\nQuestion {i}: {card['question']}")
    input("Say your answer out loud,  then press enter: ")
    print(f"Answer: {card['answer']}")
    honest = input("did you have it (y/n) ")
    if honest.lower() == "y":
        score += 1
 
print(f"\nScore: {score} out of 10")