import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluate", ROOT / "tools/evaluate.py")
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)


class EvaluateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_prepared_skill_is_blinded_and_raw(self):
        out = evaluate.prepare(self.base / "run", "skill", ["C07"])
        case = out / "C07"
        self.assertFalse((out / "gold.json").exists())
        self.assertTrue((case / "skill/SKILL.md").is_file())
        self.assertEqual(json.loads((case / "metadata.json").read_text())["source_hashes"],
                         evaluate.hashes(case / "paper"))
        self.assertEqual(evaluate.inspect(out)[0]["changed_files"], [])

    def test_baseline_has_no_skill(self):
        out = evaluate.prepare(self.base / "run", "baseline", ["C01"])
        self.assertFalse((out / "C01/skill").exists())
        self.assertNotIn("skill/SKILL.md", (out / "C01/task.md").read_text())

    def test_fresh_output_required(self):
        out = self.base / "run"
        out.mkdir()
        with self.assertRaises(FileExistsError):
            evaluate.prepare(out, "baseline", ["C01"])

    def test_unknown_case_rejected_without_writes(self):
        out = self.base / "run"
        with self.assertRaises(ValueError):
            evaluate.prepare(out, "baseline", ["UNKNOWN"])
        self.assertFalse(out.exists())

    def test_inspection_sees_edit_and_case_level_audit(self):
        out = evaluate.prepare(self.base / "run", "skill", ["C07"])
        case = out / "C07"
        (case / "paper/sections/introduction.tex").write_text("Changed.\n")
        record = case / ".math-paper-editor" / "one"
        record.mkdir(parents=True)
        (record / "manifest.json").write_text('{"state":"complete","conflicts":[]}')
        (case / "report.md").write_text("Report.\n")
        result = evaluate.inspect(out)[0]
        self.assertEqual(result["changed_files"], ["sections/introduction.tex"])
        self.assertTrue(result["report_present"])
        self.assertEqual(result["edit_records"][0]["state"], "complete")


if __name__ == "__main__":
    unittest.main()
