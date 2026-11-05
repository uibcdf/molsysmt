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

At the initial reproduction, the public one-letter/name helpers disagreed with the
explicit native protonation-template vocabulary. `get_1_letter_code_from_name('GLH')` returns Q
and `get_standard_name('GLH')` returns GLN. HID/HIE raise KeyError in the one-letter
helper. The native pinned peptide-fragment inventory includes GLH, HID and HIE;
GLH has OE1/OE2 side-chain oxygen atoms, unlike GLN's terminal amide nitrogen.

```python
# Initial reproduction, before the scheme-aware parent helper was introduced.
from molsysmt.element.group.amino_acid import get_1_letter_code_from_name, get_standard_name
print(get_1_letter_code_from_name('GLH'), get_standard_name('GLH'))
# Q GLN
get_1_letter_code_from_name('HID')  # KeyError
```

The dated delivery sections below describe the corrected parent/recognition and
preparation boundaries. The old scalar one-letter helper remains D6 cutover work;
the initial unqualified parent-helper behavior above is no longer current.

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
and native projection, including explicit conversion context, from pending other
consumer migration. It links
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

### D4/D6 receiving priorities

1. Receive the general source override below, including selected-group conflict
   diagnostics, source maps, immutable inputs and no-copy native sequence queries.
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

## D4 source interpretation and selected-axis receiving — 2026-11-04

**Implemented and contract-tested locally.** Public `convert` now accepts the
keyword-only `from_naming_scheme=None`; all prior positional arguments and
defaults remain unchanged. Native Topology/MolSys one-letter adapters expose
the same keyword. The converter-keyword domain is regenerated from actual
signatures, and the three intentional public changes have addressable signature
waivers linked to this issue. This is another D4 delivery, not completion of its
remaining consumer audit or overall #549 closure.

### Interpretation and ownership

An explicit convention must agree with every known declaration in the selected
groups. Matching parent letters do not waive a vocabulary conflict. Unknown
selected groups use the caller's convention; unknown or conflicting unselected
groups do not change that projection. No convention is inferred from a file
extension, class, numerical count or chemical-preparation history.

Native one-letter queries read existing topology directly, retaining group order
and repetitions without copying Topology, ChemicalStates or Structures. The
original labels, declarations and analyses are unchanged. The MolSys adapter no
longer extracts a separate topology snapshot merely to read its names. Group
positions are validated before lossy casts, including booleans, fractional,
masked, unit-bearing, oversized and out-of-range values.

Molecular conversion retains its atom-selection contract and maps those atoms
to source groups before checking declarations. Sequence text constructs new
slots from ordered/repeated source positions before native/dictionary/H5MSM
transport. Existing group-only inventories instead reuse the public hierarchy
extractor's unique-position contract and preserve their source IDs. They acquire
no atomic axis. Explicit group positions are supported for one-letter queries
and group-only conversion routes admitting that keyword; they cannot compete
with a non-all selection. The
existing dispatcher now forwards caller-supplied element indices once rather
than also supplying an automatic value for the same keyword.

When adding context to a molecular output, an independent native topology is
required even if `copy_if_all=False` was requested. The intermediate MolSys copy
defers geometry blocks rather than making an extra coordinate snapshot. The
ordinary final target still owns its normal conversion/copy policy. Adding a
declaration invalidates the output's named interaction coverage, including an
evaluated-empty analysis; the original analysis snapshot remains evaluated.
No detector, state selection, protonation or chemical substitution is performed.

Topology/MolSys, their dictionaries and H5MSM retain selected declarations and
index remapping. Native-backed input routes include both dictionaries, H5MSM,
sequence text and a native PDB-text read with optional inference explicitly off.
Foreign sources use their registered native conversion and retain its optional
dependency requirements; this is not selective file-backed coordinate reading.
FASTA one-letter results keep their record occurrences and empty records. An
existing one-letter text envelope and case are retained. This bounded receiving
does not certify every foreign adapter or claim unsupported targets retain the
registry; that fidelity audit remains D5 work.

An explicit source declaration for sequence construction precedes its default
alphabet metadata. This does not overwrite native or persisted declarations.
The generic conversion report continues to inspect the original source before
the naming route; a native intermediate is not presented as an exhaustive audit
of the foreign source.

### Documentation and remaining work

