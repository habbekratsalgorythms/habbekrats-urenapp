#!/usr/bin/env python3
"""Offline delivery QA for the €79 ten-caption content service (stdlib only).

The program NEVER generates factual claims, charges payments, sends email or posts
to social media. Human-reviewed JSON is mandatory, then exports local CSV and TXT.
Do not commit customer orders or real customer data to the public repository.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path

PRICE_EX_VAT_EUR = "79.00"
CAPTIONS_PER_ORDER = 10
CORRECTION_ROUNDS_INCLUDED = 2
FIRST_DELIVERY_BUSINESS_DAYS = 5
CORRECTION_REQUEST_BUSINESS_DAYS = 5
ALLOWED_STATUS = {"verified", "needs_customer_confirmation"}

def check(order):
    """Return validated posts or raise; never assert AI generated facts are true."""
    if not isinstance(order, dict):
        raise ValueError("Order must be a JSON object")
    if not order.get("briefing_complete") or not order.get("order_confirmed"):
        raise ValueError("Complete briefing AND confirmed order are required")
    if order.get("human_editor_reviewed") is not True:
        raise ValueError("Human editorial review must be confirmed")
    ref = order.get("reference")
    if not isinstance(ref, str) or not re.fullmatch(r"[A-Za-z0-9_-]{3,40}", ref):
        raise ValueError("Use a non-identifying 3–40 character reference")
    posts=order.get("posts")
    if not isinstance(posts, list) or len(posts)!=CAPTIONS_PER_ORDER:
        raise ValueError("Exactly ten posts are required")
    seen=set()
    for n,p in enumerate(posts,1):
        if not isinstance(p,dict) or p.get("number")!=n:
            raise ValueError("Posts must be numbered consecutively 1–10")
        for key in ("publish_date","platform","angle","caption","cta","fact_check","editor_note"):
            if not isinstance(p.get(key),str) or not p[key].strip():
                raise ValueError(f"Post {n}: missing {key}")
        try:
            date.fromisoformat(p["publish_date"])
        except ValueError as exc:
            raise ValueError(f"Post {n}: YYYY-MM-DD publication proposal required") from exc
        if p["fact_check"] not in ALLOWED_STATUS:
            raise ValueError(f"Post {n}: unsupported fact-check status")
        if p["fact_check"]=="needs_customer_confirmation" and not p["editor_note"].strip():
            raise ValueError(f"Post {n}: customer confirmation needs a note")
        caption=p["caption"].strip()
        if len(caption)<30 or len(caption)>2200:
            raise ValueError(f"Post {n}: caption length must be 30–2200 chars")
        if any(marker in caption.lower() for marker in ("[invullen]", "lorem ipsum", "placeholder", "tbd")):
            raise ValueError(f"Post {n}: unfinished placeholder")
        key=" ".join(caption.lower().split())
        if key in seen:
            raise ValueError(f"Post {n}: duplicate caption")
        seen.add(key)
    return posts

def export(order,output_dir):
    posts=check(order)
    dest=Path(output_dir).resolve()
    dest.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in posts:
        rows.append({
            "Nummer":p["number"],"Voorgestelde datum":p["publish_date"],
            "Platform":p["platform"],"Invalshoek":p["angle"],
            "Caption":p["caption"],"CTA":p["cta"],
            "Factcheck":p["fact_check"],"Redactienotitie":p["editor_note"]})
    csvpath=dest/f"{order['reference']}-contentplanning.csv"
    with csvpath.open("w",encoding="utf-8-sig",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),delimiter=";")
        writer.writeheader();writer.writerows(rows)
    txtpath=dest/f"{order['reference']}-levering.txt"
    text=[
        "HABBEKRATS STUDIO — CONCEPTLEVERING",
        f"Referentie: {order['reference']}",
        "Pakket: 10 Nederlandse captions met publicatieplanning.",
        "Vast pakket: €79 excl. btw. Geen automatische factuur/betaling.",
        "Eerste levering: 5 werkdagen na complete briefing EN opdrachtbevestiging.",
        "Twee gebundelde correctierondes. Correctieverzoek binnen 5 werkdagen na eerste levering.",
        "Controleer alle gemarkeerde feiten vóór daadwerkelijke publicatie.",
        "Dit programma publiceert niets automatisch.",""]
    for p in posts:
        text.extend([f"POST {p['number']:02d} | {p['publish_date']} | {p['platform']} | {p['angle']}",
                     p["caption"],f"CTA: {p['cta']}",
                     f"Factcheck: {p['fact_check']} | {p['editor_note']}",""])
    txtpath.write_text("\n".join(text),encoding="utf-8")
    return csvpath,txtpath

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft_json",type=Path)
    parser.add_argument("--out",default="output/content-levering")
    args=parser.parse_args()
    order=json.loads(args.draft_json.read_text(encoding="utf-8"))
    outputs=export(order,args.out)
    for p in outputs: print(p)

if __name__=="__main__":
    main()
