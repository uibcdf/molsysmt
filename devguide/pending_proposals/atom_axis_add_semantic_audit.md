# Atom-Axis `add()` Semantic Audit

**Status:** proposed bounded audit; no behavioral change accepted yet

**Target:** complete before the F5 exact-commit release campaign

**Implementation base:** `2865c3122`

**Checkpoint base:** `dd8d48c67`

**Related contract:** [Native Structures Contract](../native_structures_contract.md)

## Motivation

The atom-axis `add()` implementation now has one coherent mechanical contract:
it selects source atoms and structures, requires compatible structure counts,
concatenates shared atom-aligned arrays, validates candidates before assignment,
and keeps native `MolSys` topology and structures transactional.

That implementation repaired real incomplete behavior and passes its focused and
expanded regression gates. It also exposes semantic questions that must be
answered deliberately before 1.0. Passing shape checks is not sufficient
evidence that every retained or discarded structural attribute remains
scientifically meaningful after atoms are added.

This proposal defines a bounded audit. It does not reopen the implementation,
change the 96% weighted release status, or prescribe a large redesign. The audit
must first determine which cases are defects, accepted 1.0 limitations, or
post-1.0 extensions.

## Fixed Invariants

The audit must preserve these already accepted rules unless contradictory
scientific evidence is found:

- `add()` grows the atom axis;
- `append_structures()` and `concatenate_structures()` grow or join the
  structure axis;
- no materialized atom-aligned array may cover only a prefix or suffix of the
  resulting atom axis;
- a rejected native operation must not leave topology and structures
  inconsistent;
- source selection is applied before atom-axis concatenation;
- missing values must not be invented silently;
- atom, group, and other native IDs remain source data and need not be unique.

## Audit Question 1: Multiple Sources, Targets, and Selections

`molsysmt.basic.add()` currently computes `atom_indices` before iterating over
the source systems. It then applies the result while visiting every source.
This is proven for `selection='all'`, but not for a nontrivial selection over
multiple sources.

The audit must decide and test:

1. whether one string selection is evaluated independently against every
   source;
2. whether one flat explicit index collection is reused for every source or
   validated separately against each source;
3. whether nested selections mean one selection per source;
4. how different source forms and different atom counts affect selection
   dispatch;
5. whether multiple targets plus multiple sources mean a Cartesian operation
   or pairwise operations;
6. what shape and container type are returned for scalar, list, and tuple
   targets when `in_place=False`;
7. whether `msm.add(target, [source_a, source_b])` is transactional as one
   public call or only atomic per individual source;
8. whether failure on a later source or target may leave earlier additions
   committed when `in_place=True`.

The current nested-loop behavior must not become the contract merely because it
is the implementation. The intended cardinality semantics need an explicit
maintainer decision.

### Minimum evidence

- one scalar target with two sources and `selection='all'`;
- one scalar target with two sources and a string selection;
- one scalar target with two sources and explicit indices;
- nested per-source selections, if accepted;
- heterogeneous source forms;
- sources with different atom counts;
- multiple targets covering the accepted Cartesian or pairwise rule;
- failure in the second source under both `in_place=True` and
  `in_place=False`;
- exact output-type assertions for scalar, list, and tuple targets.

## Audit Question 2: Missing Atom-Aligned Attributes

The current intersection behavior treats `coordinates`, `velocities`,
`b_factor`, and `occupancy` as one aligned family:

- present on both sides: concatenate;
- absent on both sides: remain absent;
- present on only one side: drop the complete result attribute with
  `StructuralAttributeDropWarning`.

This maintains shape integrity, but it can be surprising. The most important
case is adding a topology-only source to a coordinate-bearing target: the
result cannot retain coordinates for only the old atoms, so current behavior
drops all coordinates.

The audit must compare:

| Policy | Benefit | Cost or risk |
| --- | --- | --- |
| intersection with warning | permits partial-information forms and never creates a partial atom axis | can discard valuable target data |
| strict rejection | prevents any information loss | makes topology-only or partially described additions fail |
| synthesized missing values | preserves array shapes | invents semantics, requires masks/null rules, dtype policy, persistence, and conversion support |

Synthesized values are not a 1.0 shortcut. They require the deferred
partial-series model and an H5MSM schema decision.

The bounded 1.0 question is whether `add()` should expose an
`attribute_policy` analogous to structural append:

- `intersection` retaining the current behavior;
- `strict` rejecting any one-sided atom-aligned attribute before mutation.

The audit must also decide whether coordinates deserve a stricter default than
optional observables, or whether one uniform policy is clearer.

### Minimum evidence

For every atom-aligned attribute, exercise:

- present on both sides;
- absent on both sides;
- target-only;
- source-only;
- selected source atoms and reordered structure indices;
- warning aggregation when several attributes are dropped;
- warnings treated as errors;
- strict-mode atomicity if strict mode is accepted;
- topology-only, structures-only, and full native `MolSys` inputs.

## Audit Question 3: Structure-Aligned Metadata

Adding atoms preserves the structure axis, so the implementation currently
keeps target-side structure metadata and ignores the corresponding source
metadata. That is mechanically simple but not uniformly scientific.

