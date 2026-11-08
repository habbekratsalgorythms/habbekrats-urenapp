"""Stdlib QA: ten original captions with human review before export."""
import copy
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
here=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(here))
import content_pack

class ContentDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.example=json.loads((here/"voorbeeldpakket.json").read_text(encoding="utf-8"))

    def approved_demo(self):
        order=copy.deepcopy(self.example)
        order["human_editor_reviewed"]=True  # synthetic test fixture only
        return order

    def test_example_blocked_without_human_review(self):
        with self.assertRaisesRegex(ValueError,"Human editorial review"):
            content_pack.check(self.example)

    def test_export_has_ten_unique_rows_without_external_services(self):
        order=self.approved_demo()
        with tempfile.TemporaryDirectory() as tmp:
            paths=content_pack.export(order,tmp)
            self.assertEqual(len(paths),2)
            with paths[0].open(encoding="utf-8-sig",newline="") as f:
                rows=list(csv.DictReader(f,delimiter=";"))
            self.assertEqual(len(rows),10)
            self.assertEqual(len({r["Caption"] for r in rows}),10)
            self.assertTrue(paths[0].read_bytes().startswith(b"\xef\xbb\xbf"))
            delivery=paths[1].read_text()
            self.assertIn("€79 excl. btw",delivery)
            self.assertIn("Twee gebundelde correctierondes",delivery)
            self.assertIn("Geen automatische factuur",delivery)

    def test_rejects_partial_briefing_or_unconfirmed_order(self):
        for key in ("briefing_complete","order_confirmed"):
            order=self.approved_demo();order[key]=False
            with self.assertRaisesRegex(ValueError,"Complete briefing"):
                content_pack.check(order)

    def test_rejects_duplicate_and_placeholder(self):
        order=self.approved_demo()
        order["posts"][1]["caption"]=order["posts"][0]["caption"]
        with self.assertRaisesRegex(ValueError,"duplicate caption"):
            content_pack.check(order)
        order=self.approved_demo()
        order["posts"][1]["caption"]="Dit is een tekst met [invullen] placeholder die niet mag worden geleverd."
        with self.assertRaisesRegex(ValueError,"unfinished placeholder"):
            content_pack.check(order)

    def test_rejects_missing_posts_unverified_status_and_unsafe_reference(self):
        order=self.approved_demo();order["posts"]=order["posts"][:9]
        with self.assertRaisesRegex(ValueError,"Exactly ten"):
            content_pack.check(order)
        order=self.approved_demo();order["reference"]="../unsafe"
        with self.assertRaisesRegex(ValueError,"non-identifying"):
            content_pack.check(order)
        order=self.approved_demo();order["posts"][0]["fact_check"]="magically_true"
        with self.assertRaisesRegex(ValueError,"fact-check"):
            content_pack.check(order)

if __name__=="__main__":
    unittest.main()
