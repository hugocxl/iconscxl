#!/usr/bin/env python3
"""Reject missing or stale visual reviews; never create review approval automatically."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
review = json.loads((root / 'docs/icon-review.json').read_text())
catalog = json.loads((root / 'catalog.json').read_text())
entries = {entry['name']: entry for entry in review['icons']}
assert len(entries) == len(review['icons']), 'Duplicate review entries'
assert set(entries) == {c['name'] for c in catalog}, 'Review coverage differs from catalog'
assert review['sizesPoints'] == [16, 24, 32] and review['tints'] == ['light', 'dark']
sheets = {}
for sheet in review['sheets']:
    for name in sheet['names']:
        assert name not in sheets, f'Duplicate sheet coverage: {name}'
        sheets[name] = sheet
assert set(sheets) == set(entries), 'Sheet coverage differs from reviewed icons'
count = 0
for icon in catalog:
    name = icon['name']
    entry = entries[name]
    assert entry['category'] == icon['category'] == sheets[name]['category']
    assert entry['sheet'] == sheets[name]['file']
    assert entry['result'] == 'reviewed' and entry['assessment'].strip()
    assert not entry['unresolvedFindings'], f'Unresolved findings: {name}'
    assert set(entry['sha256']) == set(icon['styles']), f'Style coverage: {name}'
    for style in icon['styles']:
        relative = f'{name}.svg' if style == 'duotone' else f'styles/{style}/{name}.svg'
        actual = hashlib.sha256((root / 'icons' / relative).read_bytes()).hexdigest()
        assert actual == entry['sha256'][style], f'Stale visual review: {name}/{style}; render and inspect the change before updating the record'
        count += 1
print(f'Visual review current: {len(entries)} names, {count} SVG hashes, {len(review["sheets"])} sheets')
