---
summary: Design H5MSM 0.6 persistence for MolecularMechanics
issue: uibcdf/molsysmt#256
status: active
opened: 2026-09-29
closed:
verification: measured
area: [form, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# H5MSM 0.6 MolecularMechanics persistence

**Reported:** 2026-09-29, during the H5MSM 0.5 pre-1.0 scope review.
**Status:** Active bounded pre-1.0 design, authorized by the maintainer on
2026-11-08. The earlier post-1.0 calendar restriction is superseded; no new file
schema or release is made public by that authorization alone.

## What

Design a versioned H5MSM 0.6 representation for the native
`MolecularMechanics` domain with an explicitly bounded parameter model.
The [H5MSM 0.5 contract](h5msm_0_5_modular_layers.md) intentionally contains
no mechanics layer. The maintainer now permits this work before MolSysMT 1.0.

## How

First define which force-field settings, atom parameters, bonded terms,
constraints, energies, and parameterization provenance belong to the native
domain. Then specify their typed file representation, physical units, index
associations, presence semantics, and compatibility rules. H5MSM 0.6 should
round-trip supported data without depending on Python object serialization.

The 0.5 writer continues to reject nonempty mechanics data before creating a
file. A default empty native mechanics object does not imply a persisted
mechanics layer. Reading a 0.5 file in a future 0.6-capable implementation
must preserve that absence rather than fabricate a parameterization.

## Why

The pre-1.0 native `MolecularMechanics` object is minimal and experimental.
Freezing its current fields into H5MSM 0.5 would make the pre-1.0 format depend
on a parameterization model that has not been settled. Deferring persistence
leaves the 0.5 topology, chemical-state, structure, and interaction contracts
free to stabilize for 1.0. The 2026-11-08 consumer review now demonstrates a
concrete prepared-system persistence need; the bounded plan below supersedes
the original scheduling decision without expanding the 0.5 schema.

## What is measured and what is assumed

**Inspected:** The H5MSM 0.5 writer rejects nonempty mechanics data in its
native `MolSys` routes. The public rejection is guarded by
`tests/form/file_h5msm/test_public_h5msm_v05.py`.

**Inspected and contract-tested locally:** the bounded existing field inventory
is specified below and a private schema-1 codec now has directed guards.
**Assumed:** a future native model may need several parameterizations per system.
The P4 section qualifies bounded experimental public whole-system routes. The
P6 study below measures three bounded synthetic storage workloads; no general
large-scale performance guarantee follows.

## What was refuted

- Persisting the current minimal object in 0.5 was rejected because its
  parameter and association contracts are not mature enough to freeze.
- Silently omitting nonempty mechanics data from 0.5 was rejected because a
  successful write would claim a lossy file is a complete molecular system.

## Scope and exclusions

This proposal covers mechanics persistence in H5MSM 0.6 and compatible reads
of older files. It excludes changes to the accepted H5MSM 0.5 root layout,
the pre-1.0 `Interactions` persistence gate, and a requirement to finish every
possible future mechanics representation before MolSysMT 1.0.

## Acceptance criteria

1. The native mechanics contract states which data are model parameters and
   which are structural observations or chemical-state facts.
2. The 0.6 schema declares units, parameterization provenance, atom and
   structure index spaces, and absent versus present-empty semantics.
3. Public read and write paths round-trip supported mechanics data and reject
   unsupported payloads without silent loss.
4. The reader handles 0.5 files without inventing mechanics data, with tests
   for mixed versions and partial domains.
5. The schema, User Guide, course, and versioned API documentation agree before
   the 0.6 format is declared public.

## Dependencies and risks

The design requires a reviewed, bounded native mechanics parameter model.
A premature codec would lock ambiguous units or particle mappings into the
file format. The maintainer permits completing that review before MolSysMT 1.0.

## Revised implementation plan — 2026-11-08

**Decision:** advance a bounded portable snapshot of the existing experimental
native domain. The successful trusted Python checkpoint review below is useful
evidence for the required content, but does not satisfy H5MSM acceptance. No
public 0.6/1.0 writer or reader is implemented by this planning update; the
private layer codec described below does not register a file format.

**Accepted versioning direction:** publish the first stable format as
**H5MSM 1.0 with MolSysMT 1.0**, after the complete schema has passed its gates.
A 0.6 development schema can precede that freeze. The maintainer accepts
independent evolution afterward: a new H5MSM major denotes an incompatible
format change, not an automatic renumbering at a MolSysMT major. A future
MolSysMT 2.0 can therefore continue using a compatible H5MSM 1.x schema.
Record the library release, writer version and file-schema version separately.
The public writer still emits 0.5 today. This is a target and versioning policy,
not a claim that H5MSM 1.0 is implemented, qualified or published; no release
artifact or tag is created by this decision.

### Required content and boundaries

- Store the existing model requests separately from actual per-atom values and
  assignment reports. `forcefield`/`implicit_solvent` describe requested models;
  their presence never certifies a completed Hamiltonian or external engine state.
- Preserve the existing `atoms_ff` columns, their positional atom axis, nullable
  values and supported dtypes. Native bare partial charges are elementary-charge
  magnitudes. `atom_ff_type` is a force-field label, not the element symbol.
  Legacy mechanical formal-charge storage must remain explicitly distinguished
  from authoritative chemical-state assignments; do not invent or migrate
  chemistry merely by reading a snapshot.
- Keep both original detached assignment reports, producer versions, scientific
  attribution, parent/projection provenance, digests and state associations.
  Parent history can intentionally refer to a larger source axis. Do not
  reinterpret every historical array as aligned to the current atom count.
- Restore stored evidence without invoking RDKit, OpenMM, Ackredit registration,
  assignment calculations or a new binding operation. Stale/unknown bindings
  remain stale/unknown and must still fail the relevant scientific consumer.
- Distinguish an absent domain from present-empty tables/reports and explicit
  false/zero settings. The parameter-only `MolecularMechanicsDict` and `to_dict()`
  projection keep their current meanings.
- Use typed numeric/string datasets, null masks and versioned declarative
  metadata. Reject unsupported classes, extensions, columns, units and engine
  objects before publishing output. No pickle or executable object codec belongs
  in this portable file layer.
- Energies already stored as structural observations remain in `Structures`;
  no second energy store or speculative bonded-term API is introduced.
- Complete or partial systems require an explicit compatible atom domain when
  mechanical atom data are present. Do not infer correspondence from equal counts.
  Unsupported independent-layer compositions receive a clear refusal.

### P1 catalog: mechanics layer schema 1 (draft)

This bounded catalog describes the private codec under development, not an
available public H5MSM format. The new root will reuse the existing four domain
codecs and add optional `molecular_mechanics`; its exact public root version is
qualified separately. A reader rejects unsupported root/layer versions and
unknown represented fields rather than dropping them.

The mechanics group declares integer `schema_version=1` and nonnegative signed-64-bit integer
`n_atoms`. Its atom axis is positional and must be explicitly associated with a
compatible system axis by the modular orchestration. The layer does not infer
system identity, particle mapping, chemistry or parameterization from counts.
Systems without a usable atom domain are outside the first full-system mechanics
composition; standalone layers declare their own atom domain explicitly.

| Settings | Admitted non-null value | Physical interpretation |
| --- | --- | --- |
| `forcefield`, `non_bonded_method`, `constraints`, `water_model`, `implicit_solvent` | Text | Original model requests; names are not resolved or rewritten by I/O. |
| `dispersion_correction`, `flexible_constraints`, `rigid_water` | Boolean | Explicit false differs from absence. |
| `ewald_error_tolerance`, `solute_dielectric`, `solvent_dielectric` | Finite dimensionless numeric scalar | Original requests, not proof that a particular engine supports them. |
| `cutoff_distance`, `switch_distance` | Scalar length quantity | Reader declares length dimensionality using nm as the schema reference. |
| `hydrogen_mass` | Scalar mass quantity | Reader declares mass dimensionality using Da. |
| `salt_concentration` | Scalar amount/volume quantity | Reader declares concentration using mole/liter. |
| `kappa` | Scalar inverse-length quantity | Reader declares inverse length using 1/nm. |

All sixteen settings are represented explicitly, including nulls. Physical
quantities use sealed PyUnitWizard `QuantityRecord` values with a field binding
and an explicit dimensional reader handshake. Original compatible units are
preserved; no session default is inferred. The reader's quantity backend is
respected without changing the application's unit policy. Bare values or text
that parses as a dimensional quantity do not substitute for these quantity
objects. Conversely, textual versions, references and labels remain literal text
even if PyUnitWizard can parse them as quantities.

`atoms_ff` is absent or a present atom-indexed table. A present table has exactly
`n_atoms` rows in a zero-based RangeIndex, preserves column order, and admits:

| Column | Values | Declared unit |
| --- | --- | --- |
| `partial_charge` | Finite numeric values or explicit missing values | elementary_charge |
| `formal_charge` | Integral numeric values or explicit missing values | elementary_charge; legacy mechanics data, not authoritative chemical-state assignments |
| `atom_ff_type` | Text labels or explicit missing values | None; these are not element symbols |

The initial dtype catalog comprises NumPy object, signed/unsigned integers up to
64 bits and float32/float64; pandas nullable integer/float dtypes; and Python-backed
pandas string dtypes with their explicit NA policy. Unsupported columns, dtypes,
table subclasses, custom attributes or noncanonical axes reject. Numeric storage
retains its dtype; object columns use typed numeric/Unicode value vectors plus
null codes distinguishing None, pandas NA and NaN. A present table with zero
columns remains present. It does not imply any assignments.

`partial_charge_assignment` and `atom_type_assignment` are absent or detached
metadata mappings. Preserve them as stored evidence, including empty mappings,
original schemas/status, software versions, scientific attribution and historical
maps; do not certify unknown evidence or rebind stale evidence. Their supported
vocabulary is primitive scalars, mappings with string keys, lists, tuples and
typed numeric/boolean/Unicode arrays. Preserve tuples separately from lists.
No Python class identity or executable payload is decoded. Nonfinite floating
metadata requires an explicit typed array. Cycles and unsupported objects reject.
Quantities outside the declared scalar settings have no negotiated meaning in
this layer and reject until explicitly specified by a future schema.

A declarative tree records metadata types and references, with arrays in separate
HDF5 datasets rather than JSON/Base64 numeric expansions or lists per atom. The
private metadata schema validates dataset references, shapes, dtypes, duplicate
keys and unused arrays. Preparation validates the whole snapshot before creating
the layer; P3 must additionally provide whole-file staging/publication semantics.
This is resident static-domain reading, not a lazy mechanics query API or an
external-engine checkpoint.

### Private wire layout and directed receiving — 2026-11-08

`molsysmt/_private/h5msm_storage/mechanics.py` owns the mechanics layer; its private sibling
`metadata.py` supplies concrete typed-tree HDF5 primitives. These are storage
implementation tools, not registered forms or public calculation functions.
New primitives live in an owning private storage package instead of adding more
root-level `form/_h5msm05_*` files. The initial `form/_h5msm` placement failed
the adapter-only directory contract; it is corrected without relaxing that gate.
The seven existing modules in #438 are not relocated by this bounded correction.

```text
molecular_mechanics/                  attrs: schema_version=1, n_atoms
    snapshot/                        attrs: schema_version=1 (metadata tree)
        json                         uint8 UTF-8 JSON, tagged nodes/references
        arrays/0, arrays/1, ...      typed HDF5 numeric/boolean/UTF-8 datasets
```

The tree has exactly `settings`, `atoms_ff`, `partial_charge_assignment` and
`atom_type_assignment`. The table is null or `{n_rows, columns}`; each ordered
column declares `{name, dtype, unit, values, null_codes}`. Array nodes declare
index, shape and NumPy dtype. Mapping/list/tuple/scalar/NumPy-scalar/quantity
nodes have distinct tags; marker-like user mappings remain literal mappings.
UTF-8 datasets use fixed byte widths sufficient for their declared Unicode
widths, with compressed block transfers. No variable-length string heap, Python
objects per atom or Base64 numeric-array expansion is used. Physical setting
quantities remain sealed PyUnitWizard records.

**Directed contract tests:** 94 cases pass, including 65 new codec guards and
29 #660 refusal guards. Complete, selected and nonpolar-H-merged actual prepared
systems retain their full mechanical reports in new process readers under a
different unit policy, without RDKit/OpenMM/Ackredit or assignment calculation.
Readers preserve original producer metadata; model settings remain requests.
All admitted nullable dtype families, exact large integer values, empty states,
three quantity integrity checks, malformed references/versions, literal text and
mask-bearing unsupported array subclasses are covered. A 100,000-element array
is a typed dataset while its fixture JSON remains under 10,000 bytes; this is a
representation guard, not a large-scale performance benchmark.

Original attempts remain separately retained: the inventory script initially
resolved Viewer’s `tests` namespace, corrected by explicit source-first lookup;
its quantity-candidate scan also recognizes parseable strings, so the actual
reported Python types determine the inventory. Prototype guards exposed empty
mask integer upcasting and validation after shared-buffer NA restoration; both
are corrected. Fixed UTF-8 output additionally required an explicit matching
HDF5 memory dtype. No published writer was changed by those prototype failures.
The final directed process tree peaks at 313,372,672 bytes and preserves over
15 GB decimal host availability with no resource stop. Clean-source receiving,
full regression/HTML gates and source delivery are still pending at this point.

### Work packages and exit evidence

#### P3 composition decisions — 2026-11-08

- Develop the whole-file path privately as root `0.6`; public 0.5 functions and
  their defaults remain unchanged until public-operation and freeze gates pass.
  Do not emit an unqualified public 1.0 file by changing a header.
- Reuse existing topology, chemistry, structure and sparse-analysis layer codecs.
  The new orchestrator lives alongside the private mechanics codec. Extend the
  shared association primitive with an explicit caller-provided layer vocabulary;
  its default remains the closed four-domain 0.5 vocabulary.
- Independent layer reads retain declared maps without coercing populations.
  Resident MolSys reconstruction requires connected identity declarations for
  each shared atom and structure axis. Equal counts alone never identify axes.
  Explicit nonidentity maps remain readable as independent layers; reconstruction
  refuses them until the caller deliberately aligns the domains.
- A single `Structures -> ChemicalStates` association preserves the optional
  nullable structure-state vector. Missing declarations remain missing. Other
  structure-state endpoints are unsupported by the current native container and
  refuse during resident assembly rather than being omitted.
- A mechanics-only layer remains accessible independently; the current MolSys
  cannot represent it without another information domain. No topology or
  coordinates are synthesized to make an unsupported composition fit.
- An explicitly present but entirely empty mechanics layer, and an empty named
  analysis collection, remain independently readable. Resident MolSys has no
  distinct presence marker for those declarations; assembly refuses them rather
  than letting a later native export silently erase their presence. Present-empty
  mechanical reports/tables have stored native markers and remain supported.
- Writer provenance is root metadata distinct from stored scientific producer
  versions. I/O never reports a new calculation or rebinds assignment evidence.
- Validate declared native extensions without building intermediate JSON record
  lists or duplicating complete coordinate arrays. Reuse a native-owned transport
  extension check across dictionary and HDF5 paths.
- Stage a private file in the destination directory, close HDF5 successfully,
  then publish exclusively through an atomic hard link. Existing files, including
  dangling symlinks and publication races, stay unchanged. Normal failure cleans
  staging files. Unsupported hard-link filesystems refuse; there is no partial
  copy fallback. This is atomic visibility, not a crash-durable transaction;
  process termination can leave a recognizable private staging file.

| Package | Current state | Required exit evidence |
| --- | --- | --- |
| P0 — repair #660 | Closed; clean `272745fc8` passes 1,111 cases, fourteen fast gates and HTML; public `af71a6d29` verified | All affected branches, strict requests, present-empty state and unchanged existing file are guarded; no expansion of 0.5. |
| P1 — bound the schema | Bounded field/type/unit catalog specified; whole-file associations remain P3 | Exact field/type/unit catalog, domain/layer versions, identity and index-link rules, absent/empty semantics and unsupported-input policy. |
| P2 — mechanics codec | Clean `5c38a1022`: 1,178 cases, fourteen fast gates; unchanged HTML scope reused with proof; public `2cca126fe` verified | Typed native/HDF5 round trips for all admitted settings, tables and reports; malformed data/unknown versions refuse; no engine imports or evidence rebinding. |
| P3 — modular orchestration | Private root qualified on clean `b184e9d18`: 1,229 cases, fourteen fast gates and HTML; public dispatch/migration remain P4 | Reuse existing domain codecs; explicit version dispatch, associations, source-preserving migration and failure before file publication; unchanged 0.3/0.4/0.5 reads. |
| P4 — public operations | Clean `69f938947`: 1,843 cases, fourteen fast gates and fresh HTML; public `52df76db2` verified; consumer qualification pending | `convert`, explicit H5MSM reads/writes/layer reads, `get`/`has_attribute`, selected extraction/reordering, copying and structure append are audited; no recognized-but-inaccessible mechanics. Preserve the legacy handler's actual scope. |
| P5 — consumer receiving | Bounded reference/E3 prerequisite received upstream on DockingMT 9b077fab; broader P5 and installed profiles remain pending | Fresh-reader complete/projected/nonpolar-H-merged fixtures, multiple unit policies, original producer labels, prepared PDBQT re-export, edit invalidation, stale refusals and the full DockingMT reference route. Provider and installed evidence remain distinct. |
| P6 — format freeze | Bounded storage study measured on clean `b7269b77e`; final schema/default/freeze pending | Public schema, API docstrings/doctests, Foundations/Toolbox/Cookbook/course, bounded memory/storage measurements, default-writer decision and old-format/migration policy agree; then qualify the exact source/artifacts. |

P1 must precede a public codec contract. P2/P3 do not make the format stable;
P4/P5/P6 determine whether a first stable H5MSM 1.0 is justified. Each package
records executed commands, source identities, original failures and resource
limits. Storage/fresh-reader tests must record pandas and the actual unit backend
alongside NumPy/h5py/PyUnitWizard. Preserve the shared-host reserve and increase
concurrency only after a measured admission check.

### Compatibility and closeout decisions still required

1. Fix the final root version and independent mechanics-layer schema version only
   after the catalog is reviewed; do not claim that merely changing a header
   provides a new supported format.
2. Keep 0.5 mechanics-free and readable. Decide its warning policy explicitly;
   experimental development of a newer layer is not itself a deprecation decision.
3. Switch public default writing to the newest qualified schema only after all
   affected adapters and fidelity/loss reports agree. Retain a documented explicit
   old-format route if supported; otherwise refuse rather than discard mechanics.
4. Keep #256 open until its portable consumer requirements are met. The existing
   native checkpoint, #660 refusal correction or a passing private codec test cannot
   close the consumer's complete H5MSM gate.
5. Deliver exact source and schema compatibility notes to DockingMT and other
   consumers. Their independent acceptance and the release/installed/platform
   gates remain separate. This plan adds no artificial scorecard completion credit.


## Additional consumer receiving — 2026-11-08

[DockingMT's new owner question](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6727270669)
retains a complete failed reference selection on its declared editable source/
native identities. Strict maps and same-current-producer preparation controls
pass before the third H5MSM write rejects a prepared native ligand with nonempty
mechanics. Reads/final checks and the second unit policy remain unreached.
This is not a newly demonstrated writer defect: rejection preserves the 0.5
contract and no file is created. Client #79/#88 must not discard mechanics or
substitute private codecs to make the workflow pass.

The requested next owner step is a bounded audit of **existing supported public
lossless compositions** for mechanics, units, associations and history. No such
route is verified by this note. Keep the consumer hold unless one is qualified;
new 0.6 storage/model design stays post-1.0. #604's separately completed pairwise/
clustering tools and provider notice do not resolve this persistence question or
accept complete client E3.

## Initial public-route inspection — 2026-11-08

**Inspected on source `68350e0b27249b8337c04779ba0a86196d861a18`:**

- The current `MolSysDict` 0.2 encoder explicitly refuses nonempty mechanics,
  as H5MSM 0.5 does. Neither is an existing complete mechanics transport.
- The registered `MolecularMechanicsDict` route calls the native parameter
  projection. Its public guide explicitly excludes complete named assignment
  reports and does not promise JSON serialization of its arrays/quantities.
  A parameter dictionary alone cannot satisfy the consumer's full-state request.
- Current native copies and composition preserve native domains in memory;
  that does not establish their disk representation. `file:trjpk` exposes only
  the structures dictionary, rather than a molecular-system snapshot.
- Native object restoration hooks exist, including ownership rebinding and
  legacy migration. Their existence alone does not receive a prepared-system
  pickle containing all current assignments, units, associations and history.
  This remains a candidate for a bounded same-stack restoration assessment,
  not a newly promised versioned file schema or a replacement for the client's
  unchanged H5MSM gate.

No new serialization experiment or complete-format absence claim is made by
this inspection. The next finite review must distinguish a supported native
object checkpoint from portable molecular interchange, inspect the relevant
existing restoration guards, and qualify any proposed public composition on
the consumer's required state before recommending it. Do not fabricate missing
assignment reports or declare parameter-only transport lossless. New H5MSM 0.6
schema/model design remains post-1.0 and does not block the initial release.

## Existing native checkpoint receiving — 2026-11-08

**Contract-tested, bounded compatible-environment route:** Python's existing
`pickle.dump(molsys, stream)` / `pickle.load(stream)` native object protocol.
No runtime implementation, registered file form or 0.6 schema is added. This
answers the public-composition question for a trusted local object checkpoint;
it does not make that checkpoint portable or accept the client's H5MSM gate.
The maintained scope is in
[Trusted native object checkpoints](../forms_and_conversions.md#trusted-native-object-checkpoints)
and the User Guide links the same contract.

`tests/native/test_prepared_system_checkpoint.py` builds actual AutoDock4 and
Gasteiger–Marsili assignments through public preparation functions, using the
existing indexed-H methanol fixture with three synthetic structures. Complete,
selected and nonpolar-H-merged representations are saved under nm/ps/e and
pm/fs/coulomb policies. Fresh readers enter an angstrom/fs/coulomb policy before
importing MolSysMT, block RDKit/OpenMM/Ackredit and forbid the public assignment
calculations. An independent observation tree compares stored tables, typed
chemical transport/history, structure quantities, explicit associations,
parameters, full original reports and sparse analyses. It never reconstructs
any molecular data from those observations.

Public PDBQT re-export validates the restored chemical/value/structure binding
and matches original single-structure outputs for indices [2, 0, 2]. Controlled
coordinate editing proves restored ownership through actual analysis invalidation;
graph-based assignments remain usable. Four adverse cases retain refusal after
charge/type/chemistry/association changes rather than rebinding stale evidence.
A synthetic reader-version label additionally checks original producer retention;
its actual version is restored before comparing current-producer export bytes.
Only the real producer records are used as scientific evidence.

The first pilot incorrectly requested all three structures from the documented
single-structure PDBQT writer and failed before serializing. After correcting
that fixture, one pilot passes; the first complete directed run passes all ten
cases. Its process tree peaks at 360,378,368 bytes with host availability above
16 GB decimal, one CPU, a 2-GiB limit and no resource interruption. Original
attempts and per-reader outputs remain under
`.pytest_cache/external-reference-421/native-checkpoint-256-*`. Final clean combined receiving below includes the added reader-label/import-policy
controls. Public source delivery and the independent consumer decision remain
separate from that evidence.

This is a current native-data checkpoint, not a fully parameterized force-field
or external simulation-engine snapshot. The stored force-field/solvent settings
are requests. Python/MolSysMT/NumPy/pandas/unit-backend compatibility, file trust
and whole-object residency are required; no cross-release/platform, arbitrary
extension, large-scale memory or speed claim is made. Native parameter-only
transport is still insufficient for full named reports. H5MSM 0.6 stays open,
post-1.0, with its original model and typed-persistence criteria unchanged.

The negative presence audit also reproduces a separate current refusal gap:
report-only mechanics with all projected parameters absent is accepted and its
metadata disappears in both full-system encoders. This uses a manual stale
negative fixture, not a valid calculated assignment or affected client file.
The defect is separately owned by uibcdf/molsysmt#660; fixing that rejection
must not introduce mechanics storage into H5MSM 0.5.

## Bounded review outcome — 2026-11-08

Clean source `e02ed4debf27ea5927eccb93c758b518f866867c` passes **235 affected
cases with no omissions**, including all ten fresh-reader scenarios and the
existing preparation, native-copy/owner, composition, typed-dictionary and H5MSM
restriction guards. Fourteen fast gates pass. Four rendered Foundation/Cookbook/
course pages and their checkpoint links are inspected; the same six preexisting
HTML warnings remain. Existing code, execution counts and outputs in both edited
notebooks are unchanged. The library runtime, dependencies and Rust binary are
unchanged by this receiving work.

The [portable receiving record](../../devtools/data/native_checkpoint_receiving_256_20261108.json)
retains every original attempt and ten distinct reader records (excluding pytest
symlink aliases). Six positive readers preserve full public observation trees,
original producer labels and byte-identical selected exports. Four adverse
readers continue to refuse stale evidence. All 8,610 source and 2,463 Viewer
before/after input hashes match. Final tests peak at 363,069,440 bytes; all final
process trees preserve more than 13 GB decimal host availability without OOM,
reserve or pressure stops. Small checkpoint lengths are fixture observations,
not a storage benchmark or evidence for large systems.

| Existing route | Current bounded conclusion |
| --- | --- |
| H5MSM 0.5 | Mechanical parameters are intentionally refused; the separate report-only refusal gap is #660. No mechanics layer is added. |
| MolSysDict 0.2 | Same parameter restriction and #660 boundary; not a complete prepared-system mechanics transport. |
| MolecularMechanicsDict | Parameter projection omits full named reports; not a complete checkpoint by itself. |
| Native Python pickle | Contract-tested for the compatible trusted native fixtures above; retains the complete represented prepared object and permits continued use. |

The owner can now offer that **existing bounded native checkpoint option** to
DockingMT for a separately declared local workflow. Its original complete H5MSM
selection must retain its failure/hold until its own criterion is met; it is
not silently replaced by this option. The H5MSM 0.6 proposal stays **open and
post-1.0** with all five original schema/model acceptance criteria. This review
adds no weighted release milestone or claimed source-issue closure. Next local
correctness work is #660's explicit rejection boundary, not new storage design.

## First clean private-layer attempt — 2026-11-08

Clean `d3e6b1ac7` passes 1,176 affected tests without omissions (two measured
workers, two CPUs, a 2-GiB cap) and HTML. The fast gate is **13/14**, not passing:
the new `form/_h5msm` package is correctly rejected as an unregistered adapter.
No public delivery or whole-format acceptance follows that attempt. Storage
helpers move to `_private/h5msm_storage` with identical implementation ASTs; the
adapter validator remains unchanged and its direct preflight now passes.
Two further guards explicitly refuse wrong/absent per-atom charge units in the
fixed elementary-charge table protocol. The next clean attempt must include
that relocation and both guards; original attempts remain retained.

## Final private-layer source qualification — 2026-11-08

**Contract-tested:** clean `5c38a102216ab8cb3dd16bf8027779d8c8b9b2fa` passes
**1,178 affected cases without omissions**, including **67 private codec guards**,
and **14/14 fast gates**. This includes the added elementary-charge protocol
refusals. The private implementation is in `_private/h5msm_storage`; no form
adapter or public calculation is introduced. The adapter gate is unchanged.

The passing HTML build on `d3e6b1ac7` is reused only for its unchanged scope:
all `docs/` bytes and public library modules agree, the two implementation module
ASTs agree across relocation, and three rendered pages are inspected. Its six
baseline warnings are unchanged. The original 13/14 fast failure on that source
is retained and does not become passing evidence. The new source has its own
passing fast and complete selected-test runs.

[Receiving](../../devtools/data/mechanics_layer_receiving_256_20261108.json)
retains all twelve original attempts, three fresh-reader payload hashes and
expected observation hashes, actual pandas/Pint/provider versions, unchanged
input manifests and resource limits. Tests use two measured workers with a
2-GiB cap; their peak remains approximately 1 GiB. No resource stop or OOM occurs.
This is bounded private-layer qualification, not a performance benchmark,
installed/platform qualification or a passed whole-system H5MSM consumer gate.

**Next P3/P4:** compose the existing domains and the new mechanics layer with
explicit atom associations, version dispatch and whole-file publication semantics;
then implement/query the supported public read/write/conversion/selection/append
routes. Preserve 0.5 mechanics exclusion and legacy reads. The first stable 1.0
root and default-writer switch await P5/P6 qualification; no new file-format
capability is public in this source checkpoint. #256 remains open.

## Public private-layer checkpoint — 2026-11-08

Public `2cca126fe25ecf8f8d40e77acd8fb930e7e34f87` independently matches all ten
changed paths and preserves the four human root files. The
[delivery record](../../devtools/data/mechanics_layer_delivery_256_20261108.json)
links the qualified private layer and
[owner response](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6731162300).
#438 receives the new placement evidence without closing its original audit.
No new public file capability, installed/client acceptance or release is added;
#256 remains open for P3–P6.

## Ownership-reference correction — 2026-11-08

The module-location owner is **uibcdf/molsysmt#438**, as declared by its owning
report. The earlier #441 references in this checkpoint were incorrect: #441 is
an unrelated closed distance bug. Current records now use #438 and retain a
correction note with their original hashes; original commands, source/data
hashes and outcomes are unchanged. The misplaced #441 comment is corrected and
[the placement evidence is recorded in #438](https://github.com/uibcdf/molsysmt/issues/438#issuecomment-6731313441).

## Private whole-file composition — 2026-11-08

The private `h5msm_storage.modular` orchestrator stages root 0.6 with the existing
four domain codecs and mechanics schema 1. Resident writes declare shared atom/
structure identities and preserve the optional nullable structure-state vector.
Independent reads retain their explicit maps; resident assembly checks connected
identity declarations instead of trusting counts. Independent mechanical atom
counts can be inspected without loading tables. Unsupported mechanical-only or
time-only combinations, unrepresented extensions and unsupported root metadata
refuse. The default public reader/writer still implements only 0.3/0.4/0.5.
Public migration/default selection belongs to P4/P6 and is not completed here.

A native-owned extension check is reused by dictionary/HDF transport; preparation
of mechanical arrays happens once. Structural transfers reuse the bounded writer.
All-identity association metadata does not allocate an atom-sized index vector,
even when another axis has an explicit map. Atomic publication uses a reusable
private file helper with guards for failure, races and existing destinations.

Three actual complete, projected and nonpolar-H-merged preparations are loaded in
fresh processes under another unit policy with RDKit/OpenMM/Ackredit unavailable.
Their observations retain original assignments, producer/history/maps, chemistry
and sparse analyses. Selected PDBQT outputs remain byte-identical; a subsequent
coordinate edit invalidates affected interaction observations through restored
ownership. The two expected transport normalizations are explicit in the oracle:
textual structure labels use object-array storage (existing structural schema 1),
and QuantityRecord scalar quantities decode to zero-dimensional arrays with the
same numeric dtype/unit. All other checkpoint observations retain strict checks.
The original pilot's three representation mismatches and mistaken expected public
exception class remain failed evidence; no stored-value loss was demonstrated.

The expanded two-worker selection passes **1,229 cases without omissions**,
including the 12 #661 public overflow guards, corrected #660 absence fixture,
existing H5MSM versions and native dictionaries. Peak cgroup memory is
1,031,282,688 bytes, host availability remains above 15 GB decimal, and there is
no resource interruption. Clean source/fast gates and public delivery follow
separately; P4–P6 and the full consumer qualification remain open.

### Final P3 private-source receiving — 2026-11-08

Clean `b184e9d181513f50580aa8243f13d9f8941acdd7` passes the same **1,229**
affected cases, fourteen fast gates and a fresh HTML build. The
[composition receiving record](../../devtools/data/mechanics_composition_receiving_256_20261108.json)
retains three actual fresh-reader whole-file outcomes, twelve public #661
overflow controls, the corrected #660 presence fixture, original failed attempts,
all source/runtime hashes and resource caps. Three rendered public pages are
inspected; six baseline HTML warnings remain. Peak memory is 1,067,900,928 bytes
for tests and 1,341,902,848 for HTML, with over 12 GB decimal host availability.
No resource interruption occurs.

This qualifies P3's private composition/atomic-publication core. Public root
registration/dispatch and source-preserving migration remain explicitly required
under P4; P3 does not waive them. Consumer E3, bounded storage measurements and
final public-schema/default-writer qualification remain P5/P6. #661 is a separate
public-input correction; #438's seven-module placement audit remains open.

### Verified P3 source delivery — 2026-11-08

Public `1d033b65693dc0db84e594efccd2bf8651a19dda` independently matches all
21 changed paths and preserves the four human files. The
[delivery record](../../devtools/data/mechanics_composition_delivery_256_20261108.json)
and [owner response](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6731932749)
retain its bounded source scope. #661 is closed through its public twelve-case
guard; #256 and the separate #438 placement review remain open. No format,
package, release, tag, installed matrix or new client acceptance is published.
The complete refreshed board contains 593 issues, 88 open, and no open PR;
there is no newer report above #661 at this checkpoint.

## P4 public operation implementation — 2026-11-08

Public 0.6 writing requires `format_version="0.6"` in `h5msm.write`,
`write_layers` or general `convert`; default writing remains 0.5. Root detection,
legacy-handler refusal, scoped queries, structural iteration, metadata cardinality
inspection, selected file extraction, byte copying and bounded topology-free
append now dispatch the two modular roots. The old 0.3/0.4 adapter retains its
actual legacy scope. Conversion upgrades use a distinct output and preserve the
source; the version-specific 0.5 migration helpers/warnings are unchanged.
The [experimental public contract](../../docs/content/user/tools/form/file/h5msm_06.md)
documents supported types/units, explicit identities and presence limits.

`read_axis_sizes` exposes independent declared cardinalities without payloads;
this matters for a mechanical layer with no atom table. Coordinate queries do
not decode mechanics; mechanical queries decode that resident static domain
without unrelated data. A full mechanics projection can avoid resident MolSys
assembly. Partial MolSys composition accepts one stored mechanical provider,
including report-only evidence, and refuses duplicates/mismatched atom rows.
Complete, selected, reordered and complementary-file preparations are exercised.

The source-call audit found chemistry/force/preparation projections still bound
to the 0.5 reader. Their shared chemistry projection now dispatches by root,
checks connected atom identities for 0.6 and can explicitly retain model requests
for force construction. Scoped chemistry/calculation reads still avoid complete
coordinate/analysis loading. No force algorithm or model is changed.

### Opaque report evidence versus scientific use

A new six-case negative selection reproduces missing-key failures for empty/
incomplete charge/type reports and acceptance of a future schema during native
atom projection. These are synthetic evidence records, not a lost valid client
artifact. The primitive transport intentionally preserves arbitrary detached
metadata mappings; it does not certify that a scientific consumer understands
those reports. This finding is tracked here as part of the #256 boundary audit.

Charge/type consumers now require their implemented schema and scalar fields,
and projection requires supported atom correspondence vectors. Unknown or
incomplete reports remain losslessly readable/copyable but fail scientific use
or remapping through the existing SMonitor structural diagnostic, before indexing
missing fields or rebinding evidence. Twelve final controls independently cover
both consumers and projection. Known assignments retain their existing scientific
criteria, calculations and attribution. Original negative attempts are retained.

### Directed evidence and remaining qualification

The initial public pilot stops at five expected-diagnostic-class mistakes after
11 passes; a corrected run has 69 passes and three fixture/API mismatches
(unknown synthetic report projected as if complete, unsupported Iterator context
syntax and a nonexistent count method). Correct fixtures pass 77 cases. A wider
selection has 1,616 passes and one old expected-refusal test; that test now checks
independent preservation of the supported single mechanical provider. A subsequent
108-case consumer selection and fourteen fast gates pass. The first calculation
fixture incorrectly indexed a returned charge quantity as a dictionary; after
using explicit elementary-charge values, 101 cases pass, including both modular
roots in streamed-force controls. None is a complete client/platform qualification.

Final clean-source receiving must combine these routes, actual fresh public
readers, argument-contract and documentation checks. P5 keeps the independent
DockingMT reference workflow and installed-consumer decision. P6 keeps bounded
storage measurements, final schema/default-writer decisions and the H5MSM 1.0
freeze. The original progress weights and closed-issue count do not gain credit
merely from the additional public experimental root.

### Final P4 source qualification — 2026-11-08

Clean `69f9389479036044fd5a3c01fbfb75b07f4c2735` passes **1,843 affected
cases without omissions**, **14/14 fast gates** and fresh HTML. Five rendered
pages and the new public API anchor are inspected; six baseline warnings remain.
Course code, execution counts and outputs are unchanged. The
[public receiving record](../../devtools/data/public_mechanics_receiving_256_20261108.json)
retains original failed attempts, twelve independent unknown-report controls,
three public and three private fresh-reader variants, typed unit/provenance
observations, original exports and actual edit invalidation. It also qualifies
known-report extraction/reordering, complete/complementary files, explicit upgrades,
scoped queries, both modular roots in streamed-force cases and documentation examples.

Tests peak at 1,741,561,856 bytes under the final 3-GiB/two-worker ceiling;
HTML peaks at 1,347,325,952 under 2 GiB. All final jobs retain over 13 GB decimal
host availability with no pressure, OOM or reserve interruption. Public source
delivery follows separately. P5 retains independent client E3/installed receiving;
P6 retains bounded storage/memory measurements, the final public/default-writer
review and H5MSM 1.0 freeze. No package, tag, release or hosted matrix is created.

### Verified experimental public delivery — 2026-11-08

Public `52df76db2e9e29cc4812493e1cf3ca984e9fd57f` independently matches all
58 changed paths and preserves the four human files. The
[delivery record](../../devtools/data/public_mechanics_delivery_256_20261108.json)
and [owner handoff](https://github.com/uibcdf/molsysmt/issues/256#issuecomment-6732726967)
provide the exact qualified source and explicit 0.6 invocation. This makes the
experimental public provider routes available from source, while the default
stays 0.5. No package/minimum released version, installed-client acceptance or
stable H5MSM 1.0 is claimed. #256 stays open for P5/P6. The complete board still
has 593 issues, 88 open and no PR, with no issue newer than #661.


### P6 bounded storage study prescription — 2026-11-08

The reusable `devtools.scripts.benchmark_h5msm_mechanics` measures public explicit
0.6 writing, full reading, mechanical-layer reading, a scalar setting query,
ordered/repeated charge selection and ordered/repeated coordinate selection.
It reuses the existing native fixture, analytical coordinate oracle and timing
helper. Each operation runs in a fresh sequential worker, with one warm-up,
three untraced timing samples and a separate traced-allocation pass. Validation
is outside timing; handles reopen per call and the OS cache stays warm/uncontrolled.
No flush/fsync or durability latency is measured. Worker high-water memory
includes imports/setup/validation, while traced operation memory excludes them.

Prospectively selected cases are 62 atoms × 5,000 structures, 10,000 × 1,000
and 100,000 × 100. The latter two each have 240,000,000 float64 coordinate bytes.
The explicit 256 MiB coordinate admission bound is not a memory reservation.
Run one computational thread under a 3 GiB cgroup, no swap, and the existing
shared-host reserve/pressure monitor; defer rather than exceed safe resources.
The nullable table contains three columns and both synthetic typed reports carry
numeric atom-aligned arrays. Chemistry, sparse parallel observations and geometry
are retained. Reports deliberately do not claim valid charge/type assignments.
Highly regular coordinates, repeated type labels and regular report arrays limit
compression representativeness; these results cannot predict arbitrary real-data
size, billion-occurrence storage, independent client acceptance or installed gates.

The first tiny pilot caught #662: public charge queries failed on an admitted
pandas-NA entry. No timing campaign is accepted from that failure. Original guards
reproduce five failures and six passes. The correction and revised guards now
pass 23 directed tests, including the doctest and all six public benchmark
operations. One intermediate test also assumed a nonexistent MolecularMechanics
`.get` method; it was corrected to call that shortcut only on MolSys. Runtime
qualification, larger measurements and their exact records follow separately.

DockingMT's independent receiving is requested in uibcdf/dockingmt#79 and #88;
its local checkout is clean but behind its fetched remote and is not altered.
The new portable handoff is source availability, not client E3 acceptance.


### Bounded storage measurements — 2026-11-08

The exact preregistered three-case campaign completes on clean
`b7269b77ec8140c88aca217fcc928e17849275f0`, with six public operations and three
untraced samples each. The
[measurements and environment](../../devtools/data/h5msm_mechanics_storage_benchmark_256_20261108.json)
retain every sample, the actual per-dataset layout/allocation, scripts, whole-source
hash evidence and shared-host limits. Linux x86-64 / Intel Xeon E5-2630 v4 / Python
3.14 uses published PyUnitWizard 0.28.1 and unchanged native bytes.

| Atoms × structures | Whole file (MiB) | Write median (s) | Full read median (s) | Mechanical layer (s) | Three selected charges (s) | Selected coordinates (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 62 × 5,000 | 3.42 | 0.215 | 0.117 | 0.009 | 0.019 | 0.015 |
| 10,000 × 1,000 | 77.37 | 5.096 | 0.934 | 0.016 | 0.025 | 0.015 |
| 100,000 × 100 | 85.12 | 5.802 | 1.567 | 0.074 | 0.093 | 0.017 |

The largest selected-coordinate operation traces about 50 kB; the full read traces
267 MB decimal. The entire sequential process tree peaks at 732,151,808 bytes
(about 698 MiB), below its 3 GiB limit; host availability stays above 15.8 GB
with zero pressure warnings, high/limit/OOM events or reserve interruption.
The complete campaign takes about 129 seconds. These are warm-cache synthetic
measurements, not independent replicates, cold-disk/device durability timings,
real-data compression predictions or a general peak-memory bound.

The file's mechanical datasets allocate 4,154 / 65,761 / 562,636 bytes in the
three cases, excluding HDF5 group/object metadata and every other domain. The
regular report arrays and repeated labels compress favorably. Full file sizes
must not be interpreted as mechanics size or predicted for arbitrary coordinates.
The actual on-disk coordinate dtype is float64 in all three cases, as recorded
per dataset; source arrays are float64 too. Numerical checks retain the existing
native-storage oracle and tolerance, without claiming a float32 measurement.

**Operational consequence:** selected geometry stays bounded and avoids loading
mechanics. A file query for a scalar setting or three charges still reads the
whole static mechanical domain; it does not become constant-memory merely because
its result is small. For repeated mechanical queries, read that layer once and
query the resident native object. This observation changes no codec/default.
P5 independent client receiving and P6 final schema/default-writer/freeze plus
exact source/artifact gates remain open. #662's broad regression qualification
is separate from this successful benchmark and its 23 directed controls.


### Source regression and storage handoff — 2026-11-08

Clean `990474db05f09b853cc470d9e9f14e3b37d0af82` receives the #662 correction
and storage tooling with 1,869 affected cases, fourteen fast gates and fresh
HTML. The [record](../../devtools/data/mechanics_storage_and_nullable_receiving_256_662_20261108.json)
retains original failures, all clean identities, resource counters, warning
baselines and four inspected pages, including the exact downloadable benchmark
JSON. Fourteen course code cells/execution counts/outputs remain unchanged.
The [nullable-charge defect](../archive/resolved_bugs/nullable_stored_partial_charges_fail_public_numeric_queries.md)
is resolved in source; the benchmark completes all three preregistered cases.
The first final-record extractor inserted spaces before inline-code punctuation;
normalizing those parser-introduced spaces confirms the actual rendered prose.
No documentation or semantic check was relaxed, and no scientific rerun was needed.

P5 still requires independent DockingMT #79/#88 receiving. P6 now has bounded
storage evidence, but final schema/default-writer policy, old-format policy and
stable H5MSM 1.0 freeze plus exact-candidate gates remain open. The default stays
0.5; 0.6 is explicit and experimental. No package, minimum released version,
tag, release, CI dispatch or installed-client acceptance is supplied.


### P6 encoding/default review — 2026-11-08

No new independent client result is present in #256 or DockingMT #79 after the
latest portable handoff. Their P5 receiving stays open. The default remains 0.5;
0.6 is explicitly experimental. Existing 0.3/0.4 warnings and source-preserving
migration to 0.5 remain applicable; experimental availability does not deprecate
0.5. The target stable root is still 1.0 only after the complete receiving/freeze.

The field audit identifies a real pre-freeze boundary defect, #663: generic
conversion silently accepted the legacy `single` precision values while the
modular structural codec writes float64 and other domains retain typed data.
The bounded correction rejects explicit global precision controls with the
existing SMonitor conflict diagnostic. It leaves schema values/dtypes, units,
scientific reports and compression defaults unchanged. This is not a lossy
precision feature or authorization to globally cast evidence. The original
32-case selection has 28 failures/four passing no-override controls; qualification
of the correction follows separately. The source availability/default decision,
format stability and external/installed acceptance remain distinct.


The corrected directed selection passes 64 cases: all 32 new option/default/
publication controls, the existing public mechanical routes and the public
conversion doctest. The immutable qualified Viewer source export inspected for
this work contains no Python references to the two precision keyword names;
this bounded source search does not establish independent client compatibility.
The existing legacy single/double fidelity selection is included in final
receiving to protect its distinct supported contract. No legacy assertion is
weakened or reassigned to a modular codec.

| Review boundary | Maintained rule after the correction | Remaining exit |
| --- | --- | --- |
| Root versus layer versions | 0.5/0.6 and their implemented layer revisions remain explicit; target stable root 1.0 is independent of library numbering. | Independent receiving and whole-format freeze before any stable claim. |
| Default writing | Ordinary conversion/write remain 0.5; mechanics requires explicit 0.6. | Default switch only after the newest schema and consuming routes qualify. |
| Precision and typed evidence | Schema-specific field types; explicit unsupported global precision flags refuse, preserving represented values and reports. | Qualify the corrected public boundary and its legacy controls. |
| Old files | 0.3/0.4 remain readable with existing warnings and source-preserving migration; no 0.5 deprecation from experimental 0.6 alone. | Decide any additional legacy policy at stable-root freeze. |
| Memory/disk | Three synthetic cases and scoped-query costs are measured with explicit limitations. | No large-scale or installed extrapolation; retain independent evidence. |
| Consumer/release | DockingMT #79/#88 own independent complete reference acceptance; #334 owns exact candidate/installed/platform gates. | Unexecuted gates remain pending and no tag/package is authorized. |


### P6 encoding receiving — 2026-11-09

Clean `f03288768` receives the #663 option-boundary repair with 1,907 affected
cases, fourteen fast gates and six inspected HTML pages, including the public
conversion API. The [record](../../devtools/data/h5msm_encoding_review_receiving_663_20261109.json)
preserves the original 28 failures/four passes, directed 64-case receipt and clean
source/runtime/resource identities. Thirty-two new guards protect actual default
field values/dtypes and refusal before publication; five unchanged legacy cases
retain single/double 0.4 precision. All course code/output cells remain unchanged.
The future #664 storage-precision study is post-1.0 and adds no initial-release
blocker. Default writing stays 0.5, explicit 0.6 remains experimental, and
independent P5 plus final stable-root/default/candidate gates are unaccepted.


### P5 independent bounded client receiving — 2026-11-09

**Upstream reported and inspected, not replayed here.** DockingMT has published
its completed original reference prerequisite and bounded three-P59-pose E3
workflow on 9b077fabf41e19ffdfb945bc7aa3fb6c53265e0f, using editable MolSysMT
efbe67e1c6042078144bce1db24aa80bb565dbd2 and its own unchanged native backend.
The [receipt](../../devtools/data/docking_h5msm06_client_receiving_256_20261109.json)
records immutable source documents and authenticated compressed/decoded reader
receipts/manifests. The public source documents' Git blob hashes also match.
The consumer backend hash differs from this machine's qualified binary; this
is independent consumer evidence, not a local ABI/platform qualification.

The reference reader receives 261 members and complete normal/pm-fs profiles,
explicit 0.6 roots, four native writes/two full reads, original producer/settings/
parameter-table/report fidelity and five actual altered-copy refusals. Its final
observer preserves literal F versus farad; **zero actual quantity objects** occur
in that mechanical observation. The earlier claim of 136 quantities came from
unit-like text probing and is explicitly superseded. Original weaker seals,
setup failures and default-0.5 failures remain historical failures. No provider
unit/storage defect is established by that consumer-observer correction.

The separate pose reader receives 256 members, 34 physical fields and four
invalid quantity handshakes without molecular replay; both policies agree within
1e-12 nm with exact cluster membership. These are the three original saved poses,
not new independent molecular cases or new native searches. DockingMT #79/#88/#96
are resolved for those bounded consumer scopes. See uibcdf/dockingmt#79 and #88
for their retained provenance, failure accounting and public records.

This receives the portable-reference prerequisite, not every P5 partial-domain,
layer/reorder/append/size profile, edit/stale binding or installed route. P6's
stable schema/default-writer and #334 exact-candidate/publication gates remain
open. Public default 0.5 and explicit experimental 0.6 stay unchanged. No extra
scorecard weight, full H5MSM closure or release authority is added.

### Finite P5 provider review and client packet — 2026-11-10

The [completion packet](../pre_1_0_completion_handoffs_20261110.md#finite-p5-review-matrix)
now maps the remaining boundaries to assertion-bearing guards instead of an
unbounded request for more client testing. Source **ee4f72796** passes **156
provider cases**: public whole/partial/layer routes, fresh readers, original
producer versions and PDBQT parity, unit-policy preservation, selected/reordered
axes, typed/nullable fields, unknown-evidence refusals and selective invalidation.
Four new 0.5/0.6 topology/interaction append-refusal cases preserve byte-exact
source files and independently readable layers. No product code or native
binary changes from 5e7d65a66. See the [provider receipt](../../devtools/data/h5msm_p5_provider_receiving_256_20261110.json).

Three already received public-writer outputs now form a [portable synthetic
fixture packet](../../devtools/data/h5msm_p5_review_20261110/README.md), with
SHA-256/sizes, explicit typed snapshots and original current-producer PDBQT
exports. These are small storage witnesses, not production force fields. The
proposed additional client profile is limited to projected/reordered readback,
restored coordinate edit/invalidation and unknown-evidence transport/refusal
under two unit policies. Existing DockingMT #79/#88/#96 acceptance stays closed;
independent execution/acceptance of the new packet remains pending. No new
docking/preparation, hidden append support or scientific search is requested.

The complete source suite is separately running on frozen 5e7d65a66 and does
not include the four later guards. Its verdict and original failed session are
not replaced by this focused receiving. P5 independent acceptance and P6 final
schema/default/stable-format/candidate decisions remain open, with no extra
scorecard credit or publication authority.

### DockingMT scope accepted for independent receiving — 2026-11-10

DockingMT [e90c0446](https://github.com/uibcdf/dockingmt/issues/73#issuecomment-6782682019)
confirms all three additional controls are relevant. The bounded plan is an
explicit atom permutation with structures `[2, 0]`, a restored coordinate edit
with selective interaction invalidation, and unknown-assignment report transport
with projection and PDBQT export refusals. Execute each applicable case in a
fresh process under the normal and pm/fs policies on the same immutable inputs.
Use the existing native guard for a representative charge and atom-type report
in an adverse copy. The three valid packet files do not contain unknown reports.
Original reference and E3 evidence at `9b077fab` remains accepted. DockingMT
#79/#88/#96 remain closed. The three additional controls have yet to run.

The exact provider reference is `ee4f727960ddb7f86b2c9c8e28e7f842fbe1bdfc`,
whose product source matches `5e7d65a665425fe6077f016dd95cbd65d424ee91`, with
Linux ABI3 `_rust.abi3.so` SHA-256
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`.
Use the [fixture manifest](../../devtools/data/h5msm_p5_review_20261110/manifest.json)
for individual file identities. This is a source/native reference, not a
published package coordinate. In an isolated consumer composition, record the
actual imported source, extension path and digest before reading the fixtures.
A separately built or different digest needs its own provider/consumer
receiving. Preserve the existing frozen DockingMT installed cohort and its
older provider binary. The three new checks do not repeat preparation or docking.

### P6 wire catalog and public-route audit — 2026-11-10

Inspected source `4e43a6557cf9ac70d3504cab35dd72281e911fe1` and the existing
[format contract](../h5msm_format.md). The proposed stable root should keep
the represented domains and their existing codecs unless an identified wire
change needs a new layer revision. The root identifier, exact admitted layer
revisions, current producer version and original stored evidence have separate
meanings. Freeze them explicitly when introducing `version="1.0"`.

| Domain or metadata | Observed 0.6 representation and stable freeze work |
| --- | --- |
| Root | `type`, `version`, `creator`, `creator_version`, `created_at` are required text fields. The root enumerates allowed groups. Preserve strict root dispatch, and decide the explicit encoding and validation of migration provenance before making a new writer. |
| `topology` | Schemas 1–4 encode typed nullable inventory tables, optional packed chain membership, direct atom-to-molecule assignments and naming declarations. Keep string IDs and positions distinct. Freeze the allowed revision/field combinations. |
| `chemical_states` | Schemas 1 and 2 separate chemistry and its optional preparation history from stable topology. Preserve the declared reference, absent/unknown/known-empty chemistry, and assignment history. |
| `structures` | Schema 1 declares atom and structure counts, positions/boxes in nm, velocities in nm/ps, time in ps, B factors in nm², occupancy, temperature in K and energies in kJ/mol. IDs retain their declared numeric/text encoding. Preserve optional bioassembly and alternate-location records, missing fields and bounded structural I/O. |
| `interactions` | Collection schema 1 contains named sparse results. Result readers accept schemas 1 and 2 and current writers emit 2 with execution provenance. Preserve coverage, occurrence identities within the stored analysis, compound roles, maps, units, producers and periodic images. A present-empty collection is meaningful at the independent-layer boundary. Standalone `Interactions.save/load` uses its own HDF5 format. |
| `molecular_mechanics` | Schema 1 stores explicit atom count, settings, typed/null-aware per-atom tables and original detached reports using the typed metadata codec. Preserve independent presence and unknown evidence without interpreting it as a usable assignment. |
| `associations` | Schema 1 links declared atom, structure and state axes, including explicit state maps. Equal sizes alone do not establish correspondence. Independent layers and whole-system composition have different representability requirements. |

Four route boundaries govern the implementation:

1. **Version admission.** Public writers and `basic.convert` share write
   validation but each currently supplies its own 0.5 default. `read` retains
   legacy 0.3/0.4 dispatch and modular reads use their validated roots. The
   low-level modular header and several mechanics/association dispatches
   explicitly recognize 0.6. A version-list-only change would leave query
   association handling, mechanics-only conversion, force input and append
   behavior incomplete. Introduce shared private root policy and exercise
   `read`, `read_layers`, `read_axis_sizes`, conversion, projected `get` and
   bounded `Iterator` through their public entry points before changing the
   ordinary writer default.
2. **Preserving and mutating operations.** Byte-copy keeps the stored version.
   Subset extraction's file adapter writes the same modular root, while
   `basic.extract(to_form=...)` has a specific 0.6 override to avoid a 0.5
   downgrade. Test both routes when adding 1.0. Append stays on the existing
   root and retains the topology/named-interaction refusals and explicit
   state-index requirement. The legacy `H5MSMFileHandler` and its OpenMM
   reporter use the 0.3/0.4 contract. The default for new public modular output
   must not silently switch these internal legacy producers.
3. **Lossless migration.** `migrate_04_to_05` and `migrate_to_05` keep their
   named 0.5 destination. They refuse ambiguous legacy zero-atom scaffolds.
   For a latest-format migration, use the independent modular layer/axis
   boundary when a source file has unbound domains or present-empty layers.
   Routing every source through `MolSys` would reject these inputs or lose
   represented presence. Validate and re-encode before publishing a new file,
   with explicit decisions for the original root producer and migration
   metadata. Retain original detector/assignment evidence and refuse lossy or
   ambiguous inputs before writing. Reconcile the legacy warning's recommended
   command after the actual latest migration path works.
4. **Acceptance before default switch.** Start with explicit 1.0 reads/writes
   and failure/nonmutation checks. Cover legacy migration, 0.5/0.6 upgrades,
   independent and whole composition, incompatible versions, missing/empty,
   named results, units and state/atom/structure mappings. Then align `write`,
   `write_layers`, `convert` and applicable adapters, and execute the docs and
   client cases. MolSysViewer sessions follow the provider writer default, so
   confirm old-session reads and the embedded root of new sessions alongside
   DockingMT's finite controls. Keep current 0.5 default, explicit 0.6 and
   exact-candidate qualification separate during this review.

Nine directed existing cases pass with pytest-receptor on the audited source
and Linux ABI3 digest `4ffb82e4…`. They cover both legacy migration routes,
mechanics-only reading and queries, bounded structural query/iteration,
version-preserving copy/extraction and four append refusals. These results
establish the pre-change baseline for the audited paths. Stable-root coding,
end-to-end migration and independent client checks remain pending.

### Explicit 1.0 source route — 2026-11-10

The development reader and writers accept `format_version="1.0"` explicitly.
Both 0.6 and 1.0 reuse the current independent domain codecs and atomic
new-file publication. The 1.0 reader recognizes the new root and its optional
`migration_source` record. The root and layer policies are shared by projected
queries, iteration, conversion, selected extraction and the admitted append
path. The public writer default still resolves to 0.5. Legacy handlers and
version-specific migration helpers keep their previous behavior.

Whole-file `convert` to 1.0 re-encodes 0.5 or 0.6 through the independent
layer codecs. This route keeps the file's declared maps and counts, independent
atom axes, absent layers, present-empty layers, typed values and original
scientific reports. It does not construct a `MolSys` as an intermediate. The
new writer records its own root identity and stores the old root metadata
under `migration_source`. Refuse unrecognized source metadata, ambiguous
provenance and existing destinations. The conversion reads resident layers.
Selected conversion and report-producing conversion retain their native route.

This is source implementation. P5 independent client receiving, the 1.0
default-writer decision and exact MolSysMT/MolSysViewer candidate qualification
are pending.

Local H5MSM, interaction persistence and API doctest regression passes
**1,238 cases** on Linux/Python 3.14 with the existing ABI3 extension. The
initial run passed 1,236 cases and failed the new test that tried to access
occurrence indices directly on `Interactions`. The corrected test obtains the
indices through the supported query export. The final run also covers duplicate
keys in migration provenance. All 683 warnings come from legacy 0.3/0.4 reads.
The one-CPU, 2-GiB scope peaks at 470,056,960 bytes and retains at least 14.37
GiB host memory available without limit or OOM events.

An additional six cases migrate the three immutable DockingMT packet inputs
under nm/ps and pm/fs, preserving complete typed native snapshots, exact PDBQT
text, and source hashes. The first comparison omitted the PDBQT writer's
required explicit `typing_scheme="autodock4"`. The corrected comparison uses
that option for both source and target. This is provider-side evidence for
the explicit 1.0 route and remains separate from DockingMT execution.

### Independent experimental 0.6 P5 acceptance — 2026-11-10

DockingMT publishes both final seven-case profiles at `d83d86d4`. They pass
with normal and pm/fs units and cover all three agreed client checks. Explicit
atom permutation and structure order `[2, 0]` retain typed states, bonds,
mechanics and coverage. Editing a restored structure invalidates only the
affected analysis. Unknown charge and atom-type reports survive storage and
refuse projection/export with source protection. Existing #79/#88/#96 and
reference/E3 acceptance retain their original scope. [DockingMT #73](https://github.com/uibcdf/dockingmt/issues/73#issuecomment-6783446850)

The source is isolated MolSysMT `5e7d65a6` with the consumer's previously
qualified Linux ABI3 `5715bda2`. The native allowance is two unchanged
connected-component calls per policy, each for one atom and zero bonds.
All changed neighbor kernels and other native calls are blocked. The
[provider-side receipt](../../devtools/data/docking_h5msm_p5_client_receiving_256_20261110.json)
authenticates both manifests and 11 selected stored records. The final
reports retain identical caller unit settings and register named fast tracks
during startup. The original failed admissions and reader remain in custody.
This closes the bounded independent P5 profile for experimental 0.6.

The next DockingMT format check belongs to P6. Use MolSysMT `05865fbb3` as
the reference for the explicit 1.0 source API, and record the actually
imported provider source and compatible binary in a separate consumer
composition. MolSysMT's reference Linux ABI3 is `4ffb82e4`; the P5 report
does not receive it. The Rust inputs are unchanged between `5e7d65a6` and
`05865fbb3`. A build on another host requires its own recorded provenance
and digest. Migrate the original fixture inputs with explicit
`format_version="1.0"`, verify the new root and old root provenance, then
repeat the three applicable persistence/edit/admission checks under both
policies. Exact release artifacts and stable-format/default acceptance remain
pending under #256/#334.

### Local P6 provider reference ready — 2026-11-10

The local worktree
`.pytest_cache/pre1-review-20261110/h5msm10-05865fbb3-dockingmt-reference`
checks out `05865fbb3ba499d4117d6ba3e1cf55d98a9e239e` and carries the
verified Linux ABI3 SHA-256
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`.
On Python 3.14 both imports resolve inside this worktree. The source import
reports `0+unknown`. All six public 1.0 migration cases pass in this
composition. DockingMT can use the same source and native binary on this
host, or record an equivalent admitted build in its own environment. Its
independent P6 profile and the MolSysViewer session profile are pending.

A provider-side session check pairs the same worktree with Viewer `5164f13b`.
Its normal save produces a 0.5 member. For the 1.0 control, migrate that member
with public `convert` and retain the session manifest and scene document. The
public Viewer loader reopens both archives under nm/ps and pm/fs. The four
loads preserve a named region, coordinates, named interaction analysis,
parallel occurrence identities, evaluation coverage and method. The initial
fixture attempt tried to assign into the read-only analysis mapping. The
passing fixture uses the public whole-mapping setter. Independent Viewer
receiving and the default-writer decision remain pending.
