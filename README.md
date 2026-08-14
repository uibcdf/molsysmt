<div align="center">

# MolSysMT

### Molecular Systems Multi-Toolkit

**Build, prepare, query, transform, analyse and visualise molecular systems
through one uniform API.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1298752.svg)](https://doi.org/10.5281/zenodo.1298752)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml/badge.svg)](https://github.com/uibcdf/molsysmt/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/uibcdf/molsysmt/graph/badge.svg?token=9ZMA4YZLOR)](https://codecov.io/github/uibcdf/molsysmt)
[![Documentation](https://github.com/uibcdf/molsysmt/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://www.uibcdf.org/MolSysMT/)
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/molsysmt)

**[Why MolSysMT?](#why-molsysmt)** |
**[Installation](#installation)** |
**[Quickstart](#quickstart)** |
**[What is inside](#what-is-inside)** |
**[Supported forms](#supported-forms)** |
**[Documentation](#documentation)** |
**[Citation](#citation)**

</div>

---

MolSysMT is a toolkit for working with molecular systems. One uniform API lets you
build a system, repair and prepare it, ask it questions, modify it, analyse its
structures and look at it — without changing library every time the task changes.

It has its own molecular model, its own storage format, its own preparation
pipeline and its own compiled compute kernels. It also speaks 89 other forms —
files, libraries and in-memory objects — so a system can arrive or leave in
whatever shape the rest of your work needs.


## Why MolSysMT?

Taking a molecular system from start to finish — obtaining it, inspecting it,
repairing what is missing, preparing it for simulation, analysing the result,
visualising it, storing it — normally means four or five libraries with
incompatible object models. The glue code between them is where the errors live,
and it gets rewritten in every group, every time.

MolSysMT covers that whole path with one set of operations and one selection
language. It does not ask you to abandon the libraries you already use: it
interoperates with them, and hands work over to them when that is what you want.

```python
import molsysmt as msm

# A raw structure, prepared and handed to OpenMM — without leaving Python
mol = msm.convert('1l2y.pdb', to_form='molsysmt.MolSys')
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
mol = msm.build.solvate(mol, box_shape='cubic', clearance='12 angstroms',
                        water_model='TIP3P', ionic_strength='0.15 molar')
sim = msm.convert(mol, to_form='openmm.Simulation', forcefield='amber14-all.xml')
```

Every step there but the last is MolSysMT's own: the preparation needs no OpenMM
or PDBFixer installation, and the analysis kernels are native. The final line is a
handoff because you asked for one.


## Installation

### Recommended (conda / mamba)

```bash
conda install -c uibcdf -c conda-forge molsysmt
```

Requires Python 3.11, 3.12 or 3.13. Compute kernels ship precompiled, so no
compiler or Rust toolchain is needed to install.

Several integrations are optional — `openmm`, `mdtraj`, `MDAnalysis`, `parmed`,
`pytraj`, `rdkit`, `nglview`, `pdbfixer`, `biopython` — and are used when present.
MolSysMT loads only what your workflow actually touches.

### From source

```bash
git clone https://github.com/uibcdf/molsysmt.git
cd molsysmt
pip install -e ".[dev]"
```

Building from source requires a Rust toolchain.


## Quickstart

### Load and inspect

```python
import molsysmt as msm

mol = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'])

n_atoms, n_groups, n_chains = msm.get(mol, n_atoms=True, n_groups=True, n_chains=True)
# [304, 20, 1]

seq = msm.convert(mol, to_form='string:amino_acids_1')
# 'NLYIQWLKDGGPSSGRPPPS'

ca = msm.select(mol, selection='atom_name=="CA"')
# 20 atom indices
```

### Structure preparation

```python
mol = msm.convert('raw_structure.pdb', to_form='molsysmt.MolSys')

# Diagnose
missing_heavy = msm.build.get_missing_heavy_atoms(mol)
missing_caps  = msm.build.get_missing_terminal_cappings(mol)

# Repair — no external dependencies required
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
rmsd = msm.structure.get_rmsd(mol, selection='backbone')
rg   = msm.structure.get_radius_of_gyration(mol)

quartets = msm.topology.get_dihedral_quartets(mol, phi=True)
phi      = msm.structure.get_dihedral_angles(mol, dihedral_quartets=quartets)

ss = msm.structure.get_secondary_structure(mol)
```

Results carry physical units. The kernels behind them are compiled and shipped
with the package: there is no just-in-time compilation and no warm-up cost on the
first call.

### Interoperability

```python
traj = msm.convert(mol,  to_form='mdtraj.Trajectory')
top  = msm.convert(mol,  to_form='openmm.Topology')
pmd  = msm.convert(mol,  to_form='parmed.Structure')
rd   = msm.convert(mol,  to_form='rdkit.Mol')

back = msm.convert(traj, to_form='molsysmt.MolSys')

msm.compare(mol, back, n_atoms=True, n_groups=True, n_bonds=True,
            output_type='dictionary')
# {'n_atoms': True, 'n_groups': True, 'n_bonds': True}
```

### Visualisation

```python
view = msm.view(mol)
view  # inline in Jupyter
```


## What is inside

- **Three operations, not an API per format.** `get`, `set` and `convert` behave
  the same way on every supported form. There are no form-specific accessors to
  memorise.
- **One selection language.** The same `selection='molecule_type=="protein"'`
  works on a PDB file, an MDTraj Trajectory, an OpenMM Topology or a native
  `MolSys`.
- **A native molecular model.** `MolSys`, `Topology`, `Structures` and
  `MolSysBuilder` hold topology, structures, chemical state and molecular
  mechanics, preserving element identifiers rather than renumbering them.
- **Native structure preparation.** Missing heavy atoms, terminal cappings,
  hydrogen placement, solvation and ions — without requiring OpenMM or PDBFixer.
- **Native compute in Rust.** Distances, contacts, neighbour lists, RMSD and
  superposition, radius of gyration, RMSF, principal axes, PCA, SASA, dihedral
  angles and periodic-boundary handling. Precompiled, with no JIT and no warm-up;
  parallelism is configurable per session or per call.
- **A native storage format.** H5MSM keeps topology, structures and metadata
  together in one HDF5-based file.
- **Visualisation** in notebooks through MolSysViewer, with optional NGLView
  interoperability.
- **No heavy mandatory dependencies.** MDTraj, MDAnalysis, OpenMM and RDKit are
  all optional.


## Supported forms

MolSysMT works with **89 forms** across files, libraries and in-memory objects,
each classified in an explicit support tier:

| Tier | Count | What it means |
|------|------:|---------------|
| **Tier 1** — stable | 75 | Fully supported, covered by the form-adapter delivery gate |
| **Tier 2** — best effort | 3 | Usable, narrower guarantees |
| **Tier 3** — experimental | 11 | Present, not yet contract-guaranteed |

They include PDB, mmCIF and BinaryCIF; H5MSM, XTC, DCD, GRO, MDCRD and XYZ; PSF,
PRMTOP and TOP topologies; MOL2 and SMILES; PDB, UniProt and AlphaFold
identifiers and amino-acid sequence strings; and the object models of MDTraj,
MDAnalysis, OpenMM, ParmEd, PyTraj, RDKit, OpenFF, PDBFixer, NetworkX, NGLView
and MolSysViewer.

Conversion routes carry an explicit fidelity record. MolSysMT reports what a
given conversion preserves and what it cannot, rather than presenting every route
as lossless, and not every pair of forms is connected. Use
`msm.convert(..., return_report=True)` to see what a specific conversion did.


## Documentation

Full documentation, tutorials and API reference:
**https://www.uibcdf.org/MolSysMT/**

**The Four Paths of the MolSysMT Master** — a 156-notebook course: a 20-module
common core followed by four applied paths.

The `devguide/` directory in this repository contains the developer guide,
architecture documentation and contribution guidelines.


## Contributing

Contributions are welcome. Please open an issue before submitting a pull request
for non-trivial changes.

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

If you use MolSysMT in your research, cite the software project through its stable
concept DOI:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1298752.svg)](https://doi.org/10.5281/zenodo.1298752)

For reproducible work, select and cite the DOI of the exact MolSysMT version from
the Zenodo version history.

A methods paper describing MolSysMT is in preparation. Please check the
documentation for the most up-to-date citation instructions.


## Acknowledgments

Thanks to the developers and maintainers of the libraries MolSysMT interoperates
with: MDTraj, MDAnalysis, OpenMM, AmberTools, ParmEd, nglview, RDKit, Biopython
and others.

- Daniel Ibarrola Sánchez for his contributions to the early development of
  MolSysMT.
