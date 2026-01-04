# Resources metadata

This directory contains lightweight metadata files (YAML) that link each tool
repository (MolSysMT, MolSysViewer, MolSys-AI, etc.) to centralized MolSysSuite
repositories (talks, papers, tutorials).

Central repositories (default):
- Talks: `uibcdf/molsyssuite-talks`
- Papers: `uibcdf/molsyssuite-papers`
- Tutorials: `uibcdf/molsyssuite-tutorials`

Files:
- `talks.yml`
- `papers.yml`
- `tutorials.yml`

Validation:
- Run: `python scripts/validate_resources.py --strict`
- Requires: `pyyaml`
