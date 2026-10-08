"""Small invariants for the round-02 source manifest and file checks."""

import copy
import unittest

import round_02_pipeline as pipeline
import structure_round_02 as structure
import probe_breakup_state as breakup_probe


class PipelineTest(unittest.TestCase):
    def test_manifest_rejects_escape_and_existing_id(self):
        manifest = pipeline.read_json(pipeline.MANIFEST)
        catalog = pipeline.read_json(pipeline.CATALOG)
        for bad_path in ("../other.twee", "C:other.twee", "nested\\other.twee"):
            changed = copy.deepcopy(manifest)
            changed["works"][0]["files"] = [bad_path]
            with self.subTest(path=bad_path), self.assertRaises(ValueError):
                pipeline.validate_manifest(changed, catalog)
        changed = copy.deepcopy(manifest)
        changed["works"][0]["id"] = "ronynn--interview-interview"
        with self.assertRaises(ValueError):
            pipeline.validate_manifest(changed, catalog)

    def test_offline_verify_current_snapshot(self):
        pipeline.verify()

    def test_story_links_and_reviewed_endings(self):
        self.assertEqual(structure.parse_link("leave<-walk away"), ("walk away", "leave"))
        self.assertEqual(structure.parse_link("Stay|Home"), ("Stay", "Home"))
        manifest = pipeline.read_json(pipeline.MANIFEST)
        decisions = pipeline.read_json(structure.DECISIONS)["works"]
        for spec in manifest["works"]:
            result = structure.build_work(spec, decisions[spec["id"]])
            with self.subTest(work=spec["id"]):
                self.assertTrue(result["audit"]["reviewedEndings"])
                self.assertEqual(result["audit"]["staticPathsToEndings"].keys(),
                                 result["audit"]["pathStepsToEndings"].keys())
        withering = next(spec for spec in manifest["works"] if spec["id"] == "hugofmramos--withering-tears")
        audit = structure.build_work(withering, decisions[withering["id"]])["audit"]
        self.assertIn("Run5 → Run6", audit["missingTargets"])
        self.assertIsNone(audit["staticPathsToEndings"]["RunENDING"])

    def test_structures_are_reproducible(self):
        structure.write_all(check=True)

    def test_breakup_finale_respects_source_thresholds(self):
        witness = breakup_probe.find_witness()
        self.assertEqual(witness["target"], "moment.")
        self.assertGreaterEqual(witness["finalState"]["options"], 5)
        self.assertEqual(witness["finalState"]["entropy"], 1)
        self.assertEqual(witness["steps"][-1]["to"], "moment.")
        self.assertEqual(pipeline.read_json(breakup_probe.ROOT / "data" / "round-02-breakup-state-witness.json"), witness)


if __name__ == "__main__":
    unittest.main()
