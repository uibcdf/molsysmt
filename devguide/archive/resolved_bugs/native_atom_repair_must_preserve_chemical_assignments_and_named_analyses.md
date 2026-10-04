---
summary: Native atom repair must preserve chemical assignments and named analyses
issue: uibcdf/molsysmt#321
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: reproduced
area: [build]
guard: tests/build/add_missing_heavy_atoms/test_domain_preservation.py
normative:
blocked_by: []
supersedes: []
---

# Native atom repair must preserve chemical assignments and named analyses

**Reported:** 2026-10-04, during observed receptor preparation for #298.
**Status:** Resolved by bounded native domain preservation and reconstruction checks; local acceptance is recorded below.

## What

Native heavy-atom repair returned a reconstructed MolSys without its original
atom-level chemical assignments, selected state identity/provenance or named
interaction analyses. The shared atom appender also serves native H and terminal
completion. The new-group builder for ACE/NME independently had the same loss.

Reproduction before the correction:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_heavy_atoms/test_domain_preservation.py
```

The initial two tests failed: the state's `state_id` became `None`, and an
expansion with two states succeeded rather than requiring explicit selection.

## How

`molsysmt/build/_native_placers.py:append_atoms_to_molsys` constructed a fresh
Topology and MolSys while copying bonds and group tables. That reconstructs an
empty reference chemical state and omits the independent interaction/mechanical
domains. `rebuild_molsys_with_new_groups` used a separate fresh-object route.
Neither atom counts nor group-name parity detects this loss.

Both paths now copy the existing single state, remap its atom attributes, retain
its ID/provenance and structure-state links, and leave added values nullable.
Connectivity completeness is partial because geometric placement does not assign
all new chemical fields or certify a complete chemical graph. Existing atom IDs
are retained; added atom IDs avoid collisions with observed IDs. New groups and
group-contiguous ordering can change indices.

The shared `_assemble_expanded_molsys` retains named analysis definitions,
participant relations and remapped source axes, invalidates all observations and
evaluated coverage, and marks new atom source indices as -1. Definitions survive;
observations must be recalculated against the expanded atom domain. Existing
coordinates, time and box survive. Unsupported structural observables and
force-field atom parameters are reported as dropped rather than silently lost.
Mechanical global settings survive; no new atom parameters are fabricated.

The public heavy-atom tool offers keyword-only `attribute_policy='strict'` to
reject attribute loss transactionally. The existing intersection default reports
loss. PDBFixer rejects strict policy explicitly; these native guarantees do not
extend through arbitrary external reconstruction or unsupported output forms.

## Why

The #298 explicit-chemistry workflow must be composable with geometric repair.
Losing declared formal charges, aromatic flags or analysis provenance could
silently change subsequent chemical recognition and preparation. Retaining old
observations as evaluated after atom expansion would also miss new candidates.
The consumer context is uibcdf/pharmacophoremt#22 and uibcdf/molsysmt#298.

## What is measured and what is assumed

**Reproduced:** two initial regression failures before correction.
**Contract-tested:** repair and ACE/NME insertion preserve known assignments,
state metadata, coordinate values in explicit nm under pm/fs/coulomb session
standards, unique string atom IDs, named pending analyses and H5MSM round trips.
Multiple states and strict loss fail without source mutation.

**Assumed:** retained chemical values are caller-declared evidence, not newly
certified chemistry. Partial completeness and unknown added values are intentional.
No force-field or geometry-quality certificate is inferred from preservation.

## What was refuted

- Rebuilding only topology and coordinates is insufficient: the independent
  chemical and interaction domains carry scientifically meaningful information.
- Copying observations unchanged is insufficient: new atoms extend the candidate
  universe even when every old coordinate is unchanged.
- Padding B-factors or force-field parameters with guessed values is not preservation.
  Report their loss or fail explicitly instead.
- A fresh state with copied bonds does not retain state identity or atom chemistry.

## Scope and exclusions

Covers both native atom-append and new-terminal-group assembly paths. Native
heavy-atom repair has strict/intersection control. Other native consumers retain
the existing reported intersection behavior; they do not acquire a new public
strict parameter in this correction. Multiple chemical states require an explicit
single-state extraction. New chemical assignment, energy refinement and full
receptor preparation remain separate. H5MSM 0.5 does not persist the experimental
MolecularMechanics domain; the roundtrip assertions concern supported domains.

## Acceptance criteria

The guard must assert chemical values and state identity by preserved source atom
IDs, pending named analyses with remapped indices, unknown new values, unchanged
source and H5MSM value persistence. Strict loss and ambiguous state selection
must fail transactionally. Both native assembly paths use one domain finalizer.

## Provenance

Linux development workspace, Python 3.13.14 under the bounded #237 migration
exception, released ArgDigest 0.13.0 override, NumPy 2.4.6, pandas 2.3.3 and
RDKit 2025.09.5 where the fixture workflow uses it. Date: 2026-10-04.
This is targeted contract evidence, not Python 3.14 release qualification or
an installed-artifact, performance or biological benchmark. Commands using the
ArgDigest override record the development environment; that override is not a
runtime requirement or a committed path.

## Local validation checkpoint — 2026-10-04

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_heavy_atoms \
  tests/build/add_missing_hydrogens/test_add_missing_hydrogens_engine_MolSysMT.py \
  tests/build/add_missing_terminal_cappings/test_add_missing_terminal_cappings_engine_MolSysMT.py \
  --doctest-modules molsysmt/build/add_missing_heavy_atoms.py
```

63 passed in 37.73 s. The 24 warnings comprised 22 reported atom-parameter drops
and two deliberate unassessed VAL controls. Strengthening the terminal preservation
fixture to start with a still-evaluated analysis and no heavy gap then passed
all five domain-preservation cases in 4.64 s. This final focused run replaces that
fixture's earlier evidence without claiming another aggregate suite execution.

The heavy-atom tutorial executed and saved its real outputs (11.9 s). Docstring,
course, public API registry/signature, dependency-import and developer-guide checks
passed. Repository-wide Ruff check and format checks passed. Sphinx HTML exited
0 with existing course/navigation/native-class reference warnings; it is not a
globally clean documentation gate. Hosted CI acceptance is separate.
