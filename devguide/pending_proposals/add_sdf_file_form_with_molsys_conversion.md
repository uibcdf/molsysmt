---
summary: Add SDF file form with MolSys conversion
issue: uibcdf/molsysmt#215
status: partial
opened: 2026-09-22
closed:
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Add SDF file form with MolSys conversion

**Reported:** 2026-09-22, from the DockingMT ligand-interchange discussion and inspection of the form registry.
**Status:** Partial. The maintainer brought this work forward on 2026-10-02.
A native, experimental single-record adapter is implemented. Explicit optional
RDKit stereo reading/writing and reusable accurate CIP analysis are available;
broader real-ligand/stereochemical validation remains pending before closure.

## What

Add a file:sdf form with supported conversions in both directions with
molsysmt.MolSys, initially for one molecular record. This establishes an
ordinary MolSysMT file form for ligand exchange. The broader SDF metadata and
multi-record design already appears in
[chemical_metadata_preservation_sdf_mol2.md](chemical_metadata_preservation_sdf_mol2.md);
this proposal makes the smaller conversion deliverable explicit. Track the
DockingMT consumer in uibcdf/dockingmt#3.

## How

- Register file:sdf in the form catalog with working public conversion routes
  to and from MolSys. The accepted implementation direction is a native CTAB
  reader/writer, with no RDKit runtime dependency. RDKit is an optional reference
  for differential tests rather than an implicit parser fallback.
- Define one-record semantics for molecular graph, atom and bond identity,
  bond order and aromaticity, formal charge, stereochemistry, and coordinates
  where the selected SDF variant represents them. Convert angstroms to
  MolSysMT nanometers and keep native element IDs as strings. Declare only
  attributes actually delivered by public getter or conversion routes.
- State how one MolSys structure is chosen for output. Multiple structures
  and multiple SDF records require an explicit, tested policy; until a
  multi-record model is accepted, reject unsupported cases rather than silently
  taking the first record or frame.
- Detect SDF property blocks that MolSys cannot represent yet. Report their
  loss clearly, including under strict conversion, rather than treating a
  parsed graph as a complete round trip. The separate metadata proposal retains
  ownership of a durable property-block and multi-molecule schema.

## Why

SDF is a common ligand interchange format, and MolSysMT's existing purpose
includes converting file forms to its native molecular-system representation.
The current form catalog has RDKit molecular forms and MOL2 files, but no
file:sdf form. One shared conversion path lets DockingMT use the same MolSys
input model for ligand data without owning general SDF parsing. This is an
architectural judgement, not a measured performance claim.

## What is measured and what is assumed

**Inspected at filing:** molsysmt/form had no SDF adapter.
[forms_and_conversions.md](../forms_and_conversions.md) explicitly leaves
property blocks and a multi-record SDF/MOL2 model to a separate schema
decision. No round-trip fidelity or performance measurement existed at filing.

**Implemented and contract-tested, 2026-10-02:** `file:sdf` is a registered Tier 3
form with public native conversion, getter piping, explicit count getters and
byte-preserving identity copies. The reusable CTAB syntax layer lives in
`molsysmt/_private/ctfile.py`; native-domain assembly remains in the adapter.
Reading retains every explicit hydrogen. V2000/V3000 ordinary covalent and
explicit aromatic bonds, finite coordinates, formal charges, absolute isotopes,
D/T, common-element mass differences and doublet/triplet radical counts are
handled without chemical sanitization. Query rules, maps, valence overrides,
stereo, Sgroups, singlet spin, unknown extensions and multiple records fail
explicitly. The writer validates before opening the destination. SD properties
are parsed, retained by identity copies, and rejected on native conversion unless
the caller explicitly requests `discard_properties=True`; reports identify the
loss and strict mode still rejects it.

Evidence is in `tests/form/file_sdf/test_native_contract.py`: independent
hand-written V2000/V3000 inputs, a bundled explicit-hydrogen molecule, an optional
independent RDKit reader, malformed/unsupported inputs, source selections, empty
records, non-default unit policy, existing-file preservation and a subprocess
that blocks RDKit imports. These are bounded compatibility results, not a claim
of complete RDKit parity or a measured speed advantage.

**Implemented and contract-tested continuation, 2026-10-02:** V3000 coordination
type 9 uses existing native dative relationships and donor/acceptor roles,
preserving direction through native endpoint sorting and extraction. It does not
join covalent components or fabricate a covalent order. Output needs V3000 and
explicit roles. Reports cover separate numeric dative orders, component-joining
overrides and source drawing-style loss; strict mode rejects detected losses.
Documented inactive V3000 flags are accepted, while active, unknown or repeated
fields still fail. No new chemistry store, parser fallback or runtime dependency
was introduced.

