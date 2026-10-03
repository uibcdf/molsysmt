---
summary: Add ligand hydrogens for a fixed chemical state while preserving existing coordinates.
issue: uibcdf/molsysmt#300
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [build, structure]
guard: tests/build/add_missing_hydrogens/test_fixed_state.py
normative:
blocked_by: []
supersedes: []
---

# Hydrogen addition for a fixed ligand chemical state

**Reported:** 2026-10-03, from the preparation requirements in
uibcdf/pharmacophoremt#22.
**Status:** Resolved for the first documented fixed-state RDKit slice; consumer biological acceptance remains separate.

The sections below retain the initial planning rationale. The delivered boundary and
measurements are recorded in the implementation section that follows.

## What

Provide a reusable MolSysMT operation that adds missing explicit hydrogen atoms
and their local coordinates to a prepared ligand in an explicitly selected
chemical state. Preserve every existing atom, including existing hydrogens, and
its coordinates. Return a new native molecular system with complete old-to-new
atom correspondence, new-H parent correspondence and an inspectable preparation
report. Start with an optional RDKit engine behind a provider-owned contract;
allow a native engine when its supported chemistry and scientific behavior are
validated.

## How

### Ownership and existing tools

Review extending `build.add_missing_hydrogens` with an explicit fixed-state mode
and an RDKit engine before introducing another public entry point. Its present
signature includes `pH=7.4` and engines `OpenMM`, `PDBFixer` and `MolSysMT`.
The native branch uses amino-acid hydrogen rules and ACE/NME residue templates;
it skips other non-amino-acid groups. Existing support does not establish general
ligand hydrogenation under this proposed contract. Preserve current documented
residue/pH behavior; an API review must define how fixed-state inputs are selected
without silently applying that default pH. If compatibility requires a distinct
public operation, document that decision and have both operations share the
applicable internal implementation. Do not export a placeholder API.

`build` owns system reconstruction and hydrogen addition, `structure` owns reusable
local placement geometry, `physchem` owns chemical interpretation and readiness,
and native `ChemicalStates` owns assignments. Reuse supported form conversion,
atom correspondence and native reconstruction facilities after verifying they
meet this contract. Independently useful geometric primitives belong in their
owning module; not every internal helper needs a public export. PharmacophoreMT
and other consumers call MolSysMT rather than implementing molecular operations
or an RDKit bridge themselves.

### Separate the scientific decisions

1. Resolve the caller-selected chemical state and its intended hydrogen inventory.
   Prepared connectivity, bond orders, aromaticity, formal charge, stereochemistry
   and applicable hydrogen counts or a declared supported valence rule must justify
   that inventory. Missing evidence is an unresolved input, not an instruction to
   assume a neutral molecule or choose a protonation state.
2. Add missing H atoms and place their coordinates using a named local geometry
   method. Existing atoms remain fixed. Generated coordinates are modeled positions,
   not experimental observations or coordinates copied from a CCD ideal conformer.
3. Environmental refinement of ambiguous OH/NH orientations is a separate explicit
   operation, with its own receptor, scoring/energy method and convergence contract.
   Local H placement must not imply that refinement has happened.

This operation does not enumerate protomers or tautomers, predict pKa, determine
equilibrium populations or generate new heavy-atom conformers. State generation
belongs to #220/#229/#230, and fixed-state conformer generation to #219.

### First implementation boundary

Accept one isolated, supported ligand with one selected chemical state and one
explicit coordinate frame. Resolve the state through native facilities before
reading state-dependent fields. Multiple frames/states must be deliberately
extracted through MolSysMT or rejected until their preservation and domain
expansion are specified; do not silently drop them. Preserve box, units and the
selected frame/state association. Whole-complex editing and multi-frame/state
extension are subsequent capabilities with explicit contracts.

