# Proposal: handle DUM (dummy) atoms/groups in `physchem`

## Problem

The `physchem` per-residue functions raise on systems built from **dummy
atoms** (placeholder probes / coarse beads). For example, a system whose atoms
are `AR` in a `DUM` group:

```python
physchem.get_hydrophobicity(ms, element='group')   # KeyError: 'DUM'
physchem.get_charge(ms, element='group')           # KeyError: 'DUM'
```

The residue-property tables (Eisenberg hydrophobicity, pH7 charge, Grantham
polarity, …) have no entry for the `DUM` atom name or the `DUM` group name, so
any lookup over a dummy system blows up instead of returning a neutral default.

## Why it matters

Dummy-atom systems are common: synthetic benchmark geometries (e.g. TopoMT's
DFND argon catalog), coarse-grained models, alchemical placeholders. Consumers
that run `physchem` over a *whole* system (e.g. colouring cavity-lining residues
by hydrophobicity/charge) cannot tolerate a hard failure on the dummy entries —
they just want those atoms treated as chemically neutral/unknown.

## Proposed behaviour

Recognise `DUM` as a first-class neutral element/group in the `physchem` tables:

- **atom name `DUM`** (and the common `AR`/dummy element conventions): neutral —
  zero charge, undefined/neutral hydrophobicity and polarity.
- **group name `DUM`**: neutral residue — `get_hydrophobicity`, `get_charge`,
  `get_polarity`, etc. return a neutral default (e.g. `0.0` or `NaN`) instead of
  raising `KeyError`.

Minimal, conservative option: add a `DUM` row (neutral values) to the residue
tables in `molsysmt/physchem/groups/*.py` (`hydrophobicity.py`, the charge table,
etc.). A more general option: a `missing='neutral'` / `missing='raise'` policy
argument so callers choose between a neutral default and a hard error for any
unknown residue, with `DUM` always neutral.

## Source

Raised while implementing TopoMT's DFND *affinity spheres* visualization, which
colours cavity-lining residence spheres by `physchem.get_hydrophobicity` +
`get_charge`; the DFND synthetic catalog is all `AR`/`DUM`, so the typing path
must not crash on dummy systems.
