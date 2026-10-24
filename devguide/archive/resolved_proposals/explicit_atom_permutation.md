---
summary: Apply explicit atom permutations through a public native molecular operation.
issue: uibcdf/molsysmt#369
status: resolved
opened: 2026-10-10
closed: 2026-10-24
verification: measured
area: [basic, native, extract, api]
guard: tests/basic/test_permute_atoms.py
normative:
blocked_by: []
supersedes: []
---

# Explicit atom permutation across molecular domains

**Reported:** 2026-10-10, provider request from uibcdf/dockingmt#49.
**Status:** Resolved on 2026-10-24 after the maintainer brings #369 forward
following the provider delivery of #223. Existing extraction semantics remain intact.

## What

Apply a caller-supplied complete atom permutation to a detached native molecular
system, with forward/inverse maps and coherent remapping of every present domain.
The immediate consumer reconstructs a prepared flexible ligand from a known PDBQT
record traversal when the original native source is unavailable.

## How

Source inspected at `072aa9bdbfb9299f7e3256f9b27f6aae8ea52629` establishes:

- `basic.extract` and `MolSys.extract` are selection operations. With topology,
  atom selections retain sorted source-index order; a full reversed selection
  does not promise a reversed output. This is documented behavior.
- `Structures.extract` can index coordinate atoms, and `Interactions.remap` accepts
  desired output atom order and composes source maps. These are useful domain
  pieces, not a complete molecular permutation operation.
- Native extraction already coordinates chemistry, structures, atom-aligned
  mechanics, preparation/type evidence and named interactions. Reuse those owners
  rather than creating an independent downstream reconstruction policy.

Consider a distinct general operation in `basic`, backed by native domain remappers;
choose its final name and public signature during design. Do not change the
meaning of `extract` to make it a permutation API.

Use an explicit convention such as `new_to_old[new_index] = old_index`. Validate
a complete integer bijection, rejecting booleans, duplicates, missing or
out-of-range positions and malformed shapes before copying/mutating domains.
Return an independent system and both directions of correspondence. Atom IDs
remain their original string labels; atom indices are positions.

Remap topology memberships, all chemical states' atom assignments and bond/stereo
references, every structure's coordinates, per-atom mechanics and named
interactions, including compound participants and coverage. Preserve box/time,
units, structure/state associations and original producer evidence. Historical
preparation records retain their declared operation axes; a derived permutation
must not silently reinterpret their recorded indices as current indices.
Specify handle/source-map behavior and trace the transformation explicitly.
Reject unsupported present domains or require a separately declared loss policy.

## Why

