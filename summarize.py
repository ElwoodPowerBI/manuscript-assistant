import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ["AZURE_AI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_AI_API_KEY"],
)

description = """
When a botanist wakes up alone on a spacecraft with no memory of how he
got there, he must piece together his mission: the sun is dimming, Earth
is doomed, and he may be humanity's last hope. A story of science,
survival, and an unexpected friendship light-years from home.
"""

response = client.chat.completions.create(
    model=os.environ["AZURE_AI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "You are an editorial assistant at a publishing house. Be concise and accurate."},
        {"role": "user", "content": f"Summarize this book description in two sentences:\n\n{description}"},
    ],
   
)

print(response.choices[0].message.content)