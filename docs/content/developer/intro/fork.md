# Fork and Workspace Setup

This guide walks you through cloning, configuring, and working on your local fork of MolSysMT.

---

## 1. Fork and Clone

1. Fork the [uibcdf/MolSysMT](https://github.com/uibcdf/MolSysMT) repository on GitHub.
2. Clone your fork locally:

```bash
git clone https://github.com/<your-username>/MolSysMT.git
cd MolSysMT
```

3. Add the upstream repository as a remote:

```bash
git remote add upstream https://github.com/uibcdf/MolSysMT.git
git fetch upstream
```

---

## 2. Setting Up the Development Environment

We recommend creating an isolated environment using conda, mamba, or micromamba with Python 3.11+:

### Using the Automated Bootstrap Script

The easiest way to configure your environment is using our automated bootstrap tool:

```bash
bash devtools/start_dev_env.sh
```

This script detects your package manager, creates or updates the environment from `development_env.yaml`, and installs MolSysMT in editable mode.

### Manual Installation

Alternatively, you can create and activate the environment manually:

```bash
conda env create -f development_env.yaml -n molsysmt_dev
conda activate molsysmt_dev
pip install --no-deps -e .
```

---

## 3. Verifying the Installation

Verify that MolSysMT imports cleanly and your development environment is active:

```bash
python -c "import molsysmt as msm; print('MolSysMT version:', msm.__version__)"
pytest tests/basic/test_get_form.py
```

---

## 4. Development Workflow and Git Conventions

When contributing code:

- **Create a feature branch**:
  ```bash
  git checkout -b feature/my-improvement upstream/main
  ```
- **Verify code style with Ruff**:
  ```bash
  ruff check molsysmt
  ```
- **Commit messages**:
  - Keep messages descriptive and concise.
  - Include `[skip ci]` in intermediate or documentation-only commits to save CI resources unless triggering the full CI pipeline is required.
  - Never add attribution footers such as `Co-Authored-By`.
