---
summary: ChemicalStates extraction changes component column dtypes from string to object.
issue: uibcdf/molsysmt#531
status: active
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [native, extract, form]
guard: tests/native/test_chemical_component_extraction.py
normative:
blocked_by: []
supersedes: []
---

# Component column types change during chemical extraction

**Reported:** PharmacophoreMT owner receiving under uibcdf/pharmacophoremt#69.
**Status:** corrected and locally qualified; hosted current-Pandas receiving remains pending.

## What

Public convert/extract changes ChemicalStatesDict component_name and
component_type descriptors from string to object even when whole components
are retained. The caller's transport contract changes although the example's
label values remain unchanged.

```python
source = msm.convert(msm.convert('smiles:CC.CC', to_form='rdkit.Mol'),
                     to_form='molsysmt.MolSys')
selected = msm.extract(source, selection=[0, 1])
```

Encoding source and selected chemical domains reproduces string/string versus
object/object. Four consumer CCD merge/extract controls report this mismatch.

## How

The complete-graph path in native/_chemical_components.py::restrict creates
component_name/type columns by scalar pd.NA assignment, losing their typed
storage before transferring exact-atom-set labels. The incomplete-graph path
already copies typed source columns. The transport encoder reports the actual
dtype; it is not the source of this mutation.

## Why

Clients must be able to compare typed chemical payloads without a consumer-side
normalizer. This is distinct from #526's Pandas column-index compatibility fix.

## What is measured and what is assumed

The issue's public CC.CC reproduction runs on main 00abb958f, Python 3.14.7,
Pandas 2.3.3 and NumPy 2.4.6. The original consumer's broader failures and newer
RDKit/Pandas environment remain its own evidence, not a provider replay.

## What was refuted

No change to atom identity, coordinates or the example's label values is needed
to expose this defect. Rewriting dtype strings in the encoder would conceal
native storage drift. A topology fallback or client-side repair is unnecessary.

## Scope and exclusions

Preserve source component label-column dtypes during restriction, including
typed missing labels for cut components and empty outputs. Keep exact-atom-set
matching, graph participation, component evidence, IDs and source nonmutation.
Legacy object-backed columns remain supported; no schema/version, chemistry,
detector, dependency or public API expansion is introduced.

## Acceptance criteria

Public basic/native extraction and merge/extract preserve declared column
types, nullable values and aligned component/atom/structure correspondence.
Cover whole, reordered, cut and empty selections, complete/incomplete graphs,
independent states, dictionary round trips and current H5MSM transport. Retain
the consumer's minimal reproduction and independent literal expectations.

## Provenance

Linux x86_64, shared development Python 3.14.7, NumPy 2.4.6, Pandas 2.3.3;
2026-11-03. No auxiliary environment or native-extension rebuild is required.

## Local correction and qualification — 2026-11-03

The complete-graph restriction now allocates each missing label column using
its source dtype before exact-atom-set value transfer. This retains nullable
string storage, supports legacy object-backed labels and avoids an intermediate
Python list per component. The encoder, graph partition, eligibility of inherited
labels, component IDs, source tables and molecular-coordinate handling are
unchanged. Atom permutation remains distinct from extraction and preserves its
other index axes.

The final, valid 23-case public regression selection fails before the change:
11 dtype assertions fail and 12 controls pass. The same selection passes all
23 cases afterward, without skips, failures, errors or warnings. It covers both
basic/native extraction, empty/cut/whole components, independent state dtypes,
nonconsecutive structures, public permutation, merge/extract, dictionary/H5MSM
recovery and the reported RDKit example. Literal expected labels, memberships,
atom IDs, bonds and coordinates are independent of the reconstruction algorithm.
Canonical primary artifacts are complete and integrity-valid; JUnit agrees.

The broader command also passes, without skips: **2,633 cases**, exit 0,
105.01 seconds, 688 disclosed warnings (mostly legacy H5MSM diagnostics).

```bash
python -m pytest --receptor=llm -n 2 \
  tests/native tests/form/molsysmt_ChemicalStatesDict \
  tests/form/molsysmt_MolSysDict tests/form/file_h5msm tests/basic/merge \
  tests/basic/test_permute_atoms.py tests/basic/test_extract.py \
  tests/basic/test_extract_extended.py
```

The 33 workflow/dependency-command controls, all 14 fast gates, whole-package
Ruff and changed-file formatting pass. The smoke workflow and local smoke tier
both include the new regression module, so current-Pandas hosted execution
exercises the actual contract rather than merely validating collection.

The shared Python 3.14/Pandas 2.3 environment is reused. Hosted current-Pandas
results remain pending at this source checkpoint. Consumer CCD replay and
installed/platform qualification remain separate; the client's assertions and
scientific profiles are not changed. Earlier test-fixture/CLI authoring errors
are retained privately and are not counted as product-regression evidence.

While preparing the independent fixture, a distinct three-domain composition
case was reproduced: Topology + ChemicalStatesDict + Structures fails, whereas
the native triple and dictionary/Structures pair succeed. The historical #269
pair remains repaired; the separate triple finding is not fixed or concealed
inside this dtype correction.
