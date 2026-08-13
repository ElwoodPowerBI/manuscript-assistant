import os
from pathlib import Path

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

client = DocumentIntelligenceClient(
    endpoint=os.environ["DOC_INTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["DOC_INTELLIGENCE_KEY"]),
)

pdf_path = sorted(Path("documents").glob("*.pdf"))[0]
print(f"Analyzing: {pdf_path.name}\n")

with open(pdf_path, "rb") as f:
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=f,
        content_type="application/octet-stream",
    )

result = poller.result()

print(f"Pages:      {len(result.pages)}")
print(f"Tables:     {len(result.tables or [])}")
print(f"Paragraphs: {len(result.paragraphs or [])}\n")

print("--- first 20 paragraphs with their roles ---")
for p in (result.paragraphs or [])[:20]:
    role = p.role or "body"
    print(f"[{role:>15}] {p.content[:70]}")