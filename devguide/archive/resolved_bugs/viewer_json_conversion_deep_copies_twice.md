# `MolSys → ViewerJSON` spends ~93% of its time deep-copying

**Reported:** 2026-07-31, from MolSysViewer, while measuring standalone startup.

**Severity:** performance only. No incorrect result, no hidden failure. It
dominates every viewer load of a trajectory.

## Evidence

`pentalanine` trajectory, 62 atoms × 5,000 structures, on Linux / Python 3.13:

```python
import cProfile, pstats, molsysmt as msm
s = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                to_form='molsysmt.MolSys')
cProfile.run("s.to_form('molsysmt.ViewerJSON')")
```

| frame | cumtime |
|---|---:|
| `molsysmt_MolSys/to_molsysmt_ViewerJSON.py:24` | **4.99 s** |
| ↳ `native/viewer_json.py:103(to_dict)` — **2 calls** | **4.64 s** |
| ↳ `molsysmt_Structures/to_molsysmt_ViewerJSON.py:20` (the real work) | 0.35 s |

1,350,867 `copy.deepcopy` calls, 330,087 of them `_deepcopy_list`. The actual
structural conversion is 7% of the total.

## Cause

`form/molsysmt_MolSys/to_molsysmt_ViewerJSON.py`:

```python
topo_vjson   = topology_to_viewer(item.topology, skip_digestion=True)
struct_vjson = structures_to_viewer(item.structures, skip_digestion=True)

viewer = ViewerJSON()
topo_data   = topo_vjson.to_dict()      # deepcopy
struct_data = struct_vjson.to_dict()    # deepcopy — ~930,000 floats here

viewer.data["atoms"]      = topo_data.get("atoms", {})
viewer.data["bonds"]      = topo_data.get("bonds", {})
viewer.data["structures"] = struct_data.get("structures", ...)
```

`ViewerJSON.to_dict()` defaults to `copy=True`
(`native/viewer_json.py:109`), which is a reasonable default for a public
accessor. But **both objects being copied here were built by this same function
two lines earlier, are local, and are discarded on return.** The copies are then
handed straight into `viewer.data`, so ownership transfers anyway. Nothing
observes the originals again.

The copy protects against nothing and costs 4.6 s.

## Proposed fix

```python
topo_data   = topo_vjson.to_dict(copy=False)
struct_data = struct_vjson.to_dict(copy=False)
```

The `copy=False` path already exists and is public.

Worth checking in the same pass whether `form/molsysmt_ViewerJSON/to_molsysmt_ViewerJSON.py`
— an identity conversion whose whole body is `deepcopy(item)` — is on any hot
path. An identity conversion that deep-copies is defensible as a contract
(callers may assume they own the result); it is expensive if it is reached
during an ordinary `to_form` chain.

## Acceptance

- `MolSys → ViewerJSON` on the 5,000-structure case drops from ~5 s to well
  under 1 s.
- A test asserts the returned `ViewerJSON` does not alias the intermediate
  topology/structures containers in any way an observer could detect — i.e. the
  intermediates are genuinely unreachable, so `copy=False` is not merely faster
  but correct.
- Mutation check: restoring `copy=True` makes the timing regress; the
  correctness test stays green either way, which is what proves the copy was
  redundant rather than load-bearing.

## Downstream note

MolSysViewer had the *same* defect one layer up — `_serialize_molsys_payload`
called `viewer_json.to_dict()` with the default copy on a fresh, local,
read-once object. Fixed there on 2026-07-31; that half was 1.23 s of a 3.9 s
load. This report is the other half, and it is the larger one.
