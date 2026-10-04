---
summary: Apply explicit chemical templates while preserving source atom correspondence and coordinates.
issue: uibcdf/molsysmt#298
status: partial
opened: 2026-10-02
closed:
verification: measured
area: [physchem, chemical-states, preparation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit chemical-template preparation

**Reported:** 2026-10-02, from uibcdf/pharmacophoremt#22.
**Status:** Bounded experimental public tools implemented and contract-tested on
2026-10-03, extended with explicit graph completion and a versioned native peptide
reference factory and declared-aromatic normalization on 2026-10-04. A bounded
observed 1QKU fragment and its explicit composition with prepared EST are
contract-tested. Consumer-reported isolated-ligand integration is
available. General polymer context/repair/mapping/reinsertion, other representation
normalization, native preparation-report attachment and complete receptor/biological
acceptance remain pending; this issue remains partial.

## What

Provide a reusable operation for applying an explicitly chosen chemical template
to existing atoms, after validating a caller-declared atom correspondence.
Chemical assignments remain in native `ChemicalStates`. The operation returns an
inspectable preparation report and preserves source identity and coordinates.
It is useful to PharmacophoreMT, DockingMT and other molecular consumers.

## How

### Owning tools and implemented boundary

Chemical interpretation and the preparation decision belong to `physchem`;
format decoding belongs to the existing `form` adapters, graph invariants to
`topology`, geometry/generation to `structure`/`build`, and stored assignments to
`ChemicalStates`. Reuse their public/native contracts. Do not create a second
chemical store, automatic repair in `convert`, or consumer-side RDKit inference.
Existing `build.editable`, basic `get`/`set`/`copy`/`extract`, the native chemical-
state codec and public property recognizers supply parts of the implementation;
the new tools provide a bounded template-application contract over those domains.

The implemented minimum has two independently useful public operations with the
same input/state/map contract: a read-only assessment and an application that
requires a compatible assessment.

```python
# Experimental public APIs; the caller supplies the curated template and map.
assessment = msm.physchem.assess_chemical_template(
    source, template=prepared_template,
    atom_correspondence=template_to_source_pairs,
    template_provenance=explicit_template_identity,
    chemical_state='reference', template_chemical_state='reference',
)
result = msm.physchem.apply_chemical_template(
    source,
    template=prepared_template,
    atom_correspondence=template_to_source_pairs,
    template_provenance=explicit_template_identity,
    chemical_state='reference',
    template_chemical_state='reference',
)
```

Use one isolated component/state in the first implementation. Require a complete,
explicit template accepted by a supported molecular form and an exhaustive,
bijective integer atom map of shape `(n_atoms, 2)`: first column template indices,
second column source indices, both zero-based in their respective full inputs.
One source atom cannot receive two template assignments. IDs and names do not
replace indices. A missing map is an error; automatic name/graph matching and
ambiguity resolution are separate future operations, not a hidden fallback.

The template does not need coordinates. Its authoritative chemical identity,
version/revision, source URI/checksum and caller-selected state are explicit
inputs. Their presence records a declaration; it does not independently establish
that a template is chemically correct. Resolve the supported state with the native
mechanism before interpreting any state-dependent property or selection.

### Phase-one scope and transaction

Phase one requires the same explicit atom set, including hydrogens, in source and
template. It neither adds atoms nor supplies donor-H geometry. A heavy-only source
cannot pass an exhaustive map to a 44-atom hydrogen-complete template. A separately
prepared heavy-only template is an explicit different input, with that hydrogen
policy recorded; missing hydrogens must not be silently declared present.

Require an isolated component and an explicit state; do not initially edit an
arbitrary subgraph of a protein/ligand complex. Consumers can extract a component
through MolSysMT and retain the full-source map. This bounds external bonds,
completeness, structure/state association and source-index ambiguity. Extending to a
whole complex must preserve unrelated components and cannot elevate incomplete
receptor chemistry to complete because its ligand was prepared.

Validate before applying anything:

- Compatible elements, isotopes where declared, atom counts, map bounds/uniqueness
  and coverage; disconnected, cut, missing or unmapped atoms are reported.
- Existing explicit connectivity and chemical assignments must agree with the
  template. An absent field may be filled; an explicit conflicting value fails.
  Unknown bond order is distinct from a declared single bond. Source evidence
  distinguishes explicit relationships from inferred ones.
- Treat Kekule/aromatic representations through provider-owned normalization,
  never a consumer-specific equality shortcut. Different encodings of a proven
  same aromatic state are not automatically chemical conflicts, and an unassessed
  aromatic state must not be labeled equivalent without an applicable method.
- Template stereochemistry, radical state, charges and bond relationships must be
  supported and explicit where the operation needs them. Do not guess neutral
  formal charges, derive protonation at a pH or overwrite conflicting stereo.
- In the first slice, do not add missing edges or overwrite inconsistent inferred
  edges. Report a graph needing reconciliation for a separate explicit preparation
  operation. Connectivity completeness is justified by validated template coverage,
  not by flipping a flag or by conversion success alone.

Always return a new native molecular system after successful preflight. Copy its
structure/topology domains, preserve atom order/IDs/membership, all coordinate
structures, box, units and structure/state associations, and replace only the selected
chemical state. No in-place option is needed in the first slice. Failure leaves
source and template unchanged. Use existing catalog-backed molecular diagnostics;
include the offending atom/bond and reason without swallowing scientific errors.

### Success and unresolved evidence

Implemented result fields:

| Field | Meaning |
| --- | --- |
| `molecular_system` | New native system, only on successful application |
| `report.schema` | Versioned provider-owned chemical-template report |
| `report.status` | `applied`; a failed operation does not report success |
| `report.method` | Named explicit-template method and version |
| `report.source` / `report.template` | Resolved states and original atom domains |
| `report.atom_correspondence` | Exact supplied map, detached and retained |
| `report.assigned_fields` | Per-atom/bond assignments and their template origin |
| `report.preserved_fields` | Explicit source fields checked and preserved |
| `report.coverage` | Atom/bond/hydrogen coverage and completeness justification |
| `report.template_provenance` | Original identity/version/source/checksum declaration |
| `report.software` | Original producer/provider versions |

The separate `assess_chemical_template` tool returns the detached report without
a prepared system and without mutation. Its status is `compatible`, `conflict` or
`unassessed`; it retains per-atom/bond issues and applicable catalog reason codes.
Malformed API arguments raise argument diagnostics; structurally valid but
insufficient/conflicting molecular inputs produce an unresolved assessment.
`apply_chemical_template` uses the same private assessment implementation and raises a catalog-backed
structural diagnostic with the detached report on either unresolved status. It
returns `molecular_system` plus an `applied` report only after successful assignment.
Reuse readiness diagnostics from #217/#218 when available. An unresolved report
must not be confused with a successful empty chemical result. Native provenance
attachment and implementation details require API review rather than placeholder
exports. Portable execution attribution follows `ACKREDIT_GUIDE.md`; template-data
provenance and executed-software/method credit remain distinguishable. Reading a
report does not repeat preparation or register another completed calculation.

## Why

The legacy ERalpha consumer used its own inference to recover ligand/receptor
chemistry. Native consumers need a declared preparation step with transferable
identity/evidence, instead of relying on conversion success or repairing chemistry
inside each workflow. This boundary also preserves future compute/backend choices:
first validate scientific behavior on small cases; accelerate a measured reusable
kernel only when warranted.

## What is measured and what is assumed

**Measured, 2026-10-02:** With MolSysMT source
`4d490427e38c5836be82472348fdf61934442bda`, the consumer's OpenMM PDB snapshot has
54,437 atoms/one structure. Its unnamed ligand has 44 atoms/47 bonds. Native classical
recognition rejects partial declared connectivity. Public PDB-text/RDKit/native
conversion preserves counts but leaves unsupported order-zero bonds and is also
rejected. Both use `MSM-ERR-STRUCT-003`; the consumer audit is in
uibcdf/pharmacophoremt#22.

**Measured, 2026-10-03:** A separately downloaded RCSB 1QKU mmCIF input has
6,596 atoms, 1,343 groups and one structure under native conversion. It contains three
20-heavy-atom EST instances. The selected native chain ID `D` is the ligand with
label asymmetry ID D (author chain A). The current CCD EST definition has 44 atoms
and 47 bonds and is exposed as a supported PDBx data container through MolSysMT.
Entry and current CCD heavy-atom names agree, including oxygens O3/O17.
Name agreement is candidate correspondence evidence; it does not prove a valid
chemical mapping. The old OpenMM snapshot instead names its oxygens O1/O2. The source has no observed ligand H
atoms, and CCD ideal/model H positions are not observed complex coordinates.

Reproduction from the PharmacophoreMT source checkout:

```python
import molsysmt as msm
source = msm.convert('tests/data/eralpha_rcsb/1qku.cif', to_form='molsysmt.MolSys')
ligand = msm.extract(source, selection='group_name == "EST" and chain_id == "D"')
ccd = msm.convert('tests/data/eralpha_rcsb/EST.cif',
                  to_form='mmcif.PdbxContainers.DataContainer')
print(msm.get(source, n_atoms=True, n_groups=True, n_structures=True))
print(msm.get(ligand, n_atoms=True))
print(ccd.getObj('chem_comp_atom').getRowCount())
```

**Contract-tested, 2026-10-03:** The new isolated-component implementation has
executed native/H5MSM controls with an independently known methanol OH donor and
oxygen acceptor, permuted indices, multiple structures/states, nondefault units,
conflict/unresolved failures, stereo-reference remapping and conservative named-
analysis invalidation. The tutorial separately executes a public builder/RDKit
template workflow. The real EST provider control below supplies a prepared native
ligand; no complete ERalpha consumer workflow, biological validation or performance
measurement is claimed.

**Contract-tested and independent chemistry/pose controls, 2026-10-03:**
`tests/physchem/test_chemical_template_est.py` applies an explicitly curated native
H5MSM template to EST from 1QKU, native chain D. The returned ligand preserves all
20 heavy atoms, 23 bonds and exact deposited coordinates/units. Recognition returns
the known six-atom aromatic ring and O3/O17 acceptors. H5MSM roundtrip preserves the
chemical values and pose. Its 24 stored H counts do not create explicit donor-H
pairs. Five canonical-descriptor CIP centers agree with independent assignment
from the 3D pose: C8 R, C9 S, C13 S, C14 S and C17 S.

The pinned CCD atom-level flag for C8 is S. The fixture explicitly selects the
CACTVS 3.341 canonical SMILES and records this disagreement; it does not substitute
the atom flag or infer its cause. The curation verifies charge/aromatic declarations,
the full heavy graph and H counts independently against CCD fields/bonds. Exact
source bytes, checksums, source atom indices and declared map are committed under
`tests/physchem/data/chemical_templates/`. The fixture-specific generator is
`devtools/scripts/curate_est_template_fixture.py`; it refuses different revisions
and ambiguous graph correspondence. This is a provider transfer control, not
consumer end-to-end acceptance or general automatic CCD interpretation.

## What was refuted

- Explicit hydrogens and plausible coordinates do not establish chemical readiness.
- A `complete` flag or public format roundtrip does not establish supported orders.
- Elemental composition alone does not establish identity or stereochemistry.
- Mapping atoms by index/order alone, or reusing ideal-template coordinates, does
  not preserve a deposited ligand pose.
- A source declaring stereo or implicit hydrogen counts does not supply explicit
  donor-H coordinates. Generating those belongs to a separate provider operation.
- The ModelServer SDF acquired for this case has an unversioned CTAB counts line;
  native SDF conversion at source `e9f135c2962aeefdb08135a7bc567d2d08bf27c5`
  rejects it. Do not alter the downloaded bytes or call it ready just because the
  service labels the response SDF. CCD chemistry needs a supported interpretation
  path; the structural mmCIF reader does not assemble a molecular system from a
  CCD-only file without `atom_site`.

## Scope and exclusions

Minimum explicit-template contract, source/evidence curation and first isolated-
component implementation. No automatic graph matching, state enumeration,
hydrogen/coordinate generation, receptor-wide coverage, pKa inference, force-field
charges, full CCD form support, or new compiled/GPU/distributed backend. Introduce
independently closable follow-up issues when an excluded capability is required.

## Acceptance criteria

- Independently documented/tested public provider tool with supported input/result,
  state, map, completeness, conflict and failure contracts.
- A permuted valid atom map transfers chemistry while preserving exact source
  coordinates, units, atom identity and structure/state associations.
- Duplicate/out-of-range/partial maps, wrong elements, graph/charge/stereo conflicts,
  unsupported chemistry, absent hydrogen correspondence and cut/external bonds fail
  before mutation. Nondefault/multiple states and independent input copies are tested.
- A complete supported template and source assignment yield recognized expected
  chemistry against an independent reference. Filling missing fields cannot be
  validated merely by comparing the output to itself.
- Reports retain original template provenance and executed provider attribution;
  absent/failing optional attribution cannot replace the science error or outcome.
- Update docstrings, user foundations/toolbox/cookbook and the relevant course
  lessons when a public implementation is delivered. The bounded experimental
  implementation does not establish consumer-specific scientific acceptance.

## Implemented slice and remaining work — 2026-10-03

The two exported tools share a coordinate-independent preflight and return schema
`molsysmt.chemical_template@1`. Argument normalization occurs at the public
ArgDigest boundary; exhaustive axis coverage and scientific scope are checked by
the private preparation operation. Application returns a new native MolSys and
only fills absent supported assignments in the chosen chemical state. It reuses
the compiled connectivity primitive instead of adding a separate graph engine.

The `explicit_atoms` policy requires zero stored virtual H counts. A separately
declared `stored_counts` template permits a heavy-only input without inventing H
atoms or geometry. The initial/default policy reconciles neither missing nor
conflicting edges. The explicit completion extension below adds absent declared
template edges; conflicting source relationships remain unsupported.
Unknown template fields, dative/cut graphs, ambiguous references, and representations
requiring normalization cannot produce a compatible report. Supported bond-stereo
reference atoms follow remapped endpoint orientation and validated neighborhoods.

Source atom identity, all structures, units/box and structure/state associations are
preserved on the returned copy. Chemical changes invalidate evaluated observations
in its named analyses through the existing native lifecycle; input snapshots remain
unchanged. An identical application without chemical changes keeps its analyses.
The returned report exposes invalidated analysis names.

The report retains declared template provenance, producer version, elementary-
charge units and detached portable software attribution. Ackredit absence/failure
does not change science; real Ackredit tests exercise nested scopes, reused items
and failed preparation without credits. A fresh subprocess denies RDKit/Ackredit
imports for native preparation. Chemical values persist through public H5MSM 0.5
conversion, but the report is not embedded in native objects or that format.

Remaining work is explicit:

- Review the bounded API with the real PharmacophoreMT/DockingMT consumer inputs
  and a separately accepted atom correspondence. Synthetic methanol and the pinned
  EST provider controls do not certify the complete ERalpha consumer workflow.
- Establish a provider-owned representation-normalization method before accepting
  differing aromatic/Kekule or stereo-reference representations as equivalent.
- Decide the native/versioned preparation-provenance attachment contract without
  competing chemical stores; retain the detached report externally meanwhile.
- Compose the separately delivered fixed-state H placement under resolved #300;
  no template-coordinate adoption is introduced as a shortcut. Polymer H geometry
  and consumer receptor acceptance remain distinct from the ligand controls.

Public lifecycle documentation covers Foundations, the paired Toolbox/Cookbook
contracts, API autosummary/stability registry and the narrative/function inventory
of course Module 12. Existing notebook code/outputs remain unchanged.

## Dependencies and risks

Related: #217 (ligand readiness), #218 (receptor coverage), #223 (atom identity),
#254 (independent chemical states), and consumer uibcdf/pharmacophoremt#22.
Current source curation resolves the new input's origin; chemical preparation and
an independently accepted atom map remain separate gates.

Hydrogen addition is tracked independently in [#300](https://github.com/uibcdf/molsysmt/issues/300). Template assessment/application assigns chemistry to existing corresponding atoms; it does not generate missing H atoms or their coordinates. For a heavy-only deposited ligand, prepare and assess an explicitly compatible heavy-only template/state first, then use the separate fixed-state hydrogen operation when its contract is implemented and validated. The hydrogen operation can also consume chemistry prepared through other supported routes; this proposal is not its universal dependency.

## Validation evidence — 2026-10-03

The controlled source run completed **118 passed in 49.03 s**, including public
doctests, the new template module and regression contracts for stored readiness,
residue coverage, native ChemicalStates, MolSys structure/state associations and named
interaction lifecycle:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/physchem/test_chemical_template.py \
  tests/physchem/test_get_chemical_readiness.py \
  tests/build/test_get_residue_chemical_coverage.py \
  tests/native/test_chemical_states.py \
  tests/native/test_molsys_chemical_state_association.py \
  tests/native/test_molsys_interactions.py --doctest-modules \
  molsysmt/physchem/assess_chemical_template.py \
  molsysmt/physchem/apply_chemical_template.py
```

The ArgDigest path is an ephemeral checkout of the published 0.13.0 release at
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`, used because the installed editable
snapshot is below the public floor. The two public boundaries retain the same
conditional compatibility check for uibcdf/argdigest#17 as the existing readiness
tool; retire it when the public floor includes that fix. Native preparation also
passes in a fresh subprocess with RDKit/Ackredit imports denied. The declared
benzene control independently recognizes one six-carbon aromatic ring; a same-
graph alternating-order representation remains unassessed until normalization.

Both public tutorial examples executed successfully. The parallel Sphinx HTML
build completed successfully; existing course/navigation warnings remain, with
no warning for the new template pages or API entries. Two existing pandas
FutureWarnings originate from the H5MSM chemical-state reader. Ruff over MolSysMT
and the new tests, dependency imports/contracts, docstrings, API stability, the
maintained course validator and developer-guide/index validators pass.

This is source-checkout evidence on Python 3.13.14 under the temporary migration
route uibcdf/molsysmt#237 (maintainer-owned, review 2026-12-31). It neither certifies
the required Python 3.14 routine route nor a published installation/release.

## Provenance

Local Linux source-checkout verification, Python 3.13.14, 2026-10-02/03.
Initial snapshot: MolSysMT source `4d490427e38c5836be82472348fdf61934442bda`;
format probes: clean source `e9f135c2962aeefdb08135a7bc567d2d08bf27c5`;
PyUnitWizard source `2ffe1885675f47c76af03c08e51bc889a5e99a05`, existing scientific
dependencies. RCSB sources, checksums and exact selections are retained in the
consumer's `tests/data/eralpha_rcsb/manifest.json`. No published installation or
hosted compatibility matrix is claimed.

## Real EST validation checkpoint — 2026-10-03

The pinned 1QKU/EST fixtures and two public real-input controls are committed with
an offline reproducible curation script. Recuration from the committed compressed
entry and verbatim CCD succeeds; the committed checksum manifest remains the
identity of the original artifact, not a promise of byte-identical future HDF5
files. Native template application consumes its H5MSM chemical state independently
of the RDKit used during fixture production. The Cookbook records both the accepted
stereo source and the limit on hydrogen geometry.

The combined regression completed **98 passed in 34.94 s**, covering template
assessment/application, the real EST pose and stereo controls, CIP recognition,
interaction attribution and the shared optional-attribution boundary:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/test_ackredit.py tests/physchem/test_chemical_template_est.py \
  tests/physchem/test_chemical_template.py tests/physchem/test_get_cip_stereochemistry.py \
  tests/interactions/test_scientific_attribution.py
```

This run found and resolved #305: promotion of optional Ackredit warnings could
otherwise discard completed preparation or mask a scientific exception. Its guard
requires actual catalog events and unchanged scientific outcomes under strict
warning filters. Two existing pandas FutureWarnings remain in the H5MSM state
reader. Ruff, dependency import/contract checks, docstring validation, course
structure and developer-guide/index validation pass. The Sphinx HTML build exits
0 with existing documentation diagnostics, including docutils errors in unrelated
legacy pages; this is not a globally clean documentation gate. The debt is recorded
in [the Sphinx baseline report](../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md).
Neither template page emits a warning. These are Python 3.13 source-checkout observations under #237, not a full
supported-interpreter matrix or consumer biological acceptance.

## Consumer receptor continuation — 2026-10-04

**Consumer-reported:** uibcdf/pharmacophoremt#22 and the latest feedback on #298
identify a separate remaining polymer boundary. The observed 1QKU label-chain A
receptor has 1,990 atoms/250 groups: 247 heavy-assessed groups and three incomplete
SER301/LYS302/LYS303 groups. Its 0.4/0.5/0.6 nm whole-residue ligand shells contain
12/19/23 groups without reported heavy-atom gaps, but formal charges/aromaticity,
bond orders, indexed H and complete polymer connectivity remain unavailable.
This is source-reported evidence; this continuation has not independently rerun
the consumer audit. Earlier native isolated-ligand template and H delivery does
not certify receptor readiness or turn failed detectors into empty observations.

Next implementation slice: reusable residue/polymer template assignment with
explicit terminal/protonation/HIS choices, mapped source atoms, declared peptide
and other inter-residue links, conflicts/unsupported portions and actual dataset
provenance. Extend the general template machinery and ChemicalStates ownership;
do not create a residue-only chemical store or duplicate chemistry downstream.
Heavy repair, fixed-state H geometry, environmental orientation and reinserting
prepared components are distinct operations. Qualify analytical peptide/terminal
controls before the observed receptor; preserve coordinates/identities and
transactional failure. Scoped completeness must not certify unevaluated groups
or unprepared full-system components used by full-graph recognition.

DockingMT's separate uibcdf/dockingmt#41 feedback reported a fixed-state H
rejection for template-prepared original 181L BNZ. Independent provider
reproduction on 2026-10-04 shows that all six bond aromatic flags and fractional
orders of 1.5 are already assigned by the template. The actual defect is an
unconditional integer bond_order column requirement, tracked by
resolved uibcdf/molsysmt#318. Positive provider tests and a public DockingMT
preparation probe now pass with the original six-carbon pose preserved. No new
perception/attachment API or guessed Kekule orders were required. Detached
perception under resolved #314 remains independent; this is not complete docking
workflow acceptance.

## Explicit connectivity completion — 2026-10-04

**Implemented and contract-tested:** Both experimental public tools now accept
keyword-only `connectivity_policy`. `require_same_graph` remains the default and
preserves all previous positional arguments/defaults. Explicit
`complete_from_template` adds only missing declared covalent edges from a complete
connected template with an exhaustive atom map. The source can contain disconnected
fragments, but cannot claim complete connectivity when its edges differ. Unexpected
source edges, known chemical conflicts, incomplete/disconnected templates and
unsupported representations still block application before changing either input.

This is a general prerequisite for residue/polymer preparation, not a residue
template generator. Legacy standard-residue references primarily supply heavy
geometry/connectivity, not complete charges/orders/aromaticity and explicit
terminal/HIS/protonation states. The separate reference factory described below
supplies a versioned chemical dataset and an explicit assembly policy. No residue
chemistry is guessed by connectivity completion.

The operation reuses native bond-table normalization and compiled connectivity
reconstruction. New edges have `user_defined` evidence, backed by the caller's
detached template declaration; existing source edge evidence stays intact.
Assessment records original template bond indices and mapped source pairs.
Application adds final bond indices and an int64 `(n_original_bonds, 2)`
`source_bond_correspondence`, because canonical insertion can reorder existing
bonds. The unchanged-graph route constructs an identity map without an extra
edge lookup dictionary. This is an implementation observation, not a benchmark.

Only the chosen state's graph/assignments/components change. Native component
indices/IDs are rebuilt and component names/types remain unknown; stable atom
order/IDs, group/molecule/chain/entity inventory, unselected states, structures,
units/box/time and structure/state associations are preserved. Named analyses on the
returned copy are invalidated through the existing ChemicalStates lifecycle.
Repeated preparation without changes preserves attached analyses. The report stays
detached; chemical fields and component membership persist through public H5MSM 0.5.

**Analytical and contract controls:** A caller-declared zwitterionic glycylglycine
heavy template specifies C4H8N2O3, ammonium/carboxylate terminal choices and one
peptide C–N bond. Completing that absent bond joins two source fragments, retains
both GLY groups and all coordinate values, and transfers exactly the declared
charges/H counts. Stored counts do not generate H atoms. Synthetic coordinates
are preservation controls, not physically optimized peptide conformations.
Additional controls cover a source without edges, a nonreference target state,
permuted axes, coordinate-free native/H5MSM forms, newly added trans-2-butene
double-bond stereo references and transactional conflict failures. A fresh
subprocess denies RDKit/Ackredit imports while successfully completing a native
template graph. No environmental protonation, conformer or performance claim
is made.

The combined regression completed **96 passed in 21.55 s**, with two existing
pandas FutureWarnings in the H5MSM ChemicalStates reader:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/physchem/test_chemical_template_connectivity.py \
  tests/physchem/test_chemical_template.py tests/physchem/test_chemical_template_est.py \
  tests/native/test_chemical_states.py \
  tests/native/test_molsys_chemical_state_association.py \
  tests/native/test_molsys_interactions.py --doctest-modules \
  molsysmt/physchem/assess_chemical_template.py \
  molsysmt/physchem/apply_chemical_template.py
```

This is Python 3.13.14 source-checkout evidence under the bounded #237 migration
route, with the same released ArgDigest 0.13.0 override recorded above. It is not
required Python 3.14 matrix qualification or immutable installed delivery.

All three Python blocks in the updated Toolbox tutorial execute successfully in
sequence. Foundations, Cookbook and course Module 12 explain explicit completion,
component rebuilding and bond remapping. Docstrings, the maintained course
validator, public API registry/signature checks, dependency imports, developer-guide
validation/indexes and repository-wide Ruff check/format checks pass. Sphinx HTML
build exits 0 with existing course/navigation/native-class reference warnings;
the chemical-template tutorial and API entries emit no warnings. This is not a
globally clean documentation gate; the tracked baseline debt remains unchanged.

**Consumer-reported checkpoint:** Feedback on #298 records public isolated-ligand
integration from PharmacophoreMT and DockingMT. Those receipts qualify template
transfer for their declared inputs; they do not complete the requested receptor
scope. No sibling source was changed during this provider extension.

**Next:** Apply the versioned reference factory through an explicit, accepted map
and supported observed polymer context, then exercise the requested receptor.
Preserve unsupported/heavy-incomplete portions as unassessed. Partial template
preparation must not certify unrelated full-system chemistry.

## Native peptide chemical references — 2026-10-04

**Implemented and contract-tested:** The experimental public
`physchem.get_peptide_chemical_template(residue_names, n_terminal_state,
c_terminal_state, *, disulfide_group_pairs=None)` constructs a coordinate-free
native `MolSys` reference for one linear peptide chain. Its detached result contains
`template`, `template_provenance` and a typed `molsysmt.peptide_template@1` report.
It is a factory, not an observed-system selector or preparation command. Apply the
result through the existing form-agnostic assessment/application tools with a
caller-declared exhaustive atom map.

The ordered names select 27 exact chemical states: ALA, ARG, ASN, ASP, ASH, CYS,
CYM, CYX, GLN, GLU, GLH, GLY, HID, HIE, HIP, ILE, LEU, LYS, LYN, MET, PHE, PRO,
SER, THR, TRP, TYR and VAL. Ambiguous HIS fails; no pH inference or implicit alias
selection occurs. N-terminal ammonium/amine and C-terminal
carboxylate/carboxylic_acid are mandatory choices. Every CYX must participate in
exactly one explicitly declared intrachain disulfide group-index pair. CYS/CYM
are not implicitly converted. The heavy graph includes terminal OXT; a missing
observed OXT needs a separate repair, not a guessed atom correspondence.

The versioned `molsysmt.peptide_fragments@1` dataset is curated from Meeko's
`meeko/data/residue_chem_templates.json` at commit
`1eac18bd6d1111f35f9f1abaa8af502c2668d054`, source SHA-256
`535dc75a2cc5db579a3114090c9ab1273892c556cb7cc1a850ce2c4cd57c7cde`.
The original source bytes are retained as a deterministic compressed snapshot;
the original LGPL 2.1 license and a data README accompany the curated library.
No sibling source was changed. The offline generator uses RDKit 2025.09.5 and
records that original producer version, independently of a later runtime.
The normal native construction path imports neither Meeko nor RDKit and adds
no optional dependency floor. Existing package-data rules include the assets.

The generator retains heavy-atom names, exact charge assignments, aromaticity and
real hydrogen inventories. Virtual hydrogens at declared link ports are excluded
before polymer assembly. CYM explicitly selects the upstream CYX- fragment.
Aromatic orders remain 1.5; no integer Kekule assignment is guessed. Source
conjugation flags are curated, while backbone carbonyl and assembled peptide/
terminal links follow the declared assembly model. The reader verifies both the
schema and formal-charge unit declaration (`elementary_charge`); native charges
remain integer multiples of that unit under non-default session unit policies.

The implementation reuses `ChemicalStates`, native bond-table normalization and
compiled connectivity reconstruction. Stored H counts do not create indexed
hydrogen atoms or geometry. Atom/group IDs are strings derived from template
indices; they are synthetic identities, not identities of an observed receptor.
Provenance distinguishes the original source hash, curated asset hash and graph-
definition digest. These are not H5MSM byte hashes or source-system authentication.
Optional Ackredit records the executed MolSysMT software and the referenced data
only after successful construction; it does not claim execution of Meeko/RDKit.

**Analytical controls:** Glycylglycine has the declared C4H8N2O3 inventory with
ammonium/carboxylate termini. Four terminal combinations, proline's secondary
amine, C8H13N3O4S2 for a declared CYX–GLY–CYX disulfide, all 26 non-CYX states
as monomers and internal residues, and histidine ring/H-count variants are covered.
Independent RDKit sanitization recomputes valence/conjugation rather than trusting
cached conversion flags. A mapped glycylglycine source receives the peptide bond
and exact assignments while preserving its coordinates, box, time and IDs.
Coordinate-free and prepared native results round trip through public H5MSM 0.5.
Controls reject ambiguous states, invalid ports, missing OXT and incompatible maps.
Fresh-process native construction succeeds with RDKit, Meeko and Ackredit imports
denied. Dataset mutation cannot alter the cached reference library.

The combined regression completed **175 passed in 32.39 s**, with two existing
pandas FutureWarnings in the H5MSM ChemicalStates reader:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/physchem/test_get_peptide_chemical_template.py \
  tests/physchem/test_chemical_template.py \
  tests/physchem/test_chemical_template_connectivity.py \
  tests/physchem/test_chemical_template_est.py \
  tests/native/test_chemical_states.py \
  tests/native/test_molsys_chemical_state_association.py \
  tests/native/test_molsys_interactions.py --doctest-modules \
  molsysmt/physchem/get_peptide_chemical_template.py \
  molsysmt/physchem/assess_chemical_template.py \
  molsysmt/physchem/apply_chemical_template.py
```

A subsequent boundary correction canonicalizes already valid disulfide inputs in
the assembler, so trusted delegation also supports `None` and list inputs. Its
focused regression completed **17 passed, 63 deselected in 4.28 s** with the new
module and `-k 'trusted_delegation or declared_disulfide or invalid_ports'`.
Evidence uses Python 3.13.14 under the bounded uibcdf/molsysmt#237 migration route,
the released ArgDigest 0.13.0 override recorded above and RDKit 2025.09.5 where
explicitly used as an oracle. It does not qualify Python 3.14, an installed release,
biological receptor preparation or runtime performance.

Foundations, Toolbox, Cookbook, API entries and course Module 12 describe the
factory and its limits. All five tutorial Python blocks execute in sequence.
Docstrings, maintained course, dependency imports, public API registry/signature
checks and repository-wide Ruff check/format checks pass. Sphinx HTML exits 0 with
existing course/navigation/native-class reference warnings and no warning for the
new factory or chemical-template tutorial; this is not a globally clean docs gate.

**Remaining acceptance:** Stereochemistry is deliberately unspecified, including
L/D and cis/trans choices. The factory does not certify L residues and cannot
overwrite known source stereo with missing declarations. Modified residues, caps,
cyclic backbones, multiple chains and arbitrary crosslinks are outside this
factory. Observed context selection, missing-heavy/OXT repair, hydrogen placement,
correspondence, reinsertion, scoped full-system chemistry and native report
attachment still need acceptance on the requested receptor. uibcdf/molsysmt#298
remains partial and open.

**Hosted checkpoint:** Commit `9615bf1fe96e0ea6922b0cdc2365d25223d5a701`
passed bundled-data, Ruff, developer-guide, MolSysSuite-policy and Conda-governance
controls. Its smoke job failed before compilation/tests because Rustup collided
with an existing Clippy binary. The separate source-build provisioning defect is
tracked in uibcdf/molsysmt#319; local chemical evidence above remains applicable,
but this original hosted run provides no smoke acceptance.

The provisioning fix at `800477575291124f6421f49e2fb9f15cde7d81d2` then passed
hosted smoke installation/import/contracts/tests and its five applicable
administrative controls. No peptide-source behavior changed between these commits;
the local chemical results remain applicable. This clears the smoke failure,
not the remaining observed-receptor or full-matrix acceptance.


## Observed 1QKU fragment checkpoint — 2026-10-04

**Implemented and contract-tested:** the separately owned
`physchem.normalize_aromatic_bond_orders()` changes only the representation of
bonds already declared aromatic. It preserves atom assignments, other states,
pose/units and connectivity completeness, returns original orders in a detached
report and invalidates named interactions only on a changed output copy.
It does not perceive aromaticity, validate valence or normalize general resonance.
Native MolSys, Topology, ChemicalStates and ChemicalStatesDict parity is tested.

The pinned fixture's label-chain A receptor has 250 residues. The first three
(SER301, LYS302, LYS303) lack heavy atoms. An explicitly bounded contiguous
304–550 scenario has 247 residues, 1,975 heavy atoms and 2,013 existing edges.
The caller chooses HIE for every HIS, ammonium at the artificial 304 N-terminal
cut, and carboxylate at the observed 550 terminal OXT. These are declared scenario
choices, not environmental protonation or a full receptor repair.

Raw assessment found 167 incompatible aromatic representations; name-preserving
mapping also exposes opposite single/double drawings at the eleven ARG terminal
nitrogen pairs. Normalization canonicalizes only those already aromatic bonds.
The caller explicitly exchanges template NH1/NH2 correspondence within those ARG
groups to match equivalent nitrogens in the deposited drawing. No source atom is
renamed/moved and no automatic matching is introduced. With that exhaustive map,
the default require_same_graph policy is compatible and adds no bonds.

The prepared fragment retains its original atoms and pose, has 31 recognized
aromatic rings, and passes independent SMARTS-site controls: backbone amide N and
cationic guanidinium N are not acceptors, whereas backbone carbonyl O are.
Elemental N/O recognition is deliberately broader and must not be treated as this
chemical validation. The separate fixed-state build operation adds 2,028 H with
RDKit, leaving all 1,975 heavy-atom positions and IDs unchanged; it reports dropped
B-factors under intersection policy. Both heavy-only and H-added chemical states
and coordinates survive public H5MSM round trips.

The aromatic NH implicit-H permission bug discovered in this composition was
fixed at the native/RDKit converter boundary in uibcdf/molsysmt#320. The strict H
preflight remains unchanged. Generated H remain local modeled coordinates;
stereo, environmental refinement and consumer biological acceptance are excluded.
Source atom-index maps remain distinct from string residue/atom IDs.

Evidence: `tests/physchem/test_chemical_template_receptor.py` and
`tests/physchem/test_normalize_aromatic_bond_orders.py`; together with affected
factory/template/converter/H contracts and public doctests, 234 tests passed in
61.38 s on Python 3.13.14 with released ArgDigest 0.13.0 and RDKit 2025.09.5.
The exact command and warning accounting are retained in the #320 archived record.
This is contract evidence, not a performance or biological benchmark.

Remaining: repair/explain the three excluded residues, general polymer context
and boundary mapping, general representation/stereo reconciliation, full-system
chemical reinsertion (related atom-projection identity concerns in uibcdf/molsysmt#223;
that issue does not supply a chemical reinsertion API), report attachment/persistence and
PharmacophoreMT's complete receptor/biological acceptance. Keep #298 partial.

## Native repair boundary checkpoint — 2026-10-04

The full label-chain A heavy-only input has 1,990 observed atoms. Native bounded
repair can add SER301 OG as an initial local-template estimate, producing 1,991.
LYS302 and LYS303 retain their four missing side-chain atoms each, with explicit
unassessed diagnostics. Their rotamers and local environment are not validated;
a complete inventory was not accepted as evidence of a correct pose. The old
unconditional path and its short LYS303 CB-CG bond motivated uibcdf/molsysmt#322.
The bounded 304–550 preparation above remains unchanged and deliberately excludes
all three residues; this checkpoint does not claim preparation of the full chain.

The operation also exposed loss of atom chemical assignments, state metadata and
named analyses in native atom repair and terminal-group rebuilding, corrected
under uibcdf/molsysmt#321. These native operations preserve existing assignments,
IDs and pose, leave added fields unknown, mark connectivity partial, and remap
named analyses while clearing occurrences and evaluated coverage. The heavy-atom
tool's strict attribute policy rejects unsupported B-factor/force-field parameter
loss. Chemical assessment/application and interaction recalculation remain
explicit subsequent steps. Geometry placement does not assign a complete state.

Remaining work is still full-context chemical preparation and correspondence,
validated handling of the lysine gaps, full-system chemistry reinsertion,
report attachment/persistence and consumer biological acceptance. #223 covers
loss-aware PDBQT atom projection, not a general chemistry reinsertion operation.
Keep #298 partial and do not reinterpret that issue's scope as this missing API.

## Prepared interface composition checkpoint — 2026-10-04

**Contract-tested:** reuse public `msm.merge` to compose the separately prepared
304–550 receptor fragment and EST after fixed-state H addition. This distinct
analysis system has 4,047 atoms, 4,088 bonds and 32 aromatic rings. The receptor
occupies indices 0–4,002; EST occupies 4,003–4,046. All 1,995 observed heavy-atom
positions and their IDs remain unchanged. The original 6,596-atom source stays
chemically partial and unmodified. This does not implement full-source chemical
reinsertion or assess excluded receptor residues.

The declared source map retains the original deposited atom indices for 1,975
receptor and 20 EST atoms, with `-1` for 2,028 receptor H and 24 ligand H. IDs
retained across independent expansions may repeat; they are not an index map.
Declare the inspected map using the public `InteractionsDict` conversion boundary,
with `source_n_atoms=6596` and `source_id='rcsb:1QKU:deposited-atom-order'`.
Typed validation checks the map's bounds and uniqueness of known source indices;
the declaration does not authenticate the source. Local participant axes,
producer software and evaluated coverage stay unchanged.

Public full-graph chemical recognizers can assess the included declared graph,
then limit geometric detection to the explicit receptor/EST interface. Native
and H5MSM file inputs are tested with `selection_mode='between'`, `pbc=False`
and repeated structure selection `[0, 0]`, deduplicated to evaluated structure 0.
The selected definitions give these geometry checkpoints:

| Named analysis | Method / profile | Occurrences |
| --- | --- | ---: |
| hydrophobic | `atom_pair_distance` / default chemical profile | 12 |
| hbonds | `donor_acceptor_distance_angle` / `smarts_donor_acceptor` | 0 |
| pi_pi | `plane_angle_intersection` / `smarts_5_6` | 0 |

Hydrophobic pair distances are independently recalculated from coordinates and
checked against the 0.45 nm cutoff and stored measures. Ligand `incident` queries
retain every interface occurrence, `internal` yields none, and explicit
`between(..., exclusive=True)` queries agree. Both zero-result analyses retain
evaluated-empty structure coverage. These counts do not establish biological
absence, method parity or a validated conformer. Generated H have only local
geometry, with no environment optimization. Independent site/coordinate inspection
found nearby donor–acceptor pairs failing the H-angle criterion; future explicit
environment-aware refinement is recorded in
[uibcdf/molsysmt#323](refine_fixed_state_hydrogen_geometry_in_an_explicit_molecular_environment.md).

Public H5MSM 0.5 roundtrip retains the composed system and all three named
analyses, occurrence indices, participant arrays, declared source maps, evaluated
coverage, original producer versions, attribution, parameters, measure units and
values. The preparation reports remain detached sidecars; merging does not attach
their template-specific provenance to MolSys or H5MSM. Source chemical completeness
cannot be elevated by preparing only this selected graph.

Durable evidence: `tests/physchem/test_chemical_template_receptor.py`. Executed:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
    tests/physchem/test_chemical_template_receptor.py
```

The expanded composition checkpoint passed six tests in 34.36 s, with
one pre-existing pandas H5MSM reader future warning. These are contract controls,
not a memory/timing benchmark or consumer biological acceptance. Linux local
environment, Python 3.13.14 under the bounded #237 exception, released ArgDigest
0.13.0, NumPy 2.4.6, pandas 2.3.3 and RDKit 2025.09.5; base source
`879c13894fbea7c09dd6b3c62f4ec458e61c1780` plus this checkpoint's test/doc changes.
The public recipe was independently executed through its query and named H5MSM
roundtrip. Ruff checks and formatting, developer-guide validation, course structure
and the API stability registry passed. The Sphinx HTML build exited successfully;
it retains the pre-existing course label and MolSys API-document warnings, without
a new prepared-interface reference warning. The public recipe, tool guide, MolSys
foundation and Module 12 now explain the
new analysis axis and scope. No new runtime API was needed for this composition.

Remaining: general polymer context and boundary mapping, supported handling of
the excluded lysine gaps, general representation/stereo reconciliation, full-system
chemistry reinsertion, native preparation-report attachment/persistence, and
consumer complete receptor/biological acceptance. Keep #298 partial. The future
refinement proposal is not a silent prerequisite or a claim that minimization
has already run.
