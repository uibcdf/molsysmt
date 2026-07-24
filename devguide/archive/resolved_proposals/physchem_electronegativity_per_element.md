# Proposal: per-element electronegativity / polarity property in `physchem`

**Status:** RESOLVED — implemented and released
**Requester:** TopoMT
**Owner:** MolSysMT

> **RESOLVED — implemented and released.** Delivered in commit `90b2a491a`
> (2026-06-15, on `main`). The proposal below is retained for design provenance;
> it does not define current behavior.
>
> **What was implemented:** a dedicated public `physchem.get_electronegativity`
> (Pauling scale, per-atom, dimensionless; unknown/dummy elements → `NaN` rather
> than raising), backed by the `physchem/atoms/electronegativity.py` data table,
> a `definition` digester entry, and a public export. The separate-function
> route was chosen over extending `get_polarity` to `element='atom'`.
>
> **Regression evidence:** `tests/physchem/get_electronegativity/test_get_electronegativity.py`
> (green as of 2026-07-23).
>
> **TopoMT cleanup (downstream, out of scope here):** replace the local
> `probe_weights` table with the upstream lookup, keeping only the topography-
> specific scoring formula in TopoMT.

## Problem

`molsysmt.physchem` exposes polarity only at the **residue** level
(`get_polarity`, with `element='group'`, Grantham/Zimmerman amino-acid scales).
There is no **per-element** electronegativity or polarity property keyed by atom
element symbol (C, N, O, S, ...).

Several spatial/physicochemical heuristics need an element-level polarity weight,
not a residue-level one. They currently hard-code a small table instead of
asking MolSysMT.

## Concrete consumer

TopoMT scores pocket–ligand contacts with an element-weighted distance decay and
hard-codes the per-element weights:

```python
# topomt/tools/features/pockets/contacts.py
probe_weights = {'C': 1.0, 'N': 0.8, 'O': 0.7, 'X': 1.0}
```

This is element-level physicochemistry living inside TopoMT because MolSysMT has
no equivalent property. `get_polarity` (per residue) cannot supply it, and
`get_charge` is residue-based or OpenMM partial charges — neither is a per-element
scale.

## Why it belongs in MolSysMT

Per-element electronegativity/polarity is a general molecular observable, not a
topography concept. Other MolSysSuite packages (pharmacophore typing, contact
scoring, coarse-grained models) plausibly need the same lookup. Centralizing it
avoids parallel hard-coded element tables drifting across the ecosystem.

## Desired contract

- a public `physchem.get_electronegativity` (and/or `get_polarity` extended to
  `element='atom'`) returning a per-atom dimensionless value looked up from a
  named, published scale (e.g. Pauling electronegativity), unit-aware where
  applicable;
- `definition` argument to select the scale, mirroring existing `physchem`
  functions (`get_charge`, `get_polarity`, `get_atomic_radius`);
- robust defaults / neutral fallback for unknown or dummy elements (see also
  `physchem_support_dummy_atoms.md`), instead of raising;
- standard `selection`, `syntax`, `skip_digestion` arguments and the usual
  return-shape conventions.

## Expected TopoMT cleanup

Once the property exists upstream, replace the local `probe_weights` table with
a `physchem` lookup, keeping only the topography-specific scoring formula in
TopoMT.

## Notes

This is the one reverse-direction gap found in a 2026-06-14 audit of the native
TopoMT/DFND boundary against the current `physchem` surface; the other historical
candidates (radii, neighbor/distance queries, SASA, surface area, buriedness)
already exist in MolSysMT and are consumed by TopoMT.
