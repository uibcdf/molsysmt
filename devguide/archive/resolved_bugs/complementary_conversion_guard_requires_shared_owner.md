---
summary: Correct complementary-conversion guard that requires shared native ownership
issue: uibcdf/molsysmt#409
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [tests, convert]
guard: tests/basic/convert/mult_to_one/test_convert_complementary_h5msm_domains.py::test_full_axes_and_independent_copy_policy
normative:
blocked_by: []
supersedes: []
---

# Complementary conversion ownership guard

## What

The full-axis complementary-conversion test still requires a shared Structures
wrapper for `copy_if_all=False`. The delivered #121 contract instead gives each
MolSys an independent wrapper and weak owner over protected geometry blocks.

## How

Keep the no-redundant-coordinate-allocation intent by asserting shared protected
backing bytes. Require distinct wrappers and correct weak owners. Exercise a
controlled edit, unchanged source coordinates, selective analysis invalidation
and preserved original coverage. This replaces an obsolete identity assertion
with observable allocation and independence requirements.

## Why

The broader #406 source run reproduced this test failure. Restoring one mutable
wrapper shared by two owners would violate the current
[native ownership contract](../../native_copy.md).

## What is measured and what is assumed

The 2026-10-22 source selection executed
`tests/basic/convert/mult_to_one/test_convert_complementary_h5msm_domains.py::test_full_axes_and_independent_copy_policy`
and failed at its shared-wrapper assertion. No runtime copy regression or
performance improvement is inferred from that failure.

The next broader selection also exposed an adjacent stale preparation guard:
`tests/build/add_missing_heavy_atoms/test_domain_preservation.py::test_multiple_chemical_states_fail_before_atom_domain_expansion`
expected evaluated coverage to survive a chemical-state inventory append. The
delivered owner contract invalidates that append. The fixture now checks the
invalidation and explicitly declares its synthetic control after preparing the
multistate input. The rejected repair must then preserve that exact control
handle and evaluated coverage. Merely expecting empty coverage after the failed
repair would weaken its transactionality requirement and was not adopted.

## What was refuted

Wrapper identity is not proof of cheap geometry allocation. Merely removing or
inverting the identity assertion would miss both unwanted coordinate copies and
shared writable ownership; the replacement guard must check both.

## Scope and exclusions

Test correction only. No production conversion/copy change, installed-client
qualification or release authorization.

## Acceptance criteria

The named test passes only with shared protected backing, independent owners and
source-preserving controlled edits. Retain the broader complementary-domain tests.

## Resolution

The revised guard requires distinct wrappers and correct weak owners, shared
protected coordinate bytes and source-preserving edits with independent coverage.
The adjacent heavy-atom guard now declares its valid synthetic control after
inventory preparation and verifies that a rejected repair preserves that exact
handle. Neither fix changes production copying or weakens source independence.
Both pass in the final 125-case focused selection recorded under #406; both also
pass in the last broad source selection. Qualification is source-local, not client
or installed-package acceptance.
