from pathlib import Path

root = Path(__file__).resolve().parents[2]
reserved = {"templates", "LICENSES"}
errors = []
for name in ("README.md", "CONTRIBUTING.md", "GOVERNANCE.md", "VERIFICATION.md", "CODE_OF_CONDUCT.md", "LICENSE.md", "CITATION.cff"):
    if not (root / name).is_file():
        errors.append(f"Missing {name}")
for domain in sorted(root.iterdir()):
    if not domain.is_dir() or domain.name.startswith(".") or domain.name in reserved:
        continue
    if not (domain / "README.md").is_file():
        errors.append(f"{domain.name}: missing README.md")
    for project in sorted(domain.iterdir()):
        if not project.is_dir() or project.name.startswith("."):
            continue
        for name in ("README.md", "AUTHORS.md"):
            if not (project / name).is_file():
                errors.append(f"{project.relative_to(root)}: missing {name}")
        for name in ("archive", "code"):
            if not (project / name).is_dir():
                errors.append(f"{project.relative_to(root)}: missing {name}/")
if errors:
    raise SystemExit("\n".join(errors))
print("Required research structure present.")
