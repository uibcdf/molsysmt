---
summary: Provide explicit small-molecule standardization with chemical-state and atom-identity evidence.
issue: uibcdf/molsysmt#366
status: open
opened: 2026-10-10
closed:
verification: inspected
area: [physchem, preparation, chemical-states, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit small-molecule standardization

**Reported:** 2026-10-10, provider request from uibcdf/pharmacophoremt#41.
**Status:** Post-1.0 capability proposal; no implementation is promised by this triage.

## What

Provide explicit, independently useful chemical preparation operations and a
declared composition of them for small molecules. Distinguish representation
normalization, fragment retention, charge/protonation changes and stereochemical
changes. Return the prepared system, atom correspondence and an auditable report
without silently replacing the input or discarding an unsuccessful molecule.

## How

Provider source inspected at `072aa9bdbfb9299f7e3256f9b27f6aae8ea52629` supplies
the following pieces, with narrower contracts:

| Existing public tool | Useful contribution | Boundary |
|---|---|---|
| `physchem.get_chemical_readiness` | Reports stored fields, connectivity boundaries and missing evidence. | Does not validate valence, repair chemistry or choose protonation. |
| `physchem.assess_chemical_template` / `apply_chemical_template` | Assesses and transfers compatible assignments with explicit maps/provenance. | A supplied template is required; it is not a general normalization policy. |
| `physchem.normalize_aromatic_bond_orders` | Normalizes already declared aromatic bonds on a copy with original representation evidence. | Does not perceive aromaticity or normalize other resonance motifs. |
| `physchem.get_aromaticity` / `get_cip_stereochemistry` | Evaluates chemistry under an explicit supported provider/model. | Recognition does not authorize changing charge, stereo or the retained fragment. |
| `basic.get`, `select`, `extract`, `convert` | Retrieves component membership and makes explicitly selected representations. | Selecting a component does not decide which fragment is chemically appropriate. |
| `build.add_missing_hydrogens` | Adds H under the supported explicit fixed-state preparation contract. | Does not select a standard protonation state for arbitrary compounds. |

No public composition covering the requested standardization policy was identified
in the inspected exports. The consumer reports a historical RDKit utility that
strips salts, normalizes/uncharges and can remove stereochemistry; it is not part
of its current native pharmacophore workflow. That consumer source was not
executed in this provider triage.

Reusable chemical interpretation/normalization belongs in `physchem`, graph and
component operations in `topology`, and stored assignments in `ChemicalStates`.
An explicitly selected preparation workflow may compose these tools in `build`;
variant protocol registration belongs to Praxis when appropriate. A genuinely
small-molecule-specific operation may belong under `element.molecule.small_molecule`;
that package currently exports no implementation to reuse here. Choose the public
owner from the operation's contract rather than creating a second chemical store.

Each transformation should identify its method, parameters, executed provider and
original producer version, retained/removed atoms and any newly introduced atoms.
Assess ambiguity and unsupported encodings before mutation. Preserve other states
and domains or report an explicit supported invalidation/loss; do not present a
changed formal charge as representation-only normalization. Keep the original
stereochemical declaration unless a separate requested transformation changes it.

## Why

The consumer needs shared preparation pieces rather than an independent local
chemistry engine. This is useful new coverage, not a defect in the narrower tools
listed above. The [frozen scope](../release_1_0_scope.md#admission-rule) therefore
places implementation after 1.0 unless the maintainer explicitly changes scope.
Related chemical-state enumeration requests uibcdf/molsysmt#220,
uibcdf/molsysmt#229 and uibcdf/molsysmt#230 remain separate scientific decisions.

## What is measured and what is assumed

Evidence is inspection of public exports and the listed source contracts, plus
the consumer's issue report. No standardization workflow, external chemistry
engine, benchmark or independent scientific comparison was executed here.
An existing component index is usable selection evidence, not proof of a preferred
parent fragment or of chemical validity.

## What was refuted

Conversion or successful sanitization alone does not establish the requested
standardization policy. Aromatic representation normalization is insufficient for
salt stripping or neutralization. Returning `None` on every exception, silently
dropping inputs or removing stereo would conceal scientifically relevant changes.

## Scope and acceptance criteria

- Define individual operations and supported chemistry before naming an aggregate
  policy. Keep input forms agnostic wherever their required attributes exist.
- Test salts/disconnected fragments, charged molecules, explicit/implicit H,
  stereochemistry, unsupported chemistry and partial/failure outcomes against
  independent expected assignments and atom maps.
- Preserve the source; report retained/removed/new atoms, state changes, units,
  provenance and any invalidated named analyses. Check supported round trips.
- Complete public argument validation, dependency handling, docstrings, User Guide,
  Cookbook and course material with the implemented coverage and exclusions.

No implicit conformer generation, tautomer enumeration, drug-likeness filter,
uncontrolled neutralization or universal chemistry guarantee is included.
The current native pharmacophore workflow need not wait for this optional extension.
