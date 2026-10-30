#!/usr/bin/env python3
"""Byte-preserving snapshots and optimistic, attributed UTF-8 source edits."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

SCHEMA = 2


class ConflictError(ValueError):
    """Observed drift; no source is overwritten."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_source(path):
    data = Path(path).read_bytes()
    data.decode("utf-8")
    if b"\0" in data:
        raise ValueError("Expected a UTF-8 text source")
    return data


def relative_name(name):
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts or rel == Path("."):
        raise ValueError(f"Expected a relative file within the root: {name}")
    return rel


def source_path(root, name):
    rel = relative_name(name)
    path = root / rel
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"Symlinked sources are not supported: {name}")
    if not path.is_file():
        raise ValueError(f"Expected an existing source: {name}")
    return path


def atomic_write(path, data, mode=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError(f"Refusing a symlink output: {path.name}")
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            tmp = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if mode is not None:
            os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()


def write_json(path, value):
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def unified(before, after, name):
    lines = difflib.unified_diff(
        before.decode("utf-8").splitlines(keepends=True),
        after.decode("utf-8").splitlines(keepends=True),
        fromfile="a/" + name, tofile="b/" + name,
    )
    return "".join(
        line if line.endswith("\n") else line + "\n\\ No newline at end of file\n"
        for line in lines
    )


def load_run(out):
    out = Path(out).resolve(strict=True)
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != SCHEMA:
        raise ValueError("Unsupported record schema. Keep older records and their original helper; start a new v2 run.")
    if manifest.get("state") not in {"open", "complete", "conflicted"}:
        raise ValueError("Invalid record state")
    root = Path(manifest["root"]).resolve(strict=True)
    if not manifest["files"]:
        raise ValueError("Empty record")
    for name, info in manifest["files"].items():
        relative_name(name)
        before = read_source(source_path(out / "before", name))
        editor = read_source(source_path(out / "editor", name))
        if digest(before) != info["before_sha256"]:
            raise ValueError(f"Original snapshot was altered: {name}")
        if digest(editor) != info["expected_sha256"]:
            raise ValueError(f"Recorded editor snapshot was altered: {name}")
    return out, root, manifest


def begin(root, out, names):
    root, out = Path(root).resolve(strict=True), Path(out).resolve()
    if not names:
        raise ValueError("Select at least one existing source")
    sources = {}
    for name in names:
        path = source_path(root, name)
        if out == path or out in path.parents:
            raise ValueError("Snapshot output cannot contain a selected source")
        sources[path.relative_to(root).as_posix()] = read_source(path)
    out.mkdir(parents=True, exist_ok=False)
    manifest = {"version": SCHEMA, "state": "open", "root": str(root),
                "files": {}, "operations": [], "conflicts": []}
    for name, data in sources.items():
        atomic_write(out / "before" / name, data)
        atomic_write(out / "editor" / name, data)
        manifest["files"][name] = {
            "before_sha256": digest(data), "expected_sha256": digest(data)}
    for name in ("changes.diff", "editor.diff", "unattributed.diff"):
        atomic_write(out / name, b"")
    write_json(out / "manifest.json", manifest)
    return out


def check(out):
    out, root, manifest = load_run(out)
    conflicts = []
    for name, info in manifest["files"].items():
        current = read_source(source_path(root, name))
        expected = info.get("after_sha256", info["expected_sha256"]) if manifest["state"] != "open" else info["expected_sha256"]
        if digest(current) != expected:
            conflicts.append(name)
    return conflicts


def apply(out, name, replacement):
    out, root, manifest = load_run(out)
    if manifest["state"] != "open":
        raise ValueError("Record is sealed; start a new run")
    name = relative_name(name).as_posix()
    if name not in manifest["files"]:
        raise ValueError("Source was not snapshotted")
    target = source_path(root, name)
    replacement = Path(replacement).resolve(strict=True)
    if replacement == target.resolve():
        raise ValueError("Stage the replacement outside the manuscript source")
    before = read_source(target)
    info = manifest["files"][name]
    if digest(before) != info["expected_sha256"]:
        raise ConflictError(f"Concurrent/untracked source change: {name}")
    after = read_source(replacement)
    if before == after:
        return False
    mode = stat.S_IMODE(target.stat().st_mode)
    # Recheck immediately before replacement. This narrows, but cannot remove,
    # the race with non-cooperating external writers.
    if read_source(target) != before:
        raise ConflictError(f"Source changed before write: {name}")
    old_manifest = json.loads(json.dumps(manifest))
    try:
        atomic_write(target, after, mode)
        atomic_write(out / "editor" / name, after)
        info["expected_sha256"] = digest(after)
        manifest["operations"].append({
            "file": name, "before_sha256": digest(before),
            "after_sha256": digest(after)})
        write_json(out / "manifest.json", manifest)
    except Exception:
        # Never undo an observed external change while rolling back our write.
        if target.is_file() and read_source(target) == after:
            atomic_write(target, before, mode)
        atomic_write(out / "editor" / name, before)
        write_json(out / "manifest.json", old_manifest)
        raise
    return True


def finish(out):
    out, root, manifest = load_run(out)
    observed = {name: read_source(source_path(root, name))
                for name in manifest["files"]}
    if manifest["state"] != "open":
        for name, data in observed.items():
            after = read_source(source_path(out / "after", name))
            if digest(after) != manifest["files"][name]["after_sha256"]:
                raise ValueError(f"Final snapshot was altered: {name}")
            if digest(data) != digest(after):
                raise ConflictError("Source changed after finalization; start a new run")
        return manifest
    patches = {"changes.diff": [], "editor.diff": [], "unattributed.diff": []}
    conflicts = []
    for name, data in observed.items():
        before = read_source(out / "before" / name)
        editor = read_source(out / "editor" / name)
        patches["changes.diff"].append(unified(before, data, name))
        patches["editor.diff"].append(unified(before, editor, name))
        patches["unattributed.diff"].append(unified(editor, data, name))
        if data != editor:
            conflicts.append(name)
    for name, data in observed.items():
        atomic_write(out / "after" / name, data)
        manifest["files"][name]["after_sha256"] = digest(data)
    for name, parts in patches.items():
        atomic_write(out / name, "".join(parts).encode("utf-8"))
    manifest["state"] = "conflicted" if conflicts else "complete"
    manifest["conflicts"] = conflicts
    write_json(out / "manifest.json", manifest)
    return manifest


def self_test():
    with tempfile.TemporaryDirectory(prefix="math-paper-editor-") as tmp:
        root = Path(tmp) / "paper"
        root.mkdir()
        source = root / "中文 draft.tex"
        original = "Author's existing edit.\r\nThis follow".encode()
        source.write_bytes(original)
        out = begin(root, Path(tmp) / "run", [source.name])
        candidate = Path(tmp) / "candidate.tex"
        candidate.write_bytes(original.replace(b"This follow", b"This follows"))
        apply(out, source.name, candidate)
        if finish(out)["state"] != "complete":
            raise AssertionError("Clean edit not recorded")
        if (out / "before" / source.name).read_bytes() != original:
            raise AssertionError("Original bytes changed")
        if (out / "unattributed.diff").read_bytes():
            raise AssertionError("Unexpected attribution")
        finish(out)
        run2 = begin(root, Path(tmp) / "run2", [source.name])
        source.write_bytes(source.read_bytes() + b"\nAuthor concurrent edit.\n")
        try:
            apply(run2, source.name, candidate)
        except ConflictError:
            pass
        else:
            raise AssertionError("Concurrent write was accepted")
        result = finish(run2)
        if result["state"] != "conflicted" or not (run2 / "unattributed.diff").read_bytes():
            raise AssertionError("Unattributed change not retained")
    print("PASS: byte-preserving snapshots, guarded apply, sealed records, drift attribution")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("begin")
    start.add_argument("--root", required=True)
    start.add_argument("--out", required=True)
    start.add_argument("files", nargs="+")
    edit = commands.add_parser("apply")
    edit.add_argument("run")
    edit.add_argument("--file", required=True)
    edit.add_argument("--replacement", required=True)
    for name in ("check", "finish"):
        commands.add_parser(name).add_argument("run")
    commands.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "begin":
            print(begin(args.root, args.out, args.files))
        elif args.command == "apply":
            print("applied" if apply(args.run, args.file, args.replacement) else "unchanged")
        elif args.command == "check":
            conflicts = check(args.run)
            print(json.dumps({"conflicts": conflicts}, ensure_ascii=False))
            return 2 if conflicts else 0
        elif args.command == "finish":
            result = finish(args.run)
            print(json.dumps({"state": result["state"], "conflicts": result["conflicts"]}))
            return 2 if result["state"] == "conflicted" else 0
        else:
            self_test()
        return 0
    except ConflictError as exc:
        parser.exit(2, f"Conflict: {exc}\n")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
