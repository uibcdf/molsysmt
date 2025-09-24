
#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# MolSysMT development bootstrap with activation switch & flexible path discovery
# - Creates/updates an environment from development_env.yaml
# - Installs MolSysMT in editable mode (no deps)
# - Optional Jupyter kernel registration
# - Supports overriding Python version
# - Auto-discovers development_env.yaml regardless of current working directory:
#     * parent-of-repo, repo root, molsysmt/, or devtools/
#
# Usage examples:
#   bash devtools/start_dev.sh --mode print
#   source devtools/start_dev.sh --mode persist
#   bash devtools/start_dev.sh --mode print --python 3.12
#
# Notes:
# - To persist activation, you MUST 'source' this script.
# - By default the script reads Python version from the YAML; --python overrides it.
# ------------------------------------------------------------------------------

ENV_NAME="molsysmt"
MODE="print"                    # 'print' (default) or 'persist'
PYTHON_VERSION=""
REGISTER_KERNEL=${REGISTER_KERNEL:-"1"}

# If provided, we'll try to honor it (can be absolute or relative).
USER_ENV_YAML="${USER_ENV_YAML:-""}"   # optional via env var
CLI_ENV_YAML=""                        # optional via --env-yaml

print_help() {
  cat <<'EOF'
Usage: devtools/start_dev.sh [OPTIONS]

Options:
  --mode {print|persist}
      - print   : Do not activate the environment; print activation instructions (default).
      - persist : Activate and keep the environment active after finishing.
                  IMPORTANT: use 'source' to persist:
                      source devtools/start_dev.sh --mode persist

  --python <version>
      Override Python version (e.g. 3.11, 3.12). If omitted, YAML decides.

  --env-name <name>
      Environment name (default: molsysmt)

  --env-yaml <path>
      Path to the YAML file. If omitted, the script auto-discovers it
      (works when called from parent-of-repo, repo root, molsysmt/, or devtools/).

  --no-kernel
      Skip Jupyter kernel registration (same as REGISTER_KERNEL=0)

  -h, --help
      Show this help and exit.

Environment variables:
  REGISTER_KERNEL=0|1   Disable/enable Jupyter kernel registration (default: 1)
  USER_ENV_YAML=<path>  Provide YAML path via env var (overridden by --env-yaml)

Examples:
  # Setup only, print activation instructions:
  bash devtools/start_dev.sh --mode print

  # Setup and persist activation in current shell:
  source devtools/start_dev.sh --mode persist

  # Setup with Python 3.12:
  bash devtools/start_dev.sh --mode print --python 3.12
EOF
}

# --- Parse args ----------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-}"; shift 2 ;;
    --python) PYTHON_VERSION="${2:-}"; shift 2 ;;
    --env-name) ENV_NAME="${2:-}"; shift 2 ;;
    --env-yaml) CLI_ENV_YAML="${2:-}"; shift 2 ;;
    --no-kernel) REGISTER_KERNEL="0"; shift ;;
    -h|--help) print_help; exit 0 ;;
    *) echo "Unknown option: $1"; echo; print_help; exit 1 ;;
  esac
done

if [[ "$MODE" != "print" && "$MODE" != "persist" ]]; then
  echo "ERROR: --mode must be 'print' or 'persist'"
  exit 1
fi

# --- Detect if sourced (needed for --mode persist) ------------------------------
IS_SOURCED="0"
if [[ "${BASH_SOURCE[0]:-}" != "$0" ]]; then IS_SOURCED="1"; fi

# --- Utility: absolute path resolver -------------------------------------------
abspath() { python - <<'PY' "$1"
import os, sys
p = sys.argv[1]
print(os.path.abspath(p))
PY
}

# --- Resolve repository paths ---------------------------------------------------
# SCRIPT_DIR = directory where this script physically lives (repo/devtools)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# REPO_ROOT = one level up from devtools/
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

# --- Auto-discover ENV_YAML ----------------------------------------------------
# Candidate locations from *current working directory*
CWD_CANDIDATES=(
  "molsysmt/devtools/conda-envs/development_env.yaml"
  "devtools/conda-envs/development_env.yaml"
  "conda-envs/development_env.yaml"
)

# Candidate locations from the *script location* (most robust)
SCRIPT_CANDIDATES=(
  "${REPO_ROOT}/molsysmt/devtools/conda-envs/development_env.yaml"
  "${SCRIPT_DIR}/conda-envs/development_env.yaml"
  "${REPO_ROOT}/devtools/conda-envs/development_env.yaml"
)

resolve_env_yaml() {
  # Precedence:
  #   1) --env-yaml if provided and exists
  #   2) USER_ENV_YAML (env var) if provided and exists
  #   3) candidates relative to CWD if exist
  #   4) candidates anchored to script/repo if exist
  local p

  if [[ -n "$CLI_ENV_YAML" ]]; then
    p="$CLI_ENV_YAML"
    [[ -f "$p" ]] || { echo "ERROR: --env-yaml '$p' not found"; exit 1; }
    echo "$(abspath "$p")"; return
  fi

  if [[ -n "$USER_ENV_YAML" ]]; then
    p="$USER_ENV_YAML"
    [[ -f "$p" ]] || { echo "ERROR: USER_ENV_YAML='$p' not found"; exit 1; }
    echo "$(abspath "$p")"; return
  fi

  for p in "${CWD_CANDIDATES[@]}"; do
    if [[ -f "$p" ]]; then echo "$(abspath "$p")"; return; fi
  done

  for p in "${SCRIPT_CANDIDATES[@]}"; do
    if [[ -f "$p" ]]; then echo "$(abspath "$p")"; return; fi
  done

  echo "ERROR: Could not locate 'development_env.yaml'. Tried:"
  printf '  - %s\n' "${CWD_CANDIDATES[@]}" "${SCRIPT_CANDIDATES[@]}"
  exit 1
}

