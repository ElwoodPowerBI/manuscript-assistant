from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


pdf_paths = sorted(Path("documents").glob("*.pdf"))
print(f"Found {len(pdf_paths)} PDFs")

for path in pdf_paths:
    text = extract_pdf_text(path)
    print(f"\n{path.name}: {len(text)} characters")
    print(text[:300].replace("\n", " "))