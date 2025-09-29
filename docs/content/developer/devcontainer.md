# Contributing: Development Environment with Devcontainers

This project provides a **pre-configured development environment** using [VS Code Devcontainers](https://code.visualstudio.com/docs/devcontainers/containers) (or [GitHub Codespaces](https://github.com/features/codespaces)) together with **micromamba** and a shared `development_env.yaml`.  

This setup ensures reproducibility, simplifies onboarding, and allows Codex (or any developer) to run tests immediately after opening the repository.

---

## 📦 How it works

1. **Environment specification**  
   All dependencies are listed in:  
   ```
   molsysmt/devtools/conda-envs/development_env.yaml
   ```
   This file is applied automatically when the container starts.

2. **Editable installation of MolSysMT**  
   The repository installs MolSysMT in editable mode:
   ```bash
   pip install --no-deps --editable .
   ```
   This allows any modification of the source code in `molsysmt/` to be tested instantly, without reinstalling.

3. **Kernel registration**  
   A Jupyter kernel named *Python (molsysmt)* is registered, so notebooks can be run inside the same environment.

---

## 🚀 Usage

- **VS Code**: open the repository and choose *Reopen in Container*.  
- **GitHub Codespaces**: open the repo in Codespaces; the container will be built automatically.  
- After build, the container will:
  - Apply `development_env.yaml` with micromamba.  
  - Install MolSysMT in editable mode.  
  - Register the Jupyter kernel.  

You can now run:
```bash
pytest -q
```
or open a notebook and select the *Python (molsysmt)* kernel.

---

## ✅ Advantages over a simple startup script

- **Reproducibility**: every developer and CI job uses the same base image and dependencies.  
- **Automation**: no need to install or activate conda manually.  
- **Codex/CI integration**: Codex can directly edit the source and run tests without managing environments.  
- **Editable mode**: changes to `molsysmt/` are reflected instantly.  
- **Collaboration**: all contributors share the same environment, avoiding "works on my machine" issues.

---

## 🔒 Optional: conda-lock

[conda-lock](https://github.com/conda/conda-lock) can be used to generate fully pinned lockfiles (e.g., `conda-linux-64.lock.yml`) from `development_env.yaml`.  

**Benefits:**
- Strong reproducibility (bit-for-bit identical environments).  
- Faster setup (no solver step, only installation).  

**Potential drawbacks:**
- Less exposure to new dependency versions: CI may miss upstream breaking changes.  
- GPU constraints: if a lock pins a CUDA runtime newer than the driver on some host, CUDA may fail.

**Possible strategy:**  
- Run CI with both **floating environments** (from `development_env.yaml`, catching new releases) and **locked environments** (from `conda-lock`, for stability).  
- Optionally, schedule a weekly CI job with `conda update --all` to detect future incompatibilities early.

---

## 🧭 Summary

- Use the provided **devcontainer** for transparent, reproducible development.  
- MolSysMT is always installed in **editable mode**.  
- Consider **conda-lock + floating strategy** if you need both stability and early detection of dependency issues.  

This approach balances **reliability, agility, and collaboration** for developers and for Codex integration.