The conceptual foundation, conversion tutorial, executed group-code tutorial,
Cookbook and Module 04 distinguish query-time interpretation from a retained
output declaration. Prior course, recipe and conversion-tutorial executable
payloads stay unchanged. The new source-override guards join the existing single
native smoke command, without a new CI test invocation or remote dispatch.

D4 still requires recognition, parent reporting, preparation and alignment
consumers to use stored naming context, preserving exact state/modified templates.
D5 must audit metadata losses and additional foreign routes; D6 must coordinate
the old public path, documentation/stability/addon inventories and #543 receiving.
At that checkpoint, the old scalar parent helper and the default direct
three-letter legacy helper were not fixed by adding the source keyword. The
later sequence-consumer block below supersedes the latter limitation. Keep
#549 open.

### D4 source-keyword validation

- Final published-provider receiving passes **344 cases**, zero failures or
  omissions, with public ArgDigest 0.13.0 py_1, Ackredit 0.9.0 py_0 and Pytest
  Receptor 1.2.1 in the existing Python 3.14.7 development environment. It includes
  **87 source-keyword cases**, the resolver/native/persistence guards, the
  generated keyword-domain contract and CI-command controls. Four warnings are
  three legacy H5MSM notices and the existing capping attribute-drop diagnostic.
- Existing conversion/preflight/native ownership, native dictionary, sequence,
  FASTA, Topology, H5MSM and group-inventory receiving passes **2,396 cases**,
  zero failures or omissions, with 684 warnings: 682 legacy H5MSM notices and
  two existing unknown-Ar-name diagnostics. The later explicit-query envelope
  branches are exercised by the final focal run; those branches do not alter
  the default routes covered by this extended run.
- Documentation source-boundary, heading and notebook-schema controls pass
  **513 cases**, with 512 Sphinx deprecation warnings. The isolated navigation
  fixture reads the real conversion tutorial label. A first invocation named a
  nonexistent heading-test file and ran no tests; only the corrected selection
  is counted. Broken-navigation controls remain unchanged.
- All **four conversion, scalar and native-adapter doctest items pass**. The
  updated group-code notebook executes its seven code cells, including retained
  H5MSM examples, using the existing environment and an authorized local Jupyter
  socket. No remote/network notebook service or new environment is used.
- Whole-tree Ruff lint/formatting (4,343 files), all 247 public docstrings,
  the 278-symbol stability registry, the intentional-signature guard, generated
  converter-domain equality, dependency checks and developer-guide/index checks
  pass. The generated naming asset remains unchanged. Four unrelated API-stub
  edits and the native backend remain outside this work.

The initial new-module run has six failures: five expose incorrect group-versus-
atom selection in the implementation, corrected by mapping molecular selections
through the original atom table; one test mistakenly assigns into the read-only
interaction mapping instead of its supported property setter. Existing guards
then expose a real ArgDigest-floor regression caused by adding a context-like
parameter to the shared value validator. Its original signature is restored,
and the source-specific wrapper supplies its own diagnostic argument. All seven
original scalar controls pass unchanged. A later text-envelope fixture used
unprefixed nonstandard codes that the existing form detector refuses before
conversion. The unprefixed control now uses admitted canonical text, while the
prefixed case still checks the extended alphabet and source case. Detection
policy and production expectations are not broadened to make that test pass.
Additional group-only controls separate repeated text construction from unique
native inventory extraction. The initial implementation incorrectly sent both
through the latter; sequence construction now consumes its original positions
before creating native slots. Existing inventory extraction validates uniqueness
through its owning tool before assigning missing context, retaining source IDs.
The target-keyed keyword domain remains intact: portable selection is used for
typed dictionary targets rather than advertising an undeclared group_indices
keyword. No general extractor contract is relaxed.

Commands retain JUnit under `.pytest_cache/group-name-resolution-549/`:
`override-published-floors-final.xml`, `override-extended.xml`,
`override-docs.xml` and `override-doctests-final.xml`. This is local source and
public-provider receiving, not a clean installed MolSysMT artifact, complete
platform matrix, final #549 qualification or release authorization. No hosted
workflow, push, tag or package publication accompanies this block.

## D4 sequence consumers and support-library receiving — 2026-11-04

