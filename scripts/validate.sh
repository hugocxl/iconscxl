#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I scripts/icons/normalize.py icons --check
python3 -I scripts/icons/test-adapt-brand.py
python3 -I scripts/icons/check-artwork.py
python3 -I scripts/icons/check-review.py
python3 -I scripts/generate.py --check
npm test
npm run typecheck
npm pack --workspaces --dry-run --json > /dev/null
echo "validation passed"
