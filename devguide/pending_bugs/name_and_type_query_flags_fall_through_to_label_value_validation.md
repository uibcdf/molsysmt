---
summary: Name and type query flags fall through to label-value validation
issue: uibcdf/molsysmt#722
status: active
opened: 2026-11-11
closed:
severity: medium
verification: reproduced
area: [argdigest, digestion, tests]
guard:
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
name/type. Preserve each helper's existing context selection and true label
constructor/setter/converter semantics. This is a host rule defect, not a
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
reproduce the missing Boolean refusal on unchanged helper sources. Thirteen
helpers receive only the missing refusal inside their existing Boolean branch;
an AST comparison proves every other branch unchanged. True labels, optional
builder values and converter bypasses retain their existing tests/semantics.

The final combined cohort passes 377 cases, including all 107 new flag guards,
existing 27 name/type and 81 core digester controls, 64 native queries and the
#719/#720 controls. The inventory constructors now use a scoped supported
ArgDigest registry and native query flag context, rather than interpreting
attribute kwargs as constructor labels/counts. Unknown keywords reject before
scientific work. No ArgDigest provider modification or new minimum API is needed.
All fifteen fast gates and applicable lint/index checks pass; complete HTML and
publication closeout remain pending. Native bytes and physical-unit policy are
unchanged. These are source contracts, not installed or final-pair qualification.
