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
No large-scale storage benchmark or public whole-system codec is qualified here.

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
The seven existing modules in #441 are not relocated by this bounded correction.

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

| Package | Current state | Required exit evidence |
| --- | --- | --- |
| P0 — repair #660 | Closed; clean `272745fc8` passes 1,111 cases, fourteen fast gates and HTML; public `af71a6d29` verified | All affected branches, strict requests, present-empty state and unchanged existing file are guarded; no expansion of 0.5. |
| P1 — bound the schema | Bounded field/type/unit catalog specified; whole-file associations remain P3 | Exact field/type/unit catalog, domain/layer versions, identity and index-link rules, absent/empty semantics and unsupported-input policy. |
| P2 — mechanics codec | Private implementation; 94 directed cases pass; clean receiving pending | Typed native/HDF5 round trips for all admitted settings, tables and reports; malformed data/unknown versions refuse; no engine imports or evidence rebinding. |
| P3 — modular orchestration | Pending | Reuse existing domain codecs; explicit version dispatch, associations, source-preserving migration and failure before file publication; unchanged 0.3/0.4/0.5 reads. |
| P4 — public operations | Pending | `convert`, explicit H5MSM reads/writes/layer reads, `get`/`has_attribute`, selected extraction/reordering, copying and structure append are audited; no recognized-but-inaccessible mechanics. Preserve the legacy handler's actual scope. |
| P5 — consumer receiving | Pending | Fresh-reader complete/projected/nonpolar-H-merged fixtures, multiple unit policies, original producer labels, prepared PDBQT re-export, edit invalidation, stale refusals and the full DockingMT reference route. Provider and installed evidence remain distinct. |
| P6 — format freeze | Pending | Public schema, API docstrings/doctests, Foundations/Toolbox/Cookbook/course, bounded memory/storage measurements, default-writer decision and old-format/migration policy agree; then qualify the exact source/artifacts. |

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
