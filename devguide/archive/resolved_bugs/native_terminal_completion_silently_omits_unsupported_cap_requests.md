---
summary: Native terminal completion silently omits unsupported cap requests
issue: uibcdf/molsysmt#708
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: high
verification: reproduced
area: [build]
guard: tests/build/add_missing_terminal_cappings/test_generation_report.py::test_native_rejects_unsupported_cap_requests
normative:
blocked_by: []
supersedes: []
---

# Unsupported native terminal-cap requests can return incomplete results

**Reported:** 2026-11-11, from PeptideMT's source receiving comment on
[uibcdf/molsysmt#685](https://github.com/uibcdf/molsysmt/issues/685#issuecomment-6788187086).
**Status:** Resolved with explicit role-specific refusal; supported reconstruction remains qualified.

## What

The native terminal reconstruction route can return without creating the explicitly
requested C-terminal primary amide. The operation parameters retain the unsupported
request, but its `unassessed` list is empty. Reproducer on two artificial Ala-Ala chains:

```python
import molsysmt as msm

molsys = msm.build.build_peptide('AA', engine='MolSysMT')
molsys = msm.remove(molsys, selection='atom_type=="H" or atom_name=="OXT"')
molsys = msm.merge([molsys, molsys], keep_ids=False)
molsys.molecular_mechanics = None
result = msm.build.add_missing_terminal_cappings(
    molsys, N_terminal='ACE', C_terminal='NH2', pH=8.0,
    keep_ids=True, engine='MolSysMT', return_report=True)
termini = msm.chemical_states.get_peptide_termini(result['molecular_system'])
```

Before correction: 20 source atoms become 32; both chains are N-capped, neither
is C-capped, and `result['report']['unassessed'] == []`. Default output without a
report also silently omits unsupported labels. Wrong-role known templates can
instead raise internal `KeyError` during placement.

## How

`molsysmt/build/add_missing_terminal_cappings.py` sent arbitrary cap strings to
`load_residue_template`. A missing template silently bypassed placement; an
existing template of a different role was sent to the ACE/NME-specific placer.
The shared ArgDigest value digesters correctly accept strings used by multiple
engines, but did not define this native placement profile.

The correction checks the selected engine's actual scientific support at the
public orchestration boundary: native requests are exactly `N_terminal=None` or
`'ACE'`, and `C_terminal=None` or `'NME'`. Other labels, wrong roles and wrong case
raise the existing SMonitor `NotImplementedMethodError`, with argument/value and
supported choices, before source selection, copying or reconstruction. The check
also applies to empty selections and trusted internal digestion bypasses.
PDBFixer retains independent provider-specific cap handling.

## Why

A caller can otherwise persist or consume an operation that omitted explicitly
requested chemistry. A primary carboxamide and N-methylamide are different
chemical groups; automatic substitution would be incorrect. High severity here
reflects a silent preparation-result mismatch, not a claim that every terminal
completion or the correctly qualified #558 map/history route is defective.

## What is measured and what is assumed

The 20-to-32-atom result and empty unassessed list were reproduced locally on
unmodified `d274c102a0cc47a90cced2d0b1a6b56a024176ce`. Twenty of the initial 21
new refusal/delegation cases fail on that source; the provider-delegation case
passes. Four further combinations cover report-mode early refusal.
After correction, all 48 generation-report cases pass, including the 25 new
cases. No claim of new cap geometry, chemical-state assignment or energetic
validation follows from these refusal tests.

## What was refuted

- Retaining a requested label in report parameters does not prove its execution.
- Availability of other exact-name templates does not make them suitable for
  the role-specific ACE or NME placement formulas.
- `NH2`/`NHE` are not aliases for NME. Recognition or fresh peptide construction
  elsewhere in MolSysMT does not extend this reconstruction route.
- This does not require reopening #558: the supported ACE/NME correspondence,
  observation-preservation and persistence contract remains independently tested.

## Scope and exclusions

This defect owns explicit refusal of unsupported native terminal-cap requests.
The broader capped, coordinate-free, stereochemically declared peptide-reference
proposal remains uibcdf/molsysmt#685. No primary-amide placement, new reference
factory, stereochemical assignment or consumer-specific builder is introduced.
The reported PeptideMT ACE/NME source receiving is a bounded downstream statement;
its local record is not an immutable published or installed-package acceptance.

## Acceptance criteria

1. Unsupported and wrong-role requests raise an actionable public exception,
   for default and report output, before source work or any partial publication.
2. Refusal preserves source inventory, coordinates and preparation history.
3. Empty selections and `skip_digestion=True` do not bypass support checks.
4. Supported native terminal reconstruction and map/history persistence pass;
   PDBFixer delegation remains independent of the native profile.
5. Docstring, User Guide, Cookbook and course explain the exact supported profile
   and distinguish primary amide from N-methylamide.

## Provenance

Linux, Python 3.14.7, public PyUnitWizard 0.29.2, existing ABI3 binary SHA-256
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`, 2026-11-11.
The reproducer used one CPU and a 1-GiB hard memory limit. Focused pytest used
one CPU / 2 GiB; the combined regression uses two workers / CPU quota 200%,
memory high/max 3/4 GiB and no scope swap. Thread pools are capped at one.
Scratch is on the workspace filesystem. Host MemAvailable was about 14 GiB and
sampled memory-pressure averages were zero before the combined run. These are
source controls, not installed release qualification.

## Resolution — 2026-11-11

**Contract-tested:** All 252 combined cases pass, including 25 new refusal and
provider-delegation cases and the three existing module doctests. The complete
selection is:

```bash
python -m pytest --receptor=llm -n2 \
  tests/build/add_missing_terminal_cappings \
  tests/build/add_missing_heavy_atoms tests/build/add_terminal_atoms \
  tests/build/test_native_placers.py tests/basic/test_compose_atom_maps.py \
  tests/topology/test_correspondence_attribution.py \
  tests/interactions/test_scientific_attribution.py \
  --doctest-modules molsysmt/build/add_missing_terminal_cappings.py \
  molsysmt/build/add_missing_heavy_atoms.py molsysmt/basic/compose_atom_maps.py
```

Existing scientific-coverage and attribute-loss warnings remain visible. The
selected guard directly requires the public refusal for unsupported/misplaced
caps in both return modes; it fails on the original source rather than merely
checking the shape of a new helper. Separate assertions verify source inventory,
coordinates and history, early refusal, empty selections, digestion bypass and
independent external-provider delegation.

Ruff, 254 public docstrings, signature stability, optional-import validation,
two notebook schemas, the 156-notebook course structure and local developer-guide
checks pass. Notebook edits change Markdown only; executable cells, saved
outputs, IDs and metadata are unchanged. Four affected API/User Guide/Cookbook/
course HTML pages build and were inspected for the supported profile and failure
contract. This selected-page build reports an incomplete search-index warning;
it is documentation receiving, not a publication build.

The existing ArgDigest type boundary remains in place; engine-dependent
scientific availability is checked even on trusted delegation. Diagnostics reuse
SMonitor's catalog exception. No dependency floor, optional import, unit rule,
scientific formula or attribution source changes. Existing attribution receiving
is retained in the regression. Broader #685 reference/cap support stays open.

Local evidence is retained under
`.pytest_cache/pre1-review-20261111/terminal-profile-685/`: `before.xml`,
`report-after.xml`, `qualified-regression.xml` and `html.log`. These are local
receipts; durable assertions and the source command above remain in Git. No
unrelated process was stopped, no hosted matrix was launched and no release
artifact was produced.
