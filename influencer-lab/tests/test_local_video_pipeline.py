"""Offline, no-cost tests: RTX 3070 check and 3-character Wan prompt plan."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
base=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,base/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
gpu=module("gpu_preflight")
jobs=module("prepare_video_jobs")

class LocalVideoPilotTests(unittest.TestCase):
    def test_parse_3070_eight_gig(self):
        cards=gpu.parse_smi("NVIDIA GeForce RTX 3070, 8192 MiB, 560.94")
        self.assertEqual(len(cards),1)
        self.assertEqual(cards[0]["vram_mib"],8192)
        self.assertEqual(cards[0]["driver"],"560.94")

    def test_no_gpu_is_not_claimed_to_work(self):
        result=gpu.probe(smi_output="",disk_path=base)
        self.assertFalse(result["cards"])
        self.assertFalse(result["local_gpu_was_exercised"])
        self.assertEqual(result["recommended_first_experiment"],"NEED_WINDOWS_NVIDIA_DRIVER_OR_WSL_GPU_VISIBILITY")
        self.assertFalse(result["allow_paid_fallback_without_approval"])

    def test_mock_3070_qualifies_for_just_a_test_not_proven_quality(self):
        result=gpu.probe(smi_output="NVIDIA GeForce RTX 3070, 8192 MiB, 560.94",disk_path=base)
        self.assertEqual(result["recommended_first_experiment"],"TRY_WAN22_5B_COMFYUI_LOW_VRAM")
        self.assertFalse(result["model_quality_is_proven"])

    def test_no_key_art_blocks_video_prompts(self):
        with self.assertRaisesRegex(ValueError,"Owner-approved image"):
            jobs.compile_jobs({},seconds=3)

    def test_three_separate_real_local_images_and_production_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            assets={}
            for name in jobs.PERSONAS:
                x=p/(name+".png");x.write_bytes(b"LOCAL TEST ART");assets[name]=str(x)
            output=jobs.compile_jobs(assets)
            self.assertEqual(len(output),3)
            self.assertEqual({x["persona"] for x in output},set(jobs.PERSONAS))
            self.assertTrue(all(x["forbid_remote_api"] for x in output))
            self.assertTrue(all(x["forbid_automatic_publication"] for x in output))
            self.assertTrue(all(x["frames"]==73 for x in output))
            self.assertTrue(all(x["width"]==480 and x["height"]==832 for x in output))
            self.assertEqual(len({x["prompt"] for x in output}),3)

    def test_rejects_8gb_unfriendly_resolution_and_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);assets={}
            for name in jobs.PERSONAS:
                x=p/(name+".png");x.touch();assets[name]=str(x)
            with self.assertRaisesRegex(ValueError,"<=480x832"):
                jobs.compile_jobs(assets,width=720,height=1280)
            with self.assertRaisesRegex(ValueError,"2-5s"):
                jobs.compile_jobs(assets,seconds=12)

if __name__=="__main__":unittest.main()
