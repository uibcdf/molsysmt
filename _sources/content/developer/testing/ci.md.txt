# Continuous Integration

MolSysMT relies on GitHub Actions to ensure code quality, test integrity, and documentation freshness on every change.

---

## 1. Workflow Architecture

- **Pull Request Checks**: Fast validation tier running on Ubuntu with Python 3.13, verifying formatting with Ruff, unit tests, and documentation build.
- **Scheduled Weekly Matrix**: Full compatibility matrix testing Python 3.11 through 3.13 across Linux and macOS environments.
- **Scientific Truth Verification**: Runs `tests/scientific_truth/` as an early gate with external engines (MDTraj, MDAnalysis, OpenMM) installed to verify algorithm correctness.
- **Documentation Deployment**: Documentation is automatically built and deployed to GitHub Pages upon merging into `main`.

---

## 2. CI Control Flags

- To skip CI runs on documentation-only commits, include `[skip ci]` in your Git commit message.
