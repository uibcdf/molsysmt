---
summary: Native ParmEd export loses coordinates and formal charges without reporting them
issue: uibcdf/molsysmt#629
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [form, convert, metadata]
guard: tests/form/molsysmt_MolSys/test_to_parmed_Structure.py
normative:
blocked_by: []
supersedes: []
---

# Native ParmEd export loses represented geometry and chemistry

**Reported:** 2026-11-06 during the optional-provider review under
uibcdf/molsysmt#524, then reproduced with plain Python and dedicated pytest cases.
**Status:** Source correction and paired actual-provider receiving complete;
public delivery and board closeout follow.

## What

Before the owner repair, `msm.convert(molsys, to_form="parmed.Structure")` omitted
native coordinates and formal charges that ParmEd can represent. An explicit
single-structure export retained a box but had no coordinates. Reimport raised
`ArgumentLengthError` because that one box had no coordinate structure to accompany it. Multiple
structure-specific boxes were rejected by the intermediate OpenMM Topology,
although ParmEd supports a cell for each coordinate structure.

The plain export observation started with charges `[1, 0, -1]` and coordinates
of shape `(2, 3, 3)`. Selecting one structure and exporting produced charges
`[None, None, None]`, no coordinates, and a retained box. The report was already
`lossy` for component semantics, but **did not identify the lost formal charges
or coordinates**. This does not establish that the report called that fixture
equivalent.

With the existing `molsyssuite@uibcdf_3.14` environment activated, the recorded
export-only observation was produced from the repository root by this command
with the pre-repair adapters. Repeating it against repaired source checks the
same route but is not expected to reproduce the old losses:

```bash
parmed_review=.pytest_cache/pre1-review-20261106/providers/parmed-review
parmed_provider="${parmed_review}/parmed-4.3.1-py314ha51126d_1/lib/python3.14/site-packages"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="${parmed_provider}:.:.pytest_cache/pr543-viewer-4223-20261105:.pytest_cache/stabilization-551/tooling/published" python -B "${parmed_review}/probe_provider.py" "${parmed_provider}" "${parmed_review}/native431-numpy246-py314-export-observation.json" native export-only
```

The probe's native exit was **0**: it completed bounded provider checks and
recorded the export defects rather than asserting successful export fidelity.
The subsequent roundtrip probe exited **1**. See the retained
[export observation](../../../.pytest_cache/pre1-review-20261106/providers/parmed-review/native431-numpy246-py314-export-observation.json)
and [single-structure reimport failure](../../../.pytest_cache/pre1-review-20261106/providers/parmed-review/native431-numpy246-py314-selected.json).

## How

Before the repair,
[native MolSys export](../../../molsysmt/form/molsysmt_MolSys/to_parmed_Structure.py)
created an OpenMM Topology and forwarded only that topology. Coordinates
never reached the ParmEd constructor. The
[OpenMM bridge](../../../molsysmt/form/openmm_Topology/to_parmed_Structure.py)
delegated to `parmed.openmm.load_topology` without coordinates. The provider
loader omitted OpenMM atom formal charges and serials: atom numbers
retained the default `-1`. Aromatic bond identity was reduced to numeric order
`1.5`, overriding a separately supplied integer order and omitting ParmEd's
qualitative aromatic type.

This is not a provider capacity limit. ParmEd 4.3.1 accepts all coordinate
structures through `Structure.coordinates`, per-structure `(lengths, angles)`
cells through `Structure.box`, nullable `Atom.formal_charge` and `Atom.aromatic`,
and independent numeric `Bond.order` and `Bond.qualitative_type` fields.

[Conversion preflight](../../../molsysmt/_private/conversion_report.py) previously
audited this unregistered route through declared chemical capabilities. ParmEd
declared formal-charge support, so that comparison did not detect the adapter's
actual omission. It supplied no exhaustive coordinate or identifier audit.
A capability declaration does not prove that every conversion delivers it.

### Implemented owner repair

Explicit empty chain labels also survive ingestion and native roundtrip. The
reader no longer replaces a supplied empty string with `A`; native and OpenMM
forward builders already pass that legitimate empty label through unchanged.
The focused regression in the existing ParmEd structural/charge module tests
this case without changing missing-label or chain-generator policy. Its pytest
execution remains part of root qualification.

