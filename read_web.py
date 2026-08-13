import requests
from bs4 import BeautifulSoup

url = "https://jobsearch.createyourowncareer.com/PRH_US/go/PRH_US_Publishing_and_Corporate/9793801/?locale=en_US"

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
print(f"Status: {response.status_code}")
print(f"HTML length: {len(response.text)} characters\n")

soup = BeautifulSoup(response.text, "html.parser")

print("Page title:", soup.title.string if soup.title else "none")
print()

for tag in soup(["script", "style", "nav", "footer", "header"]):
    tag.decompose()

text = soup.get_text(separator="\n", strip=True)
print(f"Text after stripping junk: {len(text)} characters\n")
print(text[:800])

candidates = []
for tag in soup.find_all(["div", "section", "article", "main"]):
    text = tag.get_text(strip=True)
    classes = " ".join(tag.get("class") or [])
    candidates.append((len(text), tag.name, classes, tag.get("id") or ""))

candidates.sort(reverse=True)
print("\n--- biggest text containers ---")
for size, name, classes, el_id in candidates[:12]:
    print(f"{size:>7}  <{name}> class='{classes[:45]}' id='{el_id[:25]}'")

    content = soup.select_one("#job-table")
print("\n--- job table only ---")
print(content.get_text(separator="\n", strip=True)[:1500])