---
summary: Name and type query flags fall through to label-value validation
issue: uibcdf/molsysmt#722
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [argdigest, digestion, tests]
guard: tests/_private/argdigest/test_query_label_flags.py
normative:
blocked_by: []
supersedes: []
---

# Rejecting label values in Boolean query contexts

## What

The #720 pilot accepts atom_name='yes' instead of rejecting a non-Boolean query
flag. Native get reuses the same value rule. This can silently treat a label
value as a True request. The provider executes the host digester as written.

## How

In thirteen reviewed name/type digesters, the Boolean context returns valid
bool values, but invalid values fall through to the ordinary label branches.
Cover atom name/type/force-field type and group/component/chain/molecule/entity
name/type. Preserve true label constructor/setter/converter semantics while
recognizing the existing get, compare and public Iterator query boundaries. This is a host rule defect, not a
confirmed ArgDigest provider limitation.

## Why

A query flag is a Boolean declaration, not a label assignment or a filter.
Use the existing ArgumentError through the owning digester, with no new
exception or duplicated provider-side normalization. The native inventory
iterator also needs a scoped attribute-domain contract using the existing
ArgDigest registry, rather than constructor label/count interpretation for
query kwargs. Its traversal repair remains owned by #720.

## Acceptance and scope

Reproduce invalid label values and retain actual Boolean positives across the
reviewed family. Test real native/universal get and compare, plus the existing
ordinary-label and builder/converter controls. Keep optionality and physical
quantity policies unchanged. Preserve failed pilots and before/after input
identity; do not equate adapter imports with engine execution. No scientific
algorithm, native backend, public provider floor or release scope changes.

## Provenance

2026-11-11, shared Linux/Python 3.14 development source. The actual #720 pilot
exposes the first defect; family inventory starts as source inspection pending
bounded baseline receiving. Existing reviewed support overlays and qualified
native bytes are retained; final qualification remains separate.

## Bounded source receiving

The 107-case family baseline has 56 failures and 51 passing controls. Two public
get probes originally omitted element='atom' and failed at a later missing
system getter; preserve that scope. The corrected three public probes all
reproduce the missing Boolean refusal on unchanged helper sources. The
first-stage thirteen-helper fix adds the missing refusal inside each existing
Boolean branch; an AST comparison proves every other branch unchanged
for that stage (`b0ae02b22`). True labels, optional
builder values and converter bypasses retain their existing tests/semantics.

The first combined cohort passes 377 cases, including all 107 new flag guards,
existing 27 name/type and 81 core digester controls, 64 native queries and the
#719/#720 controls. The inventory constructors now use a scoped supported
ArgDigest registry and native query flag context, rather than interpreting
attribute kwargs as constructor labels/counts. Unknown keywords reject before
scientific work. No ArgDigest provider modification or new minimum API is needed.
All fifteen first-stage fast gates and applicable lint/index checks pass.
Complete strict HTML on clean b0ae02b22 has zero warnings; the later private
Boolean-context predicates have separate focused receiving. Native bytes and
physical-unit policy are unchanged. These are source contracts, not installed or final-pair qualification.


## Boolean-context receiving

An additional positive-control matrix exposes 24 rejected valid booleans out
of 78 get/compare/Iterator calls on the first-stage source. Nine helpers lacked
one or more existing query contexts. Their predicates now recognize those
boundaries, including the public Iterator constructor, while retaining the
separate label and chemical-assignment branches. The first-stage AST proof
does not claim that these later predicate corrections were already present.

The final focused cohort passes 526 cases with zero skips: 319 flag cases,
27 existing name/type controls, 81 core digester cases, 64 native queries and
35 inventory cases. Invalid values and actual Boolean positives cover all
three query callers; four end-to-end cases check values through public get,
compare and inventory traversal for atoms/groups/molecules/entities. The
preceding attempt has 525 passes and one failed new expectation: the fixture's
entity is labelled peptide, not protein. That test-oracle correction and the
original failure are retained. These overlapping cohorts are not added as
independent coverage credit. Complete-source, installed and final-pair gates
remain separate.


## Resolution

The implementation and maintained examples are received at b0ae02b22, with
Boolean-context corrections at 4280a8d42. The [shared receipt](../../../devtools/data/native_inventory_receiving_719_720_722_20261111.json)
owns exact inputs, overlapping counts, failed probes, runtime/native identity,
resource limits and documentation scope. The addressable guard above checks
actual behavior: declared capability and live example execution (#719), source
positions/traversal and retained chunks (#720), or accepted/rejected flag values
plus public query results (#722). It cannot pass merely by matching a table's
format or silently skipping an unavailable path.

This closes these bounded defects, not the wider #378 review, #615/#713
causality, client memory campaign or installed/final-candidate acceptance. No
release/publication action or extra formal scorecard credit is implied.
