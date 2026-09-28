---
summary: Design a sparse public Interactions result and serialization contract
issue: uibcdf/molsysmt#251
status: active
opened: 2026-09-28
closed:
verification: inspected
area: [api, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Design a sparse public Interactions result and serialization contract

**Reported:** 2026-09-28, after the result-contract request from
`uibcdf/molsysviewer#114` exposed a decision left open by
[`uibcdf/molsysmt#250`](organize_interaction_detection_by_family_before_1_0.md).
**Status:** Active design proposal; no public class or storage format is implemented.

## What

Design one public `molsysmt.Interactions` result class for chemically classified
interactions across one or many structures. It should hold sparse, typed data,
support efficient structure and atom queries, and have a versioned serialization
boundary. The same class should represent hydrogen bonds, disulfide candidates,
and later interaction families without requiring a subclass per family. It is an
independent analysis result; attaching it to `MolSys` is a separate decision.

This issue decides the logical result contract and its evidence gates. Subsequent
implementation work must deliver the class, detector adapters, and file codec.

## How

### Candidate public surface

The following is a proposal, not a published signature:

```python
result = msm.Interactions.from_arrays(...)
subset = result.query(
    structure_indices=[12, 2, 12],
    atom_indices=[4, 5, 6],
    mode="incident",  # also "internal" or "cross"
    interaction_types=["hbond"],
)
columns = subset.to_dict()
subset.save("observations.h5i")
on_disk = msm.Interactions.open("observations.h5i")
```

`query` returns an `Interactions` view by default; conversion is explicit.
`to_dict()` returns a documented columnar schema, not one Python object per
occurrence. A NumPy projection can expose fixed-width columns, but a single
ordinary ndarray cannot losslessly encode variable-arity groups, roles,
geometry, metadata, and coverage without object dtype. Detector
`output_type="molsysmt.Interactions"` should initially be opt-in, preserving
current hydrogen-bond and disulfide layouts until their compatibility work is
complete. Exact names, projections, and file-backed view lifetime need review.

### Logical data model

| Layer | Required content | Candidate compact representation |
| --- | --- | --- |
| Source | Atom and structure index spaces, source identity or fingerprint, maps from local selections to original indices. | Typed metadata and integer maps. Public queries use original indices. |
| Analysis | Interaction family, named method, parameters, units, evidence origin, schema version. | Small metadata block per method/configuration. |
| Relations | Stable IDs, kind, directionality, participants, roles, constituent atom indices. | Flat typed arrays and offsets for participants and group membership. |
| Coverage | Explicitly evaluated structures, including those with zero occurrences. | Sorted unique structure indices and aligned occurrence offsets; absence means unevaluated. |
| Occurrences | Structure index, relation ID, aligned measures, optional periodic images, provenance. | Typed columns ordered by structure, relation, then image; optional columns only when used. |

An occurrence is a frame-specific observation. A source declaration with unknown
frame scope must retain `scope=unspecified` and must not silently appear in every
frame query. A separate declaration table or analysis block may represent it;
the normative contract must choose. Inferred S–S candidates retain
`evidence=observed_geometry` and do not imply a topological bond.

Relation identity includes type, ordered roles for directional interactions,
and participant identity. Symmetric pair relations require a canonical ordering
rule. Periodic image vectors belong to the occurrence when the observed copy
or geometry depends on them. Measures declare units such as nanometers or
radians; scores are not implicitly energies.

### Query semantics

`structure_indices` is an explicit selection, including nonconsecutive or
reordered indices. Repeating one index produces one result; output follows the
order of first appearance. With no restriction, only evaluated structures are
returned. Each occurrence exposes its original structure index. Coverage stays
visible so an evaluated empty frame differs from an unevaluated one.

For an atom-index set `S`, membership uses every physical atom in the
participants, including all atoms of a group participant:

- `incident`: at least one participant atom belongs to `S`;
- `internal`: every participant atom belongs to `S`;
- `cross`: `incident` minus `internal`.

The atom set is deduplicated. A single atom follows the same rule. A hydrogen
bond uses donor, hydrogen, and acceptor atoms: selecting only the donor gives
`incident` and `cross`; selecting all three gives `internal`. For a pi–pi
relation, selecting one ring atom gives `incident` and `cross`; `internal`
requires every atom in both rings. Role filters, whole-group matching, and
drawing anchors may be added separately without changing these set rules.
Atom- and type-filtered views retain coverage even when they have no matches.

Result order is deterministic: requested structure order, then canonical
relation order, then image identity. Repeated selections never duplicate
occurrences. Empty results have stable column names, typed zero-length arrays,
and explicit coverage.

### Physical indexes and performance

Frame offsets over a sorted coverage table make one frame's occurrences
addressable without scanning other frames. Atom-to-relation and
relation-to-occurrence inverted indexes support atom queries through a long
trajectory; these may be built lazily or stored. Combined structure/atom
queries should intersect the smaller posting sets. Cold index construction
and warm query cost must be reported separately. The intended cost depends on
relevant relations and occurrences, not every possible atom pair or a full
trajectory scan for each query. No numeric bound is claimed yet.

Streaming writes accept sorted, unique evaluated structure indices in bounded
chunks, including frames with zero observations. Relation IDs must stay stable
across chunks. Large analyses should use the maintained `ChunkedExecutor` path.
File-backed `open` must read frame slices lazily rather than loading the full
trajectory into memory.

### Serialization and molecular-system lifecycle

Define a versioned, typed payload independent of its container. Prototype a
standalone file with flat numeric arrays, offsets, metadata, explicit unit
strings, coverage, and optional indexes. Ragged HDF5 object or variable-length
arrays are not the default. Round trips must preserve roles, source maps,
evidence, measures, images, and empty evaluated frames. Incompatible versions
must fail clearly.

H5MSM 0.4 has no interactions layer. Embedding this payload in a later H5MSM
schema is a separate format decision and is not required for MolSysViewer 1.0.
Extraction, atom reorder, and structure subset must remap every reference and
coverage index or explicitly invalidate the result. A source fingerprint may
detect stale results, but its algorithm needs its own tests. Cross-system
interactions, symmetry mates, and structure intervals require explicit
identities before entering a first codec version.

### Decision sequence

1. Review examples and the logical schema with `uibcdf/molsysviewer#114` and
   seek equivalent needs from TopoMT, PharmacophoreMT, and DockingMT. If the
   contract becomes suite-wide policy, open a linked MolSysSuite coordination
   issue under its ownership rules.
2. Settle the open choices and write the accepted contract in a normative
   `devguide/` document. Close this design issue only then.
3. Implement an in-memory class with pair, triple, and group participants;
   query semantics and coverage precede optimization.
4. Add indexes and a streaming standalone codec. Measure cold/warm queries,
   memory, and serialized size on representative trajectories.
5. Add detector `output_type` adapters without silently changing existing
   defaults. Evaluate H5MSM integration after its separate format gate.

Steps 3–5 require tracked implementation work. Their release timing should be
decided with #250 and consumers after the contract and performance targets are
reviewed.

## Why

[`interactions_api.md`](../interactions_api.md) records method-specific
hydrogen-bond and disulfide outputs; no generic result class exists. The
[`#250 proposal`](organize_interaction_detection_by_family_before_1_0.md)
requires a minimum shared result contract but leaves its schema open.
`uibcdf/molsysviewer#114` requests fast nonconsecutive frame and atom queries,
sparse storage, evaluated-empty state, provenance, and typed serialization.
The [attribute-centric proposal](attribute_centric_molecular_system_model.md)
sketches definitions, participants, and occurrences; its broader native domain
and optional attachment remain separate. An independent result class can meet
consumer needs without making interactions mandatory for every `MolSys`.

## What is measured and what is assumed

- **Inspected:** current interaction methods have method-specific outputs and
  H5MSM 0.4 has no interactions layer. No new code or benchmark was run.
- **Consumer request:** `uibcdf/molsysviewer#114` describes the query,
  sparsity, provenance, and serialization needs above. Equivalent needs of
  other consumer teams are plausible but unconfirmed.
- **Assumed design target:** columnar arrays and secondary indexes can meet
  these needs. Their speed, memory cost, and file size must be measured.
- **Estimate:** an independent in-memory result can precede H5MSM integration.
  This is an architectural ordering, not a delivery-date claim.

## What was refuted

- One subclass per family multiplies query and codec contracts without a
  demonstrated need for different object lifecycles.
- A dense atom-pair matrix per frame scales with possible pairs and cannot
  represent triples or groups directly.
- Lists of Python objects per occurrence inflate storage and serialization;
  typed columns with offsets retain variable arity.
- One generic NumPy ndarray cannot represent the full mixed schema losslessly;
  explicit projections can still serve array callers.
- An observed S–S candidate is not a declared disulfide bond.
- Requiring H5MSM 0.5 or automatic `MolSys` attachment couples the result
  contract to a broader architecture decision.

## Scope and exclusions

This issue covers one-system result semantics, the public query contract,
sparse logical schema, versioned serialization boundary, and implementation
gates. It does not implement the class, detectors, indexes, file writer, H5MSM
integration, future interaction families, scientific validation of methods,
cross-system alignment, symmetry expansion, or automatic `MolSys` attachment.
Detector science and API migration remain with #250 or family-specific issues.

## Acceptance criteria

Close this design issue only when:

1. A normative result contract fixes index spaces, source mapping,
   relation/participant/occurrence identity, roles, coverage, evidence,
   measures and units, periodic images, query order, and empty result types.
2. It contains checkable examples for one frame, nonconsecutive and duplicate
   frame requests, variable and zero counts, one atom, atom-set
   `incident`/`internal`/`cross`, a hydrogen-bond triple, and a group relation.
3. It specifies a typed versioned payload, file-backed query expectations,
   the H5MSM boundary, and a remap-or-invalidate rule.
4. MolSysViewer and at least the known requirements of TopoMT,
   PharmacophoreMT, and DockingMT have been solicited; decisions and unanswered
   dependencies are recorded. Any suite-wide ownership issue is linked.
5. It defines measurable prototype gates: resident memory, cold and warm frame
   and atom queries over hundreds or thousands of frames, serialized size,
   chunked-writing peak memory, and round-trip fidelity. Claims of passing a
   gate require a measurement command and data.
6. The issue records the decision and implementation follow-ups. This proposal
   is archived with `normative` pointing to the accepted document.

## Dependencies and risks

- The contract must work with the migration in
  [`uibcdf/molsysmt#250`](organize_interaction_detection_by_family_before_1_0.md),
  but is not blocked on every detector gate there.
- `uibcdf/molsysviewer#114` needs a provider contract before fixing its view
  API. That does not promise the standalone codec or H5MSM integration by 1.0.
- Ring display anchors must remain separate from atom-set membership rules.
- Views over an open file need explicit lifetime, close, and ownership rules.
