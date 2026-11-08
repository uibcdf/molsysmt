---
summary: Reject invalid bare formal-charge values through the public argument boundary.
issue: uibcdf/molsysmt#644
status: active
opened: 2026-11-07
closed:
severity: medium
verification: inspected
area: [basic, argdigest, units]
guard:
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
