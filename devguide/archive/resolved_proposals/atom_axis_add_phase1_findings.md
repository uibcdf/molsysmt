# Atom-Axis `add()` — Phase 1 Contract Audit Findings

**Role:** evidence for Phase 1 of
[`atom_axis_add_semantic_audit.md`](atom_axis_add_semantic_audit.md). It records what
`add()` does today. It decides nothing and changes no production code.

**Measured:** 2026-08-07, working tree at `3cdd30380`. The `add()` implementation is
unchanged since its landing commit `2865c3122`.

**Method:** read the public dispatcher and every adapter, then confirm each reading
with an executable probe. Every statement below with a number behind it was run, not
inferred. Where a case could not be constructed from a bundled system it is marked
**not exercised** rather than assumed.

---

## 0. Scope is far narrower than the proposal assumed

Seventy-eight form packages ship an `add.py`. **Two of them implement anything**:
`molsysmt.MolSys` and `molsysmt.Structures`. Every other adapter raises
`NotImplementedMethodError`, and the dispatcher selects the implementation by the
**target** form (`basic/add.py:144`), so `add()` is only ever executable into those
two forms. `molsysmt.Topology`'s adapter raises a bare `NotImplementedError` rather
than the catalogue-backed error every other stub uses, so it escapes the error
policy; `cupy_ndarray/add.py` re-exports the `XYZ` stub.

This reduces "all Tier 1 adapters either conform or declare bounded limitations"
(acceptance criterion 7) to a statement about two implementations plus one
diagnostics defect.

---

## 1. Question 1 — cardinality is mostly unreachable, and the one reachable case is broken

The dispatcher computes `atom_indices` once and then runs a nested loop over targets
× sources (`basic/add.py:131-156`). That structure suggests a Cartesian contract. It
is almost entirely dead code.

**`to_molecular_system` and `from_molecular_system` are digested as *single*
molecular systems.** A list of two independent systems raises
`MultipleMolecularSystemsError` before the loop is ever entered. Probed and rejected:
two sources with `selection='all'`; two sources of different atom counts; two sources
with a string selection; two sources with explicit indices; two targets × two
sources; and list or tuple targets under `in_place=False`. **Every multi-item case in
the proposal's "minimum evidence" list is unreachable from the public API.**

So audit questions 1.1, 1.3, 1.5, 1.7 and 1.8 have no behaviour to decide: the
digester already decided. What remains is whether the nested loop should be deleted.

**The one list that survives digestion is a composite system — and it is
mis-iterated.** A list that reads as *one* system split into complementary items
passes digestion. The dispatcher then treats its items as independent sources:

```python
msm.add(alanine_molsys, [prmtop_file, inpcrd_file])
# ArgumentLengthError: Length mismatch for argument 'structures'. Expected 1, got 0.
```

The same list that `msm.convert` reads as one 5207-atom, 1-structure system is read
by `add` as two additions, the first of which is topology-only. This contradicts the
composite-system contract now normative in
[`forms_and_conversions.md`](../forms_and_conversions.md#composite-molecular-systems-and-the-structure-axis).
A composite **target** fails differently and more confusingly, trying to convert the
source back into `file:prmtop`:

```python
msm.add([prmtop_file, inpcrd_file], alanine_molsys)
# NotImplementedConversionError: No conversion implemented from 'molsysmt.MolSys' to 'file:prmtop'.
```

Note also that `select()` over a composite source returns indices into the *assembled*
system (18 indices, max 58 for `atom_type=="C"` on pentalanine), which the loop then
applies to each item separately.

**Return containers and atomicity behave correctly** where they are reachable.
`in_place=False` with a scalar target returns a `MolSys` and leaves the original at
22 atoms. A failure raises `ArgumentError` before any mutation, and the target is
unchanged under both `in_place=True` and `in_place=False`.

---

## 2. Question 2 — the intersection policy holds, except for coordinates

For `b_factor` and `occupancy`, all four presence combinations behave exactly as
documented: present on both sides concatenates, absent on both stays absent, and
one-sided drops the whole attribute with `StructuralAttributeDropWarning` — verified
in both directions, target-only and source-only.

**Coordinates do not follow that policy, and the proposal's description of the
current behaviour is wrong.** The proposal states that adding a topology-only source
to a coordinate-bearing target "drops all coordinates". It does not. Because
coordinates are what define the structure count for such a system, the two sides
disagree on the structure axis and the call fails first:

```
ArgumentLengthError: Length mismatch for argument 'structures'. Expected 1, got 0.
```

The diagnostic names `structures`, not `coordinates`, so a user adding a topology to
a system with coordinates is told about a length mismatch on an argument they never
passed. Whatever policy is chosen, **this message is a defect on its own.**

**Warning-as-error atomicity holds.** Under `warnings.simplefilter('error')` the
`StructuralAttributeDropWarning` propagates and the target stays at 22 atoms. The
candidate/assign structure of `MolSys.add` (`native/molsys.py:354-369`) is what buys
this, and it works.

---

## 3. Question 3 — target precedence is uniform, and that is the scientific problem

`Structures.add` copies the target's payload (`candidate = dict(current)`,
`native/structures.py:798`) and only ever rewrites the four atom-aligned entries.
Every other structure-side value is the target's, and the source's is discarded
without inspection. Confirmed for `structure_id`, `time`, `box`, `temperature`,
`potential_energy` and `kinetic_energy`.

