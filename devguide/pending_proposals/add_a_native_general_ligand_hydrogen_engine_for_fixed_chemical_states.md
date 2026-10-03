---
summary: Add a native general ligand hydrogen engine for fixed chemical states
issue: uibcdf/molsysmt#308
status: open
opened: 2026-10-03
closed:
verification: inspected
area: [build, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Add a native general ligand hydrogen engine for fixed chemical states

**Reported:** 2026-10-03, following the maintainer's review of the RDKit route in #300.
**Status:** Future implementation; not a requirement for continuing the current workflow.

## What

Provide a native MolSysMT engine for adding missing indexed H atoms to a caller's
prepared ligand state under the fixed-state contract delivered by #300. General
ligand graphs should not require recognized amino-acid residue names. Declare a
validated chemistry domain and reject unsupported cases; "general" must not imply
support for every element, valence, radical, coordination or stereo representation.
Keep the working optional RDKit route available and selectable.

## How

Extend the existing public `build.add_missing_hydrogens` engine selection in
`mode='fixed_chemical_state'` after scientific validation. Do not introduce another
public H-addition function or chemical store. Inspect and reuse:

- `physchem.get_hydrogen_inventory` for indexed and stored virtual H counts;
- chemical readiness and the authoritative `ChemicalStates` assignments;
- connectivity tools in `topology` and geometric tools in `structure`;
- the existing ideal-placement primitives in `build._native_placers`, with their
  bounded tetrahedral correction and guards from #306;
- `build.add_terminal_atoms` for native reconstruction, deterministic IDs,
  source-index correspondence, attributes and interaction invalidation;
- `pbc` tools for explicit periodic reconstruction and image conventions.

Any missing chemical interpretation or geometry operation with standalone use
belongs in its owning general module, with its own documented contract and tests.
Keep placement-specific rules and orchestration in the engine. Evaluate published
placement methods before choosing criteria, use descriptive or attributed names,
and retain executed-method references through optional Ackredit reporting. Profile
real workloads before deciding whether additional kernels belong in Rust.

## Why

The implemented fixed-state ligand route currently requires explicit RDKit. The
existing `engine='MolSysMT'` branch instead uses residue/pH inventories and named
amino-acid/capping templates. Its geometric helpers are useful ingredients, but
their existence does not establish a native fixed-state ligand engine.

Removing that optional dependency for validated ligand chemistry would broaden
local preparation workflows. This is a maintainer-requested future capability,
not evidence that the present RDKit path fails or a measured speed advantage.
PharmacophoreMT's prepared-input requirement is tracked in uibcdf/pharmacophoremt#22;
DockingMT's preparation profile is tracked in uibcdf/dockingmt#33.

## What is measured and what is assumed

**Inspected:** At commit `d04299cc4`, fixed-state dispatch requires `engine='RDKit'`.
The existing MolSysMT branch in `build.add_missing_hydrogens` uses amino-acid and
capping rules; the fixed-state implementation reuses the inventory and attachment
tools. #300 records its executed RDKit validation. No native ligand engine,
performance measurement or parity experiment is supplied by this proposal.

**Assumed:** An independently validated native engine could reduce installation
requirements for its supported domain. Its coverage, implementation effort,
memory use and runtime remain unknown.

## What was refuted

- Correcting ideal tetrahedral placement in #306 does not implement or certify
  general ligand chemistry, hybridization inference or stereo preservation.
- A protonation/pH engine cannot silently replace a fixed-state engine; changing
  the declared inventory violates the accepted contract.
- RDKit parity alone cannot validate a shared scientific mistake. Independent
  analytic or reference controls are also required.
- Compilation alone cannot establish a performance improvement.

## Scope and exclusions

Materialize the declared H inventory on a supplied pose, retaining existing H and
all original atoms, indices, string IDs, coordinates and chemical assignments.
Start with the same explicitly bounded one-state, one-frame ligand contract as
#300 unless a separately documented expansion is accepted. Preserve units,
reports, failure atomicity and source immutability. Reuse the established handling
of unsupported attributes and named interactions.

Do not choose pH, protomers, tautomers or heavy-atom conformers. Do not claim an
energy minimum or receptor-oriented OH/NH geometry. Unsupported metal, radical,
isotopic-addition or ambiguous cases must fail explicitly. A future refinement
operation is a separate capability, not an implicit placement step. The default
legacy engines and the explicit RDKit route continue under their own contracts.

## Acceptance criteria

1. Shared fixed-state contract tests cover form-agnostic inputs, unknown/conflicting
   inventories, determinism, typed empty/idempotent results, failures and no fallback.
2. Retain exact original coordinates and atom indices, charges, isotopes, bond
   chemistry and supported stereo; verify each appended H's parent correspondence.
3. Independent scientific controls cover supported hybridizations, aromatic and
   charged cases, bond lengths/angles and stereo. Include the pinned EST control
   and adversarial geometries; compare RDKit only within equivalent method scope.
4. Tests without RDKit installed or importable actually execute the native engine.
   Existing RDKit and residue/pH behavior retains its regression coverage.
5. Non-default PyUnitWizard policies, native/H5MSM round trips, attribute policies,
   interaction invalidation and detached original provenance remain contract-tested.
6. Record reproducible runtime/memory measurements before acceleration or
   performance claims; disclose unvalidated chemistry and orientation limits.
7. Update docstrings, User Guide, Cookbook and course when implementation lands.
   Close with addressable native-engine guards and the durable method specification.

## Dependencies and risks

#300 is the delivered consumer contract; #306 supplies limited native geometry
guards. Neither is an open blocker. Key risks are incorrect hybridization/valence
interpretation, underdetermined orientations, silently changed stereo or H counts,
and loss of native metadata during reconstruction. No implementation date or
release milestone is assigned. This proposal does not block RDKit-based progress.

## Provenance

Source inspection on 2026-10-03 at `d04299cc4`, covering public hydrogen dispatch,
its existing native placement helpers and the delivered inventory/attachment tools.
The current proposal adds tracking only; it supplies no new calculation or benchmark.
