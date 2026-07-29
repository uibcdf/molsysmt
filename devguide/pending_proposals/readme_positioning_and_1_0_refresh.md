# README positioning and 1.0 refresh

**Status:** accepted and largely applied on 2026-07-29. Three items remain open and
need a maintainer decision; they are listed under *Still open* below.
**Raised:** 2026-07-29, by the maintainer: the current README reads as if MolSysMT
were a converter.
**Scope as applied:** `README.md`, `pyproject.toml`, `devtools/conda-build/meta.yaml`,
`docs/index.ipynb`, `docs/content/about/what.md`, `docs/content/about/index.md`.

## Applied

- `README.md` rewritten on the framing below, with every code example executed
  against the installed package first.
- `pyproject.toml` description no longer leads with "converting".
- `devtools/conda-build/meta.yaml` had an **empty `summary`** and an informal
  internal description ("some useful classes, functions, pipes and wrappers daily
  used in the uibcdf lab"). That text is the public storefront on anaconda.org.
  Replaced.
- `docs/index.ipynb` carried the same converter tagline plus a stale release badge
  (`v0.11.2`), "50-module journey" and "60+ formats". Corrected.
- `docs/content/about/what.md` contained the most damaging statement found in the
  audit and is rewritten; see *The self-disavowal* below.
- `docs/content/about/index.md` reframed.

## Still open

Three items could not be closed in this pass, because two turn on facts only the
maintainers hold and one on release timing: the citation record
(`CITATION.cff` / `.zenodo.json`), the unreferenced duplicate landing page
`docs/index_v2.ipynb`, and the timing of the Conda installation instructions.

They are specified, with evidence and acceptance criteria, in
[`presentation_and_citation_surface.md`](presentation_and_citation_surface.md).
They are not restated here.

## The problem

The README was rewritten on 2026-04-17 (`4df91142a`). The rewrite improved the
structure, navigation and examples, but it changed the subject of the opening.

Before (`2897db9e4`):

> MolSysMT is a toolkit to handle molecular systems through a unified interface.
> It helps convert, query, modify, and visualize systems while relying on multiple
> molecular dynamics libraries.

After (current):

> One API. 60+ molecular formats and libraries. From PDB to simulation in a single
> workflow.
>
> […] MolSysMT sits *between* these tools. Its role is to make the handoffs
> transparent.

In the earlier text the subject is **the molecular system**, and MolSysMT is what
handles it: convert, query, modify and visualize are four co-equal verbs. In the
current text the subject is **the formats and the other libraries**, and MolSysMT
is defined as what goes between them. "Its role is to make the handoffs
transparent" reduces the product to transport, which makes `convert` the identity
rather than the door.

That framing is also no longer accurate. MolSysMT has its own data model
(`MolSys`, `Topology`, `Structures`, `MolSysBuilder`), its own file format
(H5MSM), its own selection language, native structure preparation that explicitly
does not require OpenMM or PDBFixer, 97 compiled Rust compute kernels rather than
delegation to MDTraj for RMSD, distances, SASA or PCA, and its own viewer. It
interoperates with 89 forms because it chooses to speak to everyone, not because
it depends on anyone.

The current "Why MolSysMT?" section compounds this: it opens by listing what
MDTraj, MDAnalysis and OpenMM each do well, then positions MolSysMT as the thing
that smooths the seams between them. That argument sells the other libraries and
leaves MolSysMT as quartermaster.

## Is the earlier approach recoverable?

Yes, and it is the right axis. But the earlier sentence should not be restored
verbatim. Two things in it are worth dropping:

1. **"toolkit to handle molecular systems"** — "handle" is a category label, not a
   claim. It says which shelf the library sits on, not why a reader should pick it
   up.
2. **"while relying on multiple molecular dynamics libraries"** — this is the seed
   of the current framing. It subordinates MolSysMT to its dependencies. It was
   more defensible in 2025; today it understates the product.

What should be kept is the *structure* of that sentence: the molecular system as
subject, several co-equal verbs, one unified interface.

There is also unused material. The name itself — **Molecular Systems
Multi-Toolkit** — already says "multi-toolkit", not "converter". The project's
internal identity phrase, "Gestor de Formas Moleculares" / Molecular Form Manager,
appears in the architecture audits under `archive/release_1_0/` but has never
reached the front page. Both point the same way.

## The self-disavowal in `docs/content/about/what.md`

The most damaging text found in the audit was not in the README. The "What is
MolSysMT?" page said:

> While most of the functions and methods in MolSysMT were purposefully developed
> and in-house programmed, **the inclusion of native objects and functions was not
> its primary goal, nor is it the strongest reason to use it.** […] Instead, it was
> conceived as an easy-to-use tool for **coordinating and integrating** the use of
> libraries such as MDAnalysis, MDTraj, PDBFixer, OpenMM, ParmED, HTMD, RDKit, or
> NGLView.

This is the project disowning its own native capability, on the page a reader
opens to find out what MolSysMT is. It was more defensible when written. It is now
contradicted by native structure preparation that needs no external engine, 97
precompiled Rust kernels, a native molecular model and a native storage format.

The rewrite keeps the genuine and generous part — MolSysMT does not try to
replicate what specialised tools already do well, and credit belongs to their
authors — while stating what MolSysMT does itself.

## Verified while rewriting: the README's examples did not run

The old README's code was not executable against the current package. Every item
below was reproduced before being corrected:

| Claim | Result |
| --- | --- |
| `msm.convert(mol, to='...')` — used **7 times** | `TypeError`. The parameter is `to_form=`. |
| `msm.get(..., element='molecule', attribute='sequence')` | `ArgumentError`. Sequence is obtained with `msm.convert(mol, to_form='string:amino_acids_1')`. |
| `msm.structure.get_dihedral_angles(mol, dihedral='phi')` | No such argument. Quartets come from `msm.topology.get_dihedral_quartets(mol, phi=True)`. |
| MolSys → MDTraj → **MDAnalysis** → MolSys round trip | `NotImplementedConversionError`. There is no route from `mdtraj.Trajectory`, nor from `molsysmt.MolSys`, to `MDAnalysis.Universe`. |
| `msm.compare(...)` returning a dict | Returns a boolean unless `output_type='dictionary'` is passed. |

The interoperability example is the most serious: it was the section demonstrating
the library's central claim, and it did not work.

## The tier table understated the product

The old README presented roughly eleven Tier 1 forms and placed MDAnalysis,
OpenMM Modeller/Simulation, RDKit, ParmEd, NGLView and MolSysViewer in Tier 2.
The live registry (`molsysmt._private.form_tier.FORM_TIERS`) reports **75 Tier 1,
3 Tier 2 and 11 Tier 3** of 89. Almost everything listed as best-effort is in fact
stable. The README was selling a fraction of the supported surface.

It also claimed that *"any Tier 1 form can be converted to any other Tier 1 form
with a single `msm.convert()` call"*. That is false — the MDAnalysis route above is
a Tier 1 pair with no implementation — and it is the kind of promise the fidelity
audit exists to prevent.

## Factual errors in the current README, independent of framing

These must be corrected before 1.0 regardless of which wording is chosen:

| Current text | Reality |
| --- | --- |
| "Numba JIT kernels … with optional CUDA GPU dispatch" | Both removed in Segment D. The runtime is a precompiled Rust extension with no JIT and no warm-up. |
| "60+ molecular formats and libraries" | The form-adapter gate audits and passes **89** adapters. |
| Python badge and install text | Correct at 3.11–3.13; verify the badge stays in sync. |
| `conda install -c uibcdf -c conda-forge molsysmt` | Not currently satisfiable — see the Conda delivery track. **Open decision below.** |

## Open decisions for the maintainer

1. **Conda instructions.** The README should describe the shipped 1.0 state, but a
   reader today would follow instructions that fail. Options: (a) keep as written
   and land the README only once the Conda track closes; (b) keep and add a short
   "available from 1.0" note; (c) lead with the source install until the channel
   is live. The draft below assumes (a) and is written for the 1.0 state.
2. **Conversion fidelity.** 39 of 481 Tier-1 conversion edges are proven
   exhaustive; 442 are accepted, recorded debt. The draft includes one modest
   sentence acknowledging this in the forms section. Cut it if it reads as
   over-qualification on a front page — but note that the alternative is a promise
   the audit does not yet back.
3. **Scope of the change.** Whether to align `docs/content/index.md` and the
   `pyproject.toml` description in the same pass.

## Proposed README

The draft keeps the current structure, navigation and the PDB-to-`openmm.Simulation`
example, which are good. It changes the opening, the "Why" argument, and every
stale fact.

````markdown
<div align="center">

# MolSysMT

**Molecular Systems Multi-Toolkit** — build, prepare, query, transform, analyse and
visualise molecular systems through one uniform API.

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
and it is rewritten in every group, every time.

MolSysMT covers that whole path with a single set of operations and a single
selection language. It does not ask you to abandon the libraries you already use:
it interoperates with them, and hands work over to them when that is what you
want.

```python
import molsysmt as msm

# A PDB file, prepared and handed to OpenMM — without leaving Python
mol = msm.convert('1l2y.pdb', to='molsysmt.MolSys')
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
mol = msm.build.solvate(mol, box_shape='cubic', clearance='12 angstroms',
                        water_model='TIP3P', ionic_strength='0.15 molar')
sim = msm.convert(mol, to='openmm.Simulation', forcefield='amber14-all.xml')
```

Every step there is MolSysMT's own: the preparation does not require an OpenMM or
PDBFixer installation, and the analysis kernels are its own. The last line is a
handoff because you asked for one.

## What is inside

- **Three operations, not an API per format.** `get`, `set` and `convert` work the
  same way on every supported form. There are no form-specific accessors to learn.
- **One selection language.** The same
  `selection='molecule_type=="protein"'` works on a PDB file, an MDTraj
  Trajectory, an MDAnalysis Universe or a native `MolSys`.
- **A native molecular model.** `MolSys`, `Topology`, `Structures` and
  `MolSysBuilder` hold topology, structures, chemical state and molecular
  mechanics, with element identifiers preserved rather than renumbered.
- **Native structure preparation.** Missing heavy atoms, terminal cappings,
  hydrogen placement, solvation and ions — without requiring OpenMM or PDBFixer.
- **Native compute in Rust.** Distances, contacts, neighbour lists, RMSD and
  superposition, radius of gyration, RMSF, principal axes, PCA, SASA, dihedral
  angles, PBC handling. Precompiled and shipped with the package: there is no
  just-in-time compilation and no warm-up on first call. Parallelism is
  configurable per session or per call.
- **A native storage format.** H5MSM stores topology, structures and metadata in
  one HDF5-based file.
- **Visualisation** in notebooks through MolSysViewer, with optional NGLView
  interoperability.

## Installation

```bash
conda install -c uibcdf -c conda-forge molsysmt
```

Requires Python 3.11, 3.12 or 3.13. Several integrations are optional — `openmm`,
`mdtraj`, `MDAnalysis`, `parmed`, `pytraj`, `rdkit`, `nglview`, `pdbfixer`,
`biopython` — and are used when present.

From source, for development:

```bash
git clone https://github.com/uibcdf/molsysmt.git
cd molsysmt
pip install -e .
```

Building from source requires a Rust toolchain; installing from the conda channel
does not.

## Quickstart

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])

