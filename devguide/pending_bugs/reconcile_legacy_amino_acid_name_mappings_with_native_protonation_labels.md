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
maintainer accepts the explicit scheme design below. Native public cutover is
delivered in D6 below; addon-expansion receiving and final acceptance remain due.

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
preparation boundaries. The old scalar one-letter helper is removed by D6 below; both initial
unqualified helper behaviors above are historical reproductions, not the current API.

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
- [x] **D4 — native producers and consumer propagation.** Producers that
  explicitly know their input vocabulary declare it. Propagate the conversion
  argument through selected direct and MolSys routes. Resolve declarations per
  selected group, preserve ordering/repetitions and refuse ambiguous mixed
  overrides. Audit sequence, recognition, missing-atom/H and preparation callers
  so a name-only lookup cannot select chemistry implicitly.
- [x] **D5 — persistence and lifecycle receiving.** Exercise mixed schemes,
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


## D4 construction and final producer review — 2026-11-05

**Implemented and contract-tested locally.** The bounded modern producer/consumer
propagation in D4 is complete. D5's final fidelity matrix, D6's old scalar/addon
cutover and D7 receiving remain open; #549 is not closed. External naming adapters
and unsupported construction/terminal chemistry remain explicit refusals rather
than unimplemented promises of this correction.

### Construction boundary

`build_peptide` preserves its three existing positional arguments and adds
`skip_digestion=False` plus keyword-only `from_naming_scheme=None`. The normal
ArgDigest boundary validates them; SMonitor supplies structured context/conflict
and unsupported-reference diagnostics. A private input reader obtains exact
ordered labels from native inventory, typed dictionaries, H5MSM topology-only
reading or the ordinary topology conversion route. Native queries copy no source
coordinates or chemical domains. String prefixes take precedence over guessing:
`amino_acids_1:ALA` is A–L–A, while `amino_acids_3:ALA` is one alanine.

Known source declarations must agree with an explicit override. Missing context
on reviewed ambiguous labels is rejected before template loading or optional
engine startup. Unsupported modified/CCD/legacy meanings do not select a
same-spelled Amber reference or a reporting parent. Construction is bounded to
the standard twenty names, eight reviewed Amber-state labels and existing caps.
It does not infer source convention from file form or selected engine.

Native products explicitly declare the Amber vocabulary used by their
construction references. The LEaP route first reads its result into native
inventory, declares that producer context and then exports it, still within its
owned scratch directory. This also repairs its former Topology-output access
through `.topology`. Its resource guard now verifies both native receiving and
export; either failure retires the scratch. Construction creates a new molecular
system from labels; it does not preserve/repair the source chemical state.

When the construction database is unavailable, native construction uses the
verified exact-name state catalogue variant rather than the first raw compound
with the same name. The existing approximate fallback coordinates and warning
remain. No geometry/minimization, force-field parameterization or disulfide-pairing
algorithm is introduced or certified. The historical construction data have no
pinned upstream revision: their bundled hash identifies the actual bytes, not a
verified contemporary Amber release.

### A real construction/preparation mismatch

An executed round trip exposes an additional defect: the Amber-derived HID
constructor has HB2/HB3, while the sole previously admitted historical reference
has HB1/HB2. Native H addition appends HB1 to an already complete HID, giving three
hydrogens on CB. This is a demonstrated wrong candidate/addition, beyond the
initial naming-only reproduction. ACE similarly uses H1/H2/H3 in the construction
data versus HH31/HH32/HH33 in the older placement reference.

The private construction-data reader is now shared by construction and reference
selection, with no import of an optional engine or a public build API from the
reference layer. Checked state alternatives include the construction layout only
when its heavy names/connectivity and per-parent H counts agree with the bundled
Meeko fragment. A corrupted construction layout raises even if the raw catalogue
is valid; a corrupted raw state still raises instead of being concealed by the
additional source. Source assets and their geometry are unchanged.

Observed H names choose a compatible layout. The old first checked historical
layout remains the default with no observed names. Declared Amber caps similarly
match existing names between supported layouts. A group convention does not
force an atom convention: even an Amber-declared cap already using HH31/HH32/HH33
must not gain alias H1/H2/H3. Tests exercise both the produced and renamed layouts.
The eight state examples are idempotent under native H addition/reconciliation;
this inventory result does not certify terminal states, charges or geometry.

