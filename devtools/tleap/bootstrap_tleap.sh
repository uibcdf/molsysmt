#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
amberclassic_dir="${AMBERCLASSIC_DIR:-${repo_root}/../AmberClassic}"

if [[ ! -d "${amberclassic_dir}" ]]; then
  parent_dir="$(dirname "${amberclassic_dir}")"
  mkdir -p "${parent_dir}"
  if command -v gh >/dev/null 2>&1; then
    echo "[tleap-bootstrap] Cloning AmberClassic with gh into ${amberclassic_dir}"
    gh repo clone Amber-MD/AmberClassic "${amberclassic_dir}"
  else
    echo "[tleap-bootstrap] gh not found; cloning AmberClassic with git into ${amberclassic_dir}"
    git clone https://github.com/Amber-MD/AmberClassic "${amberclassic_dir}"
  fi
else
  echo "[tleap-bootstrap] Using existing AmberClassic clone at ${amberclassic_dir}"
fi

if [[ ! -f "${amberclassic_dir}/configure" ]]; then
  echo "[tleap-bootstrap] ERROR: configure script was not found in ${amberclassic_dir}" >&2
  exit 1
fi

pushd "${amberclassic_dir}" >/dev/null

echo "[tleap-bootstrap] Running configure $*"
./configure "$@"

jobs="${JOBS:-}"
if [[ -z "${jobs}" ]]; then
  if command -v nproc >/dev/null 2>&1; then
    jobs="$(nproc)"
  elif command -v sysctl >/dev/null 2>&1; then
    jobs="$(sysctl -n hw.ncpu)"
  else
    jobs="1"
  fi
fi

echo "[tleap-bootstrap] Running make install -j ${jobs}"
make install -j "${jobs}"

popd >/dev/null

echo
echo "[tleap-bootstrap] Build completed."
echo "[tleap-bootstrap] Next step:"
echo "  source \"${amberclassic_dir}/AmberClassic.sh\""
echo "[tleap-bootstrap] Then verify with:"
echo "  bash \"${repo_root}/devtools/tleap/check_tleap.sh\""