n_atoms, n_groups = msm.get(molsys, n_atoms=True, n_groups=True)

ca = msm.select(molsys, selection='atom_name=="CA"')
rg = msm.structure.get_radius_of_gyration(molsys, selection='molecule_type=="protein"')

msm.view(molsys)
```

## Supported forms

MolSysMT works with 89 forms across files, libraries and in-memory objects,
including PDB and mmCIF, H5MSM, XTC, DCD and XYZ trajectories, PRMTOP, PSF and
TOP topologies, SMILES and sequence strings, and the object models of MDTraj,
MDAnalysis, OpenMM, ParmEd, PyTraj, RDKit, OpenFF, PDBFixer, NetworkX and
NGLView.

Forms are classified by support tier, and conversion routes carry an explicit
fidelity record: MolSysMT reports what a conversion preserves and what it cannot,
rather than presenting every route as lossless. See the conversion documentation
for the current state.

## Documentation

- **[User guide and API reference](https://www.uibcdf.org/MolSysMT/)**
- **The Four Paths of the MolSysMT Master** — a 156-notebook course: a 20-module
  common core followed by four applied paths.

## Citation

If MolSysMT is useful in your work, please cite it via the
[Zenodo DOI](https://zenodo.org/badge/latestdoi/137937243).

## License

MIT. See the LICENSE file.
````

In the final `README.md` the licence line should link relatively to the `LICENSE`
file at the repository root, using ordinary Markdown link syntax. It is written
without that link here because a relative link inside this proposal would resolve
against `devguide/pending_proposals/` and fail developer-guide validation.

## Acceptance criteria

1. The opening names MolSysMT as a toolkit for molecular systems, with the system
   as grammatical subject and no clause subordinating it to other libraries.
2. No statement in the README describes a removed capability. In particular, no
   mention of Numba, JIT compilation, warm-up or CUDA dispatch.
3. Form and Python-version counts match the values the release gates report.
4. The installation instructions are executable at the moment the README is
   published, under whichever option is chosen in *Open decisions*.
5. Every code example in the README executes against the released package.