**Implemented; root pytest qualification pending.** The private
[ParmEd-native exporter](../../../molsysmt/form/parmed_Structure/_from_native.py)
consumes stable Topology, ChemicalStates, Structures and MolecularMechanics
explicitly. Native Topology conversion does not recover attached chemistry.
MolSys conversion passes selected coordinates and aligned per-structure cells,
using PyUnitWizard and the existing PBC operations. It builds detached provider
objects directly without an incidental OpenMM dependency.

The direct OpenMM converter separately transfers represented serials, labels,
formal charges, independent numeric bond orders, qualitative types and its one
box. Both boundaries keep optional-provider checks and function-local imports.
Explicit provider group objects preserve duplicate group labels without merging
distinct identities. Native interleaved group layouts are rejected rather than
silently splitting a group or reordering atoms. Known element masses are supplied;
explicit isotope identity is rejected/reported instead of replaced by average mass.

Instance-aware preflight and execution checks cover unsupported serial spellings,
unknown numeric orders, distinct nominal/fractional bond-order values, unsupported
aromatic/dative combinations, missing partial-charge entries, noncanonical box
orientation and unresolved multi-state structure associations. Raw rotated or
left-handed cells are not repaired by rotating coordinates. These bounded audits
do not claim an exhaustive representation audit.

[Element readback](../../../molsysmt/form/parmed_Structure/_read_native.py) uses
ParmEd atomic numbers, keeping force-field type labels separate. Numeric and
qualitative bond fields are read independently; mechanical bond parameter objects
are not promoted into chemical bond types.

The authorized charge-presence repair uses
[stored charge assignments](../../../molsysmt/form/parmed_Structure/_mechanical.py)
instead of ParmEd's zero fallback. Explicit zero and an assigned AtomType charge
remain known values. A wholly absent charge assignment returns `None`. A numeric
query mixing assigned and unknown charges raises the typed
`NotWithThisFormError`; native MolSys conversion retains those unknown entries
as a nullable mechanics column. No missing charge is silently replaced by zero.

## Why

The reproduced defect is a high-severity data-integrity problem at a public
interoperability boundary. A plausible ParmEd object lost charge assignments and
all coordinate structures without reporting those specific losses; a retained
box could make reverse conversion fail. Raising ParmEd's
dependency floor cannot repair a consumer route that never passes the data.

## What is measured and what is assumed

With the same environment activated, the finite baseline selection is:

```bash
PYTHONPATH=.:.pytest_cache/pr543-viewer-4223-20261105:.pytest_cache/stabilization-551/tooling/published python -m pytest --receptor=llm -n 12 tests/form/molsysmt_MolSys/test_to_parmed_Structure.py tests/form/openmm_Topology/test_to_parmed_Structure.py --junitxml=.pytest_cache/pre1-review-20261106/629-native-export-valid-counterexamples.xml
```

| Baseline | Native exit | Result | Interpretation |
| --- | --- | --- | --- |
| Initial authored cases | 1 | 17 failed | 12 authoring failures used nonexistent root `msm.Structures`/`msm.MolSys` exports; five cases exposed real adapter failures. |
| Corrected public native imports | 1 | 15 failed, 2 passed | Valid counterexamples against unchanged production adapters. |

The valid failures comprise six missing-coordinate cases, four valid ParmEd
requests blocked by the intermediate OpenMM single-box restriction, two
coordinate-free export cases losing atom serials, two direct OpenMM formal-charge
losses, and one native formal-charge loss. The two empty-system cases pass.
Assertions after the first failure in a test are not independently qualified by
that run; aromaticity, bond-order and mechanical assertions remain required
acceptance checks.

The first baseline's authoring mistakes were corrected only in tests, then the
same selection was repeated. Its count is not 17 production defects. Native
command exit status is authoritative. Retained
[first invocation](../../../.pytest_cache/pre1-review-20261106/629-native-export-counterexamples-invocation.json),
[valid invocation](../../../.pytest_cache/pre1-review-20261106/629-native-export-valid-counterexamples-invocation.json)
and [valid JUnit result](../../../.pytest_cache/pre1-review-20261106/629-native-export-valid-counterexamples.xml)
record the runs.

### Bounded post-repair smoke evidence

The expanded plain probe in
[attempt 3](../../../.pytest_cache/pre1-review-20261106/629-owner-smoke-attempt3.json)
exited **0**, adding actual charge-presence checks and reported typed rejections
for noncanonical serial labels, unknown numeric order, missing partial charges
and raw box orientation. Attempt 2 exited **1** because the probe tried to edit a
read-only native box view; copying those values before preparing the negative
input corrected that probe-authoring error. Its
[failed receipt](../../../.pytest_cache/pre1-review-20261106/629-owner-smoke-attempt2.json)
is retained. Expected typed rejections emit SMonitor diagnostics and are asserted
as successful negative outcomes; they do not establish whole-route qualification.
The [owner receipt](../../../.pytest_cache/pre1-review-20261106/629-owner-receipt.json)
retains exact commands, native exits, selected installed-provider origins and
frozen source identities.

