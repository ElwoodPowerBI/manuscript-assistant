import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ["AZURE_AI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_AI_API_KEY"],
)

words = ["dog", "puppy", "banana"]
resp = client.embeddings.create(model="text-embedding-3-large", input=words)
vectors = [d.embedding for d in resp.data]

print(f"Each embedding is a list of {len(vectors[0])} numbers")

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)

print(f"dog vs puppy:  {cosine(vectors[0], vectors[1]):.3f}")
print(f"dog vs banana: {cosine(vectors[0], vectors[2]):.3f}")