The audit must classify attributes by meaning instead of treating every
structure-aligned series alike.

### Alignment and identity candidates

- `structure_id`
- `time`
- `alternate_location`
- `box`
- `time_step`

These may describe the identity or geometry of the same structure axis. When
both inputs provide them, incompatible values may indicate that atoms from
unrelated structures are being combined. In particular, source coordinates
interpreted under a different periodic box cannot be assumed compatible merely
because the structure count matches.

The audit must define:

- which attributes require equality or numerical closeness when both exist;
- unit normalization and tolerances for time and box comparisons;
- behavior when the attribute exists on only one side;
- whether target precedence is sufficient for single-structure builders;
- whether `alternate_location` is truly structure-aligned in every supported
  native workflow.

### System-level observable candidates

- `temperature`
- `potential_energy`
- `kinetic_energy`

Target precedence is especially questionable here. Adding atoms changes the
system whose energy is described. The old target energy is not generally the
energy of the combined system, and target and source energies are not generally
additive. Temperature may remain meaningful only when both fragments describe
the same ensemble and structure axis.

The audit must decide whether these values should:

- be retained after a compatibility check;
- be dropped with an explicit warning;
- cause strict rejection;
- or require an explicit future combination model.

No energy-combination rule may be inferred without scientific justification.

### Other native state

`bioassembly` and any structure-related data outside `_frame_payload()` need a
separate ownership check. The audit must determine whether atom addition
preserves, invalidates, combines, or must reject such metadata. Fields that are
not currently traversed must not escape review merely because the implementation
does not see them.

## Additional Engineering Review

The following implementation properties should be checked during the same
bounded audit:

1. **Coordinate-free `Structures`:** without any atom-aligned array,
   `Structures` has no independent atom cardinality. Determine whether
   atom-axis `add()` on two coordinate-free `Structures` is a valid no-op, an
   unsupported operation, or requires an explicit future atom-domain field.
2. **Transaction scope:** native `MolSys.add()` is atomic for one source, but
   the public multi-source and multi-target call may not be atomic as a whole.
3. **Peak memory:** candidate copies guarantee correctness but increase peak
   memory. Measure one representative large system before considering a
   preflight-and-commit optimization.
4. **Adapter parity:** every Tier 1 form adapter advertising `add()` must either
   implement the accepted contract or report a declared limitation. Conversion
   to the target form must not hide fidelity loss.
5. **Argument dispatch:** signature introspection should work through decorated
   adapters and should not become measurable overhead. Cache it only if
   profiling demonstrates value.
6. **Diagnostics:** loss and incompatibility reports must remain catalog-backed,
   aggregate related attributes, name the source and target operation, and
   preserve warning-as-error atomicity.
7. **ID and hierarchy integrity:** selected topology, structural atom axes, and
   chemical-state atom domains must remain aligned after addition without
   imposing uniqueness on `*_id`.
8. **Copy and return semantics:** `in_place=False` must protect every original
   input, and scalar versus sequence return behavior must be documented and
   stable.

## Recommended Sequence

### Phase 1 — Read-only contract audit

- trace the public dispatcher and every Tier 1 `add()` adapter;
- build the source/target/selection cardinality table;
- classify every native structural attribute;
- identify current behavior with small executable probes;
- record decisions before changing production code.

### Phase 2 — Bounded regression matrix

- add tests that demonstrate current behavior and expose disagreements;
- distinguish confirmed defects from undecided policy;
- do not weaken tests to preserve accidental behavior.

### Phase 3 — Minimal accepted corrections

- repair only confirmed 1.0 correctness defects;
- add `attribute_policy` only if the policy is accepted;
- update native, form, and public layers together;
- preserve transactional mutation and partial-information support.

### Phase 4 — Lifecycle and release evidence

- update NumPy-style docstrings;
- update the User Guide and Common Core module 18 if behavior changes;
- execute affected notebooks;
- run focused, expanded, Ruff, dependency, devguide, course, and fast gates;
- land a clean exact commit before starting the heavy F5 matrix.

## Acceptance Criteria

This proposal may be archived only when:

1. source/target cardinality semantics are explicit and tested;
2. nontrivial selections over multiple sources are correct;
3. the transaction boundary for multi-source and multi-target calls is
   documented and tested;
4. every atom-aligned presence combination has an accepted outcome;
5. structure identity, box, time, temperature, energy, alternate-location,
   time-step, and bioassembly behavior is classified;
6. topology-only and coordinate-free cases have explicit outcomes;
7. all Tier 1 adapters either conform or declare bounded limitations;
8. diagnostics and warning-as-error behavior preserve atomicity;
9. any accepted public change completes the documentation lifecycle;
10. the resulting clean exact commit passes the applicable release gates.

## Pause and Resume Point

At the pause, the implementation and documentation checkpoints are clean and
published at `dd8d48c67`. Resume with Phase 1 only. Do not begin the expensive
F5 full matrix until this bounded audit either confirms the current contract or
lands the minimal required corrections; otherwise the matrix would certify a
candidate whose `add()` semantics remain undecided.

