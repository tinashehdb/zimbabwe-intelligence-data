# Cabinet Intelligence data channels

The Android client should fetch manifest.json on launch and on manual refresh, compare each dataset version, download changed JSON feeds, validate records, then atomically replace its cached data. On failure, retain its last-known-good cache and visibly show the last successful sync and the source effective date separately.

## Feed status
The manifest is the authoritative channel registry. `connected_partial` means that the dataset contains usable records but is not complete. `not_connected` and `direct_api_planned` must not be displayed as current.

## Weekly Highlights
Animal-health weekly data are indexed at `animal_health/weekly/index_2026.json`; the Android client must use `monthlyFeeds[].url` to fetch monthly partitions. Missing reports are unknown, not zero. Cumulative metrics must not be added together across weeks. Suspected observations must remain separate from confirmed events.

Only records authorized for inclusion in a public repository may be committed. Source documents and any nonpublic material should remain in an authenticated private data source.

## Recommended client display
Per channel: source period, latest record date, last successful synchronization, source attribution, coverage warning, and an explicit retry control. Keep existing records visible when a refresh fails, clearly marked as cached.

## Integrity
Run `python scripts/validate_json.py` and `python scripts/check_feed_freshness.py` before release. A successful JSON parse does not establish source accuracy.
