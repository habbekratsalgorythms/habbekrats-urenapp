"""Validate three separate, self-original AI influencer storyboards (stdlib only).

Does not generate artwork, charge for AI providers, or authorize publishing.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).parent
EXPECTED = {"vexa-volt", "pip-patch", "blop"}

def validate_all():
    paths = sorted((ROOT/"concepts").glob("*.json"))
    if {p.stem for p in paths} != EXPECTED:
        raise ValueError("All three approved concept files are required, no others")
    concepts=[json.loads(p.read_text(encoding="utf-8")) for p in paths]
    names=set()
    for item in concepts:
        if item["id"] not in EXPECTED or item["working_name"] in names:
            raise ValueError("Concept IDs and tentative names must be unique")
        names.add(item["working_name"])
        if item["name_status"]!="WORKING_NAME_NOT_TRADEMARK_VERIFIED":
            raise ValueError("Never imply a working name is trademark-cleared")
        for key in ["art_direction","voice","quirk","audience"]:
            if not isinstance(item.get(key),str) or len(item[key])<40:
                raise ValueError(item["id"]+": incomplete creative identity "+key)
        pilot=item["pilot"]
        if pilot["commercially_released"] is not False:
            raise ValueError("No public release without human approval")
        if not 12 <= pilot["seconds"] <= 30:
            raise ValueError("Pilots should be short form")
        if len(pilot.get("shots",[]))<5:
            raise ValueError("At least five meaningful visual beats are required")
        end=0
        for shot in pilot["shots"]:
            if shot["start"]!=end or shot["end"]<=shot["start"]:
                raise ValueError(item["id"]+": broken sequential shot timing")
            if not all(isinstance(shot.get(k),str) and shot[k].strip()
                       for k in ("visual","overlay","sfx")):
                raise ValueError(item["id"]+": missing original visual/sound direction")
            end=shot["end"]
        if end!=pilot["seconds"]:
            raise ValueError(item["id"]+": duration and shot timeline mismatch")
        if not item["pilot"]["sample_script"]:
            raise ValueError(item["id"]+": no pilot")
    return concepts

if __name__ == "__main__":
    for item in validate_all():
        print(item["working_name"],item["pilot"]["seconds"],"sec",len(item["pilot"]["shots"]),"shots: CREATIVE DRAFT ONLY")