Chemical coverage retains its honest ambiguity when several H-name sets exist,
even when one candidate exactly matches the observed names. Existing raw variant
indices remain unchanged; added construction candidates receive indices after
the raw range. `variant_sources` associates every candidate with its actual
resource and digest. The primary resource/provenance remains the historical
catalogue; no synthetic index is presented as a position inside that raw file.
Content hashing is reused within an audit, rather than re-reading assets for
every group/variant.

### Producer audit disposition

| Boundary | Delivered or preserved behavior |
| --- | --- |
| Native sequence/FASTA group construction | Canonical alphabet groups declare `sequence`; other unknown labels do not gain a chemical convention. Source declarations precede defaults. |
| Fixed peptide chemical templates | Explicit Meeko-derived state construction already declares `amber`; ChemicalStates remains the assignment/connectivity owner. |
| Native/LEaP peptide construction | Exact source labels are checked before constructing new chemistry; known producer labels declare `amber` before native transport/export. |
| Atom append/repair | Existing group declarations are projected unchanged; adding atoms does not reinterpret a group name. |
| Added groups/caps and generic builders | Existing D2 rules retain unknown context for newly introduced groups unless a producer explicitly declares its known vocabulary; no convention is inferred from a resulting native class. |
| Foreign raw readers | Source labels and explicit bonds are retained; no file-form/engine heuristic supplies missing context. |
| Modern sequence, recognition, parent, atom/H and bond-candidate consumers | Share the reviewed naming authority and stored per-group declarations; unsupported reference/engine translation is explicit. |
| Old scalar one-letter helper and addon manifest/mirror | Deliberately still D6 work; they are not certified or silently retained as a second authority. |

The audit finds no remaining direct amino-acid raw-catalogue selection in modern
construction/preparation outside the owning private reference layer. The retained
raw inspection API and unrelated water/ion/cap/small-molecule catalogues are not
renamed as universal chemical-state selectors.

### Support libraries and scientific provenance

ArgDigest handles source scheme/skip validation once at the public boundary;
private data/input helpers are not decorated. Existing conversion/optional-engine
DepDigest contracts remain in force, with no new dependency or floor. TLeap
executable handling remains in its own wrapper; bundled data do not require
AmberTools, Meeko or an executed LEaP process. Geometry extraction and standardization
retain the existing PyUnitWizard boundary; naming metadata are dimensionless.

Optional Ackredit credits the bundled construction dataset or fallback catalogues
actually used. State-layout verification also credits its Meeko/Amber data and
construction source. Native construction claims no executed external engine.
Provider absence/failure preserves the result and uses the existing SMonitor
diagnostic. No automatic hooks, enrichment or journals are enabled.

### Receiving and corrected test premises

The first 319-case run passes 313 and fails six: four old geometry fixtures intend
Amber HIE/HID/HIP/CYX but omit their declaration, while two new LEaP mocks use a
non-exported root MolSys class. The fixtures now declare Amber without weakening
their geometry/count checks; mocks import the actual native class. The first
53-case new-module run passes 48 and exposes three analogous root-Topology fixture
mistakes, an incorrect exception-class expectation and a test that incorrectly
expects unique/complete H assessment. That last expectation is corrected to retain
the actual ambiguous result and inspect the exact matching candidate.

The next 372-case run passes 367 and fails five tests: three compare a base pandas
copy to the native Groups_DataFrame subclass, and two incorrectly assert that
one-letter strings containing H have no HIS group. Source values/dtypes remain
identical; only irrelevant frame-class comparison is disabled. The sequence tests
now assert all ten independently specified group labels, and require explicit
three-letter input containing a four-letter token to fail. The former tests had
merely accepted HISE/HISD strings as ten one-letter groups while describing them
as histidine aliases; no such alias chemistry is certified.

After those corrections, **373 focal cases pass**. The final affected selection
passes **3,000 cases** on Linux/Python 3.14.7 with four workers in 213 seconds,
without failures or omissions. Its 263 warnings retain 59 legacy-file notices,
three deliberately injected attribution failures, four geometry warnings and the
existing preparation/attribute diagnostics. Two later source-reading/preflight
guards pass separately; they do not modify runtime code after the wider run.

The published-provider selection passes **221 cases** with ArgDigest 0.14.0,
DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 using the previously verified
archive/import-path harness, two workers and the same entry-point-only SMonitor
plugin exclusion documented under #524. Its five warnings are four geometry
notices and one existing attribute-drop notice. Current-provider receiving keeps
the ordinary diagnostics plugin enabled. No provider source or floor is changed.

