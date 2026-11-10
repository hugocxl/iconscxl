#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I scripts/icons/normalize.py icons
python3 -I scripts/icons/test-adapt-brand.py
if ! git diff --exit-code -- icons; then
  echo "Icons must be normalized before committing" >&2
  exit 1
fi
python3 -I scripts/generate.py --check
npm test
npm run typecheck
npm pack --workspaces --dry-run --json > /dev/null
echo "validation passed"
