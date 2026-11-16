---
summary: Receive the corrected notebook kernel baseline without changing the shared prefix
issue: uibcdf/molsysmt#765
status: resolved
opened: 2026-11-15
closed: 2026-11-15
verification: measured
area: [deps, docs]
guard: devtools/tests/test_jupyter_host_contract.py
normative:
blocked_by: []
supersedes: []
---

# Corrected notebook-kernel baseline receiving

**Reported:** uibcdf/molsyssuite#200's qualified notebook-subset handoff.
**Status:** applicable declarations, user guidance and selected-kernel routes reviewed.

## What

Receive the ipykernel >=7.4.0 host baseline without modifying the paused shared
prefix or attributing #615's original historical timeout to a proven cause.
The central published 4ba79c9562716fc05e8040e1be8c387799a96e19 report retains
its own native kernel probe; MolSysMT does not replay it or treat it as a full
scientific/browser/development-environment qualification.

## How

Published owner commit 5afa582f8 already declares ipykernel>=7.4.0 in the
actual development notebook environment and public installation guidance.
The semantic guard excludes affected older versions, admits the corrected
minimum and keeps ipykernel out of core/production requirements. The main
User Guide installation entry now points directly to the notebook-host notes
and asks users to inspect sys.executable and ipykernel.__version__ inside the
selected notebook; the server's environment need not be that kernel's.

The owned prolonged Jupyter receiver writes a private kernelspec whose argv
uses its selected sys.executable; the initial-canvas path retains that exact
interpreter. Documentation execution delegates to Jupyter nbconvert and the
notebook-selected kernelspec. These are inspected routes, not new kernel runs
or proof that every existing user's named kernel has upgraded. A parent-prefix
metadata check would incorrectly reject valid isolated kernels, so no such
runtime shortcut or shared installation is added.

## Why

Notebook transport can prevent a molecular scene from executing before any
scientific or renderer code is reached. The corrected kernel belongs to the
notebook host profile; adding it to headless MolSysMT would create an unrelated
runtime dependency and would not ensure that the user's actual kernel uses it.

## What is measured and what is assumed

The existing #615 receipt independently receives normal startup 928's original
kernel provenance and 37 custody-file hashes. It records loaded ipykernel
7.4.0, 3,983 atoms and a new native draw 10.7884 seconds after Run, under the
original thirty-second allowance. Its exact source/native composition and
historical-cause uncertainty remain in the
[archived investigation](../resolved_bugs/intermittent_jupyter_initial_canvas_timeout.md).
This previously accepted control is reused rather than rerunning science.
The existing two declaration guards are selected again for this adoption;
current outcomes and strict article receiving belong to the
[combined administrative receipt](../../../devtools/data/policy_notebook_adoption_764_765_20261115.json).

## Scope, risks and acceptance

Review the actual recipe, user entry points and selected-interpreter paths;
receive the declaration guards and rendered links; preserve core requirements,
source/native scientific bytes and the paused shared prefix. Upgrading the
live prefix, restarting unrelated kernels, installing a replacement environment
and full editable/browser/platform acceptance remain separate operator/client
work under uibcdf/molsyssuite#82 and #175. A version floor does not prove all
future kernel/provider combinations. Final exact-pair qualification remains.

## Provenance

2026-11-15, existing Linux/Python 3.14.7 and frozen support tooling; no new
kernel, molecular calculation, browser run, native rebuild or shared-prefix
mutation. The accepted original normal startup uses its separately recorded
7.4.0 module origin, not the version installed in this administrative process.
