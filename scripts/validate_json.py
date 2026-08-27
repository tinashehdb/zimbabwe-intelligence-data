import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def main():
    json_files = sorted(ROOT.rglob('*.json'))
    if not json_files:
        raise SystemExit('No JSON files found')

    errors = []
    for path in json_files:
        try:
            load_json(path)
            print(f'OK  {path.relative_to(ROOT)}')
        except Exception as exc:
            errors.append((path, exc))
            print(f'ERR {path.relative_to(ROOT)}: {exc}')

    if errors:
        raise SystemExit(f'{len(errors)} JSON file(s) failed basic validation')

    manifest = load_json(ROOT / 'manifest.json')
    assert manifest.get('feedVersion'), 'manifest.feedVersion missing'
    assert manifest.get('country') == 'Zimbabwe', 'manifest.country must be Zimbabwe'

    datasets = manifest.get('datasets')
    assert isinstance(datasets, dict) and datasets, 'manifest.datasets missing or empty'

    required = ['cabinet', 'parliament', 'economy', 'tenders', 'animalHealth', 'health', 'weather', 'alerts']
    for key in required:
        assert key in datasets, f'manifest.datasets.{key} missing'
        item = datasets[key]
        assert 'status' in item, f'{key}.status missing'
        assert 'version' in item, f'{key}.version missing'
        assert 'url' in item, f'{key}.url missing'
        parsed = urlparse(item['url'])
        assert parsed.scheme == 'https', f'{key}.url must use https'

    cabinet = load_json(ROOT / 'cabinet' / 'cabinet_briefings_2026.json')
    briefs = cabinet.get('briefings')
    assert isinstance(briefs, list), 'cabinet.briefings must be an array'
    ids = [b.get('id') for b in briefs]
    assert all(ids), 'Every Cabinet briefing must have an id'
    assert len(ids) == len(set(ids)), 'Duplicate Cabinet briefing ids found'

    parliament = load_json(ROOT / 'parliament' / 'bills.json')
    bills = parliament.get('bills')
    assert isinstance(bills, list), 'parliament.bills must be an array'
    bill_ids = [b.get('id') for b in bills]
    assert all(bill_ids), 'Every Parliament bill must have an id'
    assert len(bill_ids) == len(set(bill_ids)), 'Duplicate Parliament bill ids found'

    print('All intelligence feed checks passed.')


if __name__ == '__main__':
    main()
