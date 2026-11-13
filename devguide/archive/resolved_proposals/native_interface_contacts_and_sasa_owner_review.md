---
summary: Review native contacts and SASA contracts for BindingMT interfaces
issue: uibcdf/molsysmt#734
status: resolved
opened: 2026-11-12
closed: 2026-11-12
verification: measured
area: [structure, units]
guard: tests/physchem/get_sasa/test_native_interface_handoff.py
normative: devguide/native_interface_contacts_sasa_contract.md
blocked_by: []
supersedes: []
---

# Finite molecular-owner interface review

## What

BindingMT requests a disposition of existing contact/distance calls, source/local
maps, SASA contexts/radius resource and numerical/quantity boundaries. MolSysSuite
#195 coordinates; BindingMT #112 and TopoMT #197 retain their respective owners.
This commissions no new kernel, dependency floor, campaign or release condition.

## How

The [owner contract](../../native_interface_contacts_sasa_contract.md) supplies
explicit Cartesian CPU calls and actual extraction/permutation correspondence.
Sixteen new controls test the specified contact example, inclusive/predecessor
cutoffs, paired-mode distinction, evaluated zero, nonidentity footprints,
structure/state preservation, occlusion environment and independent sphere-cap
losses under nm/ps and pm/fs. A combined 104-case cohort passes without warnings
or omissions, reusing existing meaningful reference and workflow controls. The
earlier 102-case result is retained; two unequal-radius C/H cap controls extend
it without equating both side losses or changing application defaults.
Runtime implementation and native binary are unchanged.

## Why and disposition

The first bundled-element-vdW profile needs no new general decomposition API:
public extraction, permutation/map composition, contacts, distances, radii and
SASA suffice. BindingMT owns its application cutoff, probe/density, numerical
and positive-burial membership policy, result/outcome persistence and actual
client/installed receiving. Radius alternatives and stronger interpretation are
separate profiles, not inferred requirements. The Rose descriptor is not a
coordinate burial API; no defect in it is alleged.

## What was refuted

Native extraction sorts retained source atoms; a raw requested order cannot be
used as its map. A full local permutation supplies the explicit alternate order.
Output selection cannot remove third-body SASA occluders. Equal indices/counts
and atom IDs alone do not establish foreign molecular correspondence.

The first pilot's fourteen setup errors use nonexistent root constructor aliases.
The second has nine failures/five passes from an omitted atom query axis. The
third has eight failures/six passes because ChemicalStates equality compares
identity rather than copied contents. Correcting the fixtures to public native
imports, explicit atom axes and public bond/charge content checks yields fourteen
passes; no runtime repair or weakened numerical expectation is used.

A private combined-run launcher initially tries to fingerprint pytest selectors
as filenames and exits before pytest. Its native/controller failure is retained,
not counted as a scientific test result. Corrected fingerprint paths preserve
the selected controls; all 102 pass.

## Scope, provenance and exit

Linux/Python 3.14.7, existing frozen providers and native 4ffb82e4, one CPU and
1.5 GiB/no own swap with a 6.5-GiB host reserve. The received source is 501e02b40;
the calculation/radius files match the earlier inspected ff25f120 source.
BindingMT's checkout is absent and TopoMT is ahead/behind its remote; both are
preserved. The review uses immutable published owner documents, not mutable
client source or an executed BindingMT installation.

## Resolution — 2026-11-12

The bounded molecular-owner review is complete: the existing public tools
satisfy the restricted first profile without a new operation or runtime change.
The normative contract states the accepted calls and prerequisites; sixteen
new cases distinguish Cartesian from corresponding pairs, exact cutoffs,
nonidentity maps, occlusion environments and independent unequal side losses.
The combined receiving passes 104 cases without warnings or omissions, and
all fifteen common fast gates, indexes and whole-repository Ruff checks pass.
The [receipt](../../../devtools/data/native_interface_handoff_receiving_734_20261112.json)
preserves original draft failures, exact inputs and resource limits. Nine
terminal task-owned units are retired after checking their main PIDs are zero.

Publish the accepted/deferred/gap disposition to #734 and MolSysSuite #195.
This closes only the finite provider review. A favorable owner disposition
does not close central agreement or BindingMT/TopoMT scientific, composed or
installed acceptance obligations.
