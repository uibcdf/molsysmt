---
summary: Entry mmCIF conversion retains a retired Topology component flag and blocks permutation
issue: uibcdf/molsysmt#617
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/mmcif_PdbxContainers_DataContainer/test_topology_domain_ownership.py
normative:
blocked_by: []
supersedes: []
---

# Retired Topology component flag in entry-mmCIF conversion

## What

Entry-mmCIF construction adds `_components_dirty=False` to pure native Topology,
although state-local components are owned by ChemicalStates. Public atom
permutation then correctly refuses the unexpected Topology extension. This is
reproduced on main c649e8816 with unchanged deposited 1HSG and 1STP inputs while
qualifying #557, and with a two-atom/three-structure synthetic entry.

## How

The sole remaining writer is the entry DataContainer-to-MolSys converter, just
before extraction. The native permutation validator permits only declared
built-in domain fields; its rejection must remain. Remove the obsolete write
at its producer. Existing ChemicalStates component construction, stable molecule
membership, atom axes, bonds and coordinates are unaffected.

## Why

Official CIF/BCIF/native construction should not fabricate an extension that
prevents later general atom-axis operations. Accepting arbitrary extension
fields or discarding metadata in the permutation tool would hide the ownership
error. The fix belongs in the converter, not in CCD template interpretation or
in a weaker permutation validator.

## Measured evidence

Linux/Python 3.14.7, existing development environment, published Pytest Receptor.
The mirrored three-format guard fails before the fix for container, CIF and
BCIF, each at the unexpected legacy field assertion. It then exercises the
public permutation, retained source inventory, exact reversed coordinates and
state-owned connectivity. The broader permutation guard retains its explicit
unknown-extension, metadata, reference, axis and subclass refusals.

## Acceptance and limits

Remove only the retired field write; preserve existing declared conversion data
and strict extension refusal. Execute the new guard, all entry adapter tests and
native permutation regressions. This does not normalize arbitrary legacy objects,
add a Topology component facade, change chemical interpretation or alter API
signatures. Native #557 source/application tests receive this prerequisite fix
without narrowing their permutation cases.

## Resolution — 2026-11-06

The converter no longer writes the retired private Topology flag. The three new
container/CIF/BCIF controls and all entry-adapter/native permutation controls pass:
137 cases, zero failures or omissions. The original three cases fail before
this one-line correction. Strict unsupported-extension and subclass refusals
remain unchanged. Real #557 source permutation and template-application tests
also pass after receiving this prerequisite.

This corrects an existing ownership defect; no chemistry, coordinates, public
signature, dependency, scientific method or runtime extension policy is changed.