The one-thread plain-Python
[owner smoke receipt](../../../.pytest_cache/pre1-review-20261106/629-owner-smoke-attempt1.json)
records three passing cases on Python 3.14.7, ParmEd 4.3.1 and OpenMM 8.6.1:
public native coordinate/box selection with charge/ID roundtrip, inventory-only
export, and OpenMM export with box-only readback. The selected coordinate shape
was `(2, 3, 3)` and the two boxes retained the requested reverse order. The report
still listed unsupported component semantics rather than claiming full fidelity.

This was not a pytest session and does not qualify the expanded regression
scope. New tests now cover explicit loss rejection/reporting, unit policy,
box orientation, duplicate group identity, force-field type versus element,
multi-state associations, empty inputs and direct OpenMM unknown-order handling.
The existing
[ParmEd structural/charge module](../../../tests/form/parmed_Structure/test_structural_and_charge_contract.py)
also has cases for known-zero/type-assigned/absent charges, nullable readback and
box-only structure axes. Root execution of these tests remains pending.

The [form overview](../../../docs/content/user/tools/form/class/parmed/parmed_Structure.ipynb)
describes the repaired contract and explicit limits. Its
[preservation receipt](../../../.pytest_cache/pre1-review-20261106/629-documentation-preservation.json)
records unchanged code cells, saved outputs, IDs, metadata and cell order, plus
the reviewed unchanged course/cookbook pages. No notebook execution or full
export-fidelity qualification is claimed by that prose-only check.

## What was refuted

- ParmEd cannot store multiple coordinate structures or per-structure cells:
  direct provider checks passed for both before native conversion.
- Native ingestion necessarily loses the charges: bounded ParmEd-to-native
  checks retained `[1, 0, -1]`, orders `[1, 2]`, coordinates and partial charges.
  Reverse export is the demonstrated failure.
- A green pre-repair export-only probe qualified roundtrip fidelity: its exit 0
  only meant observations were recorded. The explicit pre-repair roundtrip failed.
- A newer provider alone fixes the route: failures were reproduced with
  ParmEd 4.3.1 and OpenMM 8.6.1.
- All initial pytest failures describe production: twelve were fixture-authoring
  errors and are excluded from the valid failure classification.

## Scope and exclusions

This issue covers native MolSys/Topology export and the direct OpenMM Topology
bridge into `parmed.Structure`, selected atom/structure axes, represented
chemistry, optional guards, readback and truthful conversion reports. Topology
alone remains stable inventory without implicit chemical or coordinate recovery.

It does not qualify every ParmEd writer, parameterized force-field/Gromacs
route, all Python/platform combinations, molecular simulation or scientific
geometry. Multiple chemical states, arbitrary string IDs, unknown numeric bond
order, unknown partial charge and rotated/raw box orientation need explicit
supported behavior or a bounded limitation. ParmEd's public serial convention
is integer; numeric bond order cannot be `None`; the default charge getter can
return zero for an unassigned charge; cells store lengths and angles rather than
an arbitrary oriented matrix. Do not fabricate scientific assignments or claim
those source semantics were preserved.

Linked cache receipts are ignored local evidence, not durable repository guards
or guaranteed public artifacts. The committed report and addressable regression
modules carry the durable reproduction and acceptance contract.

## Acceptance criteria

1. Native selected coordinates and aligned boxes survive all requested
   structures, including order/repetition, with correct units under a non-default
   unit policy. Coordinate-free and empty inputs retain honest absence.
2. Available nullable formal charges, atom aromaticity, representable serials,
   group/chain labels, explicit numeric bond order and qualitative aromatic/dative
   identity reach ParmEd without inventing force parameters or changing the source.
3. Topology-only export does not recover attached chemistry. Native exporters
   and direct OpenMM conversion preserve their supported represented fields.
4. Unsupported semantics produce precise reports/rejections; strict preflight
   rejects detected loss before target construction. Report scopes retain any
   unassessed semantics explicitly.
