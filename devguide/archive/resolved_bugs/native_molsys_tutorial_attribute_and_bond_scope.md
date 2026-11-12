---
summary: Native MolSys tutorial omits explicit hydrogen counts and mislabels bond ownership
issue: uibcdf/molsysmt#726
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: low
verification: reproduced
area: [docs]
guard: tests/documentation/test_native_molsys_tutorial.py::test_molsys_tutorial_lists_the_complete_native_attribute_contract
normative:
blocked_by: []
supersedes: []
---

# Native MolSys tutorial attribute and bond scope

## What

The MolSys form tutorial lists 115 attributes while the adapter declares 116:
`n_explicit_hydrogens` is missing. Its operation rows say that add/remove bonds
edit Topology, although the registered functions delegate to ChemicalStates.
The remove description also says atom pairs rather than bond indices. Generic
structure operations use molecular-dynamics-only frame wording.

## How

Inspect source 1b98c2b1de047cf8f5d0d7dc4ed83a939db6a7cc. Compare the actual
adapter declarations with the notebook's cell 2 and inspect the add/remove
routing in their existing source modules against cell 3. The attribute already
has a delivery route; this work changes discovery/instruction, not implementation.

## Why

The tutorial is the form's public capability reference. Omitting a supported
stored hydrogen count hides useful functionality; assigning connectivity edits
to the removed Topology facade contradicts native ownership. State-local stored
counts must not be described as a recount of indexed hydrogen atoms.

## Acceptance

Match the complete runtime attribute set and its count. Exercise the actual
stored value route, including unknowns and repeated positions. Check form bond
edits against independent stable-inventory and selected-state assertions, and
make their descriptions match those executed semantics. Preserve six cells,
anchors, code, outputs, conversions and unmodified notebook metadata. Replace
the micro-governance's stale hardcoded count with the owning declaration rule.
Render and inspect the actual tutorial and its links. No scientific algorithm,
public signature, schema, dependency floor or release action belongs here.

## Receiving

The source diagnosis is inspected. Before/after native pytest receiving and
rendered article checks follow; preserve their exact input/result scopes.


## Before and after receiving — 2026-11-12

The original tutorial fails three documentation assertions: its complete
attribute set omits n_explicit_hydrogens, and both edit descriptions falsely
locate chemistry in Topology. The independent stored-count control already
passes: zero, one and unknown values survive repeated selections without
adding hydrogen atoms or bonds. Real add/remove routes likewise change the
chemical state while retaining the original stable inventory; the failures
concern their descriptions, not the implementation.

After correcting the two Markdown cells, all four controls pass. Count and
inventory agree at 116 attributes. Removal is described in bond indices;
general coordinate prose uses structures. A new explanation separates domain
ownership from historical getter-module names. The micro-governance now follows
the current adapter rather than freezing a stale count.

A structural JSON comparison confirms every other notebook field is unchanged:
code, outputs, metadata, cell order, anchors and conversion table are preserved.
No scientific code or dependency changes. Actual corrected HTML/link receiving
and common final checks follow; #725's separate full-site result keeps its
exact earlier source and unchanged input scope.


## Resolution — 2026-11-12

Corrected source 2bf21835f passes the strict targeted HTML update with zero
warnings; the actual tutorial's complete local links pass inspection. The earlier
three rendered articles remain byte-identical. The one-CPU/three-GiB/no-own-swap
update peaks near 356 MiB and preserves at least 13.78 GiB available host RAM.
All 7,405 selected inputs stay unchanged, with clean source before/after. The
primary guard compares the real runtime declaration set and displayed count;
separate controls receive actual stored counts and chemical bond edits plus
their descriptions. Merely changing the headline number cannot satisfy it.

The [combined receipt](../../../devtools/data/native_domain_documentation_receiving_725_726_20261112.json)
owns exact sources, failed attempts, observed runtime, resources and final checks.
This bounded documentation correction does not clear the complete-source/nightly
backlog, original #615/#713 uncertainty or final-pair/publication acceptance.


## Additional source-reference receiving — 2026-11-12

A stronger reference guard then exposes six omitted registered conversion routes:
TopologyDict, ChemicalStates, ChemicalStatesDict, SDF, PDBQT and PDBQT text.
The four prior attribute/ownership controls remain passing; the new reference
control fails. This is another real tutorial inventory omission, not a product
or oracle failure. The final table adds those six routes and declares all 40;
its previous 34 routes remain. Source links include all 57 adapter role
occurrences, explicitly labelled implementation/docstring references rather
than nonexistent Sphinx API articles. General user API links remain indexed.
#727 owns the separately observed wider form-reference debt.