**Implemented and contract-tested locally.** Native one-letter conversion,
direct three-letter projection and sequence identity now reuse one private
projection authority. It resolves selected profiles before contributing one
reference-data credit batch and optionally returns original group positions.
No additional per-group object store or duplicate name table is introduced.

Identity reads stored per-group schemes from native Topology/MolSys, their typed
dictionaries and H5MSM 0.5. Same labels under Amber and legacy retain different
letters. Query and reference keep independent positional maps, with order and
repetitions preserved; group IDs are unchanged. Native queries copy no molecular
domain. All/index dictionary queries decode topology only, and equivalent H5MSM
queries request only that layer through public read_layers. Predicates needing
other information retain ordinary form-agnostic selection. Missing topology,
unknown context for a state label, or a non-peptide CCD interpretation cannot
silently become an amino-acid match.

Direct three-letter conversion has a keyword-only source convention and uses
the sequence alphabet for canonical symbols, including XAA/XLE. The full input
is validated before selection. Caps are omitted afterwards. Noncanonical names
use assessed unambiguous meanings or explicit context, with no historical
fallback. Legacy remains an explicit choice. This does not relocate or retire
the old scalar public path, which remains D6 work.

Both alignment and identity now declare a conditional Biopython dependency with
DepDigest. Real missing-provider checks raise the host SMonitor catalog error;
an unsupported different engine does not load Biopython. Alignment also credits
the actual executed Biopython version through optional Ackredit. Identity reuses
the same software record alongside its existing adapted counting reference.
Scoring, pretty-print output, query-length normalization and return types are
unchanged. Real captures retain reused data/software references, provider absence
or failure preserves numerical results, and a refused projection claims no
completed naming batch. No chemical state, bond, atom or coordinate is replaced.

