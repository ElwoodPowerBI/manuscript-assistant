import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    base_url=os.environ["AZURE_AI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_AI_API_KEY"],
)

class BookMetadata(BaseModel):
    title: str
    genre: str
    themes: list[str]
    audience: str

description = """
When a botanist wakes up alone on a spacecraft with no memory of how he
got there, he must piece together his mission: the sun is dimming, Earth
is doomed, and he may be humanity's last hope. A story of science,
survival, and an unexpected friendship light-years from home.
"""

response = client.chat.completions.parse(
    model=os.environ["AZURE_AI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "Extract book metadata from the description. If the title is not stated, infer a plausible one."},
        {"role": "user", "content": description},
    ],
    response_format=BookMetadata,
)

book = response.choices[0].message.parsed
print(book)
print(f"\nThemes as a Python list: {book.themes}")