---
summary: Apply explicit atom permutations through a public native molecular operation.
issue: uibcdf/molsysmt#369
status: open
opened: 2026-10-10
closed:
verification: inspected
area: [basic, native, extract, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit atom permutation across molecular domains

**Reported:** 2026-10-10, provider request from uibcdf/dockingmt#49.
**Status:** Post-1.0 capability proposal; existing extraction semantics remain intact.

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
[admission rule](../release_1_0_scope.md#admission-rule) places the new operation
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