Validate connectedness, chemistry coverage, valence, charge and existing-H
consistency before constructing an output. An over-hydrogenated or chemically
conflicting input fails; this operation does not remove H or repair the chemical
state. Existing H positions are preserved, even when another tool might later
refine them. Zero missing H is an idempotent success with zero added atoms, not
permission to reposition the existing ones. Unsupported metals, query chemistry,
radical states or isotopic additions fail explicitly unless the chosen engine has
a documented and tested contract for them.

For the RDKit engine, use a validated native-to-backend mapping, the selected
prepared chemistry and a populated 3D conformer. RDKit's documented `AddHs`
coordinate option (`addCoords=True`) is the initial backend candidate. It needs
prototype verification on the supported chemical classes; it is not evidence of
correct receptor-facing hydroxyl orientation. Backend sanitation or aromatic
normalization must preserve the selected chemical identity. Detect incompatible
reinterpretation and reject it rather than accepting a backend-chosen state.

Convert coordinates through PyUnitWizard and the form adapter's declared unit
contract. Retain exact source values for all existing atoms when assembling the
native output; do not roundtrip their coordinates through the backend. Validate
the backend atom map and generated-H parents before updating native topology and
chemical-state domains. Return a new system only after the complete operation
succeeds. Source inputs remain unchanged on success and failure.

Append new atoms with deterministic ordering and valid native string IDs, using
native membership rules. The complete source-to-output map remains mandatory
even if this implementation preserves all original indices. Maintain element,
isotope, formal-charge, bond-order and stereochemical meaning for existing atoms;
make newly explicit H bonds consistent with the selected state. Supported forms
must not lose these fields silently. Report a failed preflight or engine failure
with catalog-backed diagnostics, including the affected atom/state and reason.

### Result, engines and attribution

The proposed result contains the native molecular system and a detached,
versioned provider-owned report. Exact API/result naming remains subject to
review. The report should retain:

- Selected source chemical state, frame, chemical readiness and the method used
  to determine missing-H inventory.
- Complete old-to-new atom mapping, new-H-to-parent mapping, generated IDs and
  added atom/bond assignments.
- Existing atom/coordinate preservation checks and generated-coordinate units,
  geometry method, parameters and limitations, including unresolved torsions.
- Original template/input provenance when present; generated-coordinate status
  distinct from observed coordinates.
- Executed engine and original software versions, supported chemistry, any seed
  needed for reproducibility, and applicable scientific references.

Select the engine explicitly. Missing RDKit or unsupported chemistry must not
silently switch to another engine. Keep RDKit optional and lazily loaded through
the existing DepDigest policy. The provider contract must allow a later native
implementation without depending on a public RDKit object or backend atom order.
Review existing `_native_placers` geometry before adding new primitives. Native
coverage, performance and parity require separate evidence; neither Rust nor a
GPU/distributed implementation is required for the first slice. Profile supported
workloads before accelerating reusable kernels.

Follow `ACKREDIT_GUIDE.md` for optional executed-method/software attribution.
Contribute to the enclosing application's session when available, retain detached
references and original versions in the result, and never enable capture hooks or
enrichment automatically. Provider absence or diagnosed attribution failure must
not invalidate a completed molecular result, including under warnings-as-errors.
Keep data/template provenance separate from software credit. Reading a report
does not register a new scientific execution.

## Why

PharmacophoreMT needs explicit donor-H geometry for traditional directional
pharmacophore modeling. Its traceable ERalpha input and preparation gap are tracked
in uibcdf/pharmacophoremt#22. Applying an explicit chemical template (#298) assigns
chemistry to corresponding existing atoms; its minimum contract deliberately does
not add missing atoms or generate coordinates. A ligand hydrogenation operation
therefore has useful standalone scope for this and other molecular workflows.
It must remain in MolSysMT so consumers share preparation, identity and diagnostic
contracts.

## What is measured and what is assumed