The support-library audit finds the already fixed ArgDigest #17 bypass in the
previous minimum 0.13.0. The existing invalid-flag test fails unchanged with that
version. The first fixed tag, 0.14.0, is verified against its public main-label
archive and tested together with minimum DepDigest/SMonitor and optional Ackredit.
The public minimum is raised to `argdigest>=0.14.0` across maintained acquisition
routes instead of forking the provider's bypass rules. Seven public boundaries
are covered by non-boolean bypass rejection tests. Biopython's host installation metadata now names
the Conda package correctly. The
[#524 receiving record](../pending_proposals/runtime_dependency_api_floors.md#argdigest-bypass-contract-and-biopython-route--2026-11-04)
owns that dependency decision, archive digest and the older-SMonitor pytest
entry-point limitation; it does not establish a clean installed closure.

The foundation, Toolbox, Cookbook and Module 13 describe the delivered sequence
consumers and retain the preparation/recognition distinction. The small group-code
tutorial executes an identity comparison against stored context. Existing large
notebook executable payloads and outputs are retained. The new guards join the
same single local/hosted native smoke command, without dispatching remote CI.

Remaining D4 work is recognition, parent reporting and preparation, including
the legacy scalar parent fallback and exact state/modified-template handling.
D5's additional metadata-loss/foreign-route audit, D6's coordinated old-path and
addon cutover, and final D7 receiving stay open. This is not #549 closure, new
scientific-profile certification, an installed-client qualification or a release.

### Sequence-consumer validation

- **363 cases pass** with public ArgDigest 0.14.0 py_0, DepDigest 0.15.1 py_0,
  SMonitor 0.16.0 py_1 and Ackredit 0.9.0 py_0 in Python 3.14.7. All 50 new
  consumer guards are included: mixed profiles/maps, missing context, non-peptide
  refusal, native no-copy, dictionary/selected-layer reads, missing-provider
  conditions, real attribution and 21 invalid bypass-flag combinations. Six
  warnings are legacy H5MSM notices. The selected offline suite explicitly
  excludes network-marked cases; those cases are not claimed as executed.
- **384 cases pass** with the current development providers and ordinary pytest
  plugin loading, including dependency architecture, installed-closure and
  wheel-contract guards. There are the same six legacy notices. Source/editable
  receiving does not qualify a different published provider artifact.
- **5,221 cases pass** in extended native, topology, both sequence alphabets,
  native Topology/dictionary/H5MSM, group-helper and conversion-preflight receiving.
  Its 729 warnings are 703 legacy-file notices, 14 pandas downcast FutureWarnings,
  nine existing unknown-atom diagnostics, one box mismatch and two attribute-drop
  diagnostics. No assertion or warning filter is weakened for this run.
- **521 documentation/command controls pass**, with 512 Sphinx deprecations.
  All four selected doctest items pass, with one legacy-file notice. The small
  naming tutorial executes all eight code cells in the existing environment;
  the new comparison returns original group positions. Existing large notebook
  executable payloads, outputs and metadata are preserved.
- Whole-tree Ruff lint/formatting (4,344 files), all 247 public docstrings,
  signature/278-symbol stability checks, generated naming/keyword-domain equality,
  dependency/dependency-contract and devguide/index validation pass. The native
  binary and four unrelated API stubs remain unchanged and outside this work.

The first 25-case new-module run has three failures: two incorrectly expect
the import name Bio rather than the provider's canonical package name biopython
in structured diagnostics; the third omits the explicit sequence prefix on a
modified-code string not admitted by the existing form detector. The corrected
controls still verify the same dependency error and MSTY projection. Detection
rules and scientific expectations are not broadened to satisfy them. That real
absence test also exposes the incorrect Conda hint in host metadata, corrected
above. The later ArgDigest 0.13 run executes 341 cases and fails the pre-existing
invalid-flag assertion; that expectation remains unchanged under the raised floor.

The minimum-provider harness's earlier pre-collection failure and its bounded
entry-point exclusion are retained in #524. The successful floor probe is not
the failed process relabelled. Archive hashes and all imported provider payload
bytes are verified; actual versions/import origins are retained in
`consumer-floor-environment.json`. JUnit under the same working-evidence directory
includes `consumer-fixed-provider-floors.xml`, `consumer-current-providers.xml`,
`consumer-extended.xml`, `consumer-documentation.xml` and `consumer-doctests.xml`.
No new environment, provider checkout modification, remote CI run, push, tag or
package publication accompanies these local results.

The separate shared-environment `pip check` exits one on unchanged AmberTools-
related extras: missing pdb2pqr and older NumPy/Biopython constraints. #524 owns
the detailed observation. No installation/downgrade is performed, and neither
the 363-case provider probe nor development receiving is labelled complete
workspace or installed-package qualification.


## D4 reference names and recognition — 2026-11-04

**Implemented and contract-tested locally.** Reference-parent reporting,
amino-acid recognition, group-type inference and the native backend of
`build.get_non_standard_residues` now consume the same bounded naming authority.
This is another D4 delivery, not completion of D4 or closure of #549.

### Delivered behavior

- `amino_acid.get_standard_name` and `amino_acid.is_amino_acid` accept
  `naming_scheme` and the standard `skip_digestion` contract. The existing
  package-exported `get_group_type_from_group_name` preserves both positional
  arguments and adds a keyword-only convention. All three boundaries use scoped
  ArgDigest validation and SMonitor diagnostics. An ambiguous scalar query needs
  context; there is no implicit legacy interpretation.
- Parent reporting distinguishes Amber GLH/GLU from explicit legacy GLH/GLN.
  CCD HID, ASH, CYX, XAA and XLE remain non-peptide components. Unassessed default
  parents return None; explicit unsupported amino-acid candidates raise.
  Negative recognition means not recognized in the selected bounded profile,
  not proof of a non-peptide chemical identity. Independent existing water/ion
  and other non-peptide catalogs remain usable without creating parent templates.
- Native inference operates directly on tables through the shared private
  recognizer. Raw readers preserve ambiguous names and unknown types without
  inferring a convention from OpenMM, MDTraj, PDB, mmCIF or another source form.
  Existing explicit declarations are respected per group; identical labels are
  not collapsed into one interpretation. A declared CCD non-peptide cannot be
  overridden by the former atom-name heuristic.
- Type queries remain non-mutating; the native all-selection query no longer
  copies/rebuilds the topology just to return inferred types. Explicit group
  reconstruction writes types and preserves stable molecule membership, names
  and declarations. Changing a declaration alone still changes metadata only.
  An unknown/missing type can supply a sequence letter when naming interpretation
  supports it; a bare ambiguous name still refuses projection.
- Empty native group-name/type fields now remain nullable strings. Their former
  `astype(str)` initialization created the literal label/type `"nan"`, which
  concealed missingness from recognition. This correction does not synthesize
  a group name or chemical identity.
- The native non-standard-group report reads stored declarations from native
  inventory, typed dictionaries and H5MSM topology layers, retaining original
  selected group indices. It reports parents without editing any domain.
  PDBFixer retains its separate catalogue. Existing parity fixtures now declare
  CCD when they deliberately rename an Amber-built group's label to MSE/PTR;
  a stale Amber declaration is not silently accepted as CCD.
- The competing direct-module group classifier is an import alias of the
  supported package-exported implementation. Its import path remains available;
  the old unexported underscore-valued implementation is gone. An explicit
  signature waiver explains the AST guard's missing-definition observation,
  and an identity assertion protects the real public alias.
- Optional Ackredit credits the reached naming dataset, including a successful
  negative CCD recognition, without claiming an executed Amber/MDTraj engine.
  Recognition/parent lookup does not credit an unused sequence alphabet.
  Provider failures preserve results with the existing structured warning.
  There is no physical quantity or new optional calculation engine at these
  scalar boundaries; PyUnitWizard and new DepDigest declarations do not apply.
  Existing optional-engine routes and lazy imports remain enforced.

### Receiving and limits

`tests/element/group/test_name_recognition.py` and
`tests/build/get_non_standard_residues/test_naming_schemes.py` protect independently
specified parent/type outcomes, missing and unsupported labels, argument/flag
rejection, per-group mixed conventions, nonconsecutive atom/group queries,
non-mutating inference, stable membership, direct private reconstruction,
raw OpenMM input, typed/H5MSM parent reporting and actual optional attribution.
The maintained smoke command includes both modules in the same pytest invocation.

The four published-provider floor probe passes **419 cases** with ArgDigest
0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0. It reuses the already
verified archives and import-path method recorded above. As in the previous
probe, only the newer editable SMonitor pytest entry point is excluded: that
plugin does not exist in the old runtime's distribution. There is no application
assertion or scientific-result exclusion. Its four warnings are three deliberately
injected optional-attribution failures and one existing attribute-drop diagnostic.

The first broad receiving run passes 2,849 cases and fails two newly written
fixture checks: direct fixture ID assignments use object dtype, while native
reconstruction correctly normalizes IDs to nullable strings. The fixtures now
use canonical native ID dtypes; value and membership assertions remain exact.
The earlier public-example test's expected count is updated from four to seven
because the new executed examples extend the docstring. A new optional-attribution
assertion initially assumes item objects; it now reads the provider's supported
capture dictionary, retaining the exact expected CCD-only reference set.
The missing-type control separately exposes the real literal-`nan` constructor
problem fixed above, rather than weakening that missingness assertion.

Three revised scalar tutorials and the existing group-type/non-standard-group
tutorials execute in the shared Python 3.14 environment. Jupyter's first sandboxed
attempt cannot create its local sockets; the same runner succeeds with the local
socket permission. No additional environment or dependency installation is used.
The course and Cookbook receive explanatory text; their executable cells and
stored results are retained. Full reader/native receiving and final governance
checks are recorded below when complete.

**Next D4 boundary:** preparation, hydrogen expectations and repair must use
exact state/modified templates with declared naming context. Their existing
parent substitutions have not been certified by this reporting/recognition
change; ambiguous bare parent requests now refuse instead of selecting a legacy
meaning. The old scalar amino-acid one-letter helper and addon mirror remain D6
cutover work; D5's conversion-fidelity audit and D7's final acceptance remain open.
No hosted CI run, push, tag, artifact or release qualification is claimed.


### Nullable-type receiving follow-up

The wider 7,431-case run passes 7,412 and fails 19 cases with one root cause:
native PDBQT/rigid-fragment construction reaches the shared private
molecule/component type aggregator with a genuine missing group type. Its
first/last type comparisons assume every value is a string and try to coerce
`pd.NA` into a boolean. The aggregator now returns unknown for empty/missing
leading types and guards the trailing cap comparison. It preserves the existing
classification rules for actual strings and does not invent a cap or name.
Seven native tests explicitly exercise None, pd.NA, numeric NaN and fresh
uninitialized groups. These join the maintained smoke invocation.

The affected PDBQT/indexed-handler/Vina and component tests, together with these
seven controls, pass **70 cases** after the correction, with one legacy-file
notice. The complete reader/native selection is rerun before closeout; the
failed wider XML is retained as `recognition-wide-nullable-failure.xml`, rather
than relabelled as a passing process. This is local receiving evidence, not an
installed-package or release-candidate gate.

The isolated Sphinx API-navigation test additionally needs the real existing
group-type tutorial as a target for the new docstring link. Its miniature source
fixture now extracts that actual page's anchor. Both the empty-warning assertion
and the deliberately broken negative control remain; no invented anchor or
warning suppression is used. The corrected documentation set passes **514 cases**
with 512 existing Sphinx deprecations.


### Final local receiving for this block

- **7,460 tests pass** in the final reader/native/sequence/preparation selection
  on Linux/Python 3.14.7 with current development providers and normal pytest
  diagnostics. Four workers complete in 293 seconds; the previous failed wider
  process is retained separately. The 777 warnings are predominantly legacy
  H5MSM 0.3/0.4 notices (723); the remaining 54 include existing parser/box,
  atom-name, attribute-drop, pandas and preparation diagnostics plus the three
  deliberately injected optional-attribution failures. No warnings are filtered
  or assertions removed for this run.
- **419 tests pass** with the four published support-library floors, including
  the seven nullable-type controls; the entry-point-only harness limitation
  remains as documented above. This probe takes 13 seconds with two workers.
- **514 documentation/command controls** and **three doctest items** pass.
  Five revised tutorials execute all **21 code cells** in the shared environment.
  The course and Cookbook retain identical executable cells, outputs and notebook
  metadata; only their explanatory text changes.
- Whole-tree Ruff lint/formatting (**4,347 files**), all **247** checked public
  docstrings, **278-symbol** and signature stability, the offline naming-asset
  generator, dependency/import-contract checks, and devguide/index validation
  pass. Four explicit signature changes/alias consolidations are accepted under
  this issue; no mandatory gate is waived by a commit marker.
- The unchanged native binary has SHA-256
  `f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c`.
  The four pre-existing unrelated human API-stub edits retain their original
  hashes and remain outside this change. No support-library checkout, runtime
  dependency floor or public package is changed in this block.

Working evidence remains under `.pytest_cache/group-name-resolution-549/`:
`recognition-provider-floors.xml`, `recognition-extended.xml`,
`recognition-nullable-followup.xml`, `recognition-documentation.xml`,
`recognition-doctests.xml` and the separately preserved failing wider XML.
These source checks do not repair the already recorded optional-environment
`pip check` failure under #524 and do not qualify an installed artifact or
another interpreter/platform. Preparation, D5 fidelity, D6 cutover and D7 final
acceptance remain open; #549 is not closed.


## D4 chemical references and preparation — 2026-11-04

**Implemented and contract-tested locally.** The atom/H expectation helpers,
missing-heavy-atom query, native H addition/removal, chemical coverage and
reference-bond candidates now read the same group naming declarations. This is
a bounded D4 delivery; broader producer audit, D5 fidelity, D6 cutover and D7
final acceptance remain open.

### Reference selection and scientific limits

The raw amino-acid atom/bond catalogue is not a chemical-state selector. Its
GLH, HIP, CYM and LYN entries contain distinct compounds under different variants
of the same label. For example, the matching Amber GLH/CYM/HIP/LYN internal
variants are at raw index 2, rather than the previously selected first variant.
The shared private reference layer filters all eight reviewed Amber-state names
against the already bundled Meeko-derived fragments: exact heavy-atom names,
heavy connectivity, H count at each heavy parent and one edge per H. Exactly one
internal catalogue variant meets those checks for each reviewed state. The raw
catalogue and pinned source assets are unchanged.

These checks establish reference-layout consistency, not bond-order, formal-charge,
stereochemical, geometric or environmental-protonation validation. Standard twenty
names retain their existing catalogue and approximate pH model. MSE/SEP/TPO/MLY
retain their separate CCD-derived heavy-only references. A sequence/reporting
parent never substitutes for an exact chemical template. Unsupported CCD/legacy
meanings and incompatible heavy layouts remain unassessed. An absent convention
on a reviewed ambiguous scalar name raises instead of choosing Amber or legacy.

`get_expected_heavy_atoms` and `get_expected_hydrogens` retain their existing
positional arguments and add the normal validation switch plus keyword-only
`naming_scheme`. Expected H names for explicit Amber states preserve their
side-chain state across pH changes. Named-state terminal completion remains
unassessed; matching an inventory is not a claim that placement coordinates are
available. Native heavy repair skips states without exact placement references;
native H completion reports unsupported terminal/layout cases with the existing
structured warning. No terminal H naming or parent coordinates are invented.
The standard pH thresholds and native placement algorithm are unchanged.

The molecular coverage audit is deliberately permissive: undeclared ambiguous
groups are reported as unassessed. Its reference cache is keyed by both label
and convention, and its identity/provenance preserves the declaration, original
catalogue variant positions and state-reference checks. Identical labels with
different conventions cannot share a cached chemical assessment. Public molecular
queries preserve selected source group indices, including H5MSM input.

### Bond candidates, raw readers and external engines

The two public group/amino-acid reference-bond maps accept the declared convention.
Named states use checked internal layouts. Standard HIS can use checked internal
histidine variants when observed H names require them; the former search across
unrelated catalogue entries is removed. Existing index mapping, duplicate-name,
scalar-ion and sorting behavior remains covered by the reference-map guards.

`build.get_missing_bonds` passes stored declarations to templates and derives any
required group type locally without rewriting stored metadata. With templates
enabled, an undeclared contextual label cannot fall through to generic geometry.
Explicit geometry-only operation remains available and does not select a naming
template or certify a bond. The optional PyTraj route requires explicit Amber
context for reviewed state labels; it cannot silently translate CCD/legacy names.

Raw OpenMM, GRO, NGLWidget and mmCIF readers remain able to load undeclared labels.
They preserve source names/edges, omit automatic missing-bond inference for the
unresolved contextual groups and do not mark that omitted connectivity complete.
The mmCIF early per-group reference lookup follows the same policy. Synthetic
OpenMM and mmCIF controls distinguish permissive loading from a later explicit
chemical-template query, which still requires context.

OpenMM/PDBFixer preparation wrappers refuse reviewed contextual labels until a
source-naming adapter is delivered, and reject incompatible declarations on curated
modified names. Selection-aware wrappers preflight only selected groups. The
fixed-state RDKit route instead follows ChemicalStates and bypasses label-based
preparation. No new optional dependency or dependency floor is introduced.

### Support libraries and independent controls

The two scalar expectation boundaries use a scoped ArgDigest registry for names,
finite dimensionless pH, actual boolean flags, supported schemes and the trusted
validation switch. Reference-bond validation reuses the same scheme authority.
Existing DepDigest guards and lazy optional-engine imports remain in force.
SMonitor carries argument, unsupported-method, invalid-reference and unassessed
preparation diagnostics. Private reference selectors are not decorated.

Optional Ackredit records only the reference datasets actually used: the historical
catalogue content identity, pinned Meeko fragment source, Amber naming dataset or
curated CCD heavy template as applicable. Reading data does not claim execution
of Meeko or Amber software. Optional-provider failure preserves the result through
the existing diagnostic. These scalar references carry atom names/graphs rather
than physical quantities; the existing geometry paths keep PyUnitWizard conversion.

`tests/element/group/amino_acid/test_naming_atom_expectations.py` and
`tests/build/test_naming_preparation.py` supply explicit state/H expectations,
missing-context refusal, terminal exclusions, mixed per-group declarations,
H5MSM selection, native addition/removal, external preflight and reader controls.
Negative controls corrupt bundled candidate connectivity/H counts/H parents and
require a structural diagnostic rather than a fallback. These two modules join
the existing smoke command, without a second pytest invocation. Existing map
validation and public scientific pair assertions remain intact.

### Receiving history and documentation

Early new-test runs expose fixture mistakes: an old HID example lacks its now
required declaration; native-placement tests accidentally use the default OpenMM
engine; and a reader assertion tries an unsupported ChemicalStates count property.
Those fixtures use explicit context/engine and the public count query. A real
warning-call error passes an unsupported `caller` keyword to the existing
UnassessedResidueWarning; the call site is corrected without changing its API.
Reference-map test doubles now accept and forward the new context argument.

The first broad 2,092-case run passes 2,080 with five failures and seven setup
errors. Nine cases need public PDB downloads blocked by the sandbox, two failures
are outdated template doubles, and one is a real reference-routing defect: native
md_1u19 bond candidates give 5,633 pairs against PyTraj's 5,632. The fixture now
declares the Amber labels it intends, and the implementation uses that context.
Both count and full pair equality remain exact at 5,632; no assertion is weakened.
The separate network-enabled retry passes all twelve selected cases. A subsequent
2,107-case run passes 2,106 and exposes the raw-reader missing-context regression
fixed above. Earlier failed process results remain separate local evidence.

Ten revised tutorials execute all 57 code cells in the shared Python 3.14
environment. Jupyter uses the existing local-socket permission; no auxiliary
environment or dependency installation is created. Their explanations distinguish
raw catalogues, bounded chemical references and unsupported preparation. The
conceptual User Guide, chemical-coverage page, Cookbook, course and docstrings
reflect those limits. The course's executable cells, stored results and notebook
metadata remain identical. The isolated documentation fixture links the actual
new tutorial targets; its no-warning assertion and broken-link negative control
are retained.


### Final local receiving for the preparation block

- **2,945 tests pass** in the affected preparation/group/reader selection, with
  no failures or omissions, on Linux/Python 3.14.7. Four workers complete in
  210 seconds. The 259 warnings include 59 legacy H5MSM notices, the three
  deliberately injected attribution failures and existing unassessed-placement,
  attribute-drop, atom-name, protonation and pandas diagnostics. No warning or
  assertion is suppressed for this run. Existing unmarked public-PDB tests use
  the network-enabled execution route; the `not network` marker selection alone
  does not make this suite fully offline.
- **333 tests pass** with public ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0
  and Ackredit 0.9.0, using the previously verified archive/import-path harness.
  The same entry-point-only SMonitor harness exclusion remains under #524; it
  excludes no runtime or scientific assertion. Two workers complete in 25 seconds
  with one existing attribute-drop warning. The additional controls include the
  raw-reader policy and the actual dataset-credit path.
- **514 documentation/command controls** pass with 512 existing Sphinx
  deprecations; **four doctest items** pass. Ten tutorial executions cover
  **57 code cells**. The unchanged course executable payload and metadata are
  verified against the parent commit.
- Whole-tree Ruff lint and formatting (**4,351 files**), all **247** checked
  public docstrings, the **278-symbol** registry, four approved signature changes,
  offline naming-asset regeneration and dependency/import-contract checks pass.
  Devguide/index and final staged-diff checks are run before the local commit.
- The native binary retains SHA-256
  `f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c`.
  The four unrelated human API-stub edits retain their prior hashes and remain
  outside this change. Support-library checkouts, runtime dependency floors,
  pinned scientific assets and public packages are unchanged.

The final broad command in the existing development environment is:

```bash
python -m pytest --receptor=llm -n 4 \
  tests/build tests/element/group \
  tests/physchem/test_get_peptide_chemical_template.py \
  tests/physchem/test_chemical_template.py \
  tests/native/test_group_naming_schemes.py \
  tests/basic/convert/test_source_naming_scheme.py \
  tests/form/openmm_Topology \
  tests/form/mmcif_PdbxContainers_DataContainer \
  tests/form/nglview_NGLWidget -m 'not network'
```

The published-provider probe selects the two new modules plus
`tests/element/group/test_reference_bond_map_validation.py`,
`tests/build/get_missing_bonds/test_pytraj_resource_lifecycle.py` and
`tests/form/mmcif_PdbxContainers_DataContainer/test_chemical_state_fidelity.py::test_undeclared_contextual_group_does_not_gain_edges_or_complete_status`.
It retains the previously recorded source-environment floor-import method, adds
`-p no:smonitor` for that distribution-entry-point mismatch and uses two workers.
Current-provider tests retain the normal diagnostics plugin.

Final local JUnit evidence under `.pytest_cache/group-name-resolution-549/` is
`preparation-extended-final.xml`, `preparation-provider-floors-final.xml`,
`preparation-documentation-final.xml` and `preparation-doctests-final.xml`.
The earlier failed/partial processes have separate filenames and are not
relabelled as passing. This work does not fix the optional-environment `pip check`
limitation under #524 or qualify an installed artifact, other interpreter or
platform. No push, hosted CI, tag or package publication accompanies this block.

**Next:** audit remaining producers such as `build_peptide`, then complete D5's
conversion/lifecycle fidelity matrix and D6's old scalar/addon cutover. Unsupported
state terminal completion and external naming translation remain explicit limits;
they are not silently certified by successful reference inventory queries.