Two revised tutorials execute all **18 code cells** in the existing environment.
The course's executable cells, outputs and notebook metadata remain identical;
only explanatory Markdown is added. Initial documentation receiving passes 513
of 514, with one failure because that new Markdown cell lacks its required stable
ID. The ID is added; all **497 notebook-schema cases pass**. The isolated source
boundary and its negative control remain intact. **Three doctest items pass**.
Final consolidated documentation receiving and governance checks are recorded
below. No auxiliary environment, hosted CI, push, tag or package publication is
claimed by these local results.

Local JUnit evidence is under `.pytest_cache/group-name-resolution-549/`:
`producer-initial.xml`, `producer-new.xml`, `producer-followup.xml`,
`producer-focus-final.xml`, `producer-extended-final.xml`,
`producer-provider-floors.xml`, `producer-input-followup.xml`,
`producer-documentation.xml`, `producer-notebook-schema-followup.xml` and
`producer-doctests.xml`. Failed processes remain separate evidence; their test
premises and the real H-alias defect are distinguished above. The broad command
is the previous preparation receiving selection, now including the new producer
module through `tests/build`; its existing unmarked PDB cases still need network
access. The maintained smoke command includes the producer module in its single
pytest invocation.

**Next:** complete the D5 conversion/lifecycle matrix, then coordinate the D6 old
scalar/addon cutover and D7 final acceptance. The environment-closure limitation
in #524 and installed-client/release qualification under #334 remain separate.


### Final documentation and attribution receiving

The consolidated documentation/command selection now passes **514 cases** with
512 existing Sphinx deprecations. No warning suppression or weakened link/schema
assertion is introduced to repair the missing notebook cell ID. The three
executed doctest items and eighteen executed tutorial cells remain as above.

Final review adds explicit dataset credit to the selected Amber cap-layout path,
which was already recognizing names correctly. The completed 3,000-case process
precedes only that optional-attribution addition and the later extra guards;
its scientific naming/geometry code is unchanged. After that final addition,
**62 producer/resource tests pass with current providers and the same 62 pass
with published floors**, covering real cap attribution, optional-provider
absence/failure, idempotent H handling, source-only H5MSM reading and preflight.
These bounded follow-ups are recorded separately as
`producer-cap-attribution-final.xml` and `producer-cap-attribution-floors.xml`;
the earlier broader process is not mislabelled as a new exact-candidate run.

Whole-tree Ruff lint/formatting (**4,353 files**), all **247** checked public
docstrings, the **278-symbol** API registry, the one approved construction
signature extension, offline naming-asset equality and dependency/import-contract
checks pass. Devguide/index and diff checks pass. The native binary retains its
previous recorded SHA-256, as do the four unrelated human API-stub edits, which
remain outside this work. The construction asset remains unchanged at SHA-256
`afb6989a938d118ac6360dbb86548d45e9d6a30b8f02d009e42e1320febe5e79`.
Local checkouts and archives are not an installed-candidate qualification; D7 and
#334 retain their actual exact-source/artifact gates.


## D5 persistence and lifecycle receiving — 2026-11-05

**Implemented, contract-tested and parity-tested locally.** D5 is complete within
this naming contract. D6 old scalar/addon cutover and D7 final acceptance remain
open; #549 is not closed. Scientific profile validation and exact installed-package
qualification remain separate from metadata/representation fidelity.

### A demonstrated preflight omission

A named Topology at f201693ba reports `equivalent` to PDB, OpenMM Topology,
Structures and one-letter text without mentioning that those representations
cannot retain its group-name declaration. Equal labels cannot substitute for the
vocabulary. The new shared private naming-fidelity audit reports an `unsupported`
`group_naming_schemes` issue in the topology scope for the relevant selected
groups. Partial coverage gains that scope without being promoted to exhaustive.
Native targets already admitted as exhaustive retain their actual preservation
obligation, protected by real output/round-trip assertions.

`get_conversion_report` now accepts keyword-only `from_naming_scheme`, preserving
all previous positional arguments. It uses the same prospective interpretation,
selected-group conflict checks and naming preflight as `convert(strict=True)` /
`convert(return_report=True)`. A supplied convention is not assigned to the source
by preflight. Empty selections and unknown selected declarations do not acquire
a loss merely because another group has context. Raw one-letter and three-letter
text interpretation continues through the existing source-conversion authority.

