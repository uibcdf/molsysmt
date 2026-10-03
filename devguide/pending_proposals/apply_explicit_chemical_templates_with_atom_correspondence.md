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
2026-10-03. Representation normalization, native preparation-report attachment
and real consumer acceptance remain pending; this issue remains partial.

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
completeness, frame/state association and source-index ambiguity. Extending to a
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
frames, box, units and frame/state associations, and replace only the selected
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
54,437 atoms/one frame. Its unnamed ligand has 44 atoms/47 bonds. Native classical
recognition rejects partial declared connectivity. Public PDB-text/RDKit/native
conversion preserves counts but leaves unsupported order-zero bonds and is also
rejected. Both use `MSM-ERR-STRUCT-003`; the consumer audit is in
uibcdf/pharmacophoremt#22.

**Measured, 2026-10-03:** A separately downloaded RCSB 1QKU mmCIF input has
6,596 atoms, 1,343 groups and one frame under native conversion. It contains three
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
oxygen acceptor, permuted indices, multiple frames/states, nondefault units,
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
  coordinates, units, atom identity and frame/state associations.
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
atoms or geometry. Neither operation reconciles missing/conflicting edges.
Unknown template fields, dative/cut graphs, ambiguous references, and representations
requiring normalization cannot produce a compatible report. Supported bond-stereo
reference atoms follow remapped endpoint orientation and validated neighborhoods.

Source atom identity, all structures, units/box and frame/state associations are
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
- Complete fixed-state H placement separately in #300; no template-coordinate
  adoption is introduced as a shortcut.

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
residue coverage, native ChemicalStates, MolSys frame/state associations and named
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