**Inspected, 2026-10-03:** `molsysmt/build/add_missing_hydrogens.py` exports the
existing pH-oriented operation and the three engine branches described above.
Its native branch uses `get_expected_hydrogens` and `_native_placers` and skips
non-amino-acid groups other than ACE/NME. No RDKit engine is present in that file.
This is source inspection, not an execution of every supported engine.

**Primary backend reference:** RDKit documents hydrogen addition and its coordinate
option in [MolOps](https://www.rdkit.org/docs/cppapi/MolOps_8h.html) and hydrogen
handling in [Getting Started in Python](https://www.rdkit.org/docs/GettingStartedInPython.html).
These describe the candidate primitive; a MolSysMT integration preserving this
report's invariants has not been executed or scientifically validated here.

**External consumer evidence:** The deposited-input identity, missing observed H
and coordinate provenance audit is recorded in uibcdf/pharmacophoremt#22 and the
related preparation report #298. This proposal adds no new hydrogen-generation
measurement. Consumer input curation is not validation of generated H geometry.

**Proposed:** RDKit is the first candidate engine. Its exact supported chemical
classes, independent geometry tolerances and native result reconstruction still
need implementation and validation. A native engine may be useful later; no speed
or scientific coverage advantage is claimed.

## What was refuted

- Existing residue-template hydrogen addition is not evidence of a general
  ligand fixed-state contract; the inspected native code skips those groups.
- Template application alone does not supply coordinates for atoms absent from
  the source, and CCD ideal/model H coordinates do not preserve a deposited pose.
- Local hydrogen coordinate generation does not choose a pH-dependent state or
  establish receptor-optimized donor orientation.
- Building a second molecular preparation layer in PharmacophoreMT would duplicate
  MolSysMT ownership and impede other consumers; use the provider boundary.

## Scope and exclusions

One prepared ligand, one selected state/frame, missing-H addition, local placement,
identity/coordinate preservation, diagnostics and optional attribution. No chemical
repair, hydrogen removal/repositioning, automatic pH choice, protomer enumeration,
whole-ligand embedding, receptor refinement, metal chemistry guarantees, full
complex preparation or accelerated backend requirement.

## Acceptance criteria

- A reviewed and documented public contract is implemented in MolSysMT with
  compatible existing residue/pH behavior, deterministic native results and
  tests that exercise preservation and failure semantics.
- Small independent reference cases cover methane, ethanol, phenol and a
  declared charged amine; expected H inventories, C-H/O-H/N-H geometry and
  appropriate angular tolerances have independent justifications. Arbitrary
  hydroxyl torsions are not compared to one alleged unique correct orientation.
- Permuted input atom order, partially/fully hydrogenated inputs and repeated
  execution preserve every original atom, identity and exact coordinates.
  Old/new and parent maps are bijective or complete as appropriate; no H is
  duplicated. Charges and supported stereo/isotope fields remain consistent.
- Unknown bond orders/charges, conflicting H inventory, unsupported chemistry,
  missing/nonfinite/degenerate geometry, ambiguous states, unsupported frame
  counts, absent backend and backend failure have deliberate tested outcomes.
  Failed operations leave source and chemical-state domains unchanged.
- Unit conversion and source-coordinate retention are tested independently of
  output self-consistency. A later alternative engine is assessed against the
  same contract and scientific references before claiming interchangeable support.
- Optional attribution is tested with real provider/session reuse, fresh report
  readers, provider absence/failure and warnings-as-errors without changing the
  molecular outcome. The executed branch receives credit, not an unused engine.
- Update docstrings, User Guide foundations/toolbox/cookbook and the relevant
  course material at implementation time. Close with addressable tests protecting
  this contract; writing the proposal does not constitute implementation acceptance.

## Dependencies and risks

Related: #298 (explicit chemical templates), #217 (readiness), #223 (atom identity),
#254 (native chemical-state domains), #219 (conformers), #220/#229/#230 (chemical
state enumeration), #177 (environmental pKa), and uibcdf/pharmacophoremt#22.
Prepared chemistry is a prerequisite, but #298 is not a universal blocker:
supported inputs can supply it through other declared routes. No tracked issue is
asserted to block the initial bounded implementation here.

Main risks are implicit state changes during backend sanitation, loss of original
atom identity, drift in source coordinates, and presenting underdetermined H
orientation as biological validation. Native-domain reconstruction and coordinate
preservation need direct contract tests before using this in the ERalpha workflow.

## Provenance

Source inspection on 2026-10-03 in the local Linux MolSysMT checkout, HEAD
`f70bb331434c44c89a21b3e7787d202c6c5dd1f4`, with unrelated uncommitted work
present. Inspected the public hydrogen-addition implementation and its native
amino-acid/protonation dependencies; no scientific calculation or performance
benchmark was run for this proposal. Consumer execution environments and source
checksums remain in the separately tracked #298/uibcdf/pharmacophoremt#22 evidence.

## Implementation and evidence, 2026-10-03

**Implemented:** Extend the existing public `build.add_missing_hydrogens` with
keyword-only `mode`, state/frame selection, report and attribute-policy options.
The original four positional parameters and defaults are preserved. Fixed-state
mode requires `mode='fixed_chemical_state'`, `pH=None` and explicit `engine='RDKit'`;
it returns a detached native system or system/report dictionary. It requires one
state and one frame already present in the source; it never silently extracts them.

**Ownership:** `physchem.get_hydrogen_inventory` independently audits indexed H
versus stored virtual counts without RDKit. `build.add_terminal_atoms` independently
attaches declared atoms and length quantities covering all frames of a one-state
system; it does not infer chemistry or generate geometry. The fixed-state consumer
uses both tools. Its private PBC preflight reuses the provider's MIC primitive with
explicit nm units. General form conversion supplies the optional C++ RDKit graph
and conformer; there is no new dependency, embedding or force-field optimization.

**Preservation:** Stamp detached temporary unique identifiers to verify conversion
order even when original IDs repeat. Check incoming geometry in angstroms and
sanitized elements/isotopes/charges/aromaticity/H inventory, plus declared absolute
stereo against source 3D geometry. Validate appended-H parents, unchanged old graph
and new bond geometry before native reconstruction. Only generated positions come
from RDKit; original nm values are copied exactly from the source. Preserve state
ID/provenance index, original string IDs, memberships, box and frame/state links.
Indexed H materialization clears old virtual counts, without creating a second
chemical store. There is no configurable isotope-addition policy in this slice.

**Metadata and validity:** Strict policy rejects attributes that cannot cover new
atoms. Intersection policy reports dropped atom-aligned attributes, system
observables and force-field parameters. Retain sparse alternate locations for
old atoms. Named interactions on an expanded copy retain provenance but have no
evaluated frames or active occurrences; adding H can change science without moving
old atoms. Zero addition returns an unchanged independent copy with valid analyses.
The original source remains unchanged on success and failure.

**Contract-tested:** Native, RDKit and H5MSM input routes; explicit mode/no fallback;
unknown fields and inventory, metals, radicals, disconnection, invalid endpoints,
multiple states/frames, missing/nonfinite/coincident geometry, periodic split
rejection and compact-pose preservation; deterministic parent/old-new maps;
existing isotopic H and permuted atoms; idempotence; backend/unit failure;
attribute loss/strict rejection; occurrence invalidation and H5MSM roundtrips.
Real Ackredit enclosing-scope credit, provider absence/failure under strict warnings,
and fresh portable-attribution readers preserve completed outcomes and producer
versions. Report retention remains detached: it is not stored automatically in
MolSys or a new H5MSM preparation-history layer.

**Scientifically validated, bounded:** Analytical methane H-H cosines (-1/3,
absolute tolerance 0.015), methylammonium N-neighbor cosines and independent broad
C-H/N-H/O-H/S-H length intervals; ethanol, phenol, charged amine, sulfide and
phosphorylated ligand counts/charge; phenol ring-H coplanarity; fixed absolute E/Z
and reflected chiral-pose rejection. The pinned real EST control yields 44 atoms,
47 bonds and 24 added H from 20 observed heavy atoms/23 bonds. Exact observed
coordinates, its six aromatic atoms, two O3/O17 donor-H sites and five CIP centers
remain consistent through H5MSM. These are provider controls, not consumer biological
acceptance or an energy minimum. Unconstrained OH/NH orientations remain modeled.

**Separate defect:** Reviewing the legacy native placer reproduced incorrect
sp3 angles; the correction and independent guards are owned by uibcdf/molsysmt#306.
This does not establish a native fixed-state ligand engine.

**Documentation:** NumPy doctests pass; the User Guide has inventory, attachment and
fixed-state pages, Foundations distinguishes counts from atoms, the explicit-template
Cookbook adds the EST continuation, and Module 12 includes a newly executed native
inventory/attachment cell. API registry classifies the two new exports experimental;
the intentional signature extension is scoped to #300. No existing positional
parameter or default is changed.

**Local validation:** The first full focused run passed 199 tests (67.48 s);
subsequent new failure/reader controls were added before the final run. Local
Python is 3.13.14 under uibcdf/molsysmt#237, RDKit 2025.09.5, NumPy 2.4.6 and released
ArgDigest 0.13.0 snapshot commit 9880fa7b990fd0987ff0de715b665eb9e11c11b2.
This is not Python 3.14, a full platform matrix or a public release certification.

**Web build:** Sphinx HTML completed with exit 0. No diagnostic refers to a new
page/function. Six existing docutils errors and unrelated warnings remain under
uibcdf/molsysmt#144; exit 0 does not certify a warning-free repository build.
Commands and final test count are recorded below before closure.

### Final commands and results

The joint command below passed **209 tests in 67.07 s**. A subsequent focused
run after terminal-attachment implementation cleanup and two additional controls
passed **53 tests in 24.37 s**, including three public doctests. A final isolated
empty-attachment guard verifies typed fields and no invalidation for zero additions.
The runs report deliberate structural-attribute drops and legacy-format diagnostics;
known H5MSM pandas FutureWarnings are not silently filtered.

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_hydrogens tests/build/test_native_placers.py \
  tests/build/add_terminal_atoms tests/physchem/get_hydrogen_inventory \
  tests/physchem/test_chemical_template.py tests/physchem/test_chemical_template_est.py \
  tests/physchem/test_get_chemical_readiness.py tests/physchem/test_get_cip_stereochemistry.py \
  tests/test_ackredit.py

env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/build/add_missing_hydrogens/test_fixed_state.py tests/build/add_terminal_atoms \
  tests/physchem/get_hydrogen_inventory --doctest-modules \
  molsysmt/build/add_missing_hydrogens.py molsysmt/build/add_terminal_atoms.py \
  molsysmt/physchem/get_hydrogen_inventory.py
```

Ruff package/changed-test checks, dependency import/floor audits, public API
classification/signature validation, docstring fidelity, course validation and
developer-guide validation pass. Sphinx command (exit 0 with the known #144 debt):

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 sphinx-build -q -j 12 -b html \
  docs /tmp/molsysmt-fixed-hydrogens-docs
```

The public User Guide contract is
[Fixed-state hydrogen placement](../../../docs/content/user/tools/build/fixed_state_hydrogens.md).
The addressable guards are in the front-matter test file and
`tests/build/add_terminal_atoms/test_add_terminal_atoms.py`,
`tests/physchem/get_hydrogen_inventory/test_inventory.py`. Multi-state expansion,
whole-complex preparation, native ligand-engine parity and environment refinement
are deliberate exclusions, not claims certified by this completion.
