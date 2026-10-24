# Tiered Test Runs

This directory contains helper scripts to run tests in progressive tiers during stabilization work.

## Usage

Run from repository root:

```bash
devtools/tests/run_tiers.sh smoke
devtools/tests/run_tiers.sh build_topology
devtools/tests/run_tiers.sh peptide_extended
```

## Tiers

- `smoke`: fast gating subset used before larger runs.
- `build_topology`: focused regression subset for peptide building and topology-related logic.
- `peptide_extended`: extended 40-sequence LEaP parity suite for `build_peptide` (slow).

The smoke tier includes independent numerical contracts for distances, extrema,
neighbors and contacts, plus sequence-codec selection and optional-Biopython
guards and weighted PCA covariance, axis, unit and rejection contracts. Keep its node list aligned with `.github/workflows/ci-smoke.yaml`.
