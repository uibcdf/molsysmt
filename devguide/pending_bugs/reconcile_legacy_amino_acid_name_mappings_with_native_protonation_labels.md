---
summary: Reconcile legacy amino-acid name mappings with native protonation labels
issue: uibcdf/molsysmt#549
status: active
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [attribute, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Legacy names versus explicit native protonation labels

**Reported:** 2026-11-03 while receiving #545/#547. **Status:** active; the
maintainer accepts the explicit scheme design below. Runtime cutover remains due.

## What

The current public one-letter/name helpers disagree with the explicit native
protonation-template vocabulary. `get_1_letter_code_from_name('GLH')` returns Q
and `get_standard_name('GLH')` returns GLN. HID/HIE raise KeyError in the one-letter
helper. The native pinned peptide-fragment inventory includes GLH, HID and HIE;
GLH has OE1/OE2 side-chain oxygen atoms, unlike GLN's terminal amide nitrogen.

```python
from molsysmt.element.group.amino_acid import get_1_letter_code_from_name, get_standard_name
print(get_1_letter_code_from_name('GLH'), get_standard_name('GLH'))
# Q GLN
get_1_letter_code_from_name('HID')  # KeyError
```

## How

The legacy MDTraj-derived `element/group/amino_acid/group_types.py` table and the
separately curated `data/databases/peptide_templates/residue_fragments.json` have
different vocabularies. A name-only helper lacks an explicit dialect or molecular
chemical context; simply broadening recognition can conflate old catalogue names
and force-field state labels. Inspect the original legacy source and the pinned
Meeko/Amber naming profiles before choosing the supported interpretation.

## Why

Sequence labels, canonical-parent reporting and preparation should not silently
imply different identities for a name produced by native workflows. No incorrect
prepared graph or downstream charge calculation was demonstrated by this report;
the observed defect is the public naming-contract mismatch.

## What is measured and what is assumed

The values and missing-key failures above were executed with Python 3.14.7 on
main be2f3fb7cb6ac0e52170669edea165166899ad3c plus the bounded #545 canonical-code
repair. Existing variants are unchanged by that repair. Two newly authored tests
incorrectly assumed HID support and GLH/E in the unqualified legacy helper; they
failed. They are not converted into assertions that Q is chemically correct.
Those external-profile assumptions are removed from #545's acceptance tests and
are instead the explicit scientific question recorded here.

## What was refuted

This is not the missing XLE/XAA canonical-table route fixed by #545. The mismatch
already exists in the prior variant catalogue and is retained by the bounded
repair. Code-table parity cannot establish the chemical interpretation of GLH.

## Scope and acceptance

Decide the public naming context and supported native protonation-label contract;
resolve GLH/HID/HIE consistently in name/code helpers and relevant consumers.
Audit additional CYM/CYX/LYN and other colliding labels rather than guessing an
exhaustive mapping. Add independent semantic controls and builder-to-name/sequence
round trips. Preserve ChemicalStates as the chemical-assignment owner: lookup
must not protonate, replace chemical graphs or choose a state implicitly.

The initial disposition is a stabilization review, not an automatic post-1.0
deferral. The maintainer accepts the scheme-aware direction on 2026-11-04.
No naming migration, runtime profile, schema field or public signature change is
implemented by this analysis/documentation checkpoint.

## Provenance

Local Linux, shared Python 3.14.7 and unchanged native backend. The native fragment
provenance is recorded in its bundled JSON and `make_peptide_chemical_templates.py`;
no upstream source or coordinate asset was changed.

## Source study — 2026-11-04

The [dated inspection record](../../devtools/data/name_scheme_review_549_20261104.json)
retains exact AmberClassic/MDTraj commits, the Amber library content digest,
native Meeko fragment provenance, bounded RCSB CCD observations and executed
native sequence probes. It is review evidence, not a new runtime dictionary.

Primary CCD metadata confirms independent meanings for HID, CYX and ASH
(non-peptide compounds), HIP (phosphonohistidine) and LYN (lysine amide).
The Amber peptide vocabulary uses the same labels for histidine, cysteine,
aspartate or lysine states. Even matching parent letters do not equate those
chemical meanings. GLH/HIE/CYM API requests returned 404; that observation does
not establish universal or historical CCD absence. The legacy table is mixed
historical data and must not be relabelled as a certified current CCD reference.

Native template-to-sequence calls on 5f3af9374 reproduce the public impact:
GLH gives Q; HID/HIE and a declared CYX pair fail with KeyError. Template group
labels remain as supplied and the bond table is unchanged by the queries.
This demonstrates incorrect or unavailable sequence projection for those native
templates, not a newly demonstrated wrong prepared graph, force-field charge or
coordinate calculation.

## Accepted design — 2026-11-04

The maintainer accepts the following decisions after the pros/cons discussion:

1. Preserve original group names and interpret them under a declared scheme.
   Do not choose a universal Amber or legacy interpretation implicitly.
2. Use `from_naming_scheme` for source interpretation in public conversion and
   `naming_scheme` for a direct name helper. `None` means no explicit override:
   read stored declarations, otherwise resolve only supported unambiguous names.
   Ambiguous or unassessed meanings require an actionable SMonitor diagnostic.
3. Detect contradictions between explicit and stored declarations. Missing
   metadata remains unknown, including on older files. File form, Python class,
   matching counts or historical preparation records are insufficient evidence.
4. Associate declarations with names in Topology at group granularity, supporting
   a mixed Amber-labelled protein and CCD-labelled ligand. MolSys coordinates
   the domain; ChemicalStates remains the assignment/connectivity owner.
5. Preserve declarations through native lifecycle operations, typed dictionaries
   and H5MSM. Select reviewed physical encoding and schema revisions before
   implementing writers; new reader behavior cannot silently reinterpret old
   bytes or discard a declaration. Root 0.5's modular layers permit a layer
   revision study; no root/layer/dictionary version is selected by this plan.
6. Make `molsysmt.element.group.get_1_letter_code_from_name` the canonical public
   entry point, reusing one private resolution authority. Update internal
   consumers, docs, stability records and bound-tool inventory together. Do not
   introduce duplicate name tables or infer an alphabet for arbitrary groups.
7. Document each supported scheme, definition version, provenance, accepted
   names and unsupported behavior, with explicit comparisons. Initial profile
   identifiers are amber, ccd, legacy and the subsequently accepted sequence
   alphabet, each bounded to its actually reviewed
   implementation. Do not advertise complete CCD or other-force-field support.

The direct scalar helper initially covers amino-acid projection. Naming
interpretation does not protonate, select a chemical state, generate coordinates
or chemically replace a modified group with its parent. General target-name
translation and atom naming remain separately scoped future operations; no
unused `to_naming_scheme` parameter is added merely to reserve a spelling.

## Documentation contract

The conceptual User Guide page
[Group naming schemes](../../docs/content/user/foundations/molecular_system/naming_schemes.md)
compares sequence/amber/ccd/legacy and distinguishes the delivered group helper
and native projection from pending other consumer/override migration. It links
primary references and distinguishes independently verified
records from legacy compatibility values and unverified record lookups.

For the initial correction, the eight reviewed state labels and the subsequently
reviewed XAA/XLE collisions require a declared scheme. Canonical names can remain convenient where their requested
interpretation is unambiguous. Definition versions/snapshots and explicit
unsupported cases must appear in published support tables when implemented.
Keep the table aligned with one runtime authority; a future generated view may
report that authority but cannot substitute for scientific review of its entries.

## Implementation sequence and exit evidence

- [x] **D0 — bounded source study and public reproduction.** Verify the naming
  collisions, native sequence failures and provider/data provenance.
- [x] **D1 — maintainer decision and documentation plan.** Record defaults,
  domain ownership, mixed groups, relocation and the required user comparison.
- [x] **D2 — typed naming declarations and schemas.** Choose group-aligned
  storage and the scheme/version registry; specify null/unknown and conflict
  rules, copy/extract/remove/merge/builder behavior, partial and atom-free native
  domains, dictionary and H5MSM readers/writers. Reject declared unsupported
  persistence rather than losing context. Do not require coordinates for names.
- [x] **D3 — shared private resolver and public helpers.** Add independent
  Amber/CCD/canonical/legacy controls, refusal paths and immutable-input tests;
  introduce the group-level public code helper with ArgDigest and SMonitor.
  Keep modified-parent projection distinct from chemical replacement.
- [ ] **D4 — native producers and consumer propagation.** Producers that
  explicitly know their input vocabulary declare it. Propagate the conversion
  argument through selected direct and MolSys routes. Resolve declarations per
  selected group, preserve ordering/repetitions and refuse ambiguous mixed
  overrides. Audit sequence, recognition, missing-atom/H and preparation callers
  so a name-only lookup cannot select chemistry implicitly.
- [ ] **D5 — persistence and lifecycle receiving.** Exercise mixed schemes,
  unknown declarations and conflicting overrides across source maps, copies,
  extraction/reordering, merging, atom-free sequences and H5MSM/dictionary round
  trips. Old files retain unknown context; no implicit online enrichment.
- [ ] **D6 — coordinated public cutover and documentation.** Move the public
  code entry point, update old-path consumers and PR #543's mirror/manifest,
  User Guide, Cookbook, course, API help and stability/tier inventories. Any
  necessary bounded compatibility alias needs an explicit removal condition.
- [ ] **D7 — final receiving and closure.** Verify exact-source guards, units
  where other operations carry quantities, source/chemistry preservation,
  documentation execution, Ruff and required gates. Close #549 only with its
  addressable guard and public evidence. Installed-client/release qualification
  remains under #334; this plan does not qualify or publish a package.

Do not patch GLH globally to E, add all state aliases to the historical table,
rename source groups during conversion or infer a scheme from native form as an
interim shortcut. Those approaches would hide the confirmed cross-scheme
collisions. Reassess progress at the phase exits rather than estimating an
unmeasured completion percentage.

## Documentation checkpoint validation — 2026-11-04

The selected heading/source-boundary/directive/notebook-schema suite passes
533 cases with zero failures or omissions and 514 Sphinx/MyST deprecation
warnings. The new conceptual page also renders independently with strict Sphinx
(`-W --keep-going`), retaining its pending-implementation warning and PyData
table markup. This is a bounded page render, not a complete site/release build.
Developer-guide, generated-index and diff checks pass. No runtime or schema is
implemented, and the four pre-existing generated API edits remain untouched.

## D2 storage and schema implementation — 2026-11-04

**Implemented and contract-tested locally.** This block implements declarations
and their native/persistence lifecycle, not the D3 name resolver or D4 conversion
argument. The legacy GLH/HID/HIE semantic defect is not yet fixed and #549 stays
active. No package, tag or external CI matrix is produced by this block.

### Native declaration boundary

`Topology.set_group_naming_schemes(naming_schemes=None, group_indices='all')`
assigns an explicit scalar vocabulary or an aligned sequence. Identifiers are
`amber`, `ccd` and `legacy`; None means unknown. The immutable
`group_naming_schemes` tuple reports group-index order. A scoped ArgDigest
registry validates types, alignment, supported identifiers and unique bounded
positions before mutation, using SMonitor argument/length diagnostics. Private
storage helpers do not use decorators or form dispatch.

An optional uint8 vector stores codes 1/2/3, with zero for unknown, at one resident
byte per group; all-unknown context stores no vector. This is the numeric payload
size, not a measured total-memory or performance benchmark. Group table columns
remain unchanged. Copies own their declarations; atom subsets and atom-free
group selections project the actual source group map. Addition concatenates
known and unknown context, atom permutation leaves the group axis intact, and
builder-added/fallback/inserted-cap groups start unknown. Table reset explicitly
clears context; stale direct changes to group counts reject instead of guessing
alignment. Name-preserving rebuilds retain declarations.

Changing a declaration explicitly replaces metadata at this setter boundary.
Interpretation/conversion overrides must still reject conflicts in D3/D4; those
are different operations. A changed attached declaration conservatively invalidates
all named analyses, including evaluated-empty coverage, using the existing staged
invalidation context. Prior analysis snapshots and coordinates remain intact;
unchanged assignment is a no-op and an invalidation failure preserves the prior
declaration and analyses. The operation changes no chemical assignment or label.

### Versioned transport

- TopologyDict 0.3 retains existing stable rows and adds required
  `group_naming_schemes`, containing declaration `schema_version=1`, the ordered
  profile registry and group-aligned primitive integer codes. Without known
  declarations the writer retains 0.2. A MolSysDict 0.2 can contain this separately
  versioned topology domain; no enclosing-root field changes.
- H5MSM keeps root 0.5. Topology layer 4 retains the five tables and optional
  chain/group and atom/molecule memberships, with a required naming subgroup.
  Its registry is explicit JSON metadata and its code dataset has dtype uint8
  and shape `(n_groups,)`. Other layer/association codecs are unchanged.
- Declaration profile version 1 versions the bounded identifier vocabulary; it
  does not claim complete Amber or CCD coverage or fix a scientific data snapshot.
  D3 must separately record the actual resolver's definitions and source evidence.
- Readers reject unsupported registries/versions, unknown fields and malformed
  codes, shapes or dtypes. Older native records/files without the field retain
  unknown context. Older readers reject the new schema rather than silently
  discarding its declaration. No online enrichment or form/history inference runs.

The maintained format contract, User Guide, dictionary explanation, H5MSM page,
Module 04 and group-free hierarchy recipe distinguish this implemented storage
from pending interpretation. Notebook changes are explanatory Markdown only;
executable cells and saved outputs are retained.

### Receiving scope and initial test corrections

The first new-test run had 46 passes and eleven failures: tests used unsupported
`to_form='h5msm'` instead of `file:h5msm`, supplied a layer mapping to the MolSys
writer, and compared pandas' base-class copy against the native table subclass
with class checking enabled. These test mistakes were corrected without changing
the public writer or table semantics. A second run had 55 passes and two failures
from assuming the existing Topology-to-file projection omits its empty Structures
container. Controls now distinguish that projection from a partial MolSys whose
absent Structures domain is preserved. No coordinates are synthesized in either.

The first broader receiving selection passes 213 cases without failures or
omissions. Final extended/native, schema, documentation and floor qualification
results are recorded below when completed; these initial counts alone do not
qualify the full issue or a release.

### Completed local receiving

- The extended native/H5MSM/dictionary/capping selection passes **2,602 cases**,
  with zero failures or omissions and 721 warnings (mostly legacy H5MSM warnings,
  plus existing pandas/unknown-name/attribute-drop/box diagnostics). This run
  precedes the final scalar-broadcast optimization, typed-read tightening,
  ordered-inventory naming comparison and additional boundary controls.
- The final focused selection passes **138 cases**, including **70 naming
  guards**, dictionary documentation execution and append atomicity. It uses the
  verified public **ArgDigest 0.13.0 py_1** payload from the existing package
  cache, with the published Pytest Receptor 1.2.1 in the shared Python 3.14.7
  environment. There are no failures or omissions and one expected capping
  attribute-drop warning. The original package identity is the same qualified
  floor recorded under #554; actual import origins are retained locally.
- The four native Topology doctest items pass on the final source. The selected
  documentation corpus initially passes 538 cases and fails one conditional-key
  assertion: the new 0.3-only field was presented as required for the existing
  0.2 example. The table now marks its conditional presence explicitly, and the
  full six-case dictionary documentation module passes in the final selection.
  The remaining 533 structural/rendering/notebook checks are reused from that
  corpus; their tested structure is unchanged by the corrected table wording.
- An additional merge control initially used partial MolSys inputs on a route
  explicitly requiring one chemical state per input. It now exercises supported
  public Topology merging, without broadening molecular merge semantics. A
  separate append control verifies that declared source chemistry refuses
  mismatching name conventions before changing the destination.
- Whole-package Ruff, the public signature guard, the 278-symbol stability
  registry, the 246-function docstring validator and lazy-dependency validation
  pass. Notebook code/output/document metadata and all four protected API-stub
  hashes are unchanged. No new dependency or compiled-backend change is needed.

Raw JUnit/environment evidence is local under `.pytest_cache/group-naming-549/`:
`receiving.xml`, `native-persistence.xml`, `final-floor.xml`,
`documentation.xml`, `final-doctests.xml` and `floor-environment.json`. Those
working files are not a published release certificate. Scope remains D2; D3/D4
must supply independent scientific resolution controls and actual conversion
propagation before the original bug can close. The work is kept local for a
batched publication; no hosted checkpoint is claimed for these changes.

## D3 resolver and initial native propagation — 2026-11-04

**Implemented and contract-tested locally.** The new canonical
`molsysmt.element.group.get_1_letter_code_from_name(name, naming_scheme=None,
skip_digestion=False)` uses a private name-resolution authority, a scoped
ArgDigest boundary and SMonitor diagnostics. The original `amino_acid` name
helpers remain unchanged pending D4/D6: this block must not be described as
their completed cutover or full #549 closure.

### Additional ambiguity and accepted sequence profile

A fresh primary RCSB review inspects 39 names. Thirty-six requests succeed:
thirty peptide entries with mutually checked parent/letter metadata and six
non-peptide entries; GLH/HIE/CYM return HTTP 404 without an absence claim. In
particular, CCD XAA and XLE are non-peptide compounds, whereas the shared sequence
alphabet uses those labels for X and J. This is an additional naming collision,
not a reason to equate the compounds with unknown/ambiguous amino acids.

After the explicit maintainer choice, `sequence` is admitted as the fourth
convention. It uses the existing 26-symbol alphabet, never a duplicate code
table. Code 4 appends it to the declaration registry without changing existing
code meanings. Old three-profile TopologyDict/H5MSM payloads remain readable;
codes are bounded by the registry actually declared in the payload. No H5MSM
root/layer or dictionary structural schema bump is required for this named
registry extension; older readers reject the unsupported new registry.

### Bounded resolver and data provenance

The offline asset and generator are under `molsysmt/data/`; the primary review
is [the dated profile receipt](../../devtools/data/name_scheme_profile_review_549_20261104.json).
Generation reuses the canonical alphabet and preserves the reviewed source URLs,
revisions/response digests and generator-input digest. `--check` regenerates and
compares the complete payload without a network request.

Sequence supports 26 codes; Amber supports twenty standard names plus eight
reviewed state labels. CCD uses the 36 inspected entries only. Legacy explicitly
uses the existing historical parent table. An explicit unsupported name never
falls back to another convention. With no context, the helper admits the 24
noncolliding alphabet labels and four reviewed matching modified projections
MSE/SEP/TPO/PTR. State labels and XAA/XLE require context even when projected
letters would coincide. Non-peptide CCD compounds have no amino-acid projection.

References are optional Ackredit data credits, not claims of executed Amber,
MDTraj, Meeko or RDKit engines. Real-provider enclosing captures retain reused
references; refusal credits nothing. Optional-provider failure or simulated
absence preserves the letter. Fresh import loads neither Ackredit nor the
profile-reading module. The bounded single-entry asset cache contains no caller
systems or unbounded reference-group payloads; no new dependency is introduced.

### Initial D4 delivery and remaining boundary

The explicit peptide-template producer declares Amber. The sequence-record
constructor declares sequence only for canonical alphabet labels and leaves
noncanonical labels unknown. Native Topology/MolSys sequence conversion reads
stored declarations per selected group, retaining order and repetitions,
without changing names or chemistry. It credits used references once per
complete query, not once per group. Native dictionary and H5MSM routes preserve
that behavior. GLH/HID/HIE and paired CYX template projections now work through
those routes with unchanged bond tables and no coordinates.

The general `from_naming_scheme` conversion argument, conflict handling for
that override, remaining recognition/preparation/alignment consumers and the
old helper retirement/addon mirror are still D4/D6 work. In particular, the
old standalone `amino_acid.get_standard_name('GLH')` is not fixed by introducing
the new helper. Do not publish this intermediate state as stabilized, change
chemical preparation by parent substitution, or mark the overall issue resolved.

The User Guide includes an executed general group-code tutorial, native
declaration/transport explanations and updated Module 04/Cookbook prose.
The two prior notebooks retain executable payloads and outputs. The source/API
navigation fixture reads the actual new tutorial and foundation anchors;
no fabricated reference targets or weakened negative control are introduced.
Both local and hosted native smoke commands include the new guards; no remote
workflow is dispatched by this local development block.

### D3 local validation and retained failures

- The focused final floor selection passes **229 cases**, with zero failures or
  omissions and one known capping attribute-drop warning, using the verified
  public ArgDigest 0.13.0 py_1 and published Pytest Receptor 1.2.1 in the existing
  Python 3.14.7 environment. It includes the scalar resolver, native projections,
  original/new registry round trips and once-per-query credit guard. No new
  environment or dependency floor is introduced.
  Real Ackredit capture uses editable 0.12.1+2.ge233973; this is provider-source
  integration evidence, not qualification of a different published package.
- An independent final receiving run also passes **229 cases**, with zero
  failures or omissions and the same capping warning, using public Ackredit
  **0.9.0 py_0**, public ArgDigest **0.13.0 py_1** and Pytest Receptor **1.2.1**.
  The cached Ackredit archive has SHA-256
  `99e6f9b9f0a3b0a22c66e476230dddabd2ba0017c59beb3253fbadc781d665c6`;
  its digest and all 62 Python payload files match the cached import route.
  Actual provider versions/import origins are retained separately in
  `published-floor-environment.json`, with `published-floors.xml` recording
  the selection. The command exits zero. This validates the exercised public
  provider-floor boundary in the existing development environment, not a
  clean installed MolSysMT artifact or a complete dependency/platform matrix.
- The sequence/FASTA/peptide-template selection passes **341 cases** without
  failures or omissions. Initial six failures in newly written graph-preservation
  controls compared pandas' base-class copy to a native table subclass; those
  assertions now compare all content/dtypes without requiring the copy to retain
  the subclass. The expected sequence strings already passed in that first run.
- The extended native/group/topology/H5MSM/dictionary run executes **4,593
  cases: 4,592 pass and one fails**, with 717 warnings (mostly legacy H5MSM
  diagnostics). The failure is an old FASTA membership test expecting dictionary
  0.2/topology layer 2 after the constructor now explicitly declares sequence.
  It now requires dictionary 0.3/layer 4 and checks preserved sequence codes,
  chain memberships and labels. Its whole module plus CI command-contract tests
  pass **41 cases**. The other 4,592 results are retained because no runtime
  implementation changed after that run; it is not relabelled as a fresh green
  full run.
- The documentation selection executes **540 cases: 539 pass and one fails**
  because the isolated API-navigation fixture did not yet include the actual
  new foundation/tutorial anchors. The fixture now reads those real sources
  and asserts the new API page is connected, retaining its broken-navigation
  negative control. All **five source-boundary cases pass** on recheck, with
  512 Sphinx deprecation warnings. Other completed structural/notebook/rendering
  results remain scoped to their tested source; no fictitious anchors are added.
- All **five native/new-helper doctest items pass**. The new tutorial's six
  code cells execute successfully with real outputs, including H5MSM persistence.
  The first execution could not start Jupyter because sandbox sockets were
  unavailable; the authorized local-socket retry succeeds in the same shared
  environment. This is not a scientific or external-network failure.
- Whole-tree Ruff lint and formatting (4,340 files), generated-profile equality,
  the 247-function docstring
  validator, public signature guard, 278-symbol registry, dependency validation
  and developer-guide/index checks pass. Previous Module 04/Cookbook executable
  payloads are retained. Four unrelated API-stub edits and the native backend
  remain outside this work. New guards are in the existing single native smoke
  command; no duplicate pytest workflow step is added.

JUnit and notebook working evidence is under
`.pytest_cache/group-name-resolution-549/` and the new tutorial's ordinary local
execution marks. This is bounded source receiving, not hosted CI, installed
artifact, complete platform or overall #549 qualification. Batch publication
continues to wait for the coordinated remaining work.

### Next D4/D6 block

1. Add the general source override with explicit conflict diagnostics and exact
   selection/group maps, preserving inputs and avoiding a coordinate copy for a
   naming-only query. Validate original group-position values before lossy casts.
2. Propagate context to recognition, parent reporting and preparation/alignment
   consumers. Preserve exact state/modified templates; a parent label is not
   permission to change chemistry. Include missing context and CCD non-peptide
   controls alongside known Amber producers.
3. Audit native/dictionary/file projections and conversion fidelity so unsupported
   target naming metadata is not silently certified as preserved. Complete
   mixed/unknown/conflicting context receiving across supported routes.
4. Retire the old one-letter public path together with all old-path consumers,
   API/tutorial/stability inventories and the addon mirror. Coordinate #543
   receiving against the final corrected native source. Keep overall #549 open
   until those paths and final qualification agree.
