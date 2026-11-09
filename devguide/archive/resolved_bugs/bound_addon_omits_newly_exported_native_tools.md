---
summary: Bound addon omits newly exported native tools
issue: uibcdf/molsysmt#665
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: high
verification: reproduced
area: [api, structure, tests]
guard: tests/molsysviewer_molsysmt/test_provider_admission_tools.py
normative:
blocked_by: []
supersedes: []
---

# Newly exported native tools are absent from the bound addon

## What

The source-integrated Viewer addon omits normalize_indexed_hydrogen_policy,
get_pairwise_rmsd, get_distance_clusters and h5msm.read_axis_sizes. Its write
and write_layers signatures also lack the explicit format/mechanics controls.
The three mandatory addon preflights and axis-angle guards reproduce one
inventory failure and 44 passes on public MolSysMT efffbaa8f, Python 3.14 and
the unchanged native backend. This reproduction uses the retained Viewer
e4dd58cf source, independently of the reporter's newer ce9163df source.

## How

Explicit namespace wrappers were not added when the native exports changed.
The strict H5MSM exposure assertion detects the omission. The existing structure
inventory honestly recorded two missing provider tools; #665 now requests their
admission, without adding graphical tasks. Reproduction command:

```bash
python -m pytest --receptor=llm -n0 \
  devtools/tests/test_smoke_addon_test_command.py \
  devtools/tests/test_molsysviewer_tools_api_inventory.py \
  devtools/tests/test_native_viewer_integration.py \
  tests/molsysviewer_molsysmt/test_axis_angle_rotation_tools.py
```

## Why

Viewer consumers cannot reach implemented native tools through the advertised
bound hierarchy, and mandatory preflight fails. This is a facade regression,
not demonstrated invalidity in the native algorithms. Native MD stubs remain
deliberately omitted. #666's contact cutoff investigation is separate.

## Implementation and acceptance

Mirror exact native signatures/defaults and skip_digestion, using addon
ArgDigest admission and SMonitor signals. Bind only actual molecular-system
operations through the serialized reader. Clustering and axis inspection keep
explicit inputs and work on an open empty owner; all calls reject closed owners.
Normalization returns an independent molecular system/report with no adoption.
Preserve native units, work/memory bounds, ordering, reports and diagnostics.
H5MSM writing stays 0.5 by default; mechanics require explicit experimental 0.6.

Receive native parity plus analytical translations/linkage, invalid requests,
pending-primary/replacement, detached results and source/scene ownership.
Update API help, User Guide, Cookbook/course and hosted selection. Retain strict
inventory checks. Record exact source/runtime/resource evidence separately from
newer Viewer, installed-package, human and release qualification. No new kernel,
dependency, graphical task or release is authorized by this correction.

## Directed receiving — 2026-11-09

The initial new-guard selection recorded seven fixture failures and 115 passes:
its fixture changed coordinates before expecting preserved coverage, used a
nonexistent generic MolecularMechanics.parameters store, and asked a zero work
bound to reach workload rejection rather than native positive-bound validation.
Those test assumptions were corrected to attach coverage after fixture setup,
use the actual stored forcefield field and request positive insufficient work.
No scientific criterion or production algorithm was changed to satisfy them.
The corrected focused selection passes 122 cases. Three additional typed-axis
and numeric-budget guards plus documentation receiving are being qualified.

## Broad receiving and corrected namespace guards — 2026-11-09

The 5,806-case broad selection reached its own 600-second time limit after
4,039 complete setup/call/teardown passes. The original invocation is incomplete,
not passing. The service journal reports timeout and a 2.4G peak; its final
per-cgroup counters were not retained after service collection. Recovered source
and Viewer hashes are unchanged. A separate collection-only manifest identifies
all 5,806 nodes; collection is not execution.

Whole files with any uncompleted case were resumed in two bounded batches:
979 cases (978 passes/one failure) and 852 cases (843 passes/nine failures).
Nine failures are stale strict namespace/count expectations in three earlier
addon modules; the remaining new help check found no native write_layers example.
Expected names and the reviewed count are updated explicitly, preserving exact
set comparisons. A real executable mechanics-layer example is added to native
help. No scientific formula, criterion or numerical assertion is changed.
Two stale sentences in the already edited course module are corrected to retain
ChemicalStates ownership and distinguish default 0.5 from experimental 0.6.
The affected complete modules and documentation are being rerun. The original
failures/time limit remain evidence; no single all-in-one passing run is claimed.

## Resolution — 2026-11-09

Implemented and contract/parity/analytically tested on clean source 46ed67b7e.
The [receiving record](../../../devtools/data/bound_provider_admission_receiving_665_20261109.json)
retains all failed/interrupted attempts and proves coverage of 5,806 current
logical test cases across bounded executions. A case requires passed setup,
call and teardown. Earlier passes are reused only for unchanged test modules;
every changed module is rerun on the final source. Scientific ASTs are unchanged
between the two receiving checkpoints; the sole native change is executable
H5MSM help. This is not one passing all-in-one run or final-candidate evidence.

The final affected selection passes 398 cases with no omissions, including the
strict namespace guards, four native additions, both H5MSM writers, six permanent
inherited-help examples and the guide recipe. Fourteen fast gates pass. Four
rendered pages (API, guide, course, Cookbook) are inspected. All fourteen course
code cells and the Cookbook's executed cell remain exact, including outputs and
execution metadata. The final smaller HTML rebuild emits no warnings; the six
existing title warnings observed earlier are not thereby repaired.

The source inventory exposes 251 of 253 callable paths; only the two unconditional
native MD stubs remain omitted. Native scientific/work/memory controls,
experimental labels, units, detached ownership and diagnostics are retained.
No new graphical task, scientific detector, dependency, backend, package or
release is introduced. Viewer e4dd58cf is the exact retained host used here;
newer-client, installed, human and final-release qualification remain separate.
Native contact review #666 and uibcdf/pyunitwizard#143 stay open, with the contact
prototype isolated. No graphical milestone credit is added.

Argument admission uses the existing addon ArgDigest configuration, while native
scientific validation, conditional DepDigest availability and executed-branch
Ackredit attribution remain at their original owners. No new scientific method
or third-party resource is implemented by these wrappers, so no additional
scientific attribution registration or dependency floor is introduced.
