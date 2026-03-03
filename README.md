MolSysMT
==============================

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/137937243.svg)](https://zenodo.org/badge/latestdoi/137937243)
[![](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://github.com/uibcdf/molsysmt/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://github.com/uibcdf/molsysmt/actions/workflows/sphinx_docs_to_gh_pages.yaml)
[![CI](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml/badge.svg)](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/uibcdf/molsysmt/graph/badge.svg?token=9ZMA4YZLOR)](https://codecov.io/github/uibcdf/molsysmt)
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/molsysmt)

**[Overview](#overview)** |
**[Installation](#installation)** |
**[Quickstart](#quickstart)** |
**[Documentation](#documentation)** |
**[Contributing](#contributing)** |
**[Citation](#citation)**

## Overview

MolSysMT is a toolkit to handle molecular systems through a unified interface. It helps convert, query, modify, and visualize systems while relying on multiple molecular dynamics libraries.

Key capabilities:
- Conversion across formats and libraries (MolSysMT, MDTraj, MDAnalysis, OpenMM, ParmEd, nglview, PDB, H5MSM, etc.).
- Consistent selection language to query atoms and groups.
- Common structural operations (selection, extraction, concatenation, copy, centering, alignment, etc.).
- Notebook-friendly visualization via MolSysViewer (with optional NGLView interoperability).
- Integrations with OpenMM and AmberTools for system preparation and simulation tasks.
- Native topologies store all element IDs (`atom_id`, `group_id`, `component_id`, `molecule_id`, `chain_id`, `entity_id`) as strings; converters normalize incoming numeric IDs automatically.

## Installation

### Recommended (conda/mamba)
```bash
conda install -c uibcdf -c conda-forge molsysmt
```
Requires Python 3.10–3.13. Some dependencies are optional (for example, `openmm`, `mdtraj`, `mdanalysis`, `parmed`, `pytraj`, `nglview`) and are used when available.

### From source (development)
```bash
git clone https://github.com/uibcdf/molsysmt.git
cd molsysmt
pip install -e .
```

## Quickstart

```python
import molsysmt as msm

# Load a bundled test system
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])

# Basic info
n_atoms, n_groups = msm.get(molsys, n_atoms=True, n_groups=True)
print(f"N atoms: {n_atoms}, N residues: {n_groups}")

# Select and extract CA atoms
ca = msm.extract(molsys, selection='atom_name=="CA"')

# Visualize (returns the default MolSysViewer backend)
view = msm.view(ca, standard=False)
view
```

## Documentation

Full docs and examples: https://www.uibcdf.org/MolSysMT/

## Contributing

🧩 Want to contribute? Check out the [contributing guide](CONTRIBUTING.md).

To run tests locally:
```bash
pytest -n auto --cov=molsysmt --cov-report=term-missing
```

Fast tier for day-to-day development:
```bash
devtools/tests/run_tiers.sh smoke
```

## License

MolSysMT is distributed under the MIT license. See [LICENSE](LICENSE) for details.

## smonitor

MolSysMT defines its diagnostics catalog in `molsysmt/_private/smonitor/catalog.py`
and metadata in `molsysmt/_private/smonitor/meta.py`. The package-level
configuration lives in `molsysmt/_smonitor.py`.

## Credits

Thanks to the developers and maintainers of the libraries MolSysMT builds on (MDTraj, MDAnalysis, OpenMM, AmberTools, ParmEd, nglview, etc.).

## Team

### Leads

Diego Prada Gracia  
Liliana M. Moreno Vargas

### Contributors

...

## Citation

### Latest version DOI
Please cite the latest release using:  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2530946.svg)](https://doi.org/10.5281/zenodo.2530946)

### All versions
You can cite all releases with the cumulative DOI (always points to the latest):  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2530945.svg)](https://doi.org/10.5281/zenodo.2530945)

## Acknowledgments

Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.
