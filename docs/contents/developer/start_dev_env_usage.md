# Development Environment Setup Guide

This repository provides a bootstrap script to simplify the setup of the MolSysMT development environment.  
The script automatically creates or updates the conda/mamba/micromamba environment, installs MolSysMT in editable mode, and optionally registers a Jupyter kernel.

The script is located at:
```
devtools/start_dev_env.sh
```

---

## 🚀 Basic Usage

### 1. Setup without activation
```bash
bash devtools/start_dev_env.sh --mode print
```
This will:
- Create or update the environment.
- Install MolSysMT in editable mode.
- Print clear instructions on how to activate the environment manually.

### 2. Setup and persist activation
```bash
source devtools/start_dev_env.sh --mode persist
```
This will:
- Create or update the environment.
- Install MolSysMT in editable mode.
- Activate the environment **in your current shell** and keep it active.  
⚠️ You must use `source` for persistence to work.

---

## 🐍 Choosing Python Version

By default, the environment uses the Python version specified in `development_env.yaml`.  
You can override this with the `--python` option:

```bash
bash devtools/start_dev_env.sh --mode print --python 3.12
```

---

## 📂 Flexible Execution Paths

You can run the script from different locations:
- Parent directory of the repository
- Repository root
- Inside `molsysmt/`
- Inside `devtools/`

The script automatically detects the correct path to:
```
molsysmt/devtools/conda-envs/development_env.yaml
```

---

## ⚙️ Options

```
--mode {print|persist}
    print   : Do not activate, only print activation instructions (default).
    persist : Activate and keep the environment active (requires 'source').

--python <version>
    Override Python version (e.g. 3.11, 3.12).

--env-name <name>
    Set environment name (default: molsysmt).

--env-yaml <path>
    Provide a custom path to a YAML file.

--no-kernel
    Skip Jupyter kernel registration.

-h, --help
    Show usage help and exit.
```

Environment variables:
- `REGISTER_KERNEL=0|1` → disable/enable Jupyter kernel registration (default: 1).  
- `USER_ENV_YAML=<path>` → provide YAML path via environment variable.

---

## 📊 Diagnostics

At the end of the run, the script prints:
- Python version inside the environment.
- Installed versions of `numpy` and `pandas`.
- Available OpenMM platforms (if OpenMM is installed).

---

## ✅ Summary

- Use `--mode print` for setup only (manual activation).  
- Use `source ... --mode persist` for setup + activation.  
- Override Python version with `--python <version>`.  
- Script auto-detects YAML path regardless of where it is called from.  

This script ensures a **consistent, reproducible, and editable development environment** for MolSysMT.
