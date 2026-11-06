---
summary: Importing the group classifier module replaces its public callable export.
issue: uibcdf/molsysmt#594
status: resolved
opened: 2026-11-05
closed: 2026-11-06
severity: medium
verification: reproduced
area: [api, tests]
guard: tests/element/group/test_name_recognition.py::test_direct_module_import_is_the_supported_classifier
normative:
blocked_by: []
supersedes: []
---

# Import-order-dependent group classifier export

## What

After importing `molsysmt.element.group.get_group_type_from_group_name`, the
public package attribute of the same name becomes a module instead of its
callable. Public classification and the bound addon then raise TypeError.
The existing compatibility-import guard checked only its local function alias,
not the public attribute after the import.

## How

`element.group.__init__` imports the function directly from get_group_type,
leaving the same-named compatibility module unimported. A later normal module
import installs that module on the parent package. The correction imports the
public function through that compatibility module during package initialization;
its implementation, identity, argument contracts and naming rules are unchanged.

The strengthened actual import guard fails on the combined unmodified source:
one failure in 0.48 s, with a module where the function is expected. In the
Python 3.14 full-CI job 127683524087 of run 42153312659, 25 of its 33 failures
belong to this same classification/export family (22 calls, two signature
queries and one doctest control). Other root causes remain separate.

## Why

Scientific query callability must not depend on import order. A consumer
fallback or direct internal import would conceal a broken public contract.
Both import routes must retain the same supported implementation.

## Scope and acceptance

- Package and direct-module imports retain the same callable after either path.
- Scalar classification, public help/signatures, native digestion and addon
  delegation continue to work in a serial import-order run.
- No naming interpretation, scientific method, public signature, dependency
  floor or compiled code changes.
- Keep the other full-suite failures visible; this correction does not qualify
  all of PR #543 or permit integration before its required gates pass.

## Provenance

Linux / shared Python 3.14.7; integration of main
ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6 with PR #543 head
1c88e785b4327350ad586d437a569eff1a2c5c9a. Hosted evidence is separately
identified above, with native command and per-job log fallback after the
receptor correctly reported an active matrix with four failed Linux jobs.

## Resolution — 2026-11-06

The original correction is already present in main through ab789897b. Current serial receiving passes 259 classifier, naming-context, public signature/doctest and real addon cases, without failure or omission. Both import routes retain the same supported callable; scientific naming rules and dependency floors are unchanged.

Verified source: cddc3f3a613282693126549654233d2fd1d739a4. Existing implementation originated in
ab789897bad51a7258f366aadc01840895d6366e; no new production fix is claimed by
this closeout. The new NMR guard belongs to the received source above.
[Exact source, JUnit digests and scope](../../../devtools/data/ordered_bug_closeout_594_598_20261106.json)
retain these independent profiles and their overlapping counts. Existing failed
full-suite history, remaining version-matrix/installed gates and release authority
are not changed by this bounded bug closure.
