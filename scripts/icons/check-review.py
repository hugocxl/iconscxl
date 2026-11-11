#!/usr/bin/env python3
"""Reject missing or stale visual reviews; never create review approval automatically."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
review = json.loads((root / 'docs/icon-review.json').read_text())
# Preserve the original review as a historical baseline. A narrowly scoped,
# visually inspected tone revision can supersede a default hash without
# falsely closing the separate strict audit's geometry/meaning findings.
tone_review = json.loads((root / 'docs/tone-review.json').read_text())
assert tone_review['scope'] == 'selective-tone'
tone_entries = {entry['name']: entry for entry in tone_review['icons']}
assert len(tone_entries) == len(tone_review['icons']), 'Duplicate tone reviews'
observed_tone_styles = set()
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
        expected = entry['sha256'][style]
        if name in tone_entries and style in tone_entries[name]['styles']:
            tone = tone_entries[name]
            assert tone['result'] == 'pass'
            assert tone['assessment'].strip() and tone['evidence'], f'Missing tone inspection: {name}'
            assert tone['beforeSha256'][style] == expected, f'Tone review baseline drift: {name}/{style}'
            assert tone['defaultTone'] == icon['defaultTone'], f'Tone decision drift: {name}'
            expected = tone['sha256'][style]
            observed_tone_styles.add((name,style))
        assert actual == expected, f'Stale visual review: {name}/{style}; render and inspect the change before updating the record'
        count += 1
assert observed_tone_styles == {(name,style) for name,tone in tone_entries.items() for style in tone['styles']}, 'Orphan tone reviews'
print(f'Review hashes current: {len(entries)} names, {count} SVGs; {len(tone_entries)} selective-tone follow-ups. Separate strict-audit findings remain open.')
