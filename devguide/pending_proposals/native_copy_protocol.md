---
summary: Native objects need an explicit copy ownership and memo contract
issue: uibcdf/molsysmt#121
status: open
opened: 2026-10-21
closed:
verification: reproduced
area: [native, api, basic]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native object copy ownership and memo contract

**Reported:** Existing issue #121 requests `copy()`, `__copy__()` and
`__deepcopy__()` and names TopoMT's `Topography` as a reference. The maintainer
requested a design study before implementation.
**Status:** Initial source inventory and small executed probes complete. The
public shallow-copy semantics below are proposed, not implemented or accepted.

## What

Define native copying without form discovery, rebuilding, chemical inference,
interaction remapping or serialization. Preserve supported data, local indices,
units, producer provenance, domain ownership and intentional internal aliases.
Keep the existing independent-copy meaning of ordinary native `.copy()` calls.

## How

### Inventory at the inspected source

| Family | Existing `.copy()` | Python copy protocol and concern |
| --- | --- | --- |
| `MolSys` | Reconstructs base-class domains; uses interaction `remap()`; separate complete/partial branches. | No explicit hooks. `copy.copy()` shares topology and rewrites its owner through `__setstate__`. |
| `Topology` | Copies known tables and its chemical-state collection; returns a base `Topology`. | Serialization restoration coerces shared chemistry during shallow copying. Owner links are intentionally omitted by serialization. |
| `Structures` | Delegates to `deepcopy`. | No explicit hooks; current deep copy is a useful behavioral reference. |
| `ChemicalStates` | Reconstructs the collection and copies private states. | No explicit hooks; preserve state inventory, history and reference selection. |
| `MolSysBuilder` | Reconstructs topology and structures in a base builder. | No explicit hooks; copying must not call `build()` or synthesize missing parents. |
| `MolecularMechanics` | Manually deep-copies listed settings, assignments and parameter tables. | Include as a resident domain without expanding its experimental scientific or persistence scope. |
| `Interactions` | No `.copy()` method. | Both Python operations use `__reduce__`, encode/decode the analysis, duplicate numeric buffers and flatten filtered/patched storage. Query views preserve their selected occurrence indices in the observed examples. |
| `MolSysDict`, `TopologyDict`, `ChemicalStatesDict`, `InteractionsDict`, `ViewerJSON` | Independent payload copies already exist. | Reconcile wrapper semantics with the chosen contract; retain their distinct schemas. `StructuresDict` is a plain dictionary form, not a native class. |
| `Simulation` | Copies settings but retains the molecular-system reference. | Configuration/reference semantics need their own explicit decision, not automatic adoption of a molecular snapshot contract. |
| File handlers and `TrajectoryFile` | Resource-specific behavior; `TrajectoryFile.copy()` currently returns an empty handler. | Exclude live resources from generic resident copying. Reopening or snapshotting files is a separate I/O contract. |

The TopoMT reference separates shallow and deep analysis payload copies,
independently owns mutable registry/index containers, rebinds copied features
and registers the target in the deep-copy `memo` before descending. Its prior
registry-ownership correction is tracked by uibcdf/topomt#74. This is useful
ownership guidance, not evidence that shared editable molecular coordinates
would preserve MolSysMT's interaction-validity guarantees.

### Proposed bounded public contract for discussion

1. `.copy()` returns an independently editable molecular snapshot. Preserve
   current calls; do not introduce `deep=False` without an agreed safe meaning.
2. `copy.deepcopy(obj, memo)` uses native hooks, registers its shell before
   traversing domains, and carries the same memo through the entire graph.
   Preserve cycles, repeated references and concrete supported subclasses.
3. For resident molecular containers, prefer a documented domain-defined
   `copy.copy(obj)` that also isolates mutable molecular domains. It may share
   strictly immutable interaction numeric buffers, but must own analysis
   metadata and named-analysis containers independently. This is intentionally
   stronger isolation than Python's generic shallow instance fallback; it is
   not a promise of constant-time or constant-memory copying of coordinates.
   The maintainer must agree to this semantic choice before implementation.
4. `Interactions.copy()` and its protocol hooks must preserve full/view state,
   selected occurrence indices, coverage, source maps, parallel observations,
   image vectors, provenance and lazy filtered/patched representation.
   Independent deep-copy storage and immutable-buffer sharing in the shallow
   path must be distinguished and tested. Do not materialize a whole analysis
   merely to copy its small owner/metadata shell.
5. Document wrapper-specific shallow behavior explicitly. Plain Python
   dictionaries retain Python's own semantics. Do not silently present all
   serializable forms as if they owned the same domains as `MolSys`.

Private shared mechanics should allocate with `type(self).__new__`, copy state
without invoking migration hooks, and handle domain-specific owner links.
`MolSys.chemical_states` and its topology facade must refer to one copied
collection, not separate copies. A copied standalone topology must be detached
from its original owner. Rebind the owner only when copying the containing
system. A shared helper is worthwhile for common mechanics, but a generic
recursive `__dict__` copier alone cannot establish these guarantees.

Keep one validated public `.copy()` boundary, with `skip_digestion` following
the native API conventions. Python's protocol-supplied memo must not be reset
by the public convenience method. This design adds no dependency, scientific
method, Rust routine or H5MSM schema field.

## Why

Native clients need a reliable way to fork a molecular system before editing.
Today the convenience methods and the Python protocols have different
ownership, representation and subclass behavior. The existing shallow MolSys
fallback demonstrably changes the original's ownership link. A seemingly
lightweight interaction copy also goes through serialization instead of
reusing immutable storage.

### Reproducing the ownership defect

Run from the repository root in the existing development environment:

