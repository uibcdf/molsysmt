---
summary: Provide a public CCD component-to-chemical-template route with retained atom identity.
issue: uibcdf/molsysmt#557
status: resolved
opened: 2026-11-04
closed: 2026-11-06
verification: measured
area: [physchem, chemical_states, topology, form, data, docs]
guard: tests/physchem/test_get_chemical_template.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# CCD component references and coordinate-free chemical templates

**Status:** resolved at the native provider boundary; scientific profiles remain
experimental. Consumer/installed-pair acceptance is separate.

## What

Provide a reusable public route that acquires one explicitly selected CCD chemical
component and constructs a coordinate-free native chemical template, preserving
source atom/bond identity and scientific declarations. Online and offline sources
must reach the same constructor. MK1 and BTN are consumer controls, not a catalogue
of two hand-authored exceptions. DockingMT supplies the workflow and source pose;
MolSysMT owns reference interpretation, correspondence tools and application.

The maintainer clarification in issue #557 explicitly requires local component
bytes/files, a selected local CCD catalogue/cache and individual online lookup.
Offline misses must not trigger network access. No new resource framework or
universal chemical resolver is required.

## Inspected reusable tools and boundaries

- `physchem.get_peptide_chemical_template` already returns a coordinate-free
  native MolSys, detached provenance and a report archived in ChemicalStates
  preparation history. Its template/application composition is the model.
- `physchem.assess_chemical_template` and `apply_chemical_template` own exhaustive
  map validation, compatible field assignment, optional graph completion,
  retained poses, scoped chemistry and conflicts. Reuse them without weakening
  their scientific checks.
- `chemical_states.get_atom_correspondences` deliberately requires complete
  declared chemical context. It cannot fill its own missing prerequisites or
  be weakened into matching by equal counts or element proximity.
- `element.atom.normalize_atom_types` already distinguishes element symbols from
  force-field types and normalizes explicit D/T aliases and isotope conflicts.
- The hard `mmcif` dependency supplies PdbxReader. Its selectList filters
  categories, not component data blocks; it does not establish bounded catalogue
  lookup by itself. Reuse the parser after bounded data-block acquisition.
- `_private.download.download_with_retries` supplies managed atomic HTTP download
  staging and retained causes. Reuse it for explicitly selected individual RCSB
  component retrieval, without silently downloading the complete catalogue.
- `devtools/scripts/curate_est_template_fixture.py` is intentionally fixture-only.
  It records an EST CCD atom-flag/canonical-descriptor stereo disagreement. It
  is evidence and an acceptance control, not a generic runtime parser/matcher.

## How

The implementation will keep three operations separate:

1. **Acquire a declared CCD reference.** The proposed public
   `physchem.get_chemical_template` requires an explicit source: RCSB individual
   lookup, caller bytes, a local component/catalogue file, or a local component
   directory. A streaming catalogue selector retains one component block, exact
   bytes/digests and source acquisition identity. It must account for CIF multiline
   text, compression, duplicate blocks, source changes and explicit misses.
2. **Interpret reference chemistry under a named policy.** A table projection
   remains available without RDKit; missing declarations stay unknown. A separately
   selected canonical-descriptor method uses the optional RDKit route and records
   the exact descriptor program/version. It checks graph/element/charge/aromatic/H
   agreement, treats all admissible descriptor mappings consistently and refuses
   truncated or conflicting assignments. The original CCD stereo flags remain
   evidence even when an explicit descriptor policy chooses another assignment.
   Neither method chooses protonation, rewrites a source system or uses CCD ideal
   coordinates. Full indexed H and stored-count projections retain original atom
   and bond row maps; information such as isotopic H cannot be silently collapsed.
3. **Make explicit name-based correspondence reusable.** A stable-inventory tool
   under topology can propose a label correspondence for caller-selected axes
   using unique exact atom names and matching elements. It must refuse missing,
   duplicate or incompatible keys and explain that this is not chemical
   isomorphism. Actual template application still verifies chemistry and graph
   correspondence through the existing public assessment. No downstream parser,
   scientific transfer loop or implicit structure-based matching is introduced.

The result will follow the existing template factory: a native template,
JSON-compatible template_provenance, and a detached report. Retain exact source
component bytes in a typed encoding, component ID/revision and full source hashes,
source row order/names, retained positional maps, units and executed software.
The stored reference state is not a prediction of the bound ligand state.
Histories use the existing ChemicalStates/H5MSM route, not another chemical store.

## Why

DockingMT needs MK1/BTN reference chemistry before it can use the complete-context
matching/application pipeline. Existing deposited-entry readers preserve observed
geometry but do not establish all required charge, H, aromatic and stereo fields.
The missing provider contract must not be replaced by consumer-specific RDKit/CIF
interpretation or two opaque curated templates.

## Initial inspection and measurement scope