`tests/form/file_sdf/test_coordination.py` covers independent hand-written inputs,
role remapping, source display options, ambiguous native roles, destination
preservation, strict reports and an optional RDKit reader. A committed corpus
contains 46 supported encodings of 17 synthetic molecular graphs covering
aromatic/Kekule bonds, nitrogen heterocycles, fused rings, nitro, phosphate,
sulfate, zwitterion, charged groups, isotopes and other ligand chemistry. The
snapshot producer is RDKit 2025.09.5; `generate_sdf_reference_corpus.py` regenerates
it without consulting the MolSysMT parser. Counts/net charges are independently
specified. Tests run from the snapshot without RDKit and optionally compare
source and native-written files with a live unsanitized reader. Three legitimate
reference records with valence overrides are rejection tests, not counted as
successful conversion coverage. This is not broad real-database validation.

Validation checkpoint: the SDF/conversion-truth/report-audit selection passed
392 tests; the final coordination follow-up passed 18 tests (overlapping that
selection, not additive). The public SDF doctest passed. Ruff, form-adapter
delivery, dependency, developer-guide and maintained course-structure checks
passed. Only Markdown changed in the affected notebooks; their code and outputs
were retained. No speed or memory benchmark was performed.

**Inspected references:** BIOVIA's
[CTFile Formats 2020](https://discover.3ds.com/sites/default/files/2020-08/biovia_ctfileformats_2020.pdf)
defines field meanings and precedence. RDKit commit
`a24ed4f06a4f73ef419e9b6347999d0abfbacabd` supplied a comparison of reader/writer
and stereo-processing boundaries; its implementation was not copied. The
reference supplier is explicitly configured with `removeHs=False`, and graph
comparisons distinguish declared CTAB aromaticity from RDKit sanitization.

**Pending:** A larger curated real-ligand and stereochemical corpus, enhanced
stereo scope/policy, and independent reusable valence/hydrogen perception tools.
The explicit optional stereo provider and reusable accurate CIP tool have since
been implemented under uibcdf/molsysmt#299; see the checkpoint below. These tools belong to their general
owners, not hidden inside the SDF adapter. Performance remains unbenchmarked.
The parser is a format utility with no new scientific attribution boundary.

**Shared-tool continuation, 2026-10-02:** The maintainer approved general
chemical atom-type validation and explicit isotope normalization, tracked in
uibcdf/molsysmt#296. Public wrappers live in `element.atom`; the SDF reader
reuses their private explicit-symbol primitive. The read-only public conversion
preflight in uibcdf/molsysmt#297 uses the existing audit core without writing
the destination. Neither change enables stereo perception, atomic-number
conversion, force-field typing or PDBQT parsing.

The next stereo stage must distinguish relative CTAB wedge/parity from absolute
CIP labels. RDKit's `finishMolProcessing` explicitly performs geometry/graph
interpretation before assigning chemical stereo; copying CTAB integers into
native R/S fields is not a faithful alternative. General graph ranking and
valence/hydrogen interpretation belong to `physchem`, connectivity traversal to
`topology`, and geometry to `structure`. The current corpus is intentionally
achiral and cannot justify enabling native tetrahedral or E/Z perception.

On 2026-10-03, uibcdf/molsysmt#299 supplies public read-only full-graph CIP
analysis under `physchem`. Explicit `stereo_engine='rdkit'` enables supported
SDF tetrahedral and double-bond reading/writing without changing the default
native route. Source atom axes and explicit hydrogens remain intact; CTAB
wedge/parity is interpreted rather than copied into R/S. Native bond storage
retains cis/trans with reference atoms; absolute E/Z is queried independently.
The verified writer rejects conflicting geometry before touching a destination.
RDKit adapters share the accurate assignment primitive and work on copies.

Focused fixtures cover L-alanine, L-cysteine, isotopic tie-breaking, E/Z,
pseudoasymmetric full-graph ranking (RDKit's Salome Rieder example), both CTAB
versions, empty selections, coordinate-unit conversion and real Ackredit credit.
The existing 46-record corpus remains achiral. A diverse curated stereo source
corpus and validation of explicitly out-of-scope encodings are still pending;
this implementation does not claim native toolkit-independent universal CIP.

**Assumed:** Single-record conversion is useful before the broader metadata
and multi-record model is settled. Representative fixtures must establish
which SDF features the first adapter supports faithfully.

## What was refuted

Treating rdkit.Mol support as equivalent to file:sdf support leaves no
discoverable file form or direct MolSys file conversion contract. Claiming
unqualified SDF round-trip fidelity would hide property-block and record
boundary loss.

## Scope and exclusions

This issue covers the first file:sdf form and single-record conversions.
Arbitrary property-block preservation, multi-molecule files, and a general
record-to-MolSys schema remain in the existing broader proposal. DockingMT's
ligand preparation and Vina protocol are outside this adapter. A string:sdf
form may be proposed separately if a consumer needs it. This is new form
coverage, not a prerequisite for the currently defined MolSysMT 1.0 contract;
the maintainer explicitly scheduled this bounded implementation before 1.0.
The wider metadata/multi-record schema remains deferred.

## Acceptance criteria

- The public form catalog recognizes .sdf files, and conversion works between
  file:sdf and MolSys in both directions for documented one-record inputs.
- Representative fixtures preserve supported graph, chemical attributes,
  coordinates, units, and atom alignment through a MolSys round trip within
  the format's precision. Tests cover selection and structure-index semantics
  where meaningful.
- Multiple records, multiple frames, and unsupported properties receive
  explicit, tested behavior. No record or property is silently dropped while
  reports or strict mode claim exhaustive preservation.
- Capability declarations, instance-aware presence, optional dependency
  behavior, docstrings, User Guide, Cookbook, and applicable course material
  match the delivered subset.
- The durable contract is incorporated into
  [forms_and_conversions.md](../forms_and_conversions.md) before closure.

## Dependencies and risks

Stereochemistry and aromaticity can change under parser normalization rules;
fixtures and fidelity claims must distinguish source information from inferred
chemistry. The deferred metadata proposal remains the owner of any broader
SDF property and multi-record schema.

## Real-input and preparation follow-up — 2026-10-03

Consumer acceptance of the adapter is requested in uibcdf/dockingmt#33,
against `eb0549b50`; reusable preparation remains separately owned. Follow
[the maintained work sequence](../roadmap.md#current-sdfpdbqt-and-chemical-preparation-sequence--2026-10-03)
and the linked #214 validation matrix. Curate the pinned Vina 1IEP/1S63/5X72
SDF inputs without rewriting unsupported flags to make tests pass. The 5X72
pair supplies real stereo controls for explicit optional interpretation;
1S63 requires separate handling of the additional prepared-reference H.
Evaluate SD-property and stereo policy per file, preserve exact source
checksums and distinguish input parsing from chemical sanitization, implicit-H
inventory and preparation. Inputs outside the bounded profile need documented
rejection or an owned extension, not a silent RDKit fallback. No new real-file
test execution is claimed by this planning checkpoint.

## Original Vina corpus checkpoint — 2026-10-03

**Contract-tested and bounded reference comparison:** nine unmodified upstream
files are committed under `tests/form/data/vina_examples`, with Apache licensing,
upstream commit, SHA-256 and independent literal controls. Real SDF tests live in
`tests/form/file_sdf/test_real_vina_examples.py`.

- 5X72 P59/P69 retain 39 atoms and 42 bonds, coordinates and opposite R/S labels
  at source atom index 7, using explicit `stereo_engine='rdkit'` and authorized
  source-property loss. Both V2000 and V3000 output are checked independently.
  Source bond IDs and Kekule encodings differ; equivalence is checked through
  independent chemical normalization rather than raw bond-table equality.
- 1IEP's declared atom valence (index 31) and 1S63's versionless counts line
  remain unsupported native semantics, with deliberate rejection controls.
  Independent RDKit accepts these sources; rejection is a bounded implementation
  gap, not evidence that the files are malformed. Extend their semantics under
  this issue before claiming their native conversion coverage.
- Opaque unselected copies now preserve all four source records without semantic
  decoding, including properties and unsupported fields. The discovered defect
  and guard are recorded in
  [the #302 resolution](../archive/resolved_bugs/sdf_identity_copies_require_native_chemical_interpretation.md).

The focused SDF/PDBQT/fragments/conversion-report regression passed 418 tests in
104.48 seconds on Linux / Python 3.13.14, with NumPy 2.4.6, RDKit 2025.9.5,
MDAnalysis 2.10.0 and Vina 1.2.7. The executable command and warnings are recorded
in #302's local resolution; this is not a full-suite or preparation result.
Source bytes are not rewritten to achieve coverage, and no optional toolkit is
used as a silent parsing fallback. Broader native SDF coverage remains pending;
the subsequent consumer evidence and stabilization review follow. This issue stays partial.

## Frozen-profile stabilization — 2026-10-05

S3 reruns native SDF, coordination, reference-corpus, stereo, real-Vina and
structure-count controls at `fe0b813d7267f4c5a0728264094441e62c910e1b`, within
the passing 1,094-case preparation/form selection. The
[execution ledger](../release_1_0_status.md#s3-preparationform-qualification--2026-10-05)
and [artifact](../../devtools/data/preparation_profiles_20261005.json) retain
commands, source/fixture hashes, environment and warnings. Optional independent
RDKit comparisons execute; they do not establish universal chemical perception.

The 1IEP valence and 1S63 versionless sources still exercise deliberate rejection,
while opaque identity copies retain their bytes. 5X72 stereoisomers keep their
distinct source-indexed assignments through explicit stereo-provider round trips.
Published uibcdf/dockingmt#33 accepts the initial prepared-input/stereo slice;
that historical evidence is inspected rather than rerun on this source. No source
is rewritten and no new dialect or chemistry is admitted. Current conservative
profiles are qualified for experimental inclusion; broader acceptance and parser
coverage remain post-1.0 work and this issue remains partial.
