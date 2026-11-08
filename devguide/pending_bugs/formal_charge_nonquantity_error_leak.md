---
summary: Reject invalid bare formal-charge values through the public argument boundary.
issue: uibcdf/molsysmt#644
status: active
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [basic, argdigest, units]
guard: tests/basic/test_set_formal_charge.py::test_invalid_nonquantity_charge_has_public_diagnostic_and_no_mutation
normative:
blocked_by: []
supersedes: []
---

# Formal-charge nonquantity diagnostics

## What

DockingMT reports that the public setter with `formal_charge=1.5` raises a
PyUnitWizard NotImplementedFormError instead of MolSysMT ArgumentError. This
blocks its negative contract control; no changed chemical assignment was
observed. Consumer evidence is retained in uibcdf/dockingmt#33 and
uibcdf/dockingmt#49. This is not an established ArgDigest/PyUnitWizard defect.

## How

The component digester accepts integer/nullable-vector branches and then calls
`puw.get_value`/`get_unit` without first recognizing a supported physical
quantity. A bare fractional float can therefore escape into another library's
form-discovery error. Current source inspection matches the consumer's named
mechanism. Local reproduction on this development environment remains due;
consumer Python/provider versions are not relabelled as local qualification.

A minimal public control constructs a one-atom ChemicalStates collection,
appends a state, sets -1, then requests 1.5 and checks the public error and
unchanged stored value. No molecular calculation or external dataset is needed.

## Acceptance and work order

1. Reproduce through `msm.set` on the current source under normal and nondefault
   pm/fs/coulomb policies, within the measured serial resource bound.
2. Reject invalid nonquantity scalar/types at the component's value boundary.
   Preserve argument/caller diagnostics, integer counts, nullable aligned arrays
   and supported genuine charge quantities. Do not truncate fractions or catch
   unrelated backend/configuration errors broadly.
3. Protect source nonmutation, quantity units and caller policy with focused
   public tests. Use existing ArgDigest and SMonitor contracts; add no dependency
   or independent unit interpreter.
4. Publish verified source and hand its actual scope back to DockingMT. Installed
   consumer and release qualification remain separate.

The issue is admitted as incoming pre-1.0 correctness work ahead of the next
composition clarification. It adds no milestone bonus or new scientific method.
#645's explicit hydrogen-policy question is separate.


## Local reproduction and bounded correction — 2026-11-07

On base `f86bd8370`, both normal and pm/fs/coulomb probes reproduce the
PyUnitWizard NotImplementedFormError while preserving the initial count and
caller policy. Current formal-charge getters return integer-count lists; that
observed representation is recorded separately from the consumer's provider.
The final unchanged-code regression baseline has 22 failures and 22 passing
controls. A preceding authoring attempt used the absent root MolSys alias in
two fixtures; those fixture errors are retained separately and corrected to
the existing native imports before the final baseline.

The component now checks `puw.is_quantity` after its existing integer/nullable-
vector branches and before extracting a value/unit. Invalid nonquantities raise
the existing catalog ArgumentError with the argument and caller. Genuine
quantity extraction/conversion still uses PyUnitWizard, with no new exception
catch, count truncation, dependency, reference or backend implementation.

All 44 directed cases pass. They cover unsupported scalar/types, existing array
rejections, Python/NumPy integer counts, nullable ordered assignments, real e/
coulomb quantities, incompatible units, unchanged unit authority, unmasked
backend failures, query flags and evaluated-empty attached analysis preservation.
The final directed process tree peaks at 177,451,008 bytes under the existing
2 GiB/one-CPU/zero-swap execution bound. This is scoped receiving, not full-suite,
installed-client or scientific-model qualification.

The setter docstring/explicit refusal example, Foundations, setter tutorial,
charge recipe and course now state the public contract. The two notebook edits
retain every executable cell, saved output, ID and metadata item. Next: affected
native/adapter/consumer receiving and public doctests, applicable checks, clean
source/publication evidence and the documented owner closeout. #645 remains a
separate policy decision; #612/#334 retain their pending qualification.


Affected native assignment/query, adapter/client and setter-doctest receiving
passes 474 cases without skips/failures/errors, peaking at 414,072,832 bytes.
The [receiving record](../../devtools/data/formal_charge_boundary_receiving_644_20261107.json)
retains all commands, original failures, source hashes and measured execution
limits. Source clean-point, fast gates and public closeout remain due; these
passing scopes do not replace #612's complete suite or consumer qualification.
