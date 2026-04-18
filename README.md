<div align="center">

# MolSysMT

**One API. 60+ molecular formats and libraries. From PDB to simulation in a single workflow.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/137937243.svg)](https://zenodo.org/badge/latestdoi/137937243)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml/badge.svg)](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/uibcdf/molsysmt/graph/badge.svg?token=9ZMA4YZLOR)](https://codecov.io/github/uibcdf/molsysmt)
[![Documentation](https://github.com/uibcdf/molsysmt/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://www.uibcdf.org/MolSysMT/)
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/molsysmt)

**[Why MolSysMT?](#why-molsysmt)** |
**[Installation](#installation)** |
**[Quickstart](#quickstart)** |
**[Supported forms](#supported-forms)** |
**[Documentation](#documentation)** |
**[Citation](#citation)**

</div>

---

MolSysMT is a Python library for working with molecular systems across formats and simulation
engines through a **uniform API**. Load a PDB file, query its topology, repair missing atoms,
solvate it, and hand it off to OpenMM — all without leaving Python and without writing
format-specific boilerplate.

## Why MolSysMT?

Most molecular simulation libraries are excellent at *one* thing:

- **MDTraj** is fast for trajectory analysis, but its topology is read-only.
- **MDAnalysis** has a rich selection language, but interoperating with OpenMM requires glue code.
- **OpenMM** is the gold standard for GPU-accelerated simulation, but it does not help you prepare or repair a structure.

MolSysMT sits *between* these tools. Its role is to make the handoffs transparent:

```python
import molsysmt as msm

# PDB file → OpenMM Simulation in ~5 lines, with structure preparation
mol = msm.convert('1l2y.pdb', to='molsysmt.MolSys')
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
mol = msm.build.solvate(mol, box_shape='cubic', clearance='12 angstroms',
                        water_model='TIP3P', ionic_strength='0.15 molar')
sim = msm.convert(mol, to='openmm.Simulation', forcefield='amber14-all.xml')
```

Key design decisions:
- **Single selection language** across all forms — the same `selection='molecule_type=="protein"'`
  string works on a PDB file, an MDTraj Trajectory, an MDAnalysis Universe, or a native MolSys.
- **`get` / `set` / `convert`** as the three fundamental operations — no form-specific accessors
  to memorize.
- **Numba JIT kernels** for structure analysis (RMSD, distances, dihedral angles, radius of
  gyration, PCA, …) with optional CUDA GPU dispatch.
- **Native structure preparation** (missing heavy atoms, terminal cappings, H placement,
  solvation with ions) that does not require an OpenMM or PDBFixer installation.
- **No heavy mandatory dependencies** — MDTraj, MDAnalysis, OpenMM, and RDKit are optional;
  MolSysMT loads only what your workflow actually needs.


## Installation

### Recommended (conda / mamba)

```bash
conda install -c uibcdf -c conda-forge molsysmt
```

Requires Python 3.11–3.13. Optional dependencies (MDTraj, MDAnalysis, OpenMM, ParmEd,
nglview, RDKit, …) are loaded on demand when available.

### From source

```bash
git clone https://github.com/uibcdf/molsysmt.git
cd molsysmt
pip install -e ".[dev]"
```


## Quickstart

### Load and inspect

```python
import molsysmt as msm

mol = msm.convert('1l2y.pdb', to='molsysmt.MolSys')

n_atoms, n_residues, n_chains = msm.get(mol, n_atoms=True, n_groups=True, n_chains=True)
# (304, 20, 1)

seq = msm.get(mol, element='molecule', selection='molecule_type=="protein"',
              attribute='sequence')
# ['NLYIQWLKDGGPSSGRPPPS']
```

### Cross-library interoperability

```python
# MolSys → MDTraj → MDAnalysis → back to MolSys, topology preserved throughout
traj   = msm.convert(mol, to='mdtraj.Trajectory')
uni    = msm.convert(traj, to='mdanalysis.Universe')
mol2   = msm.convert(uni, to='molsysmt.MolSys')

msm.compare(mol, mol2, attributes=['n_atoms', 'sequence', 'bonds'])
# {'n_atoms': True, 'sequence': True, 'bonds': True}
```

### Structure preparation

```python
mol = msm.convert('raw_structure.pdb', to='molsysmt.MolSys')

# Diagnose
missing_heavy = msm.build.get_missing_heavy_atoms(mol)
missing_caps  = msm.build.get_missing_terminal_cappings(mol)

# Repair (no external dependencies required)
mol = msm.build.add_missing_heavy_atoms(mol, engine='MolSysMT')
mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')

# Solvate
mol = msm.build.solvate(mol, box_shape='truncated_octahedral',
                        clearance='12 angstroms', water_model='TIP3P',
                        ionic_strength='0.15 molar', engine='MolSysMT')
```

### Structure analysis

```python
# RMSD, radius of gyration, dihedral angles — Numba JIT, optionally GPU
rmsd   = msm.structure.get_rmsd(mol, selection='backbone')
rg     = msm.structure.get_radius_of_gyration(mol)
phi, psi = msm.structure.get_dihedral_angles(mol, dihedral='phi'), \
           msm.structure.get_dihedral_angles(mol, dihedral='psi')

# Secondary structure via DSSP
ss = msm.structure.get_secondary_structure(mol)
```

### Visualization

```python
view = msm.view(mol, standard=True)
view  # inline in Jupyter
```


## Supported forms

MolSysMT can read, write, and interconvert 60+ molecular forms organized in three tiers:

| Tier | Forms |
|------|-------|
| **Tier 1** (stable, full test coverage) | `molsysmt.MolSys`, `file:pdb`, `file:h5msm`, `file:xtc`, `file:bcif/bcif.gz`, `file:molsys_yaml`, `openmm.Topology`, `mdtraj.Trajectory`, `mdtraj.Topology`, `string:pdb_id`, `string:alphafold_id` |
| **Tier 2** (best-effort) | MDAnalysis Universe, OpenMM Modeller/Simulation, RDKit Mol, Biopython PDBStructure, ParmEd Structure, NGLView, MolSysViewer |
| **Tier 3** (experimental) | NetworkX, pytraj, XYZ, and others |

Any Tier 1 form can be converted to any other Tier 1 form with a single `msm.convert()` call.


## Documentation

Full documentation, tutorials, and API reference: **https://www.uibcdf.org/MolSysMT/**

The `devguide/` directory in this repository contains the developer guide,
architecture documentation, and contribution guidelines.


## Contributing

Contributions are welcome. Please open an issue before submitting a pull request for
non-trivial changes.

To run the test suite locally:

```bash
# Fast smoke tier (seconds)
make -C devtools/tests smoke

# Full suite, distributed across cores
make -C devtools/tests test
```

See `devguide/testing_strategy.md` for the full testing policy.


## License

MolSysMT is distributed under the MIT license. See [LICENSE](LICENSE) for details.


## Team

### Leads

- Liliana M. Moreno Vargas
- Diego Prada Gracia

### Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the full list.


## Citation

If you use MolSysMT in your research, please cite the software release:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2530946.svg)](https://doi.org/10.5281/zenodo.2530946)

A methods paper describing MolSysMT is in preparation. Please check the documentation
for the most up-to-date citation instructions.


## Acknowledgments

Thanks to the developers and maintainers of the libraries MolSysMT builds on:
MDTraj, MDAnalysis, OpenMM, AmberTools, ParmEd, nglview, RDKit, Biopython, and others.

- Daniel Ibarrola Sánchez for his contributions to the early development of MolSysMT.
