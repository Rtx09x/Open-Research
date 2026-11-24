from pathlib import Path
import re
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parents[2]
docs = list(root.glob("*.md")) + list(root.glob("*/README.md")) + list(root.glob("templates/project/*.md"))
errors = []
for doc in docs:
    text = re.sub(r"```.*?```", "", doc.read_text(encoding="utf-8"), flags=re.S)
    for target in re.findall(r"\]\(([^\s)]+)\)", text):
        u = urlsplit(target)
        if u.scheme or u.netloc or not u.path:
            continue
        p = doc.parent / unquote(u.path)
        if not p.exists():
            errors.append(f"{doc.relative_to(root)}: missing {target}")
if errors:
    raise SystemExit("\n".join(errors))
print("Foundation relative Markdown links checked.")
