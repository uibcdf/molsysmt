---
summary: Diagnose ligand chemical readiness for a selected molecular state
issue: uibcdf/molsysmt#217
status: resolved
opened: 2026-09-22
closed: 2026-10-03
verification: measured
area: [physchem, diagnostics]
guard: tests/physchem/test_get_chemical_readiness.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Diagnose ligand chemical readiness for a selected molecular state

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Resolved. A bounded, read-only stored-field assessment is implemented
in `physchem`; chemistry repair and preparation remain separate capabilities.

## What

Provide an inspectable assessment of a selected small-molecule chemical state before downstream preparation.

## How

Report element identity, atom and bond identity, bond order, formal charge, stereochemistry, coordinates, and ambiguous or inferred fields. Distinguish absent, unsupported, and assessed data without silently completing chemistry.

## Why

MolSysMT can convert MolSys to rdkit.Mol, but a consumer needs to know whether the input chemistry was explicit and sufficient for its intended operation.

## What is measured and what is assumed

**Contract-tested:** The public audit reports complete, partial, unsupported and
ambiguous stored fields without modifying source chemistry. The dated execution
record below includes native, complementary, SDF, PDBQT, RDKit and H5MSM inputs.
**Unassessed:** Scientific chemical validity, consumer acceptance, exhaustive
format coverage and quantitative performance are not established by this audit.

## What was refuted

A successful conversion alone is insufficient evidence that every chemical field was present in the source.

## Scope and exclusions

General diagnostics for one selected state and structure; no chemical-state enumeration, atom typing, or Vina policy.

## Acceptance criteria

- A structured result distinguishes present, inferred, missing, and unassessed chemistry by field and atom or bond where useful.
- Tests include complete, incomplete, and ambiguous ligand examples, with no silent chemical assignment.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#4.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.

## First implementation contract — 2026-10-03

Expose `physchem.get_chemical_readiness` for one selected state and at most one
selected structure. The versioned detached dictionary reports field coverage,
unsupported values, limited consistency conflicts and source indices. It does
not return a universal `ready` flag: readiness depends on the downstream operation.

Inspect existing native domains directly and use supported form conversions/getters
for other representations. Read-only diagnostics must accept incomplete chemistry;
the complete-graph guard used by ring/CIP tools is therefore not applicable.
Reuse native state resolution, atom selection and fixed-unit coordinate access.
Prepared PDBQT can be inspected through its topology/getter routes without silently
attaching or discarding its torsion tree. Unsupported SDF encodings still raise
their parser diagnostics; this tool is not another parser or an implicit fallback.

Keep stored availability and origin separate. Bond `evidence` can identify explicit
or inferred relationships. Atom-level property origins are unassessed when storage
does not provide them; a value, a `complete` flag or a successful conversion alone
does not establish scientific validation. Preserve stored source provenance pointers.
Do not infer neutral charges, aromaticity, hydrogen inventory, chirality or valence.

Selections retain source indices and inspect incident bonds, including their external
endpoints. Report crossing bonds so a selected subgraph is not treated as an isolated
prepared ligand. Count explicit H atoms separately from atom-state virtual/implicit
H counts. Finite coordinates are assessed in nm through PyUnitWizard; finiteness
does not certify 3D conformer quality or compactness under PBC. No new external engine
or optional attribution boundary is introduced by the native stored-field audit.

## Resolution and execution evidence — 2026-10-03

Implemented `physchem.get_chemical_readiness`, registered as experimental, with
the [user contract](../../../docs/content/user/tools/physchem/get_chemical_readiness.md).
The selected guard exercises missing formal charges, unsupported element/order
encodings, inferred edge evidence, ambiguous references, missing frame-state
associations, incident/crossing bonds, empty selections, detached output and
unchanged sources. Real 1S63 PDBQT stays inspectable without torsion-tree loss.
RDKit benzene retains virtual H counts without materializing explicit H atoms.
H5MSM cases preserve frame/state association, permit coordinates alone and reject
undeclared combined axes. The bounded-read guard forbids full structural-layer
materialization during a numeric frame/atom query.

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/physchem/test_get_chemical_readiness.py \
  tests/physchem/test_get_cip_stereochemistry.py \
  tests/native/test_chemical_states.py \
  tests/native/test_molsys_chemical_state_association.py \
  tests/basic/convert/mult_to_one/test_convert_chemical_and_structural_domains.py \
  tests/form/file_h5msm/test_public_h5msm_v05.py \
  tests/form/file_h5msm/test_topology_free_molsys_v05_probe.py \
  tests/form/file_sdf/test_native_contract.py tests/form/file_pdbqt \
  tests/element/atom/test_atom_types.py \
  --doctest-modules molsysmt/physchem/get_chemical_readiness.py
```

Result: **296 passed, 9 warnings, 80.92 s**. This is a focused regression,
not a whole-suite or installed-wheel qualification. Warnings include known
MDAnalysis mass guessing, concatenation attribute loss and a binary-size runtime
warning; none failed these contracts. A separate new-tool/doctest run passed
21 cases against ArgDigest's fixed main source `7d88628c3003792e46b234b9e00afb2a48932943`.

The command used an isolated archive of ArgDigest's released `0.13.0` tag,
commit `9880fa7b990fd0987ff0de715b665eb9e11c11b2`, rather than changing the
older editable sibling checkout. To reproduce, create a source snapshot of that
tag outside the repository and substitute its path in `PYTHONPATH`; the temporary
path is not a maintained artifact. Other local runtime metadata: Python 3.13.14,
NumPy 2.4.6, pandas 2.3.3, h5py 3.16.0, RDKit 2025.9.5, PyUnitWizard
`0.25.0+7.g00d756c`, SMonitor `0.13.0+9.g0ec2ef9`, DepDigest
`0.10.1+15.g78a9106`. These source-environment results do not certify all public
dependency floors or release artifacts.

ArgDigest 0.13.0 predates the literal-True bypass fix in uibcdf/argdigest#17.
The new boundary temporarily reuses MolSysMT's existing skip-flag digester for
non-booleans, as the existing Interactions compaction boundary does. Retire that
compatibility check when the public runtime floor includes the provider fix;
the tests retain rejection of `skip_digestion='yes'` on both routes.

Ruff, dependency import/contract audits, public API stability, NumPy docstring
checks and the 156-notebook course structural validator passed. Sphinx HTML
builds completed; existing course heading/key-takeaway and unrelated documentation
warnings remain. The new page has no remaining build warnings. User Guide,
Foundations, Cookbook, Module 12 and its function inventory are updated. Only
course narrative changed; existing executable cells and outputs were preserved.

The accepted assessment criteria are met. Valence validation, protonation,
template assignment, fixed-state H placement, charge models and docking protocols
remain separately tracked capabilities; this closure does not complete them.
