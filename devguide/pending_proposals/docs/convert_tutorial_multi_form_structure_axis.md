# Converting several forms: explain which item owns the structure axis

**Raised:** 2026-08-03, on closing
[`structural_attribute_resolution_ignores_the_structure_axis.md`](../../archive/resolved_bugs/structural_attribute_resolution_ignores_the_structure_axis.md).

**Where:** `docs/content/user/tools/basic/convert.ipynb`, section *Multiple items
into one*. Probably also the `convert` docstring and wherever the course first
composes a topology with a trajectory.

## What a reader can conclude today

The tutorial shows the composition and nothing about its semantics:

```python
molsys = msm.convert([prmtop_file, inpcrd_file], to_form='molsysmt.MolSys')
```

That example cannot raise the question, because an INPCRD holds a single structure
and so does the resulting system. A reader generalizes it to
`[topology, trajectory]` and has no way to know:

- how many structures the resulting system has, when the items disagree;
- that a topology file holding a reference conformation contributes identity and
  topology but **not** its structural series;
- that `time` or `structure_id` can therefore be absent from the result while
  `coordinates` is present, and that a warning says so;
- that listing the items in the other order changes nothing;
- that two trajectories of different lengths are refused, and that joining them is
  `concatenate_structures` instead.

Until 2026-08-03 the answer to the first point was "it depends on the order you
typed them in", and nothing was reported. That is fixed. What is missing is telling
anyone.

## What the pages should say

The rule is already normative in
[`forms_and_conversions.md`](../../forms_and_conversions.md), section *Composite
molecular systems and the structure axis*. The documentation does not restate it as
a specification; it should make it visible through an example a reader recognizes.

Suggested shape for the tutorial section:

1. Keep the current `[prmtop, inpcrd]` example as the simple case.
2. Add a `[topology, trajectory]` example where the counts differ — a PDB and an
   XTC is the composition most readers arrive with — and show `n_structures` of the
   result.
3. Show that swapping the two items gives the same result. This is the point most
   worth making explicit, because it is the property a reader would otherwise have
   to discover by accident.
4. Mention that the reference conformation's own structural series are not carried
   over, and that MolSysMT says so rather than truncating anything.
5. Point at `concatenate_structures` for the case that is actually about joining
   trajectories, so the reader leaves knowing which function they wanted.

## Acceptance

- A reader of the convert tutorial can predict `n_structures` of a
  `[topology, trajectory]` composition without opening the developer guide.
- The example is executed in the notebook, not asserted in prose.
- No page restates the rule as if it were defined there; each links to
  `forms_and_conversions.md`.
