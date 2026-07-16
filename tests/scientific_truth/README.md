# Scientific Truth Suite

This directory contains tests whose expected results are independent of the
MolSysMT implementation under test. Passing ordinary unit, parity, or round-trip
tests is not sufficient for a claim of scientific validation.

## Evidence classes

- **Analytic:** the expected value follows from a closed-form construction with
  values declared in the test before MolSysMT is called.
- **External:** the expected value comes from an independently implemented tool
  or a versioned reference dataset that does not consume MolSysMT output.
- **Metamorphic:** a mathematical invariant is checked under a controlled
  transformation. This strengthens, but does not replace, an explicit oracle.

Cross-form agreement is parity evidence, not scientific truth, unless one side
is independently established as the oracle.

## Layout

- `pbc/` contains closed-form analytic box and minimum-image tests.
- `structure/` contains analytic ensemble descriptors and rigid-transform tests.
- `external/mdtraj/` compares geometry kernels with MDTraj.
- `external/mdanalysis/` compares geometry kernels with MDAnalysis.
- `curated/` validates bundled peptide, miniprotein, and periodic-trajectory
  artifacts whose hashes and provenance are recorded in `curated/PROVENANCE.md`.

External tests construct each backend directly from the NumPy fixture declared
in this suite. They must not call a MolSysMT converter to construct the oracle.

## Rules

1. State the mathematical convention, units, shape, and evidence class.
2. Use deterministic, minimal systems and avoid network access.
3. Take tolerances from `conftest.py`; do not choose them independently in each
   test.
4. A tolerance increase requires a documented numerical or format-specific
   reason.
5. Never derive an expected value by calling another MolSysMT function that
   shares the implementation path being tested.
6. Optional imports may skip external tests in a minimal user installation, but
   the official scientific-validation CI job must install every oracle required
   by the maintained validation index and must report zero skips for them.
7. Compare signed periodic quantities, such as dihedrals, modulo their period.
   In particular, `-pi` and `+pi` are the same physical angle.
8. When an external implementation disagrees with an exact analytic invariant,
   the analytic oracle takes precedence. Record the external numerical artifact
   instead of weakening the governed tolerance.
9. Distinguish temporal unwrapping from single-frame molecular reconstruction;
   test both contracts independently when periodic coordinates are involved.

The maintained validation index and tolerance rationale are in
`devguide/scientific_validation.md`.