Normal conversion retains its existing policy of permitting detected losses;
strict conversion refuses before creating/replacing the target. Native inventory,
the supported typed dictionaries, editable native inventory and H5MSM preserve
naming context. PDB/OpenMM receive real round-trip controls: labels survive,
missing source convention stays unknown. No reader infers it from file format.
The same-format foreign source-interpretation route is not the ordinary byte-copy
identity path: its report cannot claim exhaustive byte preservation. A group-free
SDF inventory does not gain invented naming rows under that interpretation.

### Coupled interaction evidence

The lifecycle policy already invalidates attached evaluated interactions when a
result gains a missing group declaration. Preflight previously omitted that
effect, including a meaningful evaluated-empty analysis. It now reports selected
coverage invalidation as an `interactions` issue of kind `invalidation`. Strict
mode refuses before publishing a native result or H5MSM file; ordinary conversion
retains the accepted invalidation behavior. Original sources and snapshots stay
unchanged. Matching declarations, already unevaluated analyses and coverage
outside the selected structures do not invent an invalidation loss.

The audit also exposes named analyses omitted by targets without their storage,
including an empty named result whose method/definition is still information.
Retaining only stable topology, coordinates or an editable builder is not a
lossless conversion of that named-analysis domain. These omissions are reported
as `unsupported` in the interactions scope. This closes a related false exhaustive
claim for admitted native projections without changing their runtime copy policy.

The new metadata helper reads names and, when needed, evaluated-structure indices.
For typed dictionaries it decodes only the declared coverage array through the
existing typed-array decoder, not relation/occurrence columns. A negative control
observes that boundary. Other report scopes can still read source payloads; this
is not an out-of-core or total-preflight performance claim. The report neither
runs an interaction detector nor changes scientific provenance.

### Actual lifecycle receiving

`tests/conversion_truth/test_group_naming_fidelity.py` has **63 controls**, including:

- the same GLH label under Amber, legacy, unknown and sequence context;
- actual native/typed/H5MSM output transport, unknown legacy declarations and
  selected prospective context without input mutation;
- empty selections, source group maps, nonconsecutive atom/structure selections,
  explicit atom permutation and atom-free group reorder/merge;
- independent shallow/deep/native snapshots and JSON-backed topology transport;
- full transport/extraction with two chemical states, a nontrivial state/structure
  map, named occurrences and evaluated-empty versus unevaluated structures;
- strict destination refusal with an absent or existing PDB target;
- real OpenMM label round trip without invented naming context;
- prospective naming invalidation on native and dictionary inputs, including
  selected H5MSM publication, stable original snapshots and coverage-only reads;
- named-analysis omissions from Topology/TopologyDict/Structures/MolSysBuilder;
- malformed source-context arguments and clear missing-inventory diagnostics.

The new module joins the maintained smoke invocation. Existing native naming and
H5MSM schema guards remain intact: dictionary 0.3, H5MSM root 0.5/topology layer 4,
unknown older context and rejection of unsupported/malformed registries are not
weakened. No new wire version or data asset is required by this phase.

### Partial systems and corrected test assumptions

The first 587-case run passes 586 and fails the old audit-scope expectation on an
all-unknown topology. The implementation now leaves that historical partial scope
unchanged when there is no known declaration to assess; the expectation remains.
The first 37-case new-module run passes 32 and exposes incorrect fixture premises:
atomic extraction retains canonical source order rather than acting as explicit
permutation; PDB groups follow serialized atom order; a strict MolSys-to-TopologyDict
projection also loses structures/chemistry; and merging pure Topology inputs
returns Topology. The controls now assert actual source maps/IDs, use explicit
atom permutation for that operation, and use a pure Topology input when requiring
a lossless strict inventory conversion. None of those existing semantics changes.
Later fixtures use the native class imports and atomic replacement of the readonly
interaction mapping, rather than trying to assign through its MappingProxyType.

Additional receiving exposes real missing-domain crashes: the MolSysDict audit
reads mechanics attributes through None; the PDB audit reads absent structures
and chemical states. These audits now inspect only supplied domains, including
zero-state chemistry. They do not create assignments, coordinates or mechanics
values to complete a preflight. A restored empty mechanics container is not
misreported as persisted mechanics data. The source-interpretation audit reduces
to available inventory rather than refusing a valid group-free SDF merely because
its static form lacks group labels. Pure structures still cannot supply naming
context. The SDF negative control explicitly expects no invented declaration.