Two of these are not merely surprising:

**Incompatible periodic boxes are combined silently.** A target in a 2.0 nm cubic box
and a source in a 9.0 nm cubic box produce a result in the 2.0 nm box, holding the
source's coordinates, with no warning. Coordinates interpreted under a different unit
cell are not comparable, and nothing here checks or says so.

**Energies survive a change of system.** A 22-atom system with
`potential_energy = -100 kJ/mol` becomes a 50-atom system still labelled
`-100 kJ/mol`. The value is now attributed to a system it was not computed for. The
same applies to `kinetic_energy` and `temperature`.

---

## 4. Other native state — four fields `add()` never traverses

`MolSys.add` rebuilds only `topology` and `structures`. `Structures.add` reads only
`_frame_payload()`. Anything outside both is invisible to the operation:

| Field | Probed behaviour | Assessment |
| --- | --- | --- |
| `bioassembly` | target's kept, source's discarded silently | `extract` filters assemblies by retained atoms (`native/molsys.py:241-293`); `add` does not look at them at all |
| `alternate_location` | target's kept verbatim, source's discarded silently | it is a per-structure dict keyed by **atom index**; `extract` remaps those keys, `add` never does |
| `time_step` | target's 2.0 ps kept, source's 5.0 ps discarded silently | consistent with target precedence, but undeclared |
| `molecular_mechanics` | never referenced by `MolSys.add` | **not exercised**: no bundled system reaches a populated `MolecularMechanics` through a public conversion — `file:prmtop → molsysmt.MolecularMechanics` returns an empty object, which is itself worth a separate check |

`alternate_location` deserves emphasis. It appears in `_frame_payload()` but not in
`_ATOM_ALIGNED_ATTRIBUTES`, so it is treated as structure-aligned while its *content*
is keyed by atom index. Question 3 asks whether it is "truly structure-aligned in
every supported native workflow"; the answer is no — it is structure-aligned in shape
and atom-aligned in meaning.

**Chemical-state indices:** `append_structures` handles
`_structure_chemical_state_indices` with care (`native/molsys.py:396-442`); `add`
never mentions it. The simple probes stayed consistent (one state before, one after),
but a case with *differing* inventories on the two sides is **not exercised** — no
bundled pair with different chemical-state inventories and equal structure counts was
found. Phase 2 must construct one.

---

## 5. Classification

**Confirmed contract, behaves as documented — no action:**

1. atom-aligned intersection with `StructuralAttributeDropWarning` for `b_factor`
   and `occupancy`, in both directions;
2. transactional rejection: no mutation on failure, including warnings-as-errors;
3. `in_place=False` returns a new object and leaves the original untouched;
4. structure counts must match, and source `structure_indices` selects before the
   atom-axis concatenation.

**Defects — wrong regardless of which policy is chosen:**

5. a composite-item list is accepted by digestion and then iterated as independent
   sources, contradicting the composite-system contract (both as source and target);
6. the topology-into-coordinates case reports `ArgumentLengthError` naming
   `structures`, an argument the caller never passed;
7. `molsysmt.Topology`'s `add` raises a bare `NotImplementedError`, outside the
   error policy;
8. `alternate_location` from the source is discarded while being semantically
   atom-aligned; the field is classified as structure-aligned by omission, not by
   decision.

**Undecided policy — needs a maintainer decision before Phase 3:**

9. combining systems with incompatible boxes;
10. retaining `temperature`, `potential_energy` and `kinetic_energy` across a change
    of system;
11. whether `add()` should expose `attribute_policy` (`intersection` / `strict`);
12. ownership of `bioassembly`, `time_step` and `molecular_mechanics`;
13. whether the multi-target / multi-source loop should be deleted.

---

## 6. What Phase 2 must add

Regression tests that pin items 1–4 as contract, reproduce 5–8 as failing
expectations, and record 9–13 as explicitly undecided rather than asserting the
accidental behaviour. Two probes still have to be constructed: a pair of topologies
with different chemical-state inventories and equal structure counts, and a system
carrying a populated `MolecularMechanics`.
