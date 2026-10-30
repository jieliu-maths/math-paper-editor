#!/usr/bin/env python3
"""Preview/install a local release; preserve drift and retain full backups."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "math-paper-editor"
STATE = ".math-paper-editor-install.json"
GENERATED = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files_at(root):
    result = {}
    for path in sorted(root.rglob("*")):
        if "__pycache__" in path.relative_to(root).parts or path.suffix in {".pyc", ".pyo"} or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise ValueError("Symlinked package/installation entries are not supported")
        if path.is_file() and path.name != STATE:
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result


def source_revision(root):
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def install(source, dest, backup_root, apply=False, legacy_baseline=None):
    source, dest = Path(source).resolve(strict=True), Path(dest).absolute()
    backup_root = Path(backup_root).expanduser().absolute()
    if any(backup_root == path or path in backup_root.parents for path in (source, dest)):
        raise ValueError("Backups must be outside source and destination directories")
    if dest.is_symlink() or (dest.exists() and not dest.is_dir()):
        raise ValueError("Destination must be a regular directory, not a symlink")
    if dest == source or source in dest.parents or dest in source.parents:
        raise ValueError("Source and destination must be separate")
    expected_source = files_at(source)
    version = (source / "VERSION").read_text().strip()
    current = files_at(dest) if dest.exists() else {}
    previous = None
    if dest.exists():
        state = dest / STATE
        if state.exists():
            previous = json.loads(state.read_text())
            if previous.get("schema") != 1:
                raise ValueError("Unsupported installation record")
            for name, expected in previous["files"].items():
                if current.get(name) != expected:
                    raise ValueError(f"Local modification/deletion preserved; merge before upgrading: {name}")
            for name in current.keys() - previous["files"].keys():
                if name in expected_source:
                    raise ValueError(f"New package file would overwrite an unmanaged local file: {name}")
        elif legacy_baseline is None:
            raise ValueError("Unmanaged existing skill: provide an exact legacy baseline to adopt")
        elif current != legacy_baseline:
            raise ValueError("Existing skill changed since the legacy baseline; preserve and compare it")
    plan = {"version": version, "destination": str(dest),
            "action": "upgrade" if dest.exists() else "install",
            "managed_files": len(expected_source), "applied": False}
    if not apply:
        return plan
    dest.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="." + dest.name + "-stage-", dir=dest.parent))
    backup = None
    try:
        # Managed upgrades retain untracked local extras. Legacy adoption is
        # explicit replacement, with every original file retained in the backup.
        if previous is not None:
            shutil.copytree(dest, staging, dirs_exist_ok=True, ignore=GENERATED)
            for name in previous["files"].keys() - expected_source.keys():
                (staging / name).unlink()
        shutil.copytree(source, staging, dirs_exist_ok=True, ignore=GENERATED)
        state_data = {"schema": 1, "version": version,
                      "source": "https://github.com/jieliu-maths/math-paper-editor",
                      "revision": source_revision(ROOT), "files": expected_source}
        (staging / STATE).write_text(json.dumps(state_data, indent=2) + "\n")
        if files_at(source) != expected_source:
            raise ValueError("Release source changed during installation")
        if dest.exists():
            if files_at(dest) != current:
                raise ValueError("Destination changed during installation; retry after comparison")
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = backup_root / (stamp + "-" + uuid.uuid4().hex[:8])
            backup.parent.mkdir(parents=True, exist_ok=True)
            dest.rename(backup)
        staging.rename(dest)
    except Exception:
        if backup is not None and backup.exists() and not dest.exists():
            backup.rename(dest)
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    plan.update(applied=True, backup=str(backup) if backup else None)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path,
                        default=Path.home() / ".agents/skills/math-paper-editor")
    parser.add_argument("--backup-root", type=Path,
                        default=Path.home() / ".agents/skill-backups/math-paper-editor")
    parser.add_argument("--legacy-baseline", type=Path,
                        help="Private JSON path->sha256 map of the existing unmanaged installation")
    parser.add_argument("--apply", action="store_true", help="Default only previews")
    args = parser.parse_args()
    try:
        baseline = json.loads(args.legacy_baseline.read_text()) if args.legacy_baseline else None
        print(json.dumps(install(PACKAGE, args.dest, args.backup_root,
                                 args.apply, baseline), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
