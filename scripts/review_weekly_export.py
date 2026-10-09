#!/usr/bin/env python3
"""Validate an authorized, redacted Weekly Highlights JSON export.

This script deliberately does not read Gmail or publish to GitHub. Only a
reviewed export should be supplied, and output stays on the local machine.
Usage: python scripts/review_weekly_export.py /secure/path/week.json
"""
import json
import sys
from datetime import date
from pathlib import Path

ALLOWED = {"id", "eventDate", "diseaseCode", "title", "signals",
           "summary", "metrics", "caseClassification", "sourceLabelWeek"}
PRIVATE = {"email", "phone", "contact", "patient", "owner", "farmName",
           "rawDocument", "attachment", "gps", "coordinates", "personName"}

def validate(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert isinstance(data, dict), "Expected JSON object"
    assert data.get("approvedForPublicRelease") is True, "Explicit publication approval required"
    assert isinstance(data.get("reviewedBy"), str) and data["reviewedBy"].strip(), "Reviewer required"
    date.fromisoformat(data["weekEnding"])
    observations = data.get("observations")
    assert isinstance(observations, list), "observations must be an array"
    identifiers = set()
    for o in observations:
        assert isinstance(o, dict), "Each observation must be an object"
        assert set(o).issubset(ALLOWED), "Unexpected fields: " + repr(set(o)-ALLOWED)
        assert not (set(o) & PRIVATE), "Private fields forbidden"
        assert isinstance(o.get("id"), str) and o["id"], "Observation id required"
        assert o["id"] not in identifiers, "Duplicate ID: " + o["id"]
        identifiers.add(o["id"])
        date.fromisoformat(o["eventDate"])
        assert o["eventDate"] <= data["weekEnding"], "Future-dated event"
        assert isinstance(o.get("diseaseCode"), str), "diseaseCode required"
        assert o.get("caseClassification", "not_applicable") in {
            "suspected", "confirmed", "not_applicable", "unknown"
        }, "Case classification invalid"
        assert isinstance(o.get("metrics", {}), dict), "metrics must be object"
    print(f"PASS: {len(observations)} reviewed observations; week ending {data['weekEnding']}")
    print("NOTICE: manual disclosure review remains mandatory; this is not a privacy guarantee.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: review_weekly_export.py reviewed.json")
    validate(sys.argv[1])