5. The module named by `guard` and the
   [OpenMM bridge regression module](../../../tests/form/openmm_Topology/test_to_parmed_Structure.py)
   pass on corrected adapters, with relevant existing ParmEd readback and lifecycle
   documentation checks completed before closure.

## Dependencies and risks

Keep chemistry in ChemicalStates and mechanical assignments in MolecularMechanics.
Reuse existing PBC/unit operations rather than competing conversion or storage
rules. Numeric bond order alone loses qualitative chemistry; treating every
fractional order as aromatic invents chemistry. Converting a raw box to
lengths/angles can discard orientation relative to coordinates. These are
explicit design boundaries, not permission to weaken tests or normalize data
silently.

## Provenance

Baseline host: `nauta`, Linux; local execution on 2026-11-06, with receipt
timestamps continuing into 2026-11-07 UTC. Environment:
`molsyssuite@uibcdf_3.14`, Python 3.14.7, NumPy 2.4.6, ParmEd 4.3.1 and
OpenMM 8.6.1. MolSysMT uses working source, the existing pinned Viewer overlay
and published Pytest Receptor overlay. The plain provider observation uses
Conda-forge artifact `parmed-4.3.1-py314ha51126d_1.conda`, SHA-256
`641179b6820e55ce3c13507ebe5fc2b210e18d4e4f61f0339223e3f1e9bdbf08`;
the [artifact receipt](../../../.pytest_cache/pre1-review-20261106/providers/parmed-review/artifact-verification.json)
records official-hash/source verification and import origins.

Valid-baseline test source SHA-256 values, identifying the pre-repair tested
snapshot rather than the subsequently expanded regression modules:

- [Native export regression module](../../../tests/form/molsysmt_MolSys/test_to_parmed_Structure.py):
  `4b14fee7c7c073e757c88ca8877553f9574b7744aa64b3c1b2442e7cab935a60`.
- [OpenMM bridge regression module](../../../tests/form/openmm_Topology/test_to_parmed_Structure.py):
  `357723f3dce0e19e98bfd4b7ee3ac6782c4be8bd8dbea5a3727ccaadd257ba8a`.

## Resolution — 2026-11-06

Source `e270eda9b875cb273b3774ca84f23639de4417e4` introduces a direct native
exporter that receives the stable inventory and explicitly supplied chemical,
structure and mechanical domains. Native export no longer needs an intermediate
OpenMM topology. Requested structures and repeated/nonconsecutive positions,
coordinates, cells, known/unknown formal charges, atom aromaticity, representable
serial labels, groups/chains and independent bond semantics are preserved.
Topology alone does not recover attached domains.

Readback distinguishes an assigned partial charge from ParmEd's zero fallback,
retains box-only axes and an explicitly empty chain label. Unknown numeric bond
order, noncanonical integer serial spelling, incompatible bond-order slots,
unsupported structure-state associations and rotated/reflected raw cells have
explicit typed rejection and bounded preflight findings. Chemical state and
force-field assignments are not inferred. The audit remains nonexhaustive and
documents unassessed/dropped fields; no blanket lossless-export claim is made.

The native guard above has forty concrete cases, the OpenMM bridge guard six;
existing readback cases protect distinct atomic-number/force-field type, nullable
charges and independent connectivity. Root receiving with actual public ParmEd
4.3.1/Python 3.12/OpenMM 8.2/public support floors and the verified public
ParmEd 4.3.1/Python 3.14/OpenMM 8.6.1 payload passes **185 cases each**,
no omissions, native exits zero. Coordinate units are tested under changed PUW
output policies; cell-angle tolerance reflects existing documented PBC
quantization, not a relaxed orientation-preservation requirement.

The valid unchanged-production baseline has fifteen failures/two passes. Its
predecessor also contains twelve test-authoring import errors, explicitly
excluded from production findings. A plain smoke attempt tried to mutate a
read-only input box; its corrected probe copied input instead. All attempts,
source/public artifact hashes and scopes are retained in the
[portable receipt](../../../devtools/data/parmed_runtime_receiving_524_629_20261106.json).

Integrated conversion/descriptor/docs receiving passes 1,271; registered
scientific execution passes 97 for 64 nodes, no omissions. Scopes overlap.
The separate optional `parmed>=4.3.1` declaration in
`33a702bfa638464848a77c57c642627595c759ed` follows actual NumPy2 setter/import
failures of earlier releases; upgrading alone does not repair the host adapter.
This is source receiving, not whole-platform, all parameterized writers,
installed-artifact or molecular-simulation qualification. Public source delivery
and actual board closure are recorded separately.
