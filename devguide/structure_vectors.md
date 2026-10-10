# Directed molecular vectors

**Role:** normative geometry contract. **Tracking:** uibcdf/molsysmt#375.
**Public stability:** experimental, admitted by the maintainer on 2026-10-10.

`structure.get_vectors` computes directed endpoint geometry using the same
selection vocabulary as `structure.get_distances`. Endpoint 1 is the origin;
endpoint 2 is the destination. Atoms, geometric centers and positive-weight
centers may be mixed. Nested selections imply one center per membership.
Relative weights follow flattened memberships; repeated/overlapping memberships
are retained. Geometric operations do not add hydrogens or reinterpret chemistry.

## Axes and outputs

- Atom pairs are ordered. `pairs=True` evaluates corresponding endpoints only;
  an explicit two-column numeric selection supplies donor-H or arbitrary pairs.
  The flat `[a, b]` shorthand defines one pair. Paired nested centers require
  an explicit center flag or `selection_2` to avoid pair-table ambiguity.
- Without pairs, the endpoint axes form a Cartesian product. The final axis has
  three Cartesian length components. There is no structure-axis Cartesian
  product: both structure lists have equal length and align by position.
- Requested structure order and repetitions are preserved, including repeated
  references for displacement calculations. Indices are source positions, not
  source IDs. No implicit singleton broadcasting is provided across structures.
- Array output is a PyUnitWizard length quantity. Optional endpoint and structure
  labels precede it in a tuple. Generic molecular group labels are unsupported;
  centers retain explicit atom memberships rather than invented group indices.
- Dictionary output is a flat typed record: vectors, scalar distances,
  dimensionless normalized directions, int32 images, both packed atom memberships
  and source structure axes, calculation mode, relative weighting parameters,
  direction convention and original MolSysMT producer version.
- Zero vectors are valid and have zero length; normalized direction is NaN.
  Empty axes preserve shape/dtype. Nonfinite or unrepresentable geometry raises.
  Neither source coordinates nor stored chemical/interaction domains are edited.

## Periodic convention

PBC follows the first source's box availability, as in `get_distances`. With a
box, MIC uses the shared Rust reduced-cell primitive. The first structure's
box defines the reference even when the second endpoint comes from a different
structure/system with a different box. Row-vector images reconstruct

```text
v = r_second + image @ box_first - r_first
```

The first endpoint remains the reference image. Nonfinite/numerically singular
reference boxes fail. Exact minimum-image ties follow the existing deterministic
kernel convention; endpoint reversal need not select the opposite tied vector.
This operation does not infer accumulated periodic travel or unwrap a trajectory.

Before forming a periodic center, all its atoms must already occupy the anchor's
MIC image in the reference box. Split memberships fail through the shared PBC
participant check. Users may reconstruct supported covalent components with the
public PBC tools first; vector calculation itself is immutable. This explicit
policy avoids taking an arithmetic mean across split images or inventing
connectivity for arbitrary atom memberships.

## Execution and quantities

The validated Python boundary resolves endpoint memberships and source axes once.
Internal delivery uses canonical nm blocks; final length quantities follow the
active PyUnitWizard standard/backend. Rust borrows contiguous numerical input,
reuses MIC box preparation and releases the GIL. Disjoint structure outputs use
the existing Rayon pool. Dictionary lengths/directions/images share that pass;
the ordinary array path does not allocate those detail arrays.

Already ordered atom memberships avoid duplicate discovery/sorting. Complete-axis
delivery uses the canonical `all` selector, and identity projections retain
coordinate views. Unordered/repeated memberships still use a unique coordinate
projection and explicit remapping. These optimizations do not reorder endpoints.

`ChunkedExecutor` owns large source delivery. For independent second structure
axes/systems, its second-endpoint projection collects only the current first
block, rather than all second-source coordinates. Blocks write into one resident
output allocation; no result list/concatenation is accumulated. Forced streaming
requires both sources to advertise structural delivery. Eager fallback uses
public form-agnostic getters when a declared iterator is absent.

The dense result must fit the numerical RAM budget. Planning reserves final and
unit-presentation buffers, detached metadata, first/second projected coordinates,
packed-center work and simultaneous block outputs. Working estimates are not
process-RSS guarantees: provider imports, Python objects, allocator caches and
form implementation overhead remain outside them. Output uses 24 bytes per
vector in float64, or 68 numeric bytes per comparison with dictionary details,
before metadata and unit-conversion copies. There is no automatic disk-backed
output, GPU engine, incremental writer or checkpoint/resume contract.

## Fixed-state donor composition

Use `physchem.get_hbond_sites` for chemical recognition, then pass its explicit
donor-H pairs to `get_vectors`. Retain the detached chemical inventory alongside
the geometry dictionary: geometry does not replace chemical-state/rule evidence.
Resolve a coherent chemical state in recognition before composing the recipe.
The executed hydrogen-bond cookbook demonstrates nonconsecutive structures.

This delivers observed donor-H directions. Acceptor indices alone do not specify
lone-pair directions. Named acceptor models, multiplicity and unsupported chemistry
remain the pending portion of uibcdf/molsysmt#375. Environmental refinement belongs
to uibcdf/molsysmt#323; neither capability is implicit in general vectors.

## Verification and performance

`tests/structure/test_get_vectors.py` contains independent coordinate, weighted
center and lattice-enumeration controls, source-index preservation, typed empties,
zero directions, unit/backend contexts, immutability, bounded blocks and
recognition composition. Scalar-distance parity is a supplementary contract
control, not the sole numerical oracle.

See [the reproducible measurements](benchmarking/vectors.md). Source tests and
local release-profile native measurements do not qualify a new installed package
or change any frozen candidate identity under uibcdf/molsysmt#334.