The first tutorial execution catches the missing-chemical-domain PDB crash;
that error is recorded here. The runner's current log describes the later
successful execution, not the earlier failed attempt. One initial
notebook-schema check rejects a cell ID added to the older-format convert
notebook. That cell follows its existing schema without changing the notebook
version or executable payload; course cells retain their required modern IDs.
The final no-warning/broken-link and notebook-schema assertions are unchanged.

### Support-library and units boundaries

ArgDigest validates the new public keyword and existing selection/skip contracts.
Private audit/source helpers are undecorated and reuse the shared naming authority.
SMonitor supplies the existing argument/conversion diagnostics; no new provider
API or dependency floor is needed. DepDigest guards remain on reached optional
conversions with lazy imports. This phase introduces no scientific method that
earns a new citation: metadata inspection does not claim an executed engine or
chemical reference calculation. Existing optional Ackredit attribution and stored
provenance remain untouched. Naming metadata/indices are dimensionless; coordinate
and PDB-capacity inspection retains explicit PyUnitWizard units. The transport
controls compare coordinates in nm rather than stripping their application unit.

### Final local receiving

- **4,651 affected tests pass**, no failures or omissions, on Linux/Python 3.14.7
  with four workers in 182 seconds. This is the final runtime revision, including
  named-analysis projection/invalidation and the partial-domain guards. Its 1,029
  warnings retain 977 legacy H5MSM notices, fourteen pandas notices and existing
  structural/parser/unit/import diagnostics. An import-time binary-size warning
  remains a shared-environment observation, not a demonstrated MolSysMT native
  backend defect or installed-package qualification; #524 retains environment
  closure work. No warnings are suppressed to obtain this result.
- **236 tests pass** with public ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0
  and Ackredit 0.9.0 using the previously verified archive/import-path harness.
  Two workers take 17 seconds with one existing attribute-drop diagnostic. The
  same entry-point-only SMonitor plugin exclusion remains under #524; no runtime
  or scientific assertion is excluded. Current-provider receiving retains its
  normal diagnostics plugin.
- **514 documentation/command controls** and **three doctest items pass**.
  The revised naming tutorial executes all **nine code cells**. The larger
  conversion tutorial and course retain identical code cells, saved results and
  notebook metadata; their new material is explanatory Markdown only.
- Whole-tree Ruff lint/formatting, public docstring/API/signature validation,
  dependency/import-contract and final devguide/index/diff checks are run before
  the local commit. The native binary and four unrelated human API-stub edits
  retain the hashes recorded above and remain outside this work. No provider
  checkout, runtime floor, scientific asset, source format or artifact changes.

The final command in the existing environment is:

```bash
python -m pytest --receptor=llm -n 4 \
  tests/basic tests/native tests/conversion_truth tests/form/file_h5msm \
  tests/_private/test_conversion_report_scopes.py \
  tests/_private/test_conversion_fidelity_audit.py \
  tests/interactions/test_public_molsys_h5msm_workflow.py -m 'not network'
```

Its existing unmarked PDB downloads use the authorized network-enabled runner;
the marker alone does not make it offline. Local JUnit under
`.pytest_cache/group-name-resolution-549/` retains
`fidelity-received-final.xml`, `fidelity-floors-final.xml`,
`fidelity-documentation-final.xml` and `fidelity-doctests-final.xml`.
Earlier failed and intermediate processes keep separate XML, including the
missing-domain and corrected-fixture evidence. The 4,637-case earlier broad pass
precedes the final analysis audit and is not substituted for the 4,651-case run.
No hosted CI, push, tag or installed/release qualification is claimed.

**Next:** D6 removes the competing old scalar code helper and reconciles its
consumers/docs/addon mirror, then D7 verifies the combined exact source before
issue closeout. D5 neither stabilizes unassessed chemical methods nor closes #334.


### Final governance checks for D5

Whole-tree Ruff lint and formatting (**4,355 files**), the **247-function**
docstring fidelity/content gate, the **278-symbol** API registry and the one
approved preflight signature extension pass. Dependency import/contract and
offline naming-asset equality checks pass. Devguide/index and staged diff checks
pass before the local commit. The scientific assets, native binary, dependency
floors and four pre-existing human API-stub edits are unchanged. The larger
conversion tutorial and course retain their exact executable payloads/metadata.
These local results do not qualify a public artifact or waive D7's combined gates.


