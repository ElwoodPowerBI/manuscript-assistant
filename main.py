import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


client = OpenAI(
    base_url=os.environ.get("AZURE_AI_ENDPOINT", "https://placeholder").rstrip("/") + "/openai/v1/",
    api_key=os.environ.get("AZURE_AI_API_KEY", "placeholder-key"),
)

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


def load_chunks(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


_knowledge_base = None


def get_knowledge_base():
    global _knowledge_base
    if _knowledge_base is None:
        chunks = load_chunks("posting.txt")
        vectors = [
            d.embedding
            for d in client.embeddings.create(
                model="text-embedding-3-large", input=chunks
            ).data
        ]
        _knowledge_base = (chunks, vectors)
        print(f"Knowledge base ready: {len(chunks)} chunks embedded")
    return _knowledge_base
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


class QuestionIn(BaseModel):
    question: str


class AnswerOut(BaseModel):
    answer: str
    sources: list[str]

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

@app.post("/ask", response_model=AnswerOut)
def ask(q: QuestionIn):
    chunks, chunk_vectors = get_knowledge_base()

    q_vec = client.embeddings.create(
        model="text-embedding-3-large", input=[q.question]
    ).data[0].embedding

    scored = sorted(
        zip(chunks, chunk_vectors),
        key=lambda pair: cosine(q_vec, pair[1]),
        reverse=True,
    )
    top_chunks = [chunk for chunk, vec in scored[:3]]
    context = "\n\n".join(top_chunks)

    response = client.chat.completions.create(
        model=os.environ["AZURE_AI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Answer using ONLY the provided context. If the answer is not in the context, say you do not know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {q.question}"},
        ],
    )
    return AnswerOut(answer=response.choices[0].message.content, sources=top_chunks)