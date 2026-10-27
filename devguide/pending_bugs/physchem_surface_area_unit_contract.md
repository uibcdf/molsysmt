---
summary: Verify the unit contract of Collantes surface-area descriptors.
issue: uibcdf/molsysmt#473
status: partial
opened: 2026-10-26
closed:
severity: medium
verification: inspected
area: [physchem, units, docs]
guard: tests/physchem/get_surface_area/test_get_surface_area.py::test_provisional_isa_quantity_preserves_table_scale_and_standard_units
normative:
blocked_by: []
supersedes: []
---

# Verify the unit contract of Collantes surface-area descriptors

**Reported:** 2026-10-26 during addon receiving under uibcdf/molsysmt#421,
consumer uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** partial; the maintainer has adopted provisional angstrom² typing
and PyUnitWizard standardization. Original table units, normalization and
primary values remain unverified; implementation is not paper certification.

## What

At opening, the native get_surface_area docstring described nm squared and returned
a raw float list from groups/surface_area.py with no conversion or attached unit.
The later maintainer-adopted provisional quantity contract is recorded below.
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

An explicit original definition/table, or an authoritative curated record carrying
its reference, units, normalization and exact numeric entries, supports the
physical interpretation. Implementation agreement without unit metadata is insufficient.
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

## Extended primary/source review — 2026-10-26

**Inspected:** publisher/PubMed confirm the original work and its ISA/ECI
side-chain QSAR scope. The complete original paper was not obtained: the ACS
record offers purchase access; its abstract does not give the descriptor
formula, table unit or normalization. No authentication bypass or access claim
is made. A search of the publicly accessible AAindex1 text found no Collantes
entry; no AAindex identifier is asserted for this table. This bounded lookup
does not establish that no other archive or author copy exists.

