"""Three prototypes should be different, original and still explicitly not published."""
import importlib.util
import unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"validate_pilots.py"
spec=importlib.util.spec_from_file_location("validate_pilots",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class InfluencerPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.concepts=module.validate_all()

    def test_three_concepts_not_one(self):
        self.assertEqual({x["id"] for x in self.concepts},{"vexa-volt","pip-patch","blop"})

    def test_each_has_different_visual_gimmick_and_character(self):
        self.assertEqual(len({x["quirk"] for x in self.concepts}),3)
        self.assertEqual(len({x["art_direction"] for x in self.concepts}),3)

    def test_pilot_scripts_have_own_voices_and_valid_cut_rhythm(self):
        for item in self.concepts:
            s=item["pilot"]
            self.assertGreaterEqual(len(s["shots"]),5)
            self.assertEqual(s["shots"][0]["start"],0)
            self.assertLessEqual(s["shots"][0]["end"],2)
            self.assertGreater(len(s["sample_script"]),75)

    def test_no_unverified_brand_names_claimed_or_publication(self):
        for item in self.concepts:
            self.assertEqual(item["name_status"],"WORKING_NAME_NOT_TRADEMARK_VERIFIED")
            self.assertFalse(item["pilot"]["commercially_released"])

if __name__=="__main__":
    unittest.main()
