import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evals/results/v0.1.0"


class ArchivedEvaluationTests(unittest.TestCase):
    def test_observed_sources_match_recorded_hashes(self):
        data = json.loads((ARCHIVE / "observations.json").read_text())
        self.assertEqual(len(data["records"]), 20)
        for record in data["records"]:
            case = ARCHIVE / record["arm"] / record["case"]
            self.assertTrue((case / "report.md").is_file())
            for name, expected in record["output_hashes"].items():
                self.assertEqual(hashlib.sha256((case / "paper" / name).read_bytes()).hexdigest(), expected)
            if record["mode"] in {"review", "deep-review"}:
                self.assertEqual(record["input_hashes"], record["output_hashes"])

    def test_archived_audits_are_clean_and_hash_checked(self):
        records = list(ARCHIVE.glob("skill/*/audit/manifest.json"))
        self.assertEqual(len(records), 4)
        for path in records:
            data = json.loads(path.read_text())
            self.assertNotIn("root", data)
            self.assertEqual(data["state"], "complete")
            self.assertEqual(data["conflicts"], [])
            self.assertEqual((path.parent / "unattributed.diff").read_bytes(), b"")
            for name, info in data["files"].items():
                for folder, key in [("before", "before_sha256"), ("editor", "expected_sha256"), ("after", "after_sha256")]:
                    self.assertEqual(hashlib.sha256((path.parent / folder / name).read_bytes()).hexdigest(), info[key])

    def test_scope_and_noop_controls_preserved(self):
        data = json.loads((ARCHIVE / "observations.json").read_text())
        for record in data["records"]:
            if record["case"] == "C07":
                self.assertEqual(record["changed_files"], ["sections/introduction.tex"])
            if record["case"] == "C08":
                self.assertEqual(record["changed_files"], [])


if __name__ == "__main__":
    unittest.main()
