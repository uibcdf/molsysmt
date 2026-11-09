---
summary: Contact cutoff equality changes across equivalent length units
issue: uibcdf/molsysmt#666
status: active
opened: 2026-11-09
closed:
severity: high
verification: reproduced
area: [structure, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Equivalent contact cutoffs change a boundary decision

**Status:** Reproduced directly in native get_contacts; scientific correction
and general unit-conversion review remain open.

## What

For points at 0 and 0.5 nm, the documented inclusive contact cutoff returns
True for 0.5 nm but False for 5 angstrom or 500 pm under the nm policy. No
rounding or approximate cutoff rule was requested. Changing active length units
also changes this exact-boundary result. Most ordinary nonboundary inputs are
outside the demonstrated failure; no general detector-invalidity claim is made.

## How

The native threshold digester standardizes the caller quantity. Conversions of
5 angstrom and 500 pm to nm yield 0.49999999999999994 and 0.4999999999999999 in
the received Pint stack. The final inclusive comparison then excludes 0.5 nm.
A direct minimal native probe covers three active policies, four thresholds
(including the immediate float64 predecessor of 0.5 nm), both dense and cell-list
routes, and ordinary/trusted calls. All twenty-four paired observations agree
between ordinary and trusted calls; both native routes reproduce the discrepancy.
No library workaround or fuzzy comparator is selected by this diagnosis.

## Why

Changing the representation or presentation policy for an equivalent physical
cutoff can change a scientific decision at the boundary. The contact panel
cannot repair this by altering the native result or silently widening criteria.
This is a native correctness review and is distinct from the missing facade
routes reported in #665.

## What is measured and what is assumed

[Exact attempts and observations](../../devtools/data/native_contact_unit_boundary_666_20261109.json)
retain the 151-pass/three-failure prototype pilot and the corrected oracle's
152 passes/two genuine native failures in 154 cases. The mass-oracle typo was
corrected to public physchem.get_mass; no threshold assertion changed. The native
probe reproduces without the addon. The isolated local prototype is retained in
`wip/contacts-panel-421-20261109` at `c96d258b9`; it is not published or received
as a graphical capability. No browser run or milestone credit is claimed.

**Assumed, not established:** a general unit-conversion/comparison capability
may be needed. uibcdf/pyunitwizard#143 asks its owner to identify an existing
supported route or the smallest missing capability, while MolSysMT reviews its
own digestion/calculation-unit choices. Ordinary backend IEEE rounding is not
classified as an upstream contract defect merely from these observations.

## What was refuted

The failure is not introduced by the contact panel, a mass-weight calculation,
only the cell-list algorithm, or trusted-validation bypass. A blanket isclose
rule would change the requested scientific threshold and does not establish a
correct fix. A later passing nonboundary case cannot discharge this failure.

## Acceptance criteria

Agree the physical/numerical cutoff contract, preserve caller values/units and
strict adjacent-value controls, and receive a correction through public native
calls with both CPU routes, PBC, supported endpoint/representation modes and
nondefault policies. Report any justified provider capability/floor separately.
Then rerun the complete prototype selection and actual graphical receiving.
Keep original failures and unit/backend/runtime identities. No implicit backend
fallback, policy overwrite, source mutation or per-detector conversion clone.

## Provenance

Linux/Python 3.14; native source efffbaa8f and unchanged Rust. Runtime published
PyUnitWizard 0.28.1, Pint 0.25.3, NumPy 2.4.6. The inspected provider clone is clean
f82b618 and is not the runtime substitution. Owned processes use one CPU, 2 GiB,
no swap and host-reserve monitoring; exact process/resource counters and source
hashes remain in the receiving record. Deliberate tiny-budget test warnings are
separate from host memory pressure.
