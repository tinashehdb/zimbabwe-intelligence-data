# Secure DVS Weekly Highlights publishing

This repository is publicly accessible. Never commit internal Weekly Highlights attachments, email content, individual contact details, premises-level risk records or detailed unreleased case line lists.

## Authorized workflow

1. Obtain DVS approval for public release of selected aggregates.
2. Prepare a redacted JSON file locally in a secure workspace, with `approvedForPublicRelease: true`, `reviewedBy`, `weekEnding`, and an `observations` array.
3. Run `python scripts/review_weekly_export.py <reviewed.json>`.
4. Have a second human reviewer inspect summaries and free-text fields: the validator cannot identify all sensitive information.
5. Merge only approved observations into their month under `animal_health/weekly/YYYY-MM.json`. Reject repeated observation IDs.
6. Recalculate month `reportCount` and `recordCount`, then rebuild `animal_health/weekly/index_2026.json` and update `animal_health/events.json` and `manifest.json`.
7. Validate all JSON and check Android refresh with manifest versioning and cached fallback.

## Known source gaps (not yet published)

DVS reports were located for weeks ending 18 September, 25 September and 2 October 2026. Their original source content is **not** incorporated in the public feed. The latest publicly indexed week remains 4 September 2026. Do not extend the coverage date until approval and publication are complete.

## Suggested Android behavior

On open or manual refresh: fetch `manifest.json` with conditional HTTP caching, compare `datasets.animalHealth.version`, fetch `animal_health/events.json` and the weekly index, then fetch changed `monthlyFeeds[].url` files. Validate before replacing cached data. Show both source-reporting date and last successful sync. Never present unconnected or stale channels as live. For internal detail, use a separate authenticated endpoint with explicit access controls and audit logs, never a raw.githubusercontent.com URL.
