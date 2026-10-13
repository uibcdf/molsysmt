# Chemical correspondence and pose RMSD

The experimental public tools `topology.get_atom_correspondences` and
`structure.get_symmetry_corrected_rmsd` separate chemical equivalence from
coordinate evaluation. Their accepted implementation is tracked by
uibcdf/molsysmt#310. `get_rmsd` retains positional semantics and `get_least_rmsd`
retains superposition semantics.

Caller constraints extend these tools under uibcdf/molsysmt#387.

## Declared-state admission

Select a nonempty metric population inside one covalent component. The whole
component supplies context, including explicit H and unselected substituents.
Both graphs require complete connectivity, elements, formal charges, aromaticity,
radicals, stored implicit/explicit H counts and policy, and atom stereo metadata.
Missing isotope labels mean unlabeled atoms. Bond orders 1/1.5/2/3 and aromatic
flags are exact constraints; aromatic declarations are not reperceived to make
incompatible representations match. Potential stereo must be assigned. Tetrahedral
R/S/r/s and double-bond E/Z are supported; dative, enhanced and other stereo are not.

RDKit conversion must retain those assignments. Component discovery reuses the existing Rust union-find primitive. Matches are compiled,
non-uniquified and chirality-sensitive. Exact source labels, bonds and membership
are checked after matching. Equivalent selected-atom projections are deduplicated,
retaining one whole-context witness. Maps are sorted lexically by reference source
indices in canonical query source order. Incompatible supported graphs return
int64 arrays of shape `(0, n_selected, 2)`; unsupported/missing evidence raises.

No resonance normalization is admitted. In benzamidinium +1 declared as
`NC(=[NH2+])c1ccccc1`, phenyl reflection is allowed and the two N roles stay distinct.
Both sides require the same indexed-H representation and stored H policy.
Explicit/implicit H representation normalization is separate preparation.
Different protonation/stereo states require explicit compatible preparation;
an experimental coordinate reference is not automatically a simulation-state graph.

## Detached result and reuse

`molsysmt.atom_correspondences@1` dictionaries retain selected and complete-context
maps, source atom counts, states and provenance, search completeness, original
producer versions and attribution. All pair columns are positional indices, not
IDs. Digests include ordered chemical labels, bonds, context/metric axes and state
index; a separate payload digest detects changed mapping arrays. They are consistency
checks, not authentication or a replacement for declared source correspondence.

Coordinate changes do not invalidate chemistry-only maps. Chemistry, populations
or axes changing requires recomputation. Reuse rebuilds and checks current chemical
context/witnesses without enumerating graph matches again. It retains the original
map producer and records the new geometry producer separately.

## Anchors and proposed maps

Both public tools accept keyword-only `fixed_atom_correspondence` and
`candidate_atom_correspondences`. Pair columns are query and reference source
indices. Selections are canonical populations, never positional pair declarations.

Anchors are a partial injective `(n_fixed, 2)` table, including unselected atoms
inside the complete components. RDKit compares temporary atom properties on
detached graph copies during compiled matching, pruning candidates before the
enumeration cap. Chemistry and chirality still apply; isotope labels are not
overwritten to encode pins. Empty anchors are equivalent to no anchors.
Incompatible chemical anchors yield a typed empty topology result and an explicit
RMSD failure. Duplicate endpoints, booleans, floats, negative/out-of-component
indices and contradictory candidate declarations raise argument errors.

Proposed maps cover both selected populations bijectively: `(n_selected, 2)`
for one map or `(n_maps, n_selected, 2)` for a nonempty collection. Each candidate
must extend through the whole chemical context and respect every anchor. Any
invalid proposal fails the call; candidates are not silently discarded.
Duplicates and row/input order do not alter the admitted set or lexical tie order.
Temporary exact atom/bond properties and chirality-sensitive matching find an
extension with at most one returned witness per probe. Greedy existence probes
fix the lexical minimum complete-context witness without materializing factorial
permutations of unselected H. Worst-case probe count is quadratic in context size
per candidate; search time itself remains unbounded by the count limit.

`search_scope` is explicit in both results:

| Scope | Meaning of the minimum and `search_complete=True` |
| --- | --- |
| `all_chemical_correspondences` | All admitted chemical correspondences. |
| `anchored_chemical_correspondences` | All admitted correspondences respecting the anchors. |
| `supplied_atom_correspondences` | Only the distinct validated maps supplied by the caller. |

