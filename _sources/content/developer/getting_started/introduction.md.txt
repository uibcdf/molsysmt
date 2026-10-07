# Developer Introduction

Welcome to the MolSysMT developer documentation. This guide is designed to help you understand the architecture of MolSysMT, set up your development environment effortlessly, and contribute code, form adapters, algorithms, or documentation with minimal friction.

---

## What is MolSysMT?

MolSysMT is a **form-agnostic Python library** designed to unify the manipulation, conversion, analysis, and visualization of molecular systems. Instead of forcing users to convert data between disparate library-specific containers (such as MDTraj, OpenMM, MDAnalysis, ParmEd, PyTraj, Biopython, RDKit, or file formats like PDB, H5MSM, GRO, CIF, XTC), MolSysMT operates seamlessly across dozens of in-memory classes, disk files, and string formats.

---

## Architectural Principles

When developing for MolSysMT, keep these core architectural pillars in mind:

1. **Form Agnosticism**: Functions accept any supported molecular system format at the public boundary and return predictable, standardized results.
2. **Validated Boundaries, Trusted Internals**: Public functions validate and normalize user inputs once at the API boundary using `@digest`. Internal helpers operate with `skip_digestion=True` to eliminate overhead.
3. **Physical Unit Safety**: Numerical quantities are managed safely with `pyunitwizard` using canonical units (nanometers for coordinates/box, picoseconds for time, elementary charge for charges, Kelvin for temperature).
4. **Lazy Dependency Management**: External libraries (such as MDTraj, OpenMM, MDAnalysis, etc.) are soft dependencies loaded on demand via `@dep_digest`, ensuring near-instant startup time and portability.
5. **Structured Diagnostics**: Warnings and telemetry are emitted through centralized catalogs managed by `smonitor`.

---

## Repository Layout

A quick tour of the repository structure:

```text
molsysmt/
├── molsysmt/          # Main package source code
│   ├── basic/         # Fundamental operations (convert, get, set, select, etc.)
│   ├── form/          # Form adapters across class, file, and string formats
│   ├── structure/     # Geometric and structural calculation tools
│   ├── topology/      # Topological querying and manipulation tools
│   ├── build/         # System building and editing helpers (MolSysBuilder)
│   ├── element/       # Structural element classifications (atom, group, chain, etc.)
│   ├── pbc/           # Periodic boundary conditions and box utilities
│   ├── physchem/      # Physical-chemical properties
│   ├── hbonds/        # Hydrogen bond analysis
│   ├── molecular_mechanics/ # Energy and force computations (OpenMM backend)
│   └── _private/      # Internal helpers (no digestion decorator)
├── tests/             # Pytest test suite mirroring the package structure
├── docs/              # Sphinx and MyST documentation source
├── devguide/          # Normative internal development records, bugs, and proposals
└── devtools/          # Development environment scripts and release tools
```

---

## Next Steps

To start developing:

- Set up your workspace following the {doc}`fork` and {doc}`start_dev_env_usage` guides.
- Explore the {doc}`../core_architecture/dependencies`, {doc}`../core_architecture/argdigest`, and {doc}`../core_architecture/pyunitwizard` architectural overviews.
- Learn our testing workflows in {doc}`../testing/unit_tests`.
