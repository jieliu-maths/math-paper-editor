#!/usr/bin/env python3
"""Prepare blinded local skill/baseline cases; inspect changes, not proof truth."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/math-paper-editor"


def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()
            and "__pycache__" not in p.relative_to(root).parts
            and p.suffix not in {".pyc", ".pyo"} and p.name != ".DS_Store"}


def prepare(out, arm, selected=None):
    tasks = json.loads((ROOT / "evals/tasks.json").read_text())
    selected = set(selected or [task["id"] for task in tasks])
    if selected - {task["id"] for task in tasks}:
        raise ValueError("Unknown case ID")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    for task in tasks:
        if task["id"] not in selected:
            continue
        case = out / task["id"]
        paper = case / "paper"
        shutil.copytree(ROOT / "evals/fixtures" / task["fixture"], paper)
        invocation = ""
        if arm == "skill":
            shutil.copytree(PACKAGE, case / "skill",
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store"))
            invocation = "Use the math-paper-editor skill at skill/SKILL.md in " + task["mode"] + " mode.\n\n"
        text = invocation + task["task"] + (
            "\n\nThe manuscript is in paper/. Work only within this case directory. "
            "Save the complete review/delivery report to report.md. "
            "Do not read gold labels or other cases. Do not use network access "
            "or compile; state that compilation was not run. "
            "All papers here are synthetic fixtures, not research submissions.\n")
        (case / "task.md").write_text(text)
        metadata = {"case": task["id"], "arm": arm, "mode": task["mode"],
                    "version": (PACKAGE / "VERSION").read_text().strip(),
                    "source_hashes": hashes(paper),
                    "skill_hashes": hashes(PACKAGE) if arm == "skill" else None}
        (case / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return out


def inspect(out):
    results = []
    for meta_path in sorted(Path(out).glob("*/metadata.json")):
        meta = json.loads(meta_path.read_text())
        case = meta_path.parent
        current = hashes(case / "paper")
        changed = [name for name, value in meta["source_hashes"].items()
                   if current.get(name) != value]
        records = []
        for manifest in case.rglob("manifest.json"):
            if ".math-paper-editor" in manifest.parts:
                data = json.loads(manifest.read_text())
                records.append({"path": manifest.parent.relative_to(case).as_posix(),
                                "state": data.get("state"), "conflicts": data.get("conflicts")})
        results.append({"case": meta["case"], "arm": meta["arm"],
                        "changed_files": changed, "report_present": (case / "report.md").is_file(),
                        "edit_records": records})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("--out", required=True)
    prep.add_argument("--arm", choices=["skill", "baseline"], required=True)
    prep.add_argument("--case", action="append")
    commands.add_parser("inspect").add_argument("run")
    args = parser.parse_args()
    if args.command == "prepare":
        print(prepare(args.out, args.arm, args.case))
    else:
        print(json.dumps(inspect(args.run), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
