---
summary: Attribute-alias initialization depends on cold native import order.
issue: uibcdf/molsysmt#535
status: open
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [argdigest, attribute, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Cold native declaration imports lose an attribute-alias table

**Reported:** MolSysViewer metadata-facade receiving under
uibcdf/molsysviewer#264 and uibcdf/molsysmt#421.
**Status:** independently reproduced in fresh processes; ownership diagnosis and
isolated regression remain pending.

## What

Two fresh processes on source 27c6bd3c0b4adfc1b7c3b635b9f30bcf6ffa0cab
call `msm.get(None, atom_names=True, atom_name=False)` after different imports.
Importing the private `attribute_synonyms.TABLES` declaration first yields
UnknownArgumentError. Importing public `attribute.get_argument_aliases` first
yields the intended ArgumentConsistencyError for two names of one argument.
This reproduces the incoming isolated native-test failure; it does not establish
that every ordinary public import order fails.

## How

The normalization declaration imports the public attribute package, whose
initializer also imports a decorated bond-requirement helper. This can initiate
ArgDigest discovery while the declaration module is partially initialized.
Cached partial discovery is the current hypothesis, not an established provider
defect or permission to patch ArgDigest in this repository.

## Why

A broad test run can prime the registry and conceal the missing collision check.
Changing the expected exception, preloading the package or manually translating
keywords in MolSysViewer would not repair the initialization contract.

## Acceptance and boundaries

Add fresh-process coverage for both orders, alias/canonical collisions and
ordinary accepted aliases. Diagnose declaration bootstrap versus shared provider
discovery before choosing the owner of a repair. Keep validation, scope and
function-contract lookup intact. Report a reproduced shared-provider defect to
ArgDigest through its owning issue/contribution route if needed. No correction,
new dependency floor or consumer workaround is implemented by this report.

## Provenance

2026-11-03, Linux, existing Python 3.14.7 development environment. Both subprocess
probes exit normally after reporting the distinct exception classes. No extra
environment, module-registry priming or native rebuild is used for this probe.
The bounded local receipt is retained under the ignored
`.pytest_cache/stabilization-520-533/534-535-triage.json`.
