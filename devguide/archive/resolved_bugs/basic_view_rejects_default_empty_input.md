---
summary: Basic view rejects its declared default empty molecular input.
issue: uibcdf/molsysmt#578
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [basic, argdigest, deps, tests]
guard: tests/basic/view/test_empty_view_contract.py::test_default_or_explicit_none_creates_empty_workspace
normative:
blocked_by: []
supersedes: []
---

# Basic view rejects its default empty input

## What

On main `9750272c4f321d1e3c8ae1a391f8e721e6a58f02`, both `msm.view()` and
`msm.view(viewer='NGLView')` fail normal argument digestion on their declared
None default. The same valid requests with trusted delegation create an empty
MolSysView/NGLWidget. Each returned object was closed; no browser rendering was
needed. Python 3.14.7, source MolSysViewer and installed NGLView.

## How

The molecular_system digester assesses None as an unsupported molecular form
before reaching view's explicit empty-source branch. Both runtime adapters
already support the empty case. NGLView already declares its dependency guard;
MolSysViewer's adapter lacks that corresponding explicit boundary.

## Why

A valid default must not require users to turn off argument validation. The
exception belongs to exactly molsysmt.basic.view.view, not every function
named view or other scientific operations receiving molecular_system.

## Contract and scope

None creates an empty workspace for either registered backend. All, None or a
flat empty axis is admitted; molecular expressions and explicit/nonempty indices
without a source fail before construction. Reuse shared basic index validation
with zero source counts. Existing loaded inputs still use ordinary selection
and structure validation; a loaded empty request is not rewritten to None or
silently turned into a different data model.

Keep conditional/lazy provider imports and use DepDigest for either selected
backend. Invalid viewer types retain native argument diagnostics. Preserve
static-HTML documentation behavior, caller unit policy and source ownership.
No browser/canvas/session API, scientific calculation, dependency floor or
public signature changes. No new units or attribution event is defined.

## Acceptance criteria

- Real Python object construction for omitted/explicit None, both backends,
  admitted empty axes and normal/trusted valid requests; close every object.
- Exact-caller digestion exception with unrelated scientific callers rejecting
  None as before.
- Invalid selectors, structures, backend/syntax controls and skip flags fail
  before backend creation; selected missing dependencies use native diagnostics.
- Loaded inputs remain validated and preserve their source. Explain default
  backend versus explicit viewer=None configuration and loaded-empty limits.
- User Guide, Foundations, Cookbook, course, docstrings and local records agree.

## Observed limits

MolSysViewer deliberately rejects empty selectors for a loaded source in its
load-composition policy; its own tests retain that contract. This correction
admits empty axes on an absent source only and does not alter that provider
contract. Static-HTML mode still requires a prepared asset. Python return/lifetime
checks do not certify rendering or installed/platform/release compatibility.


## Resolution and receiving — 2026-11-05

**Contract-tested** Python construction and lifetime. The exact public view
caller now admits None during ArgDigest normalization. Shared basic axis
validation uses zero available source counts before adapter dispatch; no empty
MolSys or scientific data are synthesized. Other scientific callers still reject
None. Loaded inputs keep their existing validation/delegation, including backend
requirements for nonempty loaded selections.

The MolSysViewer adapter now declares its existing hard provider through
DepDigest, matching the selected NGLView availability boundary without changing
dependency classification or eagerly importing a provider. Invalid viewer types
raise the native argument diagnostic. The valid trusted-call and ordinary-call
routes agree for the documented normalized empty-workspace inputs; users need
no skip_digestion workaround.

Receiving passes **273 affected tests** covering view, public structure-index
boundaries, selection, molecular-system validation, viewer argument normalization
and dependency architecture. **66 cases pass with published ArgDigest 0.14.0,
DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payloads**, disabling only the
known editable pytest entry point under #524, not runtime diagnostics.
**569 documentation/governance/doctest cases pass**, including the updated real
empty and loaded widget examples. These are overlapping selections, not a
unique aggregate count. Published Pytest Receptor 1.2.1 uses four workers for
receiving and two for floors/docs.

Tests construct and close actual empty widgets for omitted/explicit None, both
backends, trusted/ordinary valid calls and empty axes. Guards also check missing
providers, invalid inputs before construction, exact-caller scope, configurable
viewer=None versus omitted-viewer behavior, and forwarding a loaded empty
selection without replacing its source. Existing loaded-source comparisons
remain in the receiving suite. No browser canvas, session export, new molecular
calculation, performance benchmark or installed/platform release claim is made.

Foundations, the view tutorial, NGLView Cookbook and visualization course explain
the scope. The backend matrix now matches the two actually registered routes;
its previous Py3Dmol claim had no public dispatch route. The existing public
signature still defaults viewer to MolSysViewer; only explicit viewer=None reads
configure.default_viewer. Three notebooks retain every original executable cell,
output and metadata. Public docstrings have executable deterministic examples
with explicit widget closure instead of version-sensitive object reprs.

Ruff, dependency scanning, signature/docstring, course and developer-guide checks
pass. No dependency floor, public signature, compiled kernel, H5MSM schema or
scientific attribution changes. Unit conversion is not newly applicable to an
absent molecular payload; existing loaded-source paths remain unchanged. No
Ackredit event is added for an operation without a new scientific calculation.

The [receiving receipt](../../../devtools/data/empty_view_receiving_578_20261105.json)
records commands, file hashes and boundaries. The next
native defect is #560 (force-field registry output ownership), then #559/#561/#562.
PR #543 remains at 94548b434f5d673f6fcfc6c97db9d83601a5b4b7 at review. Routine
hosted inspection on the new delivery and installed/platform/release gates remain
separate; no additional release matrix or publication is launched by this fix.