ENV_YAML="$(resolve_env_yaml)"
echo "[setup] Using environment YAML: ${ENV_YAML}"

# --- Package manager selection --------------------------------------------------
have_cmd() { command -v "$1" >/dev/null 2>&1; }

PM=""; RUN=""
if have_cmd micromamba; then
  PM="micromamba"; RUN="micromamba run -n ${ENV_NAME}"
elif have_cmd mamba; then
  PM="mamba"; RUN="mamba run -n ${ENV_NAME}"
elif have_cmd conda; then
  PM="conda"; RUN="conda run -n ${ENV_NAME}"
else
  echo "[setup] No conda/mamba/micromamba found."
  echo "[setup] Please install one of them and ensure it's in your PATH."
  exit 1
  #echo "[setup] Installing micromamba locally..."
  #curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
  #export PATH="$PWD/bin:$PATH"
  #PM="micromamba"; RUN="micromamba run -n ${ENV_NAME}"
fi

# --- Create or update environment ----------------------------------------------
echo "[setup] Ensuring environment '${ENV_NAME}' from YAML"

if [[ -n "$PYTHON_VERSION" ]]; then
  echo "[setup] Overriding Python version to $PYTHON_VERSION"
  if [[ "$PM" == "micromamba" ]]; then
    micromamba create -y -n "${ENV_NAME}" python="${PYTHON_VERSION}" -f "${ENV_YAML}" || \
    micromamba env update -n "${ENV_NAME}" -f "${ENV_YAML}" && \
    micromamba install -y -n "${ENV_NAME}" python="${PYTHON_VERSION}"
  else
    if ! ${PM} env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
      ${PM} create -n "${ENV_NAME}" -y -f "${ENV_YAML}" python="${PYTHON_VERSION}"
    else
      ${PM} install -n "${ENV_NAME}" -y python="${PYTHON_VERSION}"
      ${PM} env update -n "${ENV_NAME}" -f "${ENV_YAML}"
    fi
  fi
else
  if [[ "$PM" == "micromamba" ]]; then
    micromamba create -y -n "${ENV_NAME}" -f "${ENV_YAML}" || \
    micromamba env update -n "${ENV_NAME}" -f "${ENV_YAML}"
  else
    if ! ${PM} env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
      ${PM} env create -n "${ENV_NAME}" -f "${ENV_YAML}"
    else
      ${PM} env update -n "${ENV_NAME}" -f "${ENV_YAML}"
    fi
  fi
fi

# --- Editable install -----------------------------------------------------------
echo "[setup] Installing MolSysMT in editable mode (no deps)..."
${RUN} python -m pip install --no-deps --editable .

# --- Optional kernel registration ----------------------------------------------
if [[ "${REGISTER_KERNEL}" == "1" ]]; then
  echo "[setup] Registering Jupyter kernel 'Python (molsysmt)'..."
  ${RUN} python -m ipykernel install --user --name "${ENV_NAME}" --display-name "Python (molsysmt)"
fi

# --- Diagnostics ----------------------------------------------------------------
echo "[setup] Environment ready."
${RUN} python - <<'PY'
import sys
print("Python:", sys.version.split()[0])
try:
    import numpy as np, pandas as pd
    print("numpy:", np.__version__)
    print("pandas:", pd.__version__)
except Exception as e:
    print("Package probe warning:", e)
try:
    import openmm as mm
    plats = [mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())]
    print("OpenMM platforms:", plats)
except Exception:
    pass
PY

# --- Activation instructions or persistence ------------------------------------
emit_activation_instructions() {
  echo
  echo "Activation instructions:"
  if [[ "$PM" == "micromamba" ]]; then
    echo 'eval "$(micromamba shell hook -s bash)"'
    echo "micromamba activate ${ENV_NAME}"
  else
    BASE="$(${PM} info --base)"
    echo "source \"${BASE}/etc/profile.d/conda.sh\""
    echo "${PM} activate ${ENV_NAME}"
  fi
  echo
}

if [[ "$MODE" == "print" ]]; then
  emit_activation_instructions
  echo "[setup] Done. Environment is NOT activated (mode=print)."
  exit 0
fi

if [[ "$IS_SOURCED" == "1" ]]; then
  if [[ "$PM" == "micromamba" ]]; then
    eval "$(micromamba shell hook -s bash)"
    micromamba activate "${ENV_NAME}"
  else
    BASE="$(${PM} info --base)"
    # shellcheck disable=SC1090
    source "${BASE}/etc/profile.d/conda.sh"
    ${PM} activate "${ENV_NAME}"
  fi
  echo "[setup] Environment '${ENV_NAME}' is now ACTIVE (mode=persist)."
else
  echo "[setup] WARNING: --mode persist requested but script not sourced."
  emit_activation_instructions
  exit 1
fi

