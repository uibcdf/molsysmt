---
summary: Expose reusable fixed-state hydrogen-bond site directions through public geometry tools.
issue: uibcdf/molsysmt#375
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [structure, interactions, physchem, pbc, api]
guard: tests/interactions/hbonds/test_get_hbond_site_directions.py
normative: devguide/hbond_site_directions.md
blocked_by: []
supersedes: []
---

# Fixed-state hydrogen-bond site directions

**Reported:** 2026-10-10, provider request from uibcdf/pharmacophoremt#41.
**Status:** Partial delivery: general directed vectors and bounded fixed-state donor/carbonyl/pyridine/nitrile directions are implemented in sources. Broader acceptor coverage remains pending; installed qualification and consumer adoption are separate.

## What

Provide general directed atom-pair geometry and compose it with fixed-state
hydrogen-bond site recognition. Donor-H directions derive from indexed observed
atoms. Acceptor directions require an explicitly named chemical/local-geometry
model with multiplicity and unsupported/undefined outcomes; they are not supplied
by the existing chemical inventory.

## How

Provider source inspected at `072aa9bdbfb9299f7e3256f9b27f6aae8ea52629` offers:

| Existing piece | Reuse | Missing contract |
|---|---|---|
| `physchem.get_hbond_sites` at the inspected checkpoint | Declared-state donor-H pairs and acceptor indices with rule/evidence. | Its contract explicitly excludes geometric directions. |
| `basic.get` | Form-agnostic coordinates, box and source axes. | Coordinate access does not define a directed-pair result or undefined-vector policy. |
| `structure.get_distances`, `get_angles`, `get_least_squares_plane` | General unit-aware scalar geometry and fitted planes. | Distances omit direction; a plane normal is not a universal lone-pair model. |
| `pbc.wrap_to_mic` | Reconstruction/wrapping of covalent components under its explicit policy. | Moving a component is not an immutable atom-pair displacement query. |
| Existing Rust MIC primitives and private periodic reconstruction helpers | Candidate calculation reuse after reviewing matching conventions. | Their internal functions are not a public form/unit/identity/image contract. |

The later namespace migration places this site's public recognition tool under
`interactions.hbonds`; the table above retains the inspected source identity.

The inspected public exports provide no directed atom-pair displacement operation
covering the consumer contract. Public geometry belongs in `structure`; periodic
image conventions/reconstruction belong in `pbc`; hydrogen-bond-specific recognition
and direction interpretation belong in `interactions.hbonds`. Consumers should compose these owners, retaining chemical
criteria locally only when genuinely pharmacophore-specific. Measure workloads
before adding new Rust routines rather than duplicating existing primitives.

Define ordered pairs and displacement sign, structure-axis order, length units,
dimensionless normalized directions, finite/zero-length handling and source maps.
For PBC, return the actually used image under the shared row-vector box convention
with an explicit reference participant. Test the selected MIC behavior, including
triclinic cells and ties; do not silently reconstruct images from a scalar distance.
Large structure selections require bounded chunked execution rather than dense
all-pairs materialization.

Then define fixed-state site geometry using recognized donor-H pairs, an explicit
acceptor model and a coherent state/structure association. Preserve directional
site multiplicity and atom correspondence. Unsupported chemistry or degenerate
geometry must remain unassessed or fail according to a documented policy; an
arbitrary default direction cannot masquerade as a calculated lone pair.

## Why

The consumer reports local donor-H subtraction and a legacy acceptor projection
from the first bonded neighbor, with a fallback axis when no neighbor exists.
That historical projection is a hypothesis heuristic, not an established general
lone-pair model. A shared molecular geometry tool would remove duplication while
PharmacophoreMT retains ownership of complementary ligand hypotheses and their
projection distances. This provider review did not execute the consumer source.