An anchored or supplied-map minimum does not certify the unrestricted minimum.
Constraints are detached, canonical and protected by the payload consistency
digest. Reuse retains the stored scope without enumerating again; passing cached
`correspondences` together with new constraint arguments raises rather than
silently changing the candidate set. Earlier unconstrained `@1` dictionaries
without these additive fields retain unrestricted semantics.

`baseline_atom_correspondence` remains independent: it determines only
`raw_rmsd`, supplies no anchors and does not admit proposed corrected maps.

## Geometric evaluation

For each query structure evaluate the equal-weight positional RMSD over admitted
maps and report its actual computed minimum. No translation, centering, rotation,
reflection or MIC is applied. Periodic reconstruction belongs to an explicit `pbc`
operation; consumers preserve a common Cartesian receptor frame.

The dictionary shares a mapping table and stores one `correspondence_indices` row
selection per requested structure. Structure order and repetitions are preserved.
Exact numeric ties choose the lexical first map. A nonnegative absolute length
`tie_tolerance` counts near-optimal maps without changing the selected minimum.
`raw_rmsd` is present only with a caller-declared original source/reference map;
its validity as source identity is the caller's declaration. It is not inferred
from equal counts, names or IDs. If the original map violates the admitted chemical
policy, there is no guarantee that corrected RMSD is below that baseline value.

Numeric inputs are converted to nm; outputs and tolerance follow the active
PyUnitWizard length policy. Nonfinite input or arithmetic fails without partial
success. An empty structure request retains empty quantities and int64 index arrays.

## Cost and limits

Enumerate at most `max_matches + 1` whole-component candidates before projection
or exact-label filtering. Overflow refuses a result. The candidate working estimate
reserves `256 + 192*n_context_atoms` bytes per candidate; one quarter of configured
RAM bounds it. This estimate includes tuples, projected keys and output packing;
full graph objects and process RSS are not bounded. A count cap does not impose a
wall-clock timeout.

Anchored enumeration counts complete candidates after anchor pruning and before
the existing exact-label/projection filter. Supplied-map mode bounds distinct
proposed maps with `max_matches` and the same candidate reserve. Input digestion,
canonicalization and detached graph objects are not a total-RSS bound. Geometry
reserves also include detached constraint tables. Supplying maps avoids global
enumeration, not chemistry validation or the optional RDKit requirement.

RMSD delivery reuses `execute_projected_geometry` and `ChunkedExecutor`. Resident
output, detached table copies, local map projections and reference workspace occupy a separate half-RAM
numeric reserve; blocks use the shared quarter-RAM reserve. The per-structure block
estimate is 4096 + 96*n_selected + 32*n_maps bytes, including the bounded score
matrix, temporary tie arithmetic and coordinate work. Only one reference coordinate
permutation is materialized at a time; no structures*maps*atoms tensor is created.
Forced streaming requires a declared real route. Complete output stays resident.

## Scientific attribution

Bell and Zhang (2019), DOI 10.1186/s13321-019-0362-7, and Meli and Biggin (2020),
DOI 10.1186/s13321-020-00455-2, are methodological inspiration. MolSysMT's exact
declared-state policy is not a faithful reproduction of DockRMSD or sPyRMSD.
RDKit is executed software. When assigned stereo labels are used, its Hanson et
al. (2018) CIP implementation (DOI 10.1021/acs.jcim.8b00324) is a separately
credited scientific criterion; the shared stereo helper retains its original
algorithm semantics. Bibliography is detached in every completed result;
Ackredit optionally records contextual roles in the application's existing session.
Failure/absence of attribution preserves science and host records; failed science
does not earn a completed-operation credit. Reading saved dictionaries credits nothing.

Anchor pruning and witness search use RDKit's documented `atomProperties` and
`bondProperties` matching API, with MolSysMT constraints and canonicalization:
[RDKit SubstructMatchParameters](https://www.rdkit.org/docs/source/rdkit.Chem.rdchem.html#rdkit.Chem.rdchem.SubstructMatchParameters).
No additional publication's anchor algorithm is claimed as faithfully reproduced.

The dictionary schema is typed in-memory interchange; it is not a native domain
or a new H5MSM result dataset. H5MSM 0.5 supplies source chemistry and coordinates
for the supported coordinate-streaming route. Source tests and benchmarks do not
qualify a changed installed release or downstream scientific evaluation.
