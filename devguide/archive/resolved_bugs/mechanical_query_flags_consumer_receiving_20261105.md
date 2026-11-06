---
summary: basic.get rejects the Boolean reader flag for stored constraints.
issue: uibcdf/molsysmt#584
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [basic, argdigest]
guard: tests/basic/get/test_mechanical_query_flags.py
normative:
blocked_by: []
supersedes: []
---

# Reading stored mechanical constraints

## What

After `msm.set(molsys, constraints='none')`, the public query
`msm.get(molsys, constraints=True)` raises ArgumentError instead of returning
the stored policy. The native molecular-mechanics field contains the value.

## How

Reproduced without Viewer on source 8c2661293 and Python 3.14 with bundled
pentalanine extracted to structure 0. The shared constraints digester treats
the get request Boolean as a physical policy value and rejects it. Setter
strings and converter-specific None have different admitted meanings; this
report does not ask for unconditional Boolean policy admission.

## Why

Generic expert readers and future panels need public access to stored physical
settings. No mutation or numerical error was observed. Broader effective-recipe
design is #582; the concrete reader failure requires its own correction. Other
mechanical flags have not been exhaustively audited and are not declared broken.

## Acceptance

Test False/True, mixed queries and the supported get/set/conversion contexts;
sweep related mechanical readers for equivalent semantic collisions. Preserve
physical policy validation and #581 translation without enabling arbitrary
Booleans as model choices. Keep native ownership and avoid an addon getter
workaround. Related: #421 / PR #543 and uibcdf/molsysviewer#264.

## Resolution

The scientific owner delivers reader/value separation in 8e9e3d207, received
through the contribution's merge of native ed09f6453. This preserves the original
consumer report rather than leaving a duplicate open record after the owner's
canonical resolution. The native guard above distinguishes query flags from
stored physical values. The receiving run also passes 128 addon System and
mechanics cases; it is separate from the owner's complete native evidence.
No scientific getter workaround is introduced in the addon. See the
[owner's resolution](basic_get_constraints_reader_flag_is_rejected.md).
