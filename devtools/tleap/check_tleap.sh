#!/usr/bin/env bash

set -euo pipefail

if ! command -v tleap >/dev/null 2>&1; then
  echo "[tleap-check] ERROR: 'tleap' was not found in PATH." >&2
  echo "[tleap-check] Hint: source ../AmberClassic/AmberClassic.sh" >&2
  exit 1
fi

echo "[tleap-check] Found: $(command -v tleap)"

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "${tmpdir}"
}
trap cleanup EXIT

cat > "${tmpdir}/leap.in" <<'EOF'
quit
EOF

output_file="${tmpdir}/tleap.out"
if tleap -f "${tmpdir}/leap.in" > "${output_file}" 2>&1; then
  echo "[tleap-check] Smoke test passed."
else
  echo "[tleap-check] ERROR: tleap smoke test failed. Output follows:" >&2
  cat "${output_file}" >&2
  exit 1
fi