The official [modlAMP core implementation](https://modlamp.org/_modules/modlamp/core.html)
lists its `isaeci` table. Its 20 ISA entries agree with the current MolSysMT
table, including ASN 19.53 and GLN 17.87. That is implementation agreement,
not original-table or physical-unit certification. A later independently
authored [descriptor application table](https://nru.uncst.go.ug/server/api/core/bitstreams/259a5ab2-84d5-4741-9759-949926a3e99c/content)
reverses these two ISA labels (ASN 17.87, GLN 19.53). Conflicting reproductions
make the original table important; they are not a sufficient basis to correct
either number here. No numerical change has been made.

## Implemented clarification

The public docstring and table comments identify the original DOI/PMID,
separate historical lookup from recomputing a descriptor, and state that a
raw float is not evidence of dimensionlessness. The tutorial, Foundations,
Cookbook and Common Core distinguish unqualified ISA reference values from
coordinate-dependent SASA and warn against assigning guessed nm²/Å² units.
No signature, value, scale, type, unit conversion or dependency changed.
No new attribution engine boundary was added: the original scientific
reference is explicitly documented rather than claiming execution of the
original descriptor-generation algorithm.

The related ECI reader wraps scores in elementary charge and sums them as
charges. Its physical dimension and aggregation are independently unverified;
that separate suspected mismatch is tracked by uibcdf/molsysmt#475. Neither
issue is closed by documenting uncertainty.

## Remaining evidence and recovery

Obtain an authorized copy of the original Collantes/Dunn paper and inspect the
ISA definition, numerical table, units and normalization, including the ASN/GLN
assignments. Request for maintainer access was sent during this review. Once
verified, choose the scientific public contract, document any compatibility
change and protect it with a primary-reference guard. Do not infer units from
value magnitude, the variable name, another library or a successful unit test.

## Local qualification of the clarification

On Linux/Python 3.14.7, the existing property-selection module and both changed
public-function doctest modules pass **437 tests** in 19.77 seconds using
`python -m pytest tests/physchem/test_property_selection_contract.py
 --doctest-modules molsysmt/physchem/get_surface_area.py
 molsysmt/physchem/get_charge.py --receptor=llm -n 12`. Four expected legacy
H5MSM warnings remain. These checks protect existing selection, containers
and numerical behavior; they are not a primary-reference certification.

AST comparison against source 9d7d81d31, excluding only docstrings, confirms
identical executable code in get_surface_area.py, get_charge.py and the ISA
table module. The changed surface-area tutorial is force-executed (6.9 seconds);
its label now says raw ISA descriptors. The other notebook changes affect
only prose. All 491 raw notebook-schema cases pass (7.49 seconds), all 251
public docstrings pass the existing validator, and selected Ruff check/format
pass. Incremental HTML compilation exits 0 with zero errors and 29 warnings
under the existing uibcdf/molsysmt#144 debt. No new unit/scientific tests are
added solely to repeat the table implementation.

The preceding source checkpoint 9d7d81d316f7e4f8d84f6d115343ed71dd1fe3d2
completed all five applicable CI workflows successfully, including smoke
run 40421796702. That is prior-source evidence, not an assertion about a later
commit, installed package, another platform or publication readiness.

## Maintainer decision: provisional typed areas — 2026-10-26

The maintainer explicitly requests unit-aware output despite unavailable original
full text. The public reader now wraps unchanged table numbers provisionally in
angstrom² and standardizes through PyUnitWizard. Thus ALA 62.9 angstrom² appears
as 0.629 nm² under the default policy; explicit angstrom² extraction preserves
the historical model input scale. The experimental return changes from a list
to an area quantity, including typed empty selections, with signatures unchanged.
No numeric table entry is edited. The native Viewer wrapper forwards that quantity
without correction. The tutorial, Foundations, Cookbook, course and help disclose
the provisional convention prominently.

This issue remains partial and open as the requested reminder to verify the
original paper; a duplicate verification issue is unnecessary. The governing
acceptance criteria above are not satisfied merely by choosing a software unit.
The related ECI output is already a quantity in elementary charge; its dimension
and aggregation remain unverified under uibcdf/molsysmt#475 and are not changed.

## User-proposed evidence and source audit — 2026-10-26

The supplied assessment suggests angstrom² from magnitude and describes hydrated
supermolecules, empirical H-bond hydration, MMFF/AMBER and a Hermann surface program.
These details are leads, not verified original-paper content in this review. The
accessible original abstract confirms ISA/ECI and optimized structures for QSAR;
it does not establish units, normalization or those computational details.
Changing 62.9 angstrom² to 0.629 nm² within a typed quantity preserves the adopted
physical area; table-scale machine-learning features should request explicit units.

A fresh official AAindex1 download contains 566 records and no matches for
Collantes, isotropic, electronic charge index, original PMID or page number.
This bounded search does not establish absence from every historical release.
Pinned modlAMP source 458c4dbb4c7888208ce3d9326484906b95324801 contains ISAECI
and agrees with all twenty current ISA entries and all twenty ECI entries.
It attaches no physical units to that table or its corresponding scale description.
Peptides R source a1a91be11bd6ba183541008cd038e328b4c33868 exposes ten families
in aaDescriptors; its R/manual text has no Collantes/ISAECI/isotropic/ECI entry.
Its charge function uses a pH/pKa model. These implementations are not primary
certification of the original units. No table value is altered from this audit.

The [source-audit receipt](../../devtools/data/collantes_external_sources_20261026.json)
records exact versions, original source hashes, searches and scope. The unit
implementation and checks are retained in
[the quantity receipt](../../devtools/data/collantes_provisional_quantity_20261026.json).

## Qualification of the provisional quantity convention

The 27 new unit/conversion cases fail against the preceding raw-list output.
With the provisional implementation, the property-selection, surface-area,
Viewer-wrapper and changed public doctest selection passes **547 tests** in
27.04 seconds with twelve workers and pytest-receptor. All twenty table entries
remain identical by literal AST comparison. The surface-area tutorial executes
successfully in 6.5 seconds. The five other course notebooks change prose only;
code cells, outputs and notebook metadata are preserved.

All **491** notebook-schema cases pass (8.05 seconds), all **14** fast release
gates pass, selected Ruff check/format pass, all 251 public docstrings pass the
existing validator and the signature guard reports zero drift. Incremental HTML
compilation completes with zero errors and 53 warnings under the existing
uibcdf/molsysmt#144 documentation debt. These checks protect the adopted
software convention, not the unresolved original-paper scientific claim.
No full-suite, installed-pair, cross-platform or publication qualification is
asserted for this checkpoint.
