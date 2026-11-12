---
summary: Native MolSys tutorial omits explicit hydrogen counts and mislabels bond ownership
issue: uibcdf/molsysmt#726
status: active
opened: 2026-11-12
closed:
severity: low
verification: reproduced
area: [docs]
guard:
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
