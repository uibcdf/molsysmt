#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
tleap_bin="${TLEAP_BIN:-}"
amberclassic_dir="${AMBERCLASSIC_DIR:-${repo_root}/../AmberClassic}"

if [[ -n "${tleap_bin}" ]] && [[ -x "${tleap_bin}" ]]; then
  export PATH="$(dirname "${tleap_bin}"):${PATH}"
fi

if ! command -v tleap >/dev/null 2>&1; then
  if [[ -x "${amberclassic_dir}/bin/tleap" ]]; then
    export PATH="${amberclassic_dir}/bin:${PATH}"
    echo "[tleap-check] INFO: using provisional tleap from ${amberclassic_dir}/bin/tleap"
  fi
fi

if ! command -v tleap >/dev/null 2>&1; then
  echo "[tleap-check] ERROR: 'tleap' was not found in PATH." >&2
  echo "[tleap-check] Hint: source ../AmberClassic/AmberClassic.sh" >&2
  echo "[tleap-check] Or run with TLEAP_BIN=/abs/path/to/tleap" >&2
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
