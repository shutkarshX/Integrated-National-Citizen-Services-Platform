#!/usr/bin/env bash
# Phase 1 Linux/CLI automation: check the local OS PBL project and run its tests.
# Run from the repository root: bash scripts/phase1_check.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=== OS PBL Phase 1 project check ==="
echo "Project: Integrated National Citizen Services Platform"
echo "Location: $ROOT_DIR"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 was not found. Install Python 3 and retry." >&2
  exit 1
fi

python3 --version

required_files=(
  "main.py"
  "os_platform/models.py"
  "os_platform/scheduler.py"
  "os_platform/storage.py"
  "tests/test_scheduler.py"
  "tests/test_storage.py"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "ERROR: Required project file missing: $file" >&2
    exit 1
  fi
  printf 'OK: %s\n' "$file"
done

echo
echo "=== Running unit tests ==="
python3 -m unittest discover -s tests -v

echo
echo "=== Running synthetic CLI demonstration ==="
python3 main.py

echo
echo "Phase 1 project check completed successfully."
