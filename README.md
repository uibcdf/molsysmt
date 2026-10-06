<div align="center">

# MolSysMT

### Molecular Systems Multi-Toolkit

**Build, prepare, query, transform, analyse and visualise molecular systems
through one uniform API.**

[![MolSysSuite: Scientific Component](https://img.shields.io/badge/MolSysSuite-scientific%20component-0b7285?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#scientific-component)
[![MolSysSuite policy](https://github.com/uibcdf/molsysmt/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/molsysmt/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/molsysmt)](https://github.com/uibcdf/molsysmt/blob/main/LICENSE)
[![Coverage](https://codecov.io/gh/uibcdf/molsysmt/branch/main/graph/badge.svg)](https://app.codecov.io/gh/uibcdf/molsysmt)
[![Tests](https://github.com/uibcdf/molsysmt/actions/workflows/ci-smoke.yaml/badge.svg?branch=main)](https://github.com/uibcdf/molsysmt/actions/workflows/ci-smoke.yaml)
[![Documentation](https://github.com/uibcdf/molsysmt/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://www.uibcdf.org/molsysmt/)
[![GitHub release](https://img.shields.io/github/v/release/uibcdf/molsysmt)](https://github.com/uibcdf/molsysmt/releases/latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1298752.svg)](https://doi.org/10.5281/zenodo.1298752)
[![Conda](https://img.shields.io/conda/vn/uibcdf/molsysmt)](https://anaconda.org/uibcdf/molsysmt)

**[Why MolSysMT?](#why-molsysmt)** |
**[Installation](#installation)** |
**[Quickstart](#quickstart)** |
**[What is inside](#what-is-inside)** |
**[Supported forms](#supported-forms)** |
**[Documentation](#documentation)** |
**[Citation](#citation)**

</div>

Coverage reporting measures Python lines and branches with the existing
`.coveragerc` exclusions, using complete Linux/Python 3.13 runs within the weekly
and conditional nightly cadence. It does not instrument Rust execution. The
[reporting procedure and measured report](devguide/coverage_reporting.md) explain
scope and actual test outcomes. The badge shows the last processed Codecov report;
it can describe a completed suite with failures.
Reports may lag later direct or skip-CI commits and do not certify a full matrix.

---

MolSysMT is a core molecular-system library in the MolSysSuite ecosystem.
One uniform API lets you
build a system, repair and prepare it, ask it questions, modify it, analyse its
structures and look at it — without changing library every time the task changes.

It has its own molecular model, its own storage format, its own preparation
pipeline and its own compiled compute kernels. It interoperates with other forms —
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

# Preparing a bundled protein with the experimental native preparation tools
molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])
molsys = msm.build.add_missing_terminal_cappings(molsys, pH=7.4, engine='MolSysMT')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4, engine='MolSysMT')
molsys = msm.build.solvate(molsys, box_shape='cubic', clearance='12 angstroms',
                           water_model='TIP3P', ionic_strength='0.15 molar',
                           engine='MolSysMT')

# Optional handoff: this line requires OpenMM
sim = msm.convert(molsys, to_form='openmm.Simulation', forcefield='AMBER14')
```

The preparation steps explicitly select MolSysMT's native engine and need no
OpenMM or PDBFixer installation. Native preparation is **experimental** and
supports documented chemical templates and profiles, rather than arbitrary
chemistry. The final line hands the prepared system to OpenMM.


## Installation

### Recommended (conda / mamba)

```bash
conda install -c uibcdf -c conda-forge molsysmt
```

Package metadata permits Python 3.11, 3.12, 3.13 or 3.14; the badge lists only
versions admitted for public release. Compute kernels ship precompiled, so no
compiler or Rust toolchain is needed to install.

macOS support is currently limited to Apple Silicon (arm64). Intel-based macOS
(x86_64) is not part of the supported platform matrix. Support may be
reconsidered if there is demonstrated user demand.

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

molsys = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'])

n_atoms, n_groups, n_chains = msm.get(molsys, n_atoms=True, n_groups=True, n_chains=True)
# [304, 20, 1]

seq = msm.convert(molsys, to_form='string:amino_acids_1')
# 'NLYIQWLKDGGPSSGRPPPS'

ca = msm.select(molsys, selection='atom_name=="CA"')
# 20 atom indices
```

### Experimental structure preparation

```python
molsys = msm.convert('raw_structure.pdb', to_form='molsysmt.MolSys',
                     get_missing_bonds=True, bond_inference_engine='MolSysMT')

# Diagnose
missing_heavy = msm.build.get_missing_heavy_atoms(molsys)
missing_caps  = msm.build.get_missing_terminal_cappings(molsys)

# Repair — no external dependencies required
molsys = msm.build.add_missing_heavy_atoms(molsys, engine='MolSysMT')
molsys = msm.build.add_missing_terminal_cappings(molsys, engine='MolSysMT')
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4, engine='MolSysMT')

# Solvate
molsys = msm.build.solvate(molsys, box_shape='truncated octahedral',
                        clearance='12 angstroms', water_model='TIP3P',
                        ionic_strength='0.15 molar', engine='MolSysMT')
```

### Structure analysis

```python
rmsd = msm.structure.get_rmsd(molsys, selection='backbone')
rg   = msm.structure.get_radius_of_gyration(molsys)

quartets = msm.topology.get_dihedral_quartets(molsys, phi=True)
phi      = msm.structure.get_dihedral_angles(molsys, dihedral_quartets=quartets)

# Experimental secondary-structure assignment
ss = msm.structure.get_secondary_structure(molsys)
```

Results carry physical units. The kernels behind them are compiled and shipped
with the package, avoiding a just-in-time compilation step.

### Interoperability

```python
traj = msm.convert(molsys,  to_form='mdtraj.Trajectory')
top  = msm.convert(molsys,  to_form='openmm.Topology')
pmd  = msm.convert(molsys,  to_form='parmed.Structure')
rd   = msm.convert(molsys,  to_form='rdkit.Mol')

back = msm.convert(traj, to_form='molsysmt.MolSys')

msm.compare(molsys, back, n_atoms=True, n_groups=True, n_bonds=True,
            output_type='dictionary')
# {'n_atoms': True, 'n_groups': True, 'n_bonds': True}
```

### Visualisation

```python
view = msm.view(molsys)
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
  `MolSysBuilder` hold topology and structures, preserving element identifiers.
  The experimental `molsysmt.ChemicalStates` and `molsysmt.Interactions` domains
  store chemical assignments and named interaction analyses. Molecular mechanics
  remains a minimal experimental domain.
- **Experimental native structure preparation.** `msm.build` supplies missing
  heavy atoms, terminal cappings, hydrogen placement, solvation and ions for its
  supported templates and profiles. Select `engine='MolSysMT'` explicitly to
  prepare these systems without requiring OpenMM or PDBFixer.
- **Native compute in Rust.** Distances, contacts, neighbour lists, RMSD and
  superposition, radius of gyration, principal axes, PCA, dihedral
  angles and periodic-boundary handling. Precompiled, with no JIT compilation;
  parallelism is configurable per session or per call.
- **Experimental analysis.** `msm.structure.get_rmsf`, `msm.physchem.get_sasa`,
  `msm.structure.get_secondary_structure` and the `msm.interactions` detectors
  offer analysis methods under the experimental API contract.
- **A native storage format.** H5MSM 0.5 stores topology, structures, chemical
  states and named interaction analyses as independently optional domains.
  Nonempty molecular-mechanics data is rejected until a later format supports it.
- **Visualisation** in notebooks through MolSysViewer, with optional NGLView
  interoperability.
- **No heavy mandatory dependencies.** MDTraj, MDAnalysis, OpenMM and RDKit are
  all optional.


## Supported forms

MolSysMT works with files, libraries and in-memory objects, each classified in
an explicit support tier. The [form contract](devguide/forms_and_conversions.md) describes these tiers;
the documentation's supported-forms catalog reports the current registry.

| Tier | What it means |
|------|---------------|
| **Tier 1** — stable | Contractual routes, checked by the form-adapter delivery gate with documented accepted debt |
| **Tier 2** — best effort | Usable, narrower guarantees |
| **Tier 3** — experimental | Present, not yet contract-guaranteed |

They include PDB, mmCIF and BinaryCIF; H5MSM, XTC, DCD, GRO, MDCRD and XYZ; PSF,
PRMTOP and TOP topologies; MOL2, SDF, PDBQT and SMILES; PDB, UniProt and AlphaFold
identifiers and amino-acid sequence strings; and the object models of MDTraj,
MDAnalysis, OpenMM, ParmEd, PyTraj, RDKit, OpenFF, PDBFixer, NetworkX, NGLView
and MolSysViewer.

Conversion routes carry an explicit fidelity record. MolSysMT reports what a
given conversion preserves and what it cannot, rather than presenting every route
as lossless, and not every pair of forms is connected. Use
`msm.convert(..., return_report=True)` to see what a specific conversion did.


## Documentation

Full documentation, tutorials and API reference:
**https://www.uibcdf.org/molsysmt/**

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

See the [GitHub contributors](https://github.com/uibcdf/molsysmt/graphs/contributors).


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
