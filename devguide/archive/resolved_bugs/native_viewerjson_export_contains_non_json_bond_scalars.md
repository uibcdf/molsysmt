---
summary: Native ViewerJSON export contains non-JSON bond scalars
issue: uibcdf/molsysmt#398
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [form, convert, tests]
guard: tests/form/molsysmt_Topology/test_to_molsysmt_ViewerJSON.py::test_topology_export_has_json_scalars
normative:
blocked_by: []
supersedes: []
---

# Native ViewerJSON export contains non-JSON bond scalars

**Reported:** 2026-10-21 during registered payload copying checks for #121.
**Status:** Resolved; the native exporter normalizes nullable table scalars.

## What

A two-atom native topology with one covalent bond exports to ViewerJSON, but
`payload.dumps()` raises because the generated bond indices are numpy.int64.
The wrapper declares JSON-compatible data and uses the standard JSON encoder.

```python
import molsysmt as msm
from molsysmt.native import Topology
source = Topology(n_atoms=2)
source.add_bonds([[0, 1]])
payload = msm.convert(source, to_form="molsysmt.ViewerJSON")
assert type(payload.data["bonds"]["atom_pairs"][0][0]).__name__ == "int64"
payload.dumps()
# TypeError: Object of type int64 is not JSON serializable
```

## How

`molsysmt/form/molsysmt_Topology/to_molsysmt_ViewerJSON.py` creates bond pairs
from pandas columns and then wraps each tuple with `list(pair)`. That changes
the container, but preserves NumPy scalar members. The same pairs feed
`indexA`/`indexB`. `ViewerJSON.dumps` delegates to `json.dumps`, which rejects
those scalar types. Audit order/type/null values as part of that converter's
JSON boundary rather than assuming that lists imply JSON-safe contents.

## Why

The native export cannot complete its advertised JSON serialization route for
an ordinary bonded system. MolSys projection reuses this topology converter.
A copy faithfully retains these values and cannot repair the producer's schema.

## What is measured and what is assumed

**Reproduced:** the exact two-atom example above in Linux/Python 3.14.7.
A separate four-atom native MolSys fixture failed identically. No performance,
visual rendering or installed-client qualification is claimed.

## What was refuted

Resident copy hooks are not the cause: the original exported wrapper fails
without copying. The payload is not an arbitrary user-supplied dictionary; it
was produced by MolSysMT's registered converter.

## Scope and exclusions

Normalize JSON scalar/container types at the native export boundary and guard
its JSON output. Keep ID/index semantics intact. The independent ViewerJSON
native reader defect is uibcdf/molsysmt#397. Do not silently make resident copy
or a query decoder responsible for repairing serialization.

## Acceptance criteria

A generated bonded topology and a MolSys with coordinates must serialize with
the standard JSON encoder. Decode the JSON and assert literal bond pairs,
indices, order/type/null values and coordinate units. Include empty bonds.
No NumPy-only custom encoder may hide non-JSON values in a supposedly pure
payload returned by `to_dict`.

## Provenance

Observed 2026-10-21, Linux, Python 3.14.7, development environment. Both the native
topology exporter and wrapper JSON encoder are unchanged from `e83d854b2`.

## Resolution — 2026-10-21

The topology exporter converts NumPy scalar values to their Python counterparts
and missing values to None at its table boundary. Bond pairs, endpoint columns,
orders, types and formal charges share this route. The wrapper and standard
JSON encoder remain unchanged. MolSys still transfers its locally owned
intermediate payloads without defensive duplicate copies. No new dependency,
scientific method, attribution boundary or persistence schema was introduced.

**Contract-tested:** before the fix, the new bonded-payload guard failed on an
int64 endpoint and the nullable formal-charge guard failed on an int16 value
(2 failed, 2 passed). After the fix, the focused native Topology/MolSys/Structures
export and ViewerJSON reader tests obtained **14 passed**, no omissions, with
`python -m pytest --receptor=llm -n 12` on Linux/Python 3.14.7.
The guard recursively checks concrete JSON types before encoding and literal
bond values after standard encoding, wrapper encoding and disk writing. Separate
tests cover nullable formal charges and MolSys coordinate/time conversion from
angstrom/femtosecond to nanometer/picosecond. This is provider-source evidence;
rendering, installed clients, non-finite input policy and full-suite qualification
are not claimed. The independent reader defect remains tracked in #397.
