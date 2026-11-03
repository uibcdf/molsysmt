---
summary: ChemicalStates extraction changes component column dtypes from string to object.
issue: uibcdf/molsysmt#531
status: resolved
opened: 2026-11-03
closed: 2026-11-03
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
**Status:** resolved on main; source qualification passes with Pandas 2.3.3 and 3.1.0.

## What

Public convert/extract changes ChemicalStatesDict component_name and
component_type descriptors from string to object even when whole components
are retained. The caller's transport contract changes although the example's
label values remain unchanged.

```python
import molsysmt as msm

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

## Hosted string-inference finding and decoder correction — 2026-11-03

The first hosted run on bd28d57f2, [41668264549](https://github.com/uibcdf/molsysmt/actions/runs/41668264549),
uses Pandas 3.1.0 and fails: **4,046 passed / ten failed / 16 skipped**, exit 1.
All ten failures are legacy-object descriptor assertions; the original nullable
string extraction regression now passes. The addon step is not executed after
that failed native tier. This is retained failed evidence, not qualification.

The decoder previously constructed a typed array and then a Series without an
explicit dtype. With Pandas string inference enabled, that final constructor
changes the declared object column to str. The correction passes the payload's
dtype to the Series boundary as well. No encoder rewriting or client comparison
relaxation is used. Two independent round-trip controls reproduce the failure
locally under future.infer_string=True before that decoder edit.

After both corrections, the same 25 focused cases pass with string inference
enabled, including the 23 extraction controls and two decoder controls. The
broader native/form/extract/merge/permutation selection passes **2,635 cases**,
without skips or failures, in 94.02 seconds with 688 visible warnings. These
executed source scopes do not replace the corrected hosted run, which remains
pending at this checkpoint. The failed original artifacts remain retained.

H5MSM keeps its existing canonical textual field schema. The dictionary/native
storage preservation demonstrated here does not add an arbitrary-Pandas-dtype
promise to the H5MSM schema or change its version.

## Resolution — 2026-11-03

The complete correction is published on main at
0faf1584d05ac47ddcebfc20d9c9978b7f4f230e, including the initial restriction
fix bd28d57f2. Source dtypes are retained both when staging missing component
labels and when constructing decoded Series. The encoder, scientific profiles,
exact-atom-set label eligibility, component/atom correspondence and wire versions
remain unchanged. No whole molecular/coordinate copy is added by the correction.

The closing guard is tests/native/test_chemical_component_extraction.py. Its
23 public controls assert literal types, null masks, values, graph memberships,
atom IDs, remapped bonds and coordinates, including source nonmutation. The
additional two controls in
tests/form/molsysmt_ChemicalStatesDict/test_roundtrip.py::test_decoding_keeps_declared_object_columns_with_string_inference
protect the decoder under actual string inference. Both guards belong to the
maintained smoke selection; no test expectation is relaxed to admit dtype drift.

The final hosted [run 41670736932](https://github.com/uibcdf/molsysmt/actions/runs/41670736932)
is completed/successful on the exact corrected source. Its actual environment
uses Pandas 3.1.0. Native smoke: **4,058 passed / 16 skipped**, 456.03 seconds,
590 visible warnings. All 25 new controls execute without skips; the omissions
are 14 optional Ackredit cases, one unyt and one astropy case. The bound-Viewer
addon passes **2,449 cases / four optional Ackredit skips**, 367.92 seconds,
1,539 visible warnings. All six source-push workflows succeed. GH Run Receptor
returns exit 0, and completed native job logs retain the actual commands,
provider versions, counts and omission reasons.

The same correction passes the shared Pandas 2.3.3 broader selection (2,635
cases), 25 focused cases with default inference and 25 with string inference
enabled. Canonical primary evidence is complete and integrity-valid; the broader
JUnit count agrees. The 33 route controls, 14 fast gates, Ruff and formatting
pass in their scoped executions. Existing unrelated modified API stubs and
the shared Rust extension retain their original hashes. No extra environment,
dependency floor, source schema or compiled primitive is introduced.

PharmacophoreMT receives the exact main source under
[its owning review](https://github.com/uibcdf/pharmacophoremt/issues/69#issuecomment-6609357426).
Its four original CCD cases remain owning-team replay, not a provider claim.
The distinct triple-composition defect is recorded separately as #532; #269's
dictionary/Structures pair remains repaired. Full exact-candidate, installed
package and release qualification are not claimed by this source bug closure.