A known export traversal can be inverted without chemical graph matching. The
consumer currently has a bounded reconstruction path, but wants to retire that
duplication under a provider-owned public contract. Its reported PDBQT example
demonstrates an API gap, not an extraction regression. The
[admission rule](../../release_1_0_scope.md#admission-rule) places the new operation
after 1.0. Atom identity/export work in uibcdf/molsysmt#223 and
uibcdf/molsysmt#226 does not imply this missing full-domain permutation contract.

## What is measured and what is assumed

This provider review inspected source/docstrings without executing a new
permutation experiment. The issue separately records a consumer reproduction on
provider `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`: a reverse full-atom
selection retains source order. That observation is consistent with the current
documented contract; it is not evidence that any proposed permutation API works.
No runtime, memory or serialization benchmark was performed here.

## What was refuted

Reordering coordinates alone leaves bonds, chemistry and interactions addressing
the wrong atoms. A complete atom selection is not implicitly a permutation.
Matching names or IDs cannot replace an explicit known bijection. Domain-local
remapping does not prove that arbitrary combined molecular domains are supported.

## Scope and acceptance criteria

- Exercise reverse and nontrivial permutations with independent expected atom
  correspondence, and verify inverse restoration and source immutability.
- Include multiple structures and chemical states, stereo references, partial and
  complete connectivity, named interactions and supported mechanical payloads.
- Verify identities, membership, units and producer/source maps across supported
  conversions and H5MSM 0.5 persistence; do not claim mechanical persistence that
  the file format explicitly excludes.
- Reject malformed permutations and unsupported domain combinations before any
  mutation or partial output; document errors and memory costs.
- Supply the public validation and full documentation lifecycle, with a consumer
  test allowing DockingMT to retire its reconstruction only for supported inputs.

No automatic atom matching, hydrogen addition, bond/stereo inference, symmetry
search or pose recovery is part of this operation. Symmetry mapping in
uibcdf/molsysmt#310 remains a separate capability.

## Accepted implementation slice — 2026-10-24

The maintainer selects #223 then #369 during the publication pause. The provider
portion of #223 is now complete. Implement an experimental form-agnostic
`basic.permute_atoms(molecular_system, atom_indices, return_report=False,
skip_digestion=False)`, returning a detached native MolSys and optionally an
existing typed `atom_map@1` report. `atom_indices[new] = old` is a complete
explicit bijection; no selection, discovery or matching is implied.

Only the atom axis changes. Group, molecule, chain, entity, component, bond and
structure axes/IDs retain their original positions. Bond endpoints and stereo
references follow the atom map while preserving canonical endpoint orientation.
Original preparation records retain historical axes; named charge/type bindings
use the existing projection owners plus an explicit permutation transform.
Coordinates are rebuilt in protected blocks through ChunkedExecutor, not a
dense trajectory intermediate. Identity permutations share protected geometry
through independent handles. Other series retain their canonical storage units.

The initial profile supports the declared built-in native domains; unknown
subclasses/extensions or unsupported present payloads fail explicitly. Non-native
inputs use ordinary public conversion, with that converter's own cost/loss
contract. Full output remains resident: numeric output over the configured
budget fails before allocation; no incremental file permutation is promised.
No public extract or principal Iterator behavior changes.


## Delivered contract and evidence — 2026-10-24

`molsysmt.basic.permute_atoms` and the root alias apply the declared full
bijection. The private native orchestrator uses existing native copy/ownership
hooks with already-remapped tables in a shared deepcopy memo. It does not copy
then rebuild an entire molecule a second time. Atom validation is linear after
normalization; no pair matrix or graph matching is constructed. Optional report
label arrays are built only when requested.

The existing bond remapper now optionally canonicalizes remapped endpoints,
swapping endpoint-associated stereo neighbors together. Directed donor/acceptor
references retain their roles. This keeps bond row indices fixed, unlike a new
bond-table sort. Components retain even unused rows. Named interactions reuse
`Interactions.remap`; occurrence identity and source maps survive. Protected
coordinate delivery reuses ChunkedExecutor and native immutable blocks; no
principal Iterator or extract contract changes.

Mechanics supports its canonical per-atom columns and scalar settings (plus
force-field name lists). Unknown positional payloads, subclasses, extension
fields, table metadata and inconsistent references reject explicitly. The
function transports existing chemistry; it does not validate that a scientific
assignment was originally correct. Charge/type projection owners preserve
original producer attribution, bind valid assignments to the new axis, retain
stale status and add `atom_order_transform`. Historical reports retain their
historical axes. No new scientific calculation or Ackredit credit is generated.

Validation in the development Python 3.14.7 environment:

- 1,087 selected regression tests and doctests passed in 26.64 s with pytest-receptor and
  twelve workers: native domains, atom maps, nonpolar-H projection, name
  projection, known-source PDBQT poses and public interaction persistence.
  These retain the selected suites' 42 legacy/deprecation/domain warnings.
- The final focused guard covers 48 cases, including reverse/nontrivial/identity
  and empty orders; both validation paths; malformed/unit-bearing axes; multiple
  states and structures; literal bond and stereo references; independent RDKit
  E/Z and absolute-stereo recovery; compound/parallel interaction observations;
  empty versus unevaluated coverage; original and stale scientific provenance;
  source independence; chunk bounds without dense geometry/extract fallback;
  full and structures-only H5MSM; and restoration of a literal PDBQT writer axis.
- The public docstring doctest passed. Both new tutorial/recipe pages' Python
  blocks executed. Common Core module 18 was re-executed successfully (8.6 s),
  including its existing extraction/removal content.
- Public API/signature, docstrings, dependency contract, course and fourteen
  fast release checks passed. Sphinx HTML compilation passed with inherited
  course-heading and orphan-document warnings; this is not a warning-free build.
- H5MSM 0.5 excludes MolecularMechanics. The full-system persistence guard clears
  that domain explicitly; it does not claim the omitted mechanics was persisted.

### Bounded local allocation experiment

Single measured calls after a two-atom warm-up, Linux/Python 3.14.7, using the
existing development environment. Inputs are built-in MolSys with default
identity/chemical tables and zero coordinates; order is full reverse and
`return_report=True`. There are no bonds, alternate sites or interaction analyses
in this experiment. It is an axis-transport measurement, not a general molecular
workflow benchmark or installed-candidate qualification.

| Atoms | Structures | Coordinate output bytes | Seconds | Traced retained bytes | Traced peak bytes |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 1,000 | 24,000,000 | 0.149 | 24,530,519 | 25,576,669 |
| 10,000 | 100 | 24,000,000 | 0.202 | 25,448,792 | 27,094,799 |
| 100,000 | 10 | 24,000,000 | 1.025 | 37,502,348 | 56,336,323 |

Reproduction of the measured section (construct each source before starting
tracemalloc, collect garbage between cases):

```python
import gc
import time
import tracemalloc
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys, Structures
msm.permute_atoms(MolSys(n_atoms=2), [1, 0])
for n_atoms, n_structures in [(1000, 1000), (10000, 100), (100000, 10)]:
    source = MolSys(n_atoms=n_atoms)
    source.structures = Structures(coordinates=msm.pyunitwizard.quantity(
        np.zeros((n_structures, n_atoms, 3)), 'nm'))
    order = np.arange(n_atoms - 1, -1, -1)
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()
    result = msm.permute_atoms(source, order, return_report=True)
    elapsed = time.perf_counter() - start
    retained, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(n_atoms, n_structures, elapsed, retained, peak)
    del source, result
```

Tracemalloc starts after source construction, so these numbers exclude the
resident input and are not process RSS. They include the measured call's numeric
and tracked object allocations. Output geometry remains fully resident; bounded
coordinate delivery does not make a molecular file permutation out-of-core.
More atoms also require more tables, labels and maps even at equal coordinate
payload. Identity geometry uses independent handles over shared immutable bytes.
The preflight budget estimates numeric/table payload; temporary remapping,
Python object overhead and conversion costs still need additional memory.

### Consumer handoff and remaining boundaries

DockingMT can consume the declared prepared/written bijection and use the public
operation for supported native payloads. The consumer's producer/reconstruction
migration remains owned by uibcdf/dockingmt#49; provider tests do not establish
that its production pipeline has migrated. The PDBQT guard restores only
information present in the parsed file, including its partial graph. It invents
no missing hydrogens, chemical bonds or coordinates. Symmetry discovery remains
uibcdf/molsysmt#310. Out-of-core transforms and extension remapping require a
separate demonstrated need. No package/tag/Release or installed-candidate
qualification is included in this delivery.
