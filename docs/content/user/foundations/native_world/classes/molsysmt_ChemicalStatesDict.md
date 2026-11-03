(user-foundations-native-world-classes-molsysmt-chemicalstatesdict)=
# ChemicalStatesDict

## Overview and Role

`molsysmt.ChemicalStatesDict` wraps versioned typed chemical-state columns on one
declared atom-index domain. Its `.data` is a Python dictionary containing NumPy
arrays and explicit null masks. It does not contain coordinates or replace the
stable atom/group/molecule inventory in Topology. The form remains experimental
during the coordinated ChemicalStates migration.

## Declarative Schema

| Field | Meaning |
| :--- | :--- |
| `schema` | `molsysmt.chemical_states_dict`. |
| `version` | 1, or 2 when preparation history is encoded. |
| `n_atoms` | Shared atom-domain size; atom indices remain positions. |
| `reference_chemical_state_index` | Nullable reference position. One stored state resolves as reference 0 even if this field is None. |
| `states` | Ordered state records, each with IDs, completeness/evidence, optional history, atom attributes, bonds, component rows and atom-to-component membership. |

Each table stores `n_rows` and a `columns` mapping. A column carries `dtype`,
one-dimensional `values` and a same-shaped boolean `null_mask`. True in the mask
means unknown; its placeholder magnitude carries no value. A missing atom-property
column differs from a present nullable column. Formal charges retain Int16 counts
in multiples of elementary charge. Bond order is dimensionless. No coordinate
units or application-dependent charge conversion are inferred while reading.

## Querying Stored Data

Use `payload.get(...)` or `msm.get(payload, ...)` for the same supported stored
axes, counts, atom/bond fields, membership and component labels as
{ref}`ChemicalStates <user-foundations-native-world-classes-molsysmt-chemicalstates>`.
State-dependent reads accept `chemical_state` as an explicit positional index or
the reference sentinel. Collection inventory remains collection-wide. Missing,
invalid and ambiguous state selections reject without changing `.data`.

Explicit atom, bond and component index lists retain order and repetitions. Masks
use the same sorted intersection as `basic.get`. Bounds follow the selected state.
Unknown memberships project to None, preserving nullable field/stereo-reference
shapes and the distinction between zero states and a complete edge-free graph.
`payload.info(...)` follows the same output vocabulary as `basic.info`; its
summaries currently use the reference state, without a new state-selector option.

These reads use typed columns directly. They do not decode a native collection,
construct Topology, infer chemistry or validate unrelated state/history records.
Requested metadata and column lengths, masks, dtypes and references are checked.
A successful query does not certify the entire payload or historical evidence.
Small field selections slice values/masks before producing Python results; no
full-state caches or analysis objects are attached to the payload.

## Editing and Copying

Use `msm.set(payload, chemical_state=..., ...)` for the same stored atom/bond
assignments and declared component membership/labels as ChemicalStates. One
attribute materializes only the selected state through the existing typed codec,
uses the canonical native validation/mutation boundary, and encodes its replacement
before publication. Failure preserves the original payload; other records and the
reference remain unchanged. Several attributes are separate assignments. This
write boundary can cost the selected state's storage, unlike small direct reads.
For graph editing methods, explicitly convert to ChemicalStates first.

`msm.contains` and `msm.is_composed_of` accept the keyword-only `chemical_state`
selector for state-dependent supported counts. Stable hierarchy requires a provider
that actually stores it. Direct `.data` writes bypass validation, graph
reconstruction and owner notification; raw mutation is not controlled editing.

Converting native chemical states to this form creates independent writable
column values and null masks, including with Pandas Copy-on-Write. Editing that
transport does not edit the source state. Convert the edited payload back to
ChemicalStates when you need native validation.

`payload.copy()` and `to_dict(copy=True)` return detached mutable payloads;
`to_dict(copy=False)` exposes the current mapping. Copying does not validate or
decode chemical states. Independent payload wrappers have independent query
scopes; nested/concurrent read-only state selections restore their callers.
Concurrent mutation is outside this contract.

## Persistence Boundaries

The NumPy-backed payload is not directly JSON serializable. Convert explicitly to
the native owner before using the public molecular persistence routes. H5MSM 0.5
stores the chemical domain independently of topology, structures and interactions;
see {ref}`user-tools-form-h5msm-05`. Reading these in-memory columns is distinct
from a public on-disk query API and does not change any file or dictionary schema.

## API Documentation

See {ref}`API Native Queries` for inherited method signatures,
{func}`molsysmt.basic.get`, {func}`molsysmt.basic.info` and
{ref}`the native chemical editing guide <Tutorial_Native_Chemical_Editing>`.
The executed native-forms course example demonstrates selected-state queries
on the typed payload.
