"""Fail-closed tests for LOCAL_ONLY Wan 5B image-to-video worker."""
import argparse
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(BASE))
import local_wan_render as wan

def fixture():
    # Minimal native ComfyUI API export with official Wan2.2 5B built-in nodes.
    return {
      "37":{"class_type":"UNETLoader","inputs":{"unet_name":wan.MODEL,"weight_dtype":"default"}},
      "38":{"class_type":"CLIPLoader","inputs":{"clip_name":wan.TEXT_ENCODER,"type":"wan","device":"default"}},
      "39":{"class_type":"VAELoader","inputs":{"vae_name":wan.VAE}},
      "56":{"class_type":"LoadImage","inputs":{"image":"source.png"}},
      "55":{"class_type":"Wan22ImageToVideoLatent","inputs":{
          "width":1280,"height":704,"length":121,"batch_size":1,
          "vae":["39",0],"start_image":["56",0]}},
      "6":{"class_type":"CLIPTextEncode","inputs":{"text":"original pos","clip":["38",0]}},
      "7":{"class_type":"CLIPTextEncode","inputs":{"text":"original neg","clip":["38",0]}},
      "48":{"class_type":"ModelSamplingSD3","inputs":{"model":["37",0],"shift":8}},
      "3":{"class_type":"KSampler","inputs":{"seed":1,"steps":20,"cfg":5,
          "sampler_name":"uni_pc","scheduler":"simple","denoise":1,
          "model":["48",0],"positive":["6",0],"negative":["7",0],
          "latent_image":["55",0]}},
      "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["39",0]}},
      "57":{"class_type":"CreateVideo","inputs":{"images":["8",0],"fps":24}},
      "58":{"class_type":"SaveVideo","inputs":{"video":["57",0],
          "filename_prefix":"video/ComfyUI","format":"auto","codec":"auto"}},
    }

class WanLocalTests(unittest.TestCase):
    def test_all_three_personas_rewrite_external_prompt_and_dimensions(self):
        original=fixture()
        for name in wan.PERSONAS:
            with self.subTest(name=name):
                result=wan.build_workflow(original,name,name+".png")
                self.assertEqual(result["55"]["inputs"]["width"],480)
                self.assertEqual(result["55"]["inputs"]["height"],832)
                self.assertEqual(result["55"]["inputs"]["length"],73)
                self.assertEqual(result["55"]["inputs"]["batch_size"],1)
                self.assertEqual(result["56"]["inputs"]["image"],name+".png")
                self.assertIn(name, result["58"]["inputs"]["filename_prefix"])
                self.assertIn(wan.PERSONAS[name]["motion"],result["6"]["inputs"]["text"])
                self.assertNotEqual(result["7"]["inputs"]["text"],"original neg")
                self.assertEqual(result["3"]["inputs"]["steps"],20)
        self.assertEqual(original["55"]["inputs"]["width"],1280)  # copy-on-write

    def test_graph_with_any_unknown_node_denied(self):
        for bad in ("ExecutePython","HTTPGet","LoadVideo","CheckpointLoaderSimple"):
            wf=fixture();wf["100"]={"class_type":bad,"inputs":{}}
            with self.subTest(node=bad), self.assertRaises(ValueError):
                wan.validate_api_workflow(wf)

    def test_ui_export_is_not_api_export(self):
        with self.assertRaises(ValueError):
            wan.validate_api_workflow({"nodes":[{"id":1}]})

    def test_reject_changed_model(self):
        wf=fixture();wf["37"]["inputs"]["unet_name"]="some-other-model.safetensors"
        with self.assertRaisesRegex(ValueError,"Wrong model"):wan.validate_api_workflow(wf)

    def test_refuse_disconnected_image_to_video(self):
        wf=fixture();wf["55"]["inputs"]["start_image"]=None
        with self.assertRaisesRegex(ValueError,"Image-to-video"):wan.validate_api_workflow(wf)

    def test_refuse_aliasing_negative_prompt(self):
        wf=fixture();wf["3"]["inputs"]["negative"]=["6",0]
        with self.assertRaisesRegex(ValueError,"separate"):wan.validate_api_workflow(wf)

    def test_refuse_extra_node_input_structure(self):
        wf=fixture();wf["3"]["inputs"]["evil"]={"shell":"whoami"}
        with self.assertRaisesRegex(ValueError,"input structure"):wan.validate_api_workflow(wf)

    def test_refuse_changed_node_link(self):
        wf=fixture();wf["55"]["inputs"]["vae"]=["10000",0]
        with self.assertRaisesRegex(ValueError,"Graph link escapes"):wan.validate_api_workflow(wf)

    def test_refuse_image_name_traversal(self):
        for name in ("../foo.png","folder.png","unsafe;echo.png"):
            with self.subTest(name=name),self.assertRaises(ValueError):
                wan.build_workflow(fixture(),"vexa-volt",name)

    def test_refuse_any_non_loopback_port(self):
        for port in (22,80,443,4444,8500):
            with self.subTest(port=port),self.assertRaises(ValueError):
                wan._url(port,"/prompt")
        self.assertEqual(wan._url(8000,"/system_stats"),
                         "http://127.0.0.1:8000/system_stats")

    def test_real_png_signature_and_no_parent_escaping(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            image=root/"vexa-volt.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n"+b"0"*150)
            self.assertEqual(len(wan._read_image(root,"vexa-volt")),158)
            image.write_bytes(b"EVIL"+b"0"*150)
            with self.assertRaisesRegex(ValueError,"PNG signature"):
                wan._read_image(root,"vexa-volt")

    def test_offline_default_no_network_no_gpu_or_files_created(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);workflow=root/"template_api.json"
            workflow.write_text(json.dumps(fixture()),encoding="utf-8")
            render_dir=root/"not_created"
            with patch.object(wan,"_send",side_effect=AssertionError("Network must stay OFF")):
                with patch.object(sys,"argv",["local_wan_render.py",
                     "--workflow",str(workflow),"--images",str(root/"none"),
                     "--renders",str(render_dir)]):
                    self.assertEqual(wan.main(),0)
            self.assertFalse(render_dir.exists())

    def test_invalid_template_blocks_network_even_if_execute_flag_set(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);workflow=root/"bad.json"
            wf=fixture();wf["37"]["inputs"]["unet_name"]="wrong-model"
            workflow.write_text(json.dumps(wf),encoding="utf-8")
            with patch.object(wan,"_send",side_effect=AssertionError("No network")):
                with patch.object(sys,"argv",["local_wan_render.py",
                     "--workflow",str(workflow),"--images",str(root/"none"),
                     "--renders",str(root/"renders"),"--execute"]):
                    with self.assertRaises(ValueError):wan.main()

    def test_upload_only_png_image_and_reject_wrong_echo_filename(self):
        with patch.object(wan,"_send",return_value=b'{"name":"evil.png"}'):
            with self.assertRaisesRegex(ValueError,"exact image upload"):
                wan._upload_png(8000,b"\x89PNG\r\n\x1a\n"+b"x"*100,"vexa-volt")

if __name__=="__main__":
    unittest.main()
