#!/usr/bin/env python3
"""Offline release checks; no third-party modules, model calls, or TeX needed."""
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/math-paper-editor"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    required = [
        "README.md", "README.zh-CN.md", "LICENSE", "CHANGELOG.md",
        "CONTRIBUTING.md", "AGENTS.md", ".github/workflows/check.yml",
        "skills/math-paper-editor/SKILL.md", "skills/math-paper-editor/VERSION",
        "skills/math-paper-editor/LICENSE", "skills/math-paper-editor/agents/openai.yaml",
        "evals/tasks.json", "evals/gold.json",
    ]
    for name in required:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing release file: {name}")
    version = (PACKAGE / "VERSION").read_text().strip()
    if not re.fullmatch(r"0|[1-9]\d*", version.split(".")[0]) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Expected a numeric release version")
    if (ROOT / "LICENSE").read_bytes() != (PACKAGE / "LICENSE").read_bytes():
        raise ValueError("Runtime license differs from repository license")
    entry = (PACKAGE / "SKILL.md").read_text()
    # This package deliberately uses a simple scalar frontmatter subset.
    # Full YAML/Codex format validation is also run separately for the release.
    fields = entry.split("---\n", 2)
    if len(fields) != 3 or fields[0] != "":
        raise ValueError("Missing skill frontmatter")
    if "name: math-paper-editor\n" not in fields[1] or "description: " not in fields[1]:
        raise ValueError("Missing skill routing fields")
    if len(entry.splitlines()) > 180:
        raise ValueError("Keep the common entrypoint compact; load references as needed")
    tasks = json.loads((ROOT / "evals/tasks.json").read_text())
    gold = json.loads((ROOT / "evals/gold.json").read_text())
    ids = [task["id"] for task in tasks]
    if len(ids) != len(set(ids)) or set(ids) != set(gold):
        raise ValueError("Task/gold ID mismatch")
    for task in tasks:
        if task["mode"] not in {"review", "edit", "deep-review", "rewrite"}:
            raise ValueError("Unknown evaluation mode")
        if not (ROOT / "evals/fixtures" / task["fixture"] / "main.tex").is_file():
            raise ValueError("Missing raw fixture")
    record = ROOT / "evals/results" / ("v" + version + ".md")
    if not record.is_file():
        raise ValueError("Missing evaluation record for this release")
    observations = json.loads((record.with_suffix("") / "observations.json").read_text())
    runtime = {p.relative_to(PACKAGE).as_posix(): sha(p)
               for p in PACKAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    if observations["skill_hashes"] != runtime:
        raise ValueError("The runtime package differs from the evaluated candidate")
    private_path = re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")
    credential = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}")
    count = 0
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__"} for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Do not publish symlinks: {rel}")
        if not path.is_file():
            continue
        if ".math-paper-editor" in rel.parts or path.name == ".math-paper-editor-install.json":
            raise ValueError(f"Local manuscript/install record in release: {rel}")
        if path.suffix in {".pyc", ".pdf", ".zip"}:
            raise ValueError(f"Unexpected generated/binary release file: {rel}")
        text = path.read_text(encoding="utf-8")
        if private_path.search(text) or credential.search(text):
            raise ValueError(f"Possible local path or secret: {rel}")
        if path.suffix == ".py":
            ast.parse(text, filename=str(rel))
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                target = target.split("#", 1)[0]
                if target and not (path.parent / target).exists():
                    raise ValueError(f"Broken local Markdown link: {rel} -> {target}")
        count += 1
    print(f"PASS: v{version}; {count} UTF-8 release files; {len(tasks)} cases; evaluated package matches; links/path/secret checks")
    return count


if __name__ == "__main__":
    try:
        check()
    except (OSError, ValueError, KeyError, SyntaxError) as exc:
        raise SystemExit("Release check failed: " + str(exc))
