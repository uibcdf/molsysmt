---
summary: Verify the unit contract of Collantes surface-area descriptors.
issue: uibcdf/molsysmt#473
status: open
opened: 2026-10-26
closed:
severity: medium
verification: inspected
area: [physchem, units, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Verify the unit contract of Collantes surface-area descriptors

**Reported:** 2026-10-26 during addon receiving under uibcdf/molsysmt#421,
consumer uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** open; suspected unit/documentation inconsistency, not an established
incorrect numerical result.

## What

The native get_surface_area docstring describes nm squared. The function returns
a raw float list from groups/surface_area.py with no conversion or attached unit.
The table identifies Collantes and Dunn, J. Med. Chem. 1995, 38, 2705–2713 and
isotropic surface area, without stating a unit or normalization.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])
values = msm.physchem.get_surface_area(molsys, selection="group_name=='ALA'")
assert values == [62.9] * 5
assert not msm.pyunitwizard.is_quantity(values)
```

## How

The function obtains each selected group name, looks up the raw table value,
and appends it without conversion. The addon delegates exactly. Neither a bare
list nor a descriptor scale alone establishes the physical unit. The exact
primary reference has not been independently verified in this receiving.

## Why

A consumer must distinguish a reference descriptor from an actual conformational
surface measurement, and must not guess nm squared or silently rescale values.
The raw-number route is usable with explicit qualification; its physical unit
label is not scientifically certified by addon parity tests.

## What is measured and what is assumed

Executed on frozen native d7c82e92f: five ALA groups yield [62.9] * 5 as a list,
not a quantity. The docstring and lack of table unit metadata are inspected.
No incorrect magnitude, alternative unit, normalization or scale conversion is
claimed. The scientific interpretation remains a question for the primary
reference and owning provider.

## What was refuted

There is no missing addon unit conversion: the native public function itself
returns these numbers. Adding a guessed quantity wrapper downstream would not
resolve the ambiguity. This is not the geometry calculation performed by SASA.

## Scope and exclusions

Verify the original descriptor meaning, unit and normalization. Decide whether
the public API deliberately returns raw reference values or physical quantities;
align its table provenance, help, tutorial/course and tests. Any type/scaling
change needs explicit compatibility treatment. Do not change a scientific table
merely to satisfy a dimensional assertion.

## Acceptance criteria

A precise primary reference supports the declared interpretation and unit.
Native guards protect representative values and that contract; documentation
agrees. Then receive the contract in the thin addon without an independent
formula or normalization. Until then, keep the unit uncertainty visible.

## Provenance

Linux, Python 3.14.7, molsyssuite@uibcdf_3.14, frozen native d7c82e92f.
Public native calls only; bundled pentalanine input. No primary-paper
verification or installed-artifact qualification is claimed.


## Primary-reference lookup — 2026-10-26

The [publisher record](https://pubs.acs.org/doi/10.1021/jm00014a022) confirms
the article title, authors, volume/pages and DOI 10.1021/jm00014a022. Its full
text is purchase-only in this lookup. The [indexed original abstract](https://pubmed.ncbi.nlm.nih.gov/7629809/)
identifies isotropic surface area (ISA) and electronic charge index (ECI) as
side-chain descriptors derived from optimized amino-acid structures. Neither
accessible record establishes the table unit used by the current API. Thus
this lookup strengthens descriptor provenance, without resolving nm-squared
versus another unit/normalization or certifying the table numerically.
