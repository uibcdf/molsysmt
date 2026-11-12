---
summary: Form tutorial API roles render as unlinked code despite a warning-free build
issue: uibcdf/molsysmt#727
status: partial
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Receiving actual form implementation links

## What

Native form tutorials use Python func/mod roles for adapter objects that have
no indexed Sphinx API target. Full strict HTML can finish with zero warnings
while those references render as unlinked code. Actual compiled MolSys,
Topology and Structures operation/conversion tables show this defect. Link
inspection that considers only existing hrefs cannot detect missing intended
links, even when every link it sees resolves.

## How

Complete HTML on 1b98c2b1d and targeted MolSys receiving on 2bf21835f finish
with zero warnings. Inspect actual article tables: their implementation and
converter references have code.xref elements without enclosing anchors.
The source objects exist; their existence is different from a rendered link.
The bounded #725/#726 article proof remains valid for its 130/16 actual local
destinations, not for unlinked intended API references.

## Why

Users cannot follow the advertised API/implementation references. A good guard
must check the intended references, not accept an empty/partial set merely
because the existing links resolve. This is owning documentation/indexing debt,
not a demonstrated Sphinx provider bug or a scientific/runtime failure.

## Partial correction and acceptance

The MolSys tutorial now replaces all 57 role occurrences with clearly labelled
links to immutable published owning source/docstrings. Every operation/module
and registered conversion route must retain its real source destination; this
is not a new placeholder API page. Keep general user APIs linked to indexed
Sphinx targets. Runtime attribute/delivery, H-count semantics and bond ownership
retain #726's separate guards. Actual HTML must contain every intended source
link and no unlinked adapter role; source/reference existence alone is insufficient.

Topology and Structures retain this unlinked-reference debt; the wider form
inventory is not yet audited. Continue per-form review before claiming full
closure, respecting live route limits, source identities, supported signatures,
conversion declarations and notebook code/output preservation. No shared guide,
provider, dependency floor, scientific algorithm or release is changed.

## Evidence and next action

Private before-DOM counts, exact role/source map and corrected source/HTML
receiving belong to the #725/#726 combined receipt. Its declaration-only source
checks do not claim installed/provider execution for every optional converter.
Close this issue only after the remaining intended form references are audited
and repaired or explicitly scoped with an owned disposition.


## Received MolSys increment — 2026-11-12

Clean 115ebe335 receives the final native MolSys article with zero warnings,
57 intended reference occurrences and 55 distinct real published source files.
The actual DOM has 14 operation and 40 converter links, no unlinked Python
roles and all 16 existing local destinations. Earlier three foundation articles
remain unchanged. Five source/semantic controls pass. The earlier strong guard
also exposes six undocumented converter routes, now corrected under #726.
See the [combined receipt](../../../devtools/data/native_domain_documentation_receiving_725_726_20261112.json).
Topology and Structures still need intended-link correction, and the wider
form scope remains unaudited. This report therefore stays partial.


## Topology and Structures source receiving — 2026-11-12

The next owner baseline has two failures and twelve passing controls. The
Topology failure concerns missing complete source links; Structures first
fails its route-set check because its MolSys embedding route is omitted.
The prior source-object existence check passes during this baseline, showing
why existence alone cannot establish link delivery. Earlier native MolSys
references and domain/availability controls remain received.

Topology now has explicit published-source references while preserving its
38 declarations, seventeen registered converters, unavailable hooks, chemical
separation and executable inventory example. Structures retains 22 declarations
and adds the already implemented MolSys embedding to list all seven converters;
that route does not invent Topology or ChemicalStates. Both notebooks preserve
all code, outputs, cell order and non-source metadata. General axis descriptions
use structures. Their 52 final reference occurrences cover the existing 51
roles plus the formerly omitted converter.

The existing MolSys and Topology guards now reuse one private test-only source
checker; it requires the reviewed operation inventory, every runtime-registered
converter, actual defining function/line and no unlinked adapter role in source.
An explicit non-default HTML guard separately requires every expected href in
the actual article and validates local destinations. This introduces no public
runtime API or provider dependency.

Fourteen corrected controls pass. The first expanded cohort has fourteen
passes and two test-draft failures: its coordinate edit passes a quantity as
the positional indices argument. ArgDigest correctly refuses it. Preserve that
draft and use the documented value keyword, retaining the intended geometry,
unit, order and independence assertions. The initial provisional pass sentence
was incorrect and is corrected before publication. Final expanded and actual
HTML receiving follow before claiming these checks or links delivered.

A complete source notebook census finds 94 pages/1,832 func/mod role occurrences
under the form-tool root. These include indexed generic user APIs; syntax alone
is not a rendered failure. Literal-file feasibility is similarly bounded: aliases
and generic API spelling can require different resolution, so its unknowns are
not declared missing implementations. Other form-reference scope remains owned
here, with real source/HTML matching still required before broader acceptance.


## Expanded source cohort received — 2026-11-12

The corrected sixteen-case cohort passes with unchanged selected inputs. Both
unit policies preserve the original coordinate/time values and selected source
axis order, keep topology/chemical states absent and detach coordinate edits.
The two initial test-draft rejections and their erroneous provisional note are
retained separately; neither is a product or provider failure. Actual HTML
receiving is still pending at this checkpoint.
