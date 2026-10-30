import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("changes", ROOT / "skills/math-paper-editor/scripts/changes.py")
changes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(changes)


class ChangesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / "paper"
        self.root.mkdir()
        self.source = self.root / "中文 draft.tex"
        self.original = b"Author's existing edit.\r\nThis follow"
        self.source.write_bytes(self.original)
        self.candidate = self.base / "candidate.tex"
        self.candidate.write_bytes(self.original.replace(b"follow", b"follows"))
        self.run = changes.begin(self.root, self.base / "run", [self.source.name])

    def tearDown(self):
        self.tmp.cleanup()

    def test_bytes_crlf_and_no_final_newline(self):
        changes.apply(self.run, self.source.name, self.candidate)
        result = changes.finish(self.run)
        self.assertEqual(result["state"], "complete")
        self.assertEqual((self.run / "before" / self.source.name).read_bytes(), self.original)
        self.assertEqual((self.run / "after" / self.source.name).read_bytes(), self.candidate.read_bytes())
        self.assertIn(b"No newline at end of file", (self.run / "changes.diff").read_bytes())
        self.assertEqual((self.run / "unattributed.diff").read_bytes(), b"")

    def test_noop_is_empty_and_unrecorded(self):
        self.candidate.write_bytes(self.original)
        self.assertFalse(changes.apply(self.run, self.source.name, self.candidate))
        self.assertEqual(changes.finish(self.run)["operations"], [])
        self.assertEqual((self.run / "changes.diff").read_bytes(), b"")

    def test_source_drift_rejects_write(self):
        concurrent = self.original + b"\nAuthor concurrent change.\n"
        self.source.write_bytes(concurrent)
        with self.assertRaises(changes.ConflictError):
            changes.apply(self.run, self.source.name, self.candidate)
        self.assertEqual(self.source.read_bytes(), concurrent)
        self.assertEqual(changes.check(self.run), [self.source.name])

    def test_direct_changes_not_attributed(self):
        self.source.write_bytes(self.candidate.read_bytes())
        self.assertEqual(changes.finish(self.run)["state"], "conflicted")
        self.assertEqual((self.run / "editor.diff").read_bytes(), b"")
        self.assertNotEqual((self.run / "unattributed.diff").read_bytes(), b"")

    def test_concurrent_after_editor_edit_separated(self):
        changes.apply(self.run, self.source.name, self.candidate)
        self.source.write_bytes(self.source.read_bytes() + b"\nAUTHOR_NOTE\n")
        result = changes.finish(self.run)
        self.assertEqual(result["state"], "conflicted")
        self.assertNotIn(b"AUTHOR_NOTE", (self.run / "editor.diff").read_bytes())
        self.assertIn(b"+AUTHOR_NOTE", (self.run / "unattributed.diff").read_bytes())

    def test_repeated_apply_chains(self):
        changes.apply(self.run, self.source.name, self.candidate)
        self.candidate.write_bytes(self.source.read_bytes() + b"\nSecond edit.\n")
        changes.apply(self.run, self.source.name, self.candidate)
        self.assertEqual(len(changes.finish(self.run)["operations"]), 2)

    def test_seal_is_idempotent_and_preserves_outputs(self):
        changes.apply(self.run, self.source.name, self.candidate)
        changes.finish(self.run)
        manifest_bytes = (self.run / "manifest.json").read_bytes()
        changes.finish(self.run)
        self.assertEqual((self.run / "manifest.json").read_bytes(), manifest_bytes)
        self.source.write_bytes(b"Later author edit.\n")
        with self.assertRaises(changes.ConflictError):
            changes.finish(self.run)
        self.assertEqual((self.run / "manifest.json").read_bytes(), manifest_bytes)

    def test_apply_after_seal_rejected(self):
        changes.finish(self.run)
        with self.assertRaises(ValueError):
            changes.apply(self.run, self.source.name, self.candidate)

    def test_before_snapshot_tamper(self):
        (self.run / "before" / self.source.name).write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            changes.finish(self.run)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_editor_snapshot_tamper(self):
        (self.run / "editor" / self.source.name).write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            changes.apply(self.run, self.source.name, self.candidate)

    def test_final_snapshot_tamper(self):
        changes.finish(self.run)
        (self.run / "after" / self.source.name).write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            changes.finish(self.run)

    def test_unknown_file_and_source_as_candidate_rejected(self):
        with self.assertRaises(ValueError):
            changes.apply(self.run, "missing.tex", self.candidate)
        with self.assertRaises(ValueError):
            changes.apply(self.run, self.source.name, self.source)

    def test_path_escape_and_missing_source_rejected(self):
        for name in ("../outside.tex", "/outside.tex", ".", "missing.tex"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                changes.begin(self.root, self.base / "bad", [name])

    def test_existing_record_not_overwritten(self):
        with self.assertRaises(FileExistsError):
            changes.begin(self.root, self.run, [self.source.name])

    def test_symlink_source_rejected(self):
        (self.root / "link.tex").symlink_to(self.source)
        with self.assertRaises(ValueError):
            changes.begin(self.root, self.base / "bad", ["link.tex"])

    def test_symlink_parent_rejected(self):
        (self.root / "alias").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            changes.begin(self.root, self.base / "bad", ["alias/" + self.source.name])

    def test_non_utf8_and_nul_rejected(self):
        for data in (b"\xff", b"text\0"):
            self.candidate.write_bytes(data)
            with self.assertRaises((UnicodeError, ValueError)):
                changes.apply(self.run, self.source.name, self.candidate)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_permissions_retained(self):
        self.source.chmod(0o640)
        changes.apply(self.run, self.source.name, self.candidate)
        self.assertEqual(stat.S_IMODE(self.source.stat().st_mode), 0o640)

    def test_record_failure_rolls_back_without_source_loss(self):
        real = changes.write_json
        with patch.object(changes, "write_json", side_effect=[OSError("injected"), None]):
            with self.assertRaises(OSError):
                changes.apply(self.run, self.source.name, self.candidate)
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertEqual((self.run / "editor" / self.source.name).read_bytes(), self.original)
        # The initial manifest was never replaced by the injected failing call.
        self.assertEqual(json.loads((self.run / "manifest.json").read_text())["operations"], [])
        self.assertEqual(changes.finish(self.run)["state"], "complete")


if __name__ == "__main__":
    unittest.main()