## D6 native public cutover and addon receiving — 2026-11-05

**Native cutover implemented; coordinated expansion still pending.** The sole
public scalar code query is `molsysmt.element.group.get_1_letter_code_from_name`.
The former amino-acid export and implementation are removed, without a runtime
alias. Historical values remain available through explicit `naming_scheme='legacy'`;
this is a naming-contract correction, not a claim of unchanged implicit semantics.
The old unexported amino-acid classifier is also removed: it imported an absent
legacy data package and called a dictionary as a function, and no live consumer
used it. The supported group classifier/import alias remains intact.

### Consumers, documentation and classifications

The canonical alphabet tests now call the group helper with explicit `sequence`.
Existing modified-name controls retain their historical expected values under
explicit `legacy`; primary-source semantic controls continue to distinguish
Amber, CCD, sequence and historical meanings. A public guard checks one supported
function identity, absence of the old export/module and literal Amber/legacy GLH
results, including refusal without context. No scientific data table is changed.

The duplicate tutorial becomes a narrative migration page at the same published
HTML location with its original tutorial anchor. The canonical executed tutorial
retains the original twenty-code demonstration, adds all six extended symbols,
and preserves naming, source-map, identity, conflict and disk examples. Related
recognition/parent links move with that content. API navigation, its historical
migration page, the manifest, User Guide, Cookbook and Module 12 explain the new
route. The course's executable cells, outputs, IDs and metadata are unchanged.
The two group package scopes are tracked explicitly by the stability registry;
all twenty newly enumerated exports retain their inherited Experimental status,
and the derived support-tier view follows that same authority. This neither
promotes scientific coverage nor invents a semantics-preserving namespace move.

### Existing addon conversion boundary

The first existing signature guard reproduces two failures and one pass: the
bound conversion/preflight signatures lag their updated native providers.
Both wrappers now expose and forward keyword-only `from_naming_scheme=None`,
retaining all original positional arguments/defaults. ArgDigest still delegates
scientific validation to the native function; no flag is forced, input is
reinterpreted locally or metadata inferred from the Viewer. New real-view cases
check independent declarations, selected-coverage invalidation, unchanged source
coordinates/analysis identity, scene and synchronization state, and matching
native conflict/unsupported-profile diagnostics.

The first new 29-case module run has 27 passes and two failures because its
invalid-profile fixture expects ArgumentError rather than the distinct native
ArgumentChoiceError. The fixture now specifies the intended class separately;
provider behavior is unchanged. Failed and final runs have separate JUnit files.

### PR #543 adaptation handoff

Inspected published expansion head:
`a1dbe0fb67373c32b0ca3276aa40f52250ff9554`, branch
`addon/element-utilities-20261103`. Its sources are read without modifying its
working tree or merging the unrelated build/mechanics expansion. Before receiving
that PR on the corrected native source, its owner must make these changes:

| Surface | Required receiving change |
| --- | --- |
| `element.group.get_1_letter_code_from_name` | Move the wrapper from `_AminoAcidTools` to `_GroupTools`; mirror `(name, naming_scheme=None, skip_digestion=False)` and forward all three arguments. Retire the old addon path too. |
| `element.group.get_group_type_from_group_name` | Retain the original arguments and forward keyword-only `naming_scheme=None`. |
| `element.group.amino_acid.get_standard_name` and `is_amino_acid` | Mirror native naming_scheme/skip_digestion instead of adding an addon-only skip flag. Native recognition/parent semantics stay authoritative. |
| Group/amino-acid `get_bonded_atom_pairs`, `get_expected_heavy_atoms` and `get_expected_hydrogens` | Mirror their actual keyword-only naming_scheme plus native skip flag; preserve every prior positional input, unit and mapping behavior. |
| `build.build_peptide` | Forward keyword-only `from_naming_scheme=None` and the native skip flag. Preserve exact source labels, explicit state/reference limits and independent ownership. |
| Existing `basic.convert` and `get_conversion_report` | Retain the native-owner changes delivered here when merging `_basic.py`; do not restore the older signatures. |
| Discovery, inventory, help and tests | Move the old path rather than adding an alias; adjust namespace sets, direct native-signature comparisons, forwarding and explicit context examples. Recompute live exposure instead of editing historical receipts. |

