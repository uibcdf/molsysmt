---
summary: Add element-level selection masks to molecular summaries.
issue: uibcdf/molsysmt#206
status: resolved
opened: 2026-10-20
closed: 2026-10-20
verification: reproduced
area: [api, basic]
guard: tests/basic/test_info_masks.py
normative:
blocked_by: []
supersedes: []
---

# Selection masks for molecular summaries

## What

MolSysViewer requests the same explicit scope on `info` that `select` and `get`
already provide. Its correction in #206 is authoritative: masks are indices or
Boolean flags at the requested element level, not implicitly atom-index masks
for every query. The maintainer authorizes a bounded improvement during the
continued 1.0 publication pause on 2026-10-20.

## How

Add an optional keyword-only `mask=None` to `basic.info` and `MolSys.info`,
preserving existing positional calls. Resolve an active mask through public
`select` before building the existing table. Its intersection, ordering,
deduplication, syntax and invalid-index handling remain owned by `select`.
An omitted or all-elements mask preserves the current path.

`info(element='system')` already interprets its selection as atoms for summary
counts; its mask uses that same atom axis. Other summaries use the declared
element axis. Structure selection retains its existing independent meaning.
No atom-to-group mask conversion is implicit.

## Why

This removes caller-side intersection plumbing for already levelled masks.
It does not eliminate the need for a region owner to map an atom inventory to
group indices before a group-level query. No new selector, chemistry model,
backend or dependency is required.

## What is measured and what is assumed

Source inspection finds `mask` on `select` and `get`, but not on either info
entry point. `info` already supports Styler, DataFrame and dictionary results;
its return modes are not expanded here. Runtime regression evidence follows
implementation. No speedup is claimed.

## What was refuted

An atom mask is not a valid universal scope for non-atom queries. The consumer
corrected that claim in #206. Resolving chemistry or converting to a new native
system solely to apply a mask would duplicate existing selection tools.

## Scope and exclusions

Covers basic/native info, shared mask argument digestion, all current summary
element levels, existing result types and documentation. Does not add masks to
other functions or change stored indices, counts, chemistry or coordinates.

## Acceptance criteria

- Omitted/all masks preserve existing values and positional calling conventions.
- Integer, Boolean, expression and empty masks match public select semantics.
- Group masks use group indices; invalid shape/range/type requests fail clearly.
- System counts summarize the masked atom inventory; structure counts remain
  independent.
- File, native and supported multi-form inputs retain their existing routes.
- Native forwarding, docstrings/doctests, User Guide, Cookbook and course agree.
- Focused regression, documentation, dependency and fast gates pass; the
  publication pause remains intact.

## Provenance

2026-10-20, Linux development checkout at `94e579356`, existing Python 3.14
development interpreter. Incoming scope and consumer correction:
uibcdf/molsysmt#206, related to uibcdf/molsysviewer#71.

## Resolution — 2026-10-20

Both public info boundaries accept optional keyword-only mask=None. Existing
positional arguments/defaults and unmasked code paths are retained. Active masks
are resolved once through select with the appropriate source element axis;
shared argument digestion admits the same mask types and expressions. The
consumer still owns atom-to-group conversion. The independent duplicate-mask
defect discovered during this work is repaired in select under
uibcdf/molsysmt#389 rather than hidden in info.

The initial combined selector/summary selection passes 148 cases. The broader
basic suite and native shortcut validation pass 1,075 cases in 98.12 seconds,
with twelve workers and pytest-receptor. Five changed-module doctests pass.
Fourteen fast gates, whole-repository Ruff lint/format, and the public signature
guard pass; its two exact waivers record the intended keyword-only API additions.
The new test module protects all six element levels, system atom summaries,
independent structure counts, repeated/nonmonotonic/empty/Boolean/string scopes,
invalid axes/types/ranges, positional compatibility, trusted delegation, native,
file and complementary inputs, and unchanged source tables/coordinates.

The Toolbox, Foundations, Cookbook and Common Core explain scope axes. Three
self-contained new examples execute in the existing Python 3.14 interpreter,
with actual outputs saved; no auxiliary environment or whole-notebook execution
mark is created. A focused Sphinx project renders the actual public/native
docstrings, selection guide and those three sections without diagnostics.
Existing legacy examples/outputs are not requalified. Two older notebooks move
to schema 4.5 with deterministic missing cell IDs; prior code, outputs, metadata
and existing IDs remain unchanged. The public info return documentation now
accurately distinguishes existing Styler/DataFrame/record modes.

The [receipt](../../devtools/data/info_mask_qualification_20261020.json) retains
counts, versions, warning limits and notebook preservation. This is local source
qualification, not an installed-pair or exact 1.0 candidate admission. The
maintainer's two-day publication postponement and broader #334 pause remain.