```bash
python - <<'PY'
import copy
from molsysmt.native import MolSys

source = MolSys(n_atoms=2)
assert source.topology._molsys_owner_ref() is source
clone = copy.copy(source)
assert clone.topology is source.topology
print(source.topology._molsys_owner_ref() is source)  # False at inspected source
print(source.topology._molsys_owner_ref() is clone)   # True at inspected source
PY
```

This is observable before any coordinate or bond edit. It is covered by this
copy-ownership theme rather than a second duplicate issue.

### Reproducing interaction reconstruction

```bash
python - <<'PY'
import copy
import numpy as np
from molsysmt import Interactions

source = Interactions.from_records(
    [{"structure_index": 0, "interaction_type": "pair", "participants": [
        {"role": "first", "atom_indices": [0]},
        {"role": "second", "atom_indices": [1]},
    ]}], n_atoms=2, n_structures=2,
    evaluated_structure_indices=[0, 1], method="synthetic")
for operation in (copy.copy, copy.deepcopy):
    clone = operation(source)
    print(np.shares_memory(source.participant_atoms, clone.participant_atoms))
    print(clone.participant_atoms.flags.writeable)
# False, False for each operation at the inspected source.
PY
```

## What is measured and what is assumed

**Executed:** On small synthetic systems, generic shallow MolSys copying
reassigns the shared topology's owner; ordinary `.copy()` and `deepcopy()`
isolate coordinate buffers in the inspected examples. Editing a bond on the
shallow clone changes the original's bond table as expected from the sharing,
but ownership has already changed even without that edit.

**Executed:** Copying full, queried, invalidated and replaced interaction
results through both Python operations reconstructs numeric storage. The
queried example preserves occurrence order `[2, 0]`; the tested invalidated
and replaced results become ordinary `Interactions` objects. Their source
`_packed_result` remains absent after a fresh copy operation. Do not describe
this as a retained source cache or as measured occurrence-index corruption.

**Executed:** A minimal trusted construction of a `MolSys` subclass followed by
`.copy()` returns base `MolSys`, whereas `deepcopy()` preserves the subclass.
Custom application attributes on `MolSys` are discarded by its manual copy;
the generic deep copy preserves a test cycle and a repeated chemistry alias.
Those custom attributes are an extension-design observation, not a claim that
all arbitrary application payloads are currently supported scientific data.

**Inspected:** `Topology.__setstate__` contains migration and chemistry
normalization; `get_substructure_matches` already constructs a private
inventory view explicitly to avoid that shallow-copy restoration behavior.
Revisit this consumer after the new protocol is proven; do not remove the
workaround merely because hooks have been added.

No representative timing, RSS/peak-memory, large-trajectory or installed-client
benchmark has been run for #121. Buffer sharing and source-state probes are
not performance qualification. Speed or memory improvements remain unmeasured.

## What was refuted

- A plain Python shallow instance copy is already safe: contradicted by the
  owner-link reproduction.
- Reusing `remap()` is equivalent to copying: it is an index transformation,
  rejects query views and reconstructs relations/occurrences. Copy hooks need
  their own invariant-preserving native route.
- Serialization reconstruction is a harmless universal copy backend: it can
  execute migration logic, allocate columns and change lazy representation.
- A shallow molecular copy can share editable coordinates while independently
  guaranteeing interaction freshness: existing edit operations invalidate the
  edited owner, not every possible alias owner. A shared invalidation graph or
  copy-on-write engine would require a separate design and evidence.
- Every Python object under `native` should receive identical copy behavior:
  resident data, payload wrappers, configuration and live file resources have
  different ownership contracts.

## Scope and exclusions

First implement the seven resident data types and their interaction lifecycle;
then reconcile the five payload wrappers. Preserve partial and explicitly
absent domains. Decide the protocol semantics before adding signatures or
changing user documentation to promise them.

Do not implement a shared writable-coordinate view, an automatic dependency
tracker, general copy-on-write, file-resource cloning, another chemical store,
interaction compaction/remapping, or a new scientific detector under #121.
Simulation and file-resource behavior stays an explicit follow-up, not an
unqualified claim that all native types are complete.

## Acceptance criteria

- Public calls preserve expected values, units, IDs, exact indices and partial
  domain presence; invalid options fail at the public validation boundary.
- Copying leaves the original's ownership, data, coverage and lazy state intact.
- Molecular edits through an independent copy invalidate only that copy's named
  observations. The original's coordinates and analyses remain unchanged.
- Standalone topology copies have no original MolSys owner; complete system
  copies bind the copied topology to the copied system and preserve the single
  chemical-state collection behind the compatibility facade.
- A shared memo preserves graph aliases and cycles; supported subclasses retain
  their type and extension state without calling ordinary constructors.
- Interaction hooks preserve parallel occurrence identity, reordered query
  views, invalidated/replaced results, metadata and periodic geometry; shallow
  immutable storage sharing and deep buffer independence are asserted directly.
- No form discovery, inference, migration, encoding or disk I/O is needed to
  copy an ordinary resident object. Copying a lazy result does not pack it.
- Focused memory/timing probes use fixed data sizes and account for the allowed
  shallow sharing separately from full independent mutable storage.
- NumPy docstrings, native Foundations, Toolbox, Cookbook and the relevant
  course sections explain the chosen semantics with executable examples.

## Provenance

Inspected MolSysMT `3d47650271ea518042419b24de1a108a187415c4` and TopoMT
`c3f72a9177ab8a205b69fefc2963800a2d0b4feb` on 2026-10-21. Local probes used
Linux, Python 3.14.7, NumPy 2.4.6 and pandas 2.3.3 in the existing development
environment. TopoMT was read only. No runtime implementation was changed.