The initial [frozen scope](../release_1_0_scope.md#admission-rule) deferred these
new public tools and scientific models. The maintainer subsequently admitted
`structure.get_vectors` and fixed-state donor-H composition on 2026-10-10;
the first exception did not include acceptor models. The maintainer subsequently
authorized the bounded profile documented below. The existing molecular site inventory and interaction
detectors do not claim to supply them. Environment-dependent hydrogen refinement
in uibcdf/molsysmt#323 and aromaticity diagnostics in uibcdf/molsysmt#350 remain
separate concerns, not prerequisites to the elementary donor-vector operation.

## What is measured and what is assumed

Initial evidence was source/contract inspection and the consumer issue. The
partial delivery now has executed geometry controls, documentation examples and
source-tree performance measurements, described below. The later bounded site
profile adds independently tested ideal geometry; it does not establish universal
acceptor accuracy or qualify installed artifacts. A donor-H vector
is directly geometric; assigning an acceptor's local directions requires
additional scientific assumptions and evidence.

## What was refuted

Candidate acceptor indices do not encode lone-pair direction. A first-neighbor
projection or a fallback `[0, 0, 1]` cannot establish one. Providing donor vectors
alone would not complete the acceptor-model portion of this request. A public
geometry tool must not require the consumer to import private MIC helpers.

## Scope and acceptance criteria

- Validate ordered-pair and nonconsecutive structure selections, empty results,
  source maps and immutable input across forms supplying required attributes.
- Compare independently expected displacements/directions under changed length
  units, pair reversal, PBC images, zero/nonfinite geometry and reordered axes.
- For each named acceptor model, document its source, chemistry coverage,
  multiplicity and unsupported cases; test numerical geometry against an
  independent reference rather than the implementation's own formula.
- Exercise selected chemical-state coherence and preserve original method,
  parameters, units, evidence and producer versions in derived site results.
- Complete argument/dependency validation, scalability controls, docstrings,
  User Guide, Cookbook and course material before exporting the new tools.

No implicit protonation, hydrogen addition, environmental optimization, pocket
inference or pharmacophore projection policy is included. PharmacophoreMT can
continue its bounded donor-vector migration while recording this provider gap;
it need not create a new local lone-pair engine to unblock current workflows.

## Partial delivery — 2026-10-10

The maintainer selected `structure.get_vectors`, requested the endpoint/center
and structure-pair conventions of `get_distances`, required efficient native
execution and explicitly authorized implementation. The
[bounded scope admission](../release_1_0_scope.md#bounded-geometry-admission--2026-10-10)
does not reopen acceptor-model or environmental-refinement work.

The public geometry tool covers ordered atom pairs, Cartesian products, mixed
atom/center endpoints, nested positive-weight centers, distinct sources and
nonconsecutive/repeated aligned structure indices. Arrays carry length units;
dictionary details include distances, normalized directions, source memberships,
source structure axes, actual periodic images, weighting/reference parameters and
producer version. The immutable first-source-box convention is explicit.

Existing center kernels and MIC preparation are reused. The new Rust vector
kernel borrows contiguous inputs, releases the GIL and follows the shared thread
policy. Identity projections and complete-axis selectors avoid repeated gathers;
ordered memberships avoid duplicate-discovery work. ChunkedExecutor bounds the
independent second projection to the current block and writes preallocated output.
Resident-output planning includes unit presentation; it is not an RSS guarantee.

The donor-H composition is verified against explicitly declared water chemistry
and executed in the maintained hydrogen-bond cookbook. It retains recognition
separately from geometry and does not reinterpret an elemental rule as universal
donor/acceptor chemistry. The old bundled alanine H5MSM fixture lacks bond-chemistry
columns required for site recognition; that fixture is used for geometry/mass
controls only, not as a chemically complete site-recognition control.

See [the normative contract](../structure_vectors.md),
[benchmark procedure and limits](../benchmarking/vectors.md), the public tutorial,
and `tests/structure/test_get_vectors.py`. Source/unit/scientific controls and
optimized source-tree measurements do not qualify a new installed candidate.
Existing frozen package identities and publication pause are unchanged.

At that first checkpoint, remaining work was to choose and independently qualify named acceptor local-geometry models,
including multiplicity, participating atoms, supported chemistry and explicit
undefined/unsupported outcomes. Consumer adoption is separate from provider
qualification. General vectors alone do not close uibcdf/molsysmt#375.


## Acceptor-model reconnaissance — 2026-10-10

**Evidence:** inspected reference code and documentation; two executed RDKit
controls. The following is a design proposal, not an implemented acceptor API,
an electronic-structure calculation or acceptance of a larger release scope.

RDKit's [feature-direction documentation](https://www.rdkit.org/docs/source/rdkit.Chem.Features.FeatDirUtilsRD.html)
distinguishes finite directions from a cone for incompletely specified
orientation. The local reference checkout at
`cbfb37abddcd5b5feeac97d53530ae6be83cac0d` contains
`rdkit/Chem/Features/FeatDirUtilsRD.py`: two-heavy-neighbor nitrogen uses a negative
normalized bond-vector sum, oxygen has two rotated directions, and three-neighbor
tetrahedral geometry uses the opposite neighbor-vector sum, subject to a
planarity check. These are reference geometric hypotheses, not measurements of
orbitals or universally valid acceptor assignments.

The single-heavy-neighbor helper requires caution. Its prose describes two
in-plane directions for a carbonyl and a cone for an unresolved single bond,
but the branch tests `bond_type > SINGLE` before returning the cone. An executed
RDKit 2025.09.5 control with explicitly placed acetaldehyde (`CC=O`, oxygen index 2)
returned one cone; methanol (`CO`, oxygen index 1, implicit hydrogens) raised
`AttributeError` when the adjacent carbon supplied no other indexed neighbor.
Both observations concern `GetAcceptor1FeatVects`, not general RDKit chemical
recognition. The installed helper and the inspected checkout share that branch.
Do not reproduce a reference implementation blindly or treat parity as an
independent chemistry oracle. Upstream reporting/coverage remains a separate
maintainer decision.

Mol* source at `4807179589f43c20f38d689e4acbc3fc8590df14`, in
`src/mol-model-props/computed/interactions/hydrogen-bonds.ts` and
`chemistry/geometry.ts`, tests bond-angle and out-of-plane deviations according
to an ideal local geometry. It does not expose a universal detached lone-pair
inventory; adopting its hydrogen-bond detection criteria would be a separate
scientific profile. Its recognition also differs from the fixed-state
recognition contract already offered here.

[Wood, Pidcock and Allen (2008)](https://doi.org/10.1107/S0108768108015437)
compare C=O/C=S hydrogen-bond geometries and interaction energies. This supports
separating acceptor environments; it does not qualify our unimplemented ideal
geometry or establish a universal sulfur/oxygen rule. Published abstract and
reference code inspection are separate from reproducing the full paper's
numerical results.

### Proposed bounded next delivery

| Environment | Proposed geometric representation | Required evidence / refusal |
| --- | --- | --- |
| Declared ordinary carbonyl O | Two ideal trigonal directions, 120 degrees to O-to-C, in the carbonyl substituent plane. | Explicit bond order and a nondegenerate local plane; exclude ambiguous resonance/sulfonyl assignments. |
| Declared pyridine-like N | Opposite bisector of the two normalized neighbor bonds. | Chemically recognized acceptor with the selected state's aromatic/conjugation assignment; do not admit pyrrole or amide by element alone. |
| Declared nitrile N | Opposite the indexed N-to-C bond direction. | Explicit supported triple-bond environment and nonzero bond vector. |
| Supported pyramidal amine N | Opposite normalized neighbor-vector sum. | Complete indexed local neighbors including needed hydrogens; reject planar or degenerate arrangements. |
| Ether, alcohol and water O | Consider an explicitly named ideal tetrahedral model with two directions. | Review conjugation and indexed hydrogen requirements first; a missing rotational reference is unresolved, not an arbitrary chosen axis. |
| Carboxylate, phosphate, sulfate, sulfonyl, metal-bound and other chemistry | Explicit unsupported outcome in the first bounded profile. | Their distinct angular preferences/chemistry require later named coverage and independent controls. |

Method names should describe their geometry and carry the reference author or
software separately, as in the existing interaction-method/attribution contract.
A public owner considered at reconnaissance was `physchem.get_hbond_site_directions`, composing
`get_hbond_sites` and `structure.get_vectors`; its signature and first supported
profile had not yet been accepted at the reconnaissance checkpoint. The existing recognition function remains a
coordinate-independent inventory.

A useful result must carry source atom and structure indices, the selected
chemical state, role, model, supporting atom memberships, a typed sparse table
of directional records and per-site/per-structure status. Distinguish at least
supported geometry, unsupported chemistry and undefined geometry. Multiple
finite directions belong to one site. A cone axis must not be flattened into a
unique lone-pair vector; cone support can be deferred explicitly. Normalized
directions are dimensionless; source positions carry length units and observed
bond images retain the row-box convention. No projection distance is inferred.

Before implementation, specify the chemistry coverage and independent controls
for rotations/translations, neighbor reordering, multiplicity, nonconsecutive
structures, unit changes, incomplete chemistry, coincident/collinear/planar
limits, selected states and PBC. Measure the actual geometric workload before
adding another compiled kernel; the existing vector kernel is available now.

## Bounded site-profile delivery — 2026-10-10

The maintainer initially authorized implementation in `physchem` after the
reference review, then accepted canonical ownership in `interactions.hbonds`
on the same date. `get_hbond_site_directions` now composes the public recognition,
SMARTS and vector tools. The first geometric method is `ideal_local_geometry`;
its default `site_method='smarts_donor_acceptor'` remains a separately attributed
chemical rule. Observed donor-H vectors and ordinary carbonyl/pyridine/nitrile
acceptor hypotheses are implemented. Other acceptors are explicit unsupported
outcomes; missing indexed support and degenerate geometry are undefined, never
an arbitrary fallback axis.

The result has versioned experimental dictionary metadata, static role/model and
CSR support membership, a bounded per-site/per-structure status matrix and sparse
numeric finite direction records. It retains source structure indices and their
positions in the requested axis, including repeats, plus actual support images,
unit-aware origins, dimensionless directions, selected state, producer versions
and separate recognition/geometric attribution. No source domain is changed and
this derived dictionary is not automatically attached or natively persisted as a
named H5MSM Interactions analysis.

Execution reuses Rust vector/MIC primitives and NumPy fixed-arity model arithmetic,
with projected ChunkedExecutor delivery and bounded sparse packing. The common
numeric helper owned by `structure` avoids public-wrapper work per canonical
block while remaining shared with `get_vectors`. The common
index-count helper now reads atom/structure axes from H5MSM 0.5 metadata: this
avoids full structural materialization or the legacy 0.4 handler during index
validation. A guard forbids the complete reader during projected site geometry.

See the [normative contract](../hbond_site_directions.md), public tutorial,
hydrogen-bond persistence recipe, executed course section and
`tests/interactions/hbonds/test_get_hbond_site_directions.py`. Independent analytic vectors
and periodic reconstruction checks establish the specified ideal geometry, not
electronic or energetic truth. RDKit feature helpers are geometric inspiration,
not an exact-parity oracle; Ackredit and result metadata distinguish that role.

Remaining: review and independently qualify additional amine, ether/alcohol/water,
resonance/sulfur/phosphorus and coordinated-acceptor models, including any cone
representation; validate consumer adoption. These extensions do not block use of
the bounded delivered profile. Frozen installed candidates and the publication
pause under uibcdf/molsysmt#334 remain unchanged. The issue remains partial.

### Executed source evidence

- 173 focused tests pass on Python 3.14 with `pytest -n 12 --receptor=llm`, covering
  new geometry, site chemistry, general SMARTS/vectors, attribution, common axis
  boundaries and strict API docstring rendering. The only warning groups are
  existing Sphinx Napoleon deprecation and legacy H5MSM reads.
- The new public module's doctest passes; full-source Ruff and the public
  docstring validator pass. The 14 fast repository gates pass. These checks do
  not execute a new full platform or installed-package matrix.
- The tutorial and hydrogen-bond persistence recipe execute. Only the new
  independent site-direction section of the existing biophysics course module
  was executed; prior legacy/network-dependent cells were preserved without
  reexecution.
- The [normative performance section](../hbond_site_directions.md#local-performance-controls--2026-10-10)
  links the isolated-process receipt: 20,000/200,000 finite directions with
  source identities, warm timings and numeric/RSS distinctions. No broad
  accuracy, memory-RSS guarantee or installed artifact claim follows from it.

## Canonical namespace consolidation — 2026-10-10

The maintainer reconsidered ownership and accepted `interactions.hbonds` as the
complete hydrogen-bond domain: participant recognition, local direction models
and occurrence detection. The existing public `get_donor_atoms` and
`get_acceptor_atoms` already occupy this namespace. Reusability does not require
placing a hydrogen-bond-specific interpretation in `physchem`.

Both `get_hbond_sites` and `get_hbond_site_directions`, and the private direction
reducer, now live under `interactions.hbonds`. Their pre-release `physchem`
exports are removed. Public signatures, scientific profiles, result schemas,
units, bounded delivery and attribution are unchanged. Detection still consumes
recognition directly; it does not require site directions. General graph/vector/
PBC operations remain with their existing owners. Other site APIs were not moved
as part of this change.

The public API registry, argument caller maps, detector/chemical-preparation
consumers, tests, API reference, Foundations, Toolbox, Cookbook and course
inventory/examples use the new paths. Historical benchmark and qualification
receipts retain their original paths and hashes. This change updates sources;
it does not modify frozen installed candidates or settle the broader coverage
pending in this issue.

Executed on Python 3.14: 1,036 focused tests pass with `pytest -n 12
--receptor=llm`, including all interaction tests and affected chemical-template,
hydrogen-building, SMARTS/vector and API documentation consumers. Both public
module doctests pass. All 14 fast repository gates, full-source Ruff and the
public docstring validator pass. The two relocated tutorials and persistence
recipe execute, as does the independent course site-direction section; existing
legacy/network-dependent course cells remain unexecuted in this check.
The full Sphinx HTML build exits successfully, with warnings on other existing
pages and no reported warnings for the relocated site tutorials/API references.
This is focused source verification, not full platform/installed qualification.

The local default `python3` Jupyter kernelspec points to Python 3.13, independently
of the interpreter launching `nbconvert`. The final example execution explicitly
selected the existing development Python 3.14 through a temporary kernelspec;
no auxiliary environment was created or shared kernelspec changed. The tutorial
metadata records the actual Python 3.14 interpreter. The earlier successful
Python 3.13 execution is additional source evidence, not the required local
development baseline.
