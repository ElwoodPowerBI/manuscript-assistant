import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    base_url=os.environ["AZURE_AI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_AI_API_KEY"],
)

app = FastAPI(title="Manuscript Assistant")


class ManuscriptIn(BaseModel):
    text: str


class SummaryOut(BaseModel):
    summary: str


class BookMetadata(BaseModel):
    title: str
    genre: str
    themes: list[str]
    audience: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummaryOut)
def summarize(manuscript: ManuscriptIn):
    response = client.chat.completions.create(
        model=os.environ["AZURE_AI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You are an editorial assistant at a publishing house. Be concise."},
            {"role": "user", "content": f"Summarize in two sentences:\n\n{manuscript.text}"},
        ],
    )
    return SummaryOut(summary=response.choices[0].message.content)


@app.post("/extract-metadata", response_model=BookMetadata)
def extract_metadata(manuscript: ManuscriptIn):
    response = client.chat.completions.parse(
        model=os.environ["AZURE_AI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Extract book metadata from the description."},
            {"role": "user", "content": manuscript.text},
        ],
        response_format=BookMetadata,
    )
    return response.choices[0].message.parsed