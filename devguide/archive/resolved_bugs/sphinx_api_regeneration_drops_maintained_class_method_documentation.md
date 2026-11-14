---
summary: Sphinx API regeneration drops maintained class method documentation.
issue: uibcdf/molsysmt#752
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: medium
verification: reproduced
area: [docs, api]
guard: devtools/tests/test_autosummary_owned_pages.py
normative: devguide/documentation_sync.md
blocked_by: []
supersedes: []
---

# API regeneration removes maintained method documentation

**Reported:** 2026-11-14, while checking the actual pre-1.0 publication configuration.
**Status:** configuration corrected; focused controls and actual full-site receiving pass.

## What

The ordinary documentation configuration enables autosummary generation and
inherits its overwrite default. A disposable full-site build replaces 26
existing RST stubs. Most differences are formatting, but the maintained
ProtonationAssessment page loses its explicit `:members: to_dict, apply`.
Its rendered `apply` and `to_dict` API entries disappear. The read-only build
of maintained RST has both entries; a warning-clean build alone would not
establish that these method descriptions survived.

## How

Keep automatic generation enabled and set
`autosummary_generate_overwrite=False` in docs/conf.py. Existing maintained
pages retain their text and explicit member coverage. New entries with a
toctree still receive missing stubs. Runtime autodoc continues reading the
current callable docstrings; this is not frozen function documentation.

The real-Sphinx regression consumes the repository's actual configuration.
It builds an authored class page with two complete method entries and a
separate missing function page. The original configuration has two failures
and one pass: maintained source/context and complete methods are lost while
new-page generation works. The correction passes all three controls, plus
the existing source-boundary and public-API documentation cohort: 40 cases,
zero failures/errors/skips. The 591 Python warnings retain 588 installed
Sphinx Napoleon deprecations and three expected legacy-H5MSM warnings.

## Why

The release documentation must retain the supported public method contracts
that were deliberately written and reviewed. Rendering only a default class
summary can silently remove user guidance despite a successful generator.
Disabling all generation would instead stop new reference pages from appearing.
The regression protects both required behaviors using rendered content.

## What is measured and what is assumed

The initial full default-configuration experiment also fails for an isolated
harness reason: its docs-only copy omits the downloadable mechanics benchmark
JSON stored outside docs/. Preserve that missing-input warning and native exit
one. It is not a MolSysMT source-asset defect or a passing site. The next
complete copy includes that unchanged source asset with its hash recorded.
The independent miniature Sphinx witness has no build warnings and confirms
the method-loss mechanism separately from the omitted download.

The complete source suite continues on its separately frozen source. Neither
this documentation correction nor the #751 developer probe changes production
molecular code or the native binary. New focused controls and actual site
receiving retain their own source/delta identities.

## What was refuted

Turning off autosummary entirely can preserve a maintained page but fails the
missing-page control. Accepting only a zero warning count can miss absent
method bodies. Regenerating every RST and committing it would discard the
reviewed member lists rather than preserve their intent.

## Scope and exclusions

Only Sphinx configuration, rendering guards and contributor explanation change.
No molecular algorithm, notebook code/output, dependency, scientific criterion,
API signature or stability classification changes. No hosted deployment,
installed pair, package, tag or publication is authorized or qualified here.

## Acceptance criteria

- A real build retains maintained source/context and complete method entries.
- Missing public reference pages still generate.
- The full site with actual configuration is warning-clean, includes its
  referenced source assets and retains the real ProtonationAssessment methods.
- Intended-reference HTML guards, applicable fast gates and Ruff pass.

## Provider contract

This is MolSysMT configuration ownership, not an upstream Sphinx defect.
[Sphinx documents the overwrite control](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#confval-autosummary_generate_overwrite)
for preserving existing stubs. The local miniature/full builds use Sphinx 9.1.0;
no provider installation or upgrade occurs.

## Complete configuration receiving

The corrected disposable copy includes the unchanged external benchmark asset
and the reviewed configuration/README delta. The actual configuration has no
Sphinx overrides: autosummary generation stays enabled and overwrite is false.
All 1,034 documents produce 1,400 HTML files with zero warnings. No disposable
source is changed by that build. Both real ProtonationAssessment method entries
survive, and all 101 intended-reference HTML controls pass. Stored notebooks
are rendered without execution; no browser, deployment or final-pair result is
inferred.

The [receiving receipt](../../../devtools/data/autosummary_preservation_receiving_752_20261114.json)
retains actual command exits, the two-failure/one-pass miniature baseline,
original full-copy missing-asset failure, regenerated-page witnesses, reviewed
delta identities, complete-site and focused results, and conservative shared-host
limits. Applicable final checks retain their own results.