Exact native signatures are available through `inspect.signature` after importing
the corrected provider. In this main worktree the live inventory remains
155/244 paths, including zero of 57 element paths; only the canonical code path
is declared. The expansion's earlier 57/57 receipt does not qualify these changed
provider bytes. The new inventory guard rejects reintroduction of the old
amino-acid declaration. No new addon source file is added on main, so its strict
TOOLS_FILES distribution registry is unchanged. The expansion keeps its separate
new-file registry and must retain it while adapting its mirrors.

The owning #421/#543 handoff and final combined receiving remain necessary for
D6; no downstream compatibility or package qualification is claimed yet.


### Final local receiving for the native cutover

On Linux/Python 3.14.7, **9,062 affected native tests** pass in 534 seconds with
four workers, covering element/build/topology/native/basic/conversion/physchem,
H5MSM and the public interaction persistence workflow. The **2,699 existing addon
and integration-command controls** pass in 257 seconds with four workers.
Neither run has omissions, failures or errors. The native binary is unchanged;
these are final native and final addon source checks, not an installed-pair gate.

The native run retains 1,435 warnings, predominantly 1,143 legacy-file notices,
45 pandas notices and existing assessment/drop/PBC/GPU/unit/parser diagnostics,
three controlled Ackredit failures and the already observed environment
binary-size warning tracked separately under #524. Addon receiving retains
1,620 warnings: 1,613 legacy notices, four attribute-drop notices, two deliberate
unknown-digester controls and one determinant warning. No warning is suppressed
for test receiving. The tutorial retains its existing presentation-only warning
filter, separate from the tests.

Published-floor receiving passes **241 naming/alphabet/sequence cases** and the
**29-case addon conversion module**, with no omissions. Its thirty warnings are
legacy-file notices in the addon fixtures. It uses ArgDigest 0.14.0, DepDigest
0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 from the already verified public-payload
harness. The same entry-point-only SMonitor pytest-plugin exclusion remains
bounded by #524; normal current-provider receiving keeps that plugin enabled.
No support-library source or dependency floor is changed.

Final documentation receiving passes **548 controls** and **three doctest
items**. The small canonical tutorial executes **ten code cells** in the
existing environment. The first kernel attempt is blocked by the sandbox's
local-socket restriction; authorized socket-enabled execution succeeds. The
first documentation run has four failures from a disconnected historical API
page, its short heading underline and the missing transferred related-links
block. The migration page is connected, its heading corrected and the original
links preserved on the canonical tutorial; the original guards and negative
controls remain unchanged. Failed XML remains separate from final receiving.

Whole-tree Ruff lint/format (**4,353 files**), **246 public docstrings**, the
**298-symbol** registry, derived tiers, signature/dependency/import-contract,
profile-generation, devguide/index and diff checks pass. The four unrelated
human API stubs retain their recorded hashes. ArgDigest/SMonitor validation and
optional Ackredit remain at the canonical native boundary. This cutover adds no
physical quantity, heavy backend or optional dependency: there is no additional
PyUnitWizard/Rust/DepDigest capability to invent.

The [receiving receipt](../../devtools/data/group_naming_cutover_receiving_549_20261105.json)
retains final code/test hashes and JUnit identities in
`.pytest_cache/group-name-resolution-549/`. Native/runtime tests and public
source attribution are distinct from hosted exact-source, expansion and
installed-candidate qualification. D6's expansion receiving and D7 stay open;
#549 is not closed by this checkpoint.


### Source checkpoint and miniature course-site receiving — 2026-11-05

Published source d3650cc09735ccfc7bf02d35ca4e0a746f83f96f passes all seven
routine push workflows, including smoke 42074491673. The #543 adaptation
handoff is published as PR comment 6664622011; no receiving acknowledgement or
new expansion source is inferred from that delivery. Full matrix, combined
expansion and installed-candidate acceptance remain separate D7/#334 work.

While receiving the subsequent alternate-site corrections (#569–#571), the
course navigation test exposes a miniature-site fixture omission from the
naming-guide addition: real course links use its existing anchor, but the fixture
never copies that target. The fixture now copies the actual guide heading/label
and asserts the rendered destination. No production label is invented and no
undefined-reference warning is ignored. This is bounded #549 documentation
receiving, not a new naming-runtime change or admission of #543.

The final course/navigation/schema selection passes 498 cases. Its intermediate
link assertion incorrectly treated saved notebook outputs as navigation;
the final guard uses only the Markdown navigation excerpt, requires the two
actual source modules to retain the naming reference, and checks their exact
rendered page/anchor destinations. Missing real targets still fail Sphinx.
