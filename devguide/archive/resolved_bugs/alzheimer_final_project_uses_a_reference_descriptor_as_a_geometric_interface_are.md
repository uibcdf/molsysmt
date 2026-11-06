---
summary: Alzheimer final project uses a reference descriptor as a geometric interface area.
issue: uibcdf/molsysmt#589
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [api, docs, tests]
guard: tests/physchem/get_sasa/test_course_interface_sasa.py
normative:
blocked_by: []
supersedes: []
---

# Final-project interface observable

**Reported:** course-call review during #562 receiving on 2026-11-05.
**Status:** resolved; actual lesson cells and independent analytic controls pass.

## What

Alzheimer Module 54 calls `physchem.get_area_buried` with `selection_2` and
labels the result geometric interface surface. The API is a Rose group-table
lookup, independent of coordinates, and does not admit that keyword. Removing
it would still mislabel the scientific observable. The lesson also assumes
molecule_type identifies the two partners, although both can be peptides.

```bash
python -m pytest tests/physchem/get_sasa/test_course_interface_sasa.py -k tracks_geometry --receptor=llm -n 2
```

Baseline on main `8e9e3d2078ef41d22f6198e1d5c23379e11f4619`: four actual
lesson-cell executions fail with UnknownArgumentError in 2.91 s.

## How

Use existing owning tools: `basic.get` and `merge` declare source atom ranges;
ordinary OpenMM solvation retains the source prefix; `basic.extract` makes the
dry pair and isolated partners; `physchem.get_sasa` performs existing native
Shrake–Rupley sampling. Reconstruct local indices after extraction rather than
using IDs or type labels as partner identity. Refuse empty, repeated or
intersecting partner populations before evaluation.

Calculate total SASA loss at fixed coordinates as
`SASA(A) + SASA(B) - SASA(A union B)`, then report its half separately as mean
interface area. All three calls use the same native radii, 0.14 nm probe,
960 sphere points and explicit Cartesian `pbc=False` geometry. Extraction, not
output selection, removes background solvent and the isolated partner's other
occluder. Partners must already be whole and in the intended common image.
No relaxation, docking, periodic reconstruction or new surface algorithm is
inserted. Areas retain quantities until explicit nm-squared report conversion.

The existing H-bond detector uses the declared dry partner selections, explicit
0.23 nm H–acceptor cutoff and the same Cartesian geometry. Counts are criterion
matches, not demonstrated stabilizing energies. Supplied hydrogen inventory
limits their interpretation.

## Why

A table descriptor, a conformational area and evidence of binding are different
observables. Geometric interface reporting requires coordinates, consistent
occluder populations, an explicit half-area convention and explicit units.
Identical group inventories at different separations must give different
geometric losses; a reference lookup cannot establish that behavior.

## What is measured and what is assumed

Ten bounded controls execute the actual course characterization cell, actual
merge/map statements and the actual Toolbox example. Carbon-probe controls use
an independent closed-form spherical-cap oracle at 0.31 nm separation and a
zero-area Cartesian control at 2.9 nm across a 3 nm cell. A nearby background
oxygen must not occlude the extracted dry pair. Both nm and angstrom standard
policies preserve the same physical area and source coordinates/tables.
The two equal carbon probes use a declared 0.17 nm vdW radius plus a 0.14 nm
probe. The existing scientific-truth registry supplies the sampling tolerance:
0.0101 nm-squared per atom; total-loss tolerance is twice that value. This is not
a general error bound for arbitrary molecular surfaces.

These are analytic/contract source controls, not full biological preparation,
installed-package/platform qualification, affinity estimation or PISA parity.

## What was refuted

- Deleting only selection_2 would leave a static descriptor mislabeled geometry.
- Selecting SASA outputs alone would retain the other partner and solvent as
  occluders instead of measuring isolated partners.
- Type-based peptide/protein selection cannot identify this particular pair.
- Half the total loss is an explicitly named convention; the two sides need
  not have equal sampled areas for arbitrary unequal atom radii.
- A hydrogen-bond count or local optimization does not establish binding
  stability or a favorable biological effect.

## Scope and exclusions

Preserve the 2BEG/KLVFF capstone context and its retained minimization result.
Steps 1–4 remain explicitly unqualified; #593 separately owns unsupported
builder keywords, discarded independent repairs and complete preparation
qualification. This issue does not block on that different correction.
Original biological cells had no stored outputs; no synthetic result is
published under biological labels. The independently executed Toolbox example
is labeled carbon-probe geometry. Source APIs, compiled kernels, dependency
floors and persistence schemas are unchanged.

## Acceptance criteria

- Actual lesson code computes coordinate-dependent area from existing tools.
- Nonempty, disjoint, unique explicit source populations replace type inference.
- Total loss and its half retain shapes, quantities and declared units.
- A sphere oracle and separated control expose coordinate-independent or
  incorrectly selected substitutes; source ownership and policy are preserved.
- H-bond counts use the same geometry and do not claim energetic stabilization.
- Foundations, Toolbox, Cookbook and course distinguish geometric observations,
  reference descriptors, provenance and the unqualified preparation route.

## Provenance

Linux, shared Python 3.14.7; baseline source identified above. Primary sources:
[Shrake and Rupley (1973)](https://doi.org/10.1016/0022-2836(73)90011-9) for the
existing sampling method and [PDBePISA interface-area FAQ](https://www.ebi.ac.uk/pdbe/prot_int/pi_tips.html)
for only the half-area convention. The FAQ's other model choices or energetic
claims are not adopted; PISA is not executed or credited as software.

## Resolution and receiving

Receiving passes 749 related cases, 22 published-support-floor cases and 569
documentation/doctest cases. Suites overlap. All ten new guards execute the
actual course/Toolbox statements; they cannot pass with an empty demonstration
or a table lookup substituted for geometry. Existing bounded minimization
continuation controls still pass on the edited capstone. The complete SASA
tutorial executes all seven code cells in 11.2 s. Its original examples remain;
the new numeric outputs are labeled carbon-probe geometry. Original biological
preparation/minimization code and unexecuted output payloads are preserved,
apart from explicit assembly maps and the corrected characterization block.

Foundations corrects the Rose/Janin scope and units; the Toolbox and Cookbook
explain extraction and occluders. The capstone's new content contract preserves
the original scenario and distinguishes bounded scientific evidence from #593's
unqualified full preparation. Ruff, public API stability, docstrings, course
and developer-guide checks pass. Source runtime APIs, scientific kernels,
dependency floors and persistence schemas are unchanged.

See the [receipt](../../../devtools/data/course_interface_sasa_receiving_589_20261105.json)
for commands, source identity, provider origins/hashes, artifact hashes and
the independent oracle boundary. Hosted, installed/platform and release gates
remain separate under #334; no tag, Release, promotion or new release matrix.
