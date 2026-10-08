"""Small invariants for the round-02 source manifest and file checks."""

import copy
import unittest

import round_02_pipeline as pipeline


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


if __name__ == "__main__":
    unittest.main()