Source inspection at prepared baseline
8941bcfd4 (Python 3.14 development environment) establishes the reusable routes
above. No generic CCD construction, MK1/BTN application parity or performance
was claimed at that initial inspection. Runtime validation must identify actual
provider origins and versions.

Primary CCD semantics are defined by the wwPDB dictionary, including
[atom stereo](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_chem_comp_atom.pdbx_stereo_config.html).
The parser owner is [RCSB py-mmcif](https://github.com/rcsb/py-mmcif).
The EST fixture's exact hashes and independently checked stereo are recorded in
`tests/physchem/data/chemical_templates/manifest.json` and its owning generator.

## Alternatives rejected at this checkpoint

- Shipping only MK1 and BTN does not satisfy the maintainer's generic retrieval
  requirement.
- Replacing observed coordinates with CCD model/ideal coordinates would destroy
  the deposited-pose contract and is unnecessary for chemical assignment.
- Treating every unknown stereo/radical/H field as zero or achiral fabricates
  completeness. A native table projection must expose its actual unknown scope.
- Selecting the first graph match hides symmetry or ambiguity. A bounded search
  must prove assignment consensus within a complete declared scope or refuse it.
- Reusing complete-context isomorphism before source chemistry exists is circular.
- A global implicit online fallback violates local/offline source authority.

## Acceptance criteria

1. Individual online lookup, exact caller bytes, local component/catalogue files,
   compressed input and local cache lookup share source identity/constructor
   behavior. Distinguish not found, duplicate/ambiguous, malformed, incomplete,
   unsupported and unavailable-source cases; keep original operational causes.
2. Preserve exact source atom/bond axes and names through row permutations and
   heavy/full-H projection. Validate duplicate/missing sites and dangling/conflicting
   edges. No coordinates, minimization or conformer generation enter construction.
3. Qualify charge units and non-default application policy, explicit H counts,
   aromatic orders, stereo conflicts, isotope limits, symmetry consensus and
   bounded-search refusal. Missing values remain unknown rather than neutral.
4. Execute MK1/BTN and EST controls plus small independent charged, aromatic,
   stereogenic and adversarial references. Test explicit name maps and unchanged
   source coordinates/chemistry, application conflicts, optional dependency
   absence and real attribution capture/portable records.
5. Preserve reports, producer versions, maps and template chemistry in H5MSM and
   typed dictionaries. Update docstrings, User Guide, Cookbook/course and
   maintained contracts. Run applicable lint, dependency, API and fast gates.
6. Integrate and close only in the maintainer's fifteen-issue order. Published
   prepared source and consumer review are separate from installed qualification.

## Scope and risks

CCD is the initial supported resource. It does not contain every possible ligand,
and a CCD entry is not a bound-state protonation/tautomer choice. Unsupported
valence/aromatic/stereo models must remain explicit. No receptor terminal repair,
H placement, force-field parameterization, scoring, docking search or biological
pharmacophore validation belongs to this capability. Additional concrete resource
adapters may reuse the contract later without introducing speculative registries.

## Local implementation checkpoint — 2026-11-06

Unpublished implementation on the #557 working branch now passes **54 cases**
with the existing Linux/Python 3.14 development interpreter, twelve workers and
published Pytest Receptor. This combines 36 acquisition/template cases, 17
name-correspondence cases and one public name-correspondence doctest; no failure
or omission remains in that selection. The result is source contract evidence,
not full application, provider-floor, installed or scientific qualification.

Implemented acquisition covers bytes, local files/directories, compressed input,
bounded catalogue scanning, explicit online lookup and operational failure causes.
The generic constructor is exercised on unchanged public MK1/BTN CCD files and
the existing EST reference, including complete descriptor symmetry consensus,
atom/bond row permutations, declared stereo disagreement, H projection, typed
dictionary/H5MSM histories and detached provenance. Adversarial checks refuse
discarding an H atom whose formal charge is unknown: the new control failed before
that conservative projection correction. A draft unit assertion incorrectly
treated stored integer formal-charge multiples as continuously valued quantities;
the final test checks the existing integer-e contract and serialized unit under
a non-default Coulomb session policy.

The independent public `topology.get_atom_name_correspondence` uses unique exact
names and elements, returning int64 query/reference source-index pairs. Native
Topology/MolSys, typed dictionaries and topology-only H5MSM are tested, along
with nonconsecutive axes, refusals, empty shape and unchanged input. It reads
stable inventory through public form-agnostic select/get; no coordinates or
chemical assignments are prerequisites. The resulting labels remain proposals
for the existing chemical-template assessment, not chemical identity evidence.

**Remaining at that earlier checkpoint:** real deposited MK1/BTN application and unchanged source poses;
broader adversarial/optional-engine/attribution controls; public-provider floors;
constructor doctests, user/course documentation and API/scientific inventories;
full affected checks, source publication and ordered closeout. No #557 completion
or readiness claim follows from this checkpoint. Earlier ordered installed #428
receiving remains independent and does not consume these uncommitted files.

After the native/provider closures, this working branch is advanced to main
c649e8816 without changing its unfinished implementation. Exploratory public-path
application now also succeeds for unchanged deposited 1HSG/MK1 (45 selected atoms,
group index 198) and 1STP/BTN (16 atoms, group index 121), each projected to three
structures. Explicit name correspondence feeds the existing assessment/application;
source inventory/bonds and every retained coordinate remain unchanged. These are
cached probes, not yet bundled regression evidence, and do not establish a bound
protonation state or docking readiness. The first probe incorrectly expected an
application result to retain assessment status `compatible`; the existing public
application contract uses `applied`. Only that probe assertion was corrected.

## Final local receiving — 2026-11-06

The final source selection passes **421 affected cases**, without failures or
omissions, using the existing Linux/Python 3.14 development interpreter, twelve
workers and published Pytest Receptor. It includes public API docstring rendering,
existing template/context/EST/receptor and correspondence contracts, attribution,
typed dictionary/H5MSM history and the new generic references. The source-qualified
selection passes **101 cases** against unchanged published payloads of ArgDigest
0.14.0, SMonitor 0.16.0 build 1, DepDigest 0.15.1 and Ackredit 0.9.0. No environment
or package installation was added. Only the incompatible development SMonitor
pytest plugin is disabled for that floor profile; runtime diagnostics remain active.
Two public doctests pass. Fourteen fast gates, repository Ruff lint and format
verification also pass at their recorded checkpoints; the final closeout reruns
the lifecycle checks after archival.

The 1HSG/MK1 and 1STP/BTN regression controls now retain exact deposited and CCD
bytes in the fixture manifest. Public construction and name correspondence feed
the unchanged assessment/application. Native/H5MSM and reversed full atom axes
retain all three deliberately repeated structures, original names/IDs and exact
coordinates under non-default units. Outside chemical fields and bonds remain
unchanged, and a proper subset preserves global partial completeness. Conflicting
observed charges fail transactionally. The prerequisite converter ownership defect
is separately published and closed as #617 in main 34b8c09e2; the unknown-extension
permutation refusal remains intact.

Charged and radical references, E/Z endpoint maps, H projection/isotope refusals,
symmetric stereo consensus/conflicts, missing/foreign descriptors, case-insensitive
CCD codes and malformed identity/edges are exercised beyond the two consumers.
The selected wwPDB dictionary pages confirm case-insensitive stereo/aromatic codes
and integer net component charge. Aromatic triples/quadruples remain outside the
bounded canonical interpretation model; they are reported as unsupported rather
than declared physically impossible. Initial tests exposed hidden order loss and
raw charge overflow before the conservative interpretation corrections. Candidate
and acquisition buffer limits fail with typed diagnostics instead of returning
truncated consensus or claiming a process-wide RSS bound.

A real explicit individual RCSB BTN request returns the exact pinned offline
component hash, with acquisition time, revision, source bytes and software record.
Offline tests forbid network fallback. Real Ackredit capture retains reused
references and portable attribution; absent/failing attribution preserves science.
Fresh H5MSM reads keep original producer metadata without claiming new calculation
credit. Supplied definitions are not authenticated wwPDB records, and a descriptor
program is never credited as executed software merely because its name is present.

The new course example executes through the existing quiet notebook runner. Its
three cells are inserted with their saved output; every pre-existing cell, output,
ID and notebook metadata value is unchanged. Both code blocks in the new label
correspondence tutorial execute with the documented maps. The first draft used an
unexported root Topology alias; it was corrected to the supported native import.
API stability remains experimental and the generated scientific-evidence view
leaves these APIs outside independent scientific qualification. This is a tested
reference-interpretation/application contract, not universal CCD chemistry or
bound-state validation.

Exact JUnit digests, source-file identity, actual provider origins, public-floor
payloads, original version strings, online acquisition and limits are retained in
`devtools/data/ccd_template_receiving_557_20261106.json` at closeout. Development
editable-distribution metadata is retained as observed; it does not identify the
current source commit. The receipt records that commit and its file digests
separately. There is no new installed consumer pair, addon facade, canvas/session
qualification, force-field/protonation inference or release/publication claim.

## Resolution — 2026-11-06

Implemented in d419e6fc2c73ff00c0caad8d6a70fde23e3b6dd6. The native public factory, explicit label
correspondence, persistent evidence, lifecycle documentation and receiving above
fulfil the generic provider scope. Reuse the unchanged assessment/application;
no downstream parser or special two-component template catalogue is required.
The reproducible source/fixture/JUnit receipt is
[ccd_template_receiving_557_20261106.json](../../../devtools/data/ccd_template_receiving_557_20261106.json).
