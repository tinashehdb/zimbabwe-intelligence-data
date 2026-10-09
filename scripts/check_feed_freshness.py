#!/usr/bin/env python3
"""Report freshness for every configured Cabinet Intelligence channel.

Usage: python scripts/check_feed_freshness.py [YYYY-MM-DD]
Exit 0 for a report; exits 1 when the manifest is invalid.
"""
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_AGE_DAYS = {
    "cabinet": 14, "parliament": 14, "economy": 3,
    "tenders": 14, "animalHealth": 14, "health": 30,
    "weather": 2, "alerts": 2,
}

def parse_day(value):
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None

def main():
    today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(timezone.utc).date()
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    datasets = manifest["datasets"]
    print(f"Cabinet Intelligence freshness audit | {today}")
    print("Channel       Status                         Latest date   Age (days)  Assessment")
    for name in MAX_AGE_DAYS:
        dataset = datasets.get(name, {})
        status = str(dataset.get("status", "missing"))
        day = next((d for k in ("effectiveDate", "coverageTo", "snapshotAsOf", "lastChecked", "updatedAt") if (d := parse_day(dataset.get(k))) is not None), None)
        age = (today - day).days if day else None
        if status in {"not_connected", "direct_api_planned", "missing"}:
            assessment = "UNCONNECTED"
        elif age is None:
            assessment = "UNKNOWN"
        elif age < 0:
            assessment = "FUTURE DATE - CHECK"
        elif age > MAX_AGE_DAYS[name]:
            assessment = "STALE - VERIFY SOURCE"
        else:
            assessment = "DATE WITHIN THRESHOLD"
        print(f"{name:13} {status:30} {str(day or '-'):13} {str(age if age is not None else '-'):10} {assessment}")
    print("\nThis checks dates and connection labels, not whether source records are factually correct.")
if __name__ == "__main__":
    main()
