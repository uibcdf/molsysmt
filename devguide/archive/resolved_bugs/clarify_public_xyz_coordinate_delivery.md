---
summary: Clarify public XYZ coordinate delivery and default-element behavior
issue: uibcdf/molsysmt#610
status: resolved
opened: 2026-11-06
closed: 2026-11-08
severity: medium
verification: reproduced
area: [docs, form]
guard: tests/form/XYZ/test_public_coordinate_delivery.py
normative:
blocked_by: []
supersedes: []
---

# Public delivery of declared coordinate values

## What and why

DockingMT #80 originally requested coordinates from an XYZ length quantity with
the default `basic.get` element. The system-level route is unsupported and raises
NotWithThisFormError. The quantity already contains the prepared pose; this is
an attribute-level composition problem, not missing molecular chemistry or a
detector failure. The issue preserves the original exact source and receiver
artifacts. DockingMT subsequently received the explicit atom-level route in run
42206087852; those are downstream observations, not newly executed here.

## Supported contract

Keep the existing XYZ system-coordinate refusal. Read with
`msm.get(quantity, element='atom', coordinates=True)` or assign the existing
quantity directly with `msm.set(molsys, structure_indices=0, coordinates=quantity)`.
The latter is preferred when no query is needed. Positional atom correspondence
is declared by the caller; axis shape does not prove molecular identity. Ranks
one, two and three normalize to rank-three query results. Length units, selected
order/repeats, target structure choice and physical values must survive normal
and nondefault application policy. Invalid ranks, bare arrays and nonlength
quantities are not XYZ. No new getter, automatic correspondence or downstream
adapter is needed. Public documentation is in
[the recipe](../../../docs/content/user/cookbook/delivering_coordinates.md),
the XYZ Tool page, basic.get docstring, Module 8 and the maintained
[form contract](../../forms_and_conversions.md).

## Evidence and acceptance — 2026-11-08

An initial directed campaign receives 32 cases with zero failures/skips, including
the public omitted-element refusal, ranks one/two/three, both delivery routes,
nonconsecutive/repeated atom and structure indices, empty structure selection
and existing prepared-system composition. Tests use nm/ps and pm/fs policies;
the original quantity retains its magnitude and Angstrom units. The campaign
peaks at 499,392,512 bytes under the enforced 2 GiB/one-CPU/no-swap cap and
preserves the shared-host reserve. Its 21 warnings are existing legacy H5MSM
and structural-attribute-drop diagnostics, not suppressed. Additional recipe,
invalid-input and clean-source gates remain pending.

No optional dependency, scientific method, unit implementation or public
signature changes. Existing public routes retain ArgDigest, PyUnitWizard and
SMonitor ownership. DepDigest and Ackredit gain no new boundary. Provider-source
tests do not requalify DockingMT's original complete workflow or installed pair.

## Resolution — 2026-11-08

Clean source `d2ce182a46cf247fa466f31606402cf3734ba8d4` passes 89 combined cases,
including twenty new example/axis controls and the changed public getter
doctest; zero skips/failures/errors. Fourteen fast gates and the incremental
HTML build pass on the same source with no changed hashed inputs. Actual
Tool/Cookbook/course HTML content is checked separately from Python execution.
No scientific algorithm or dependency changes. The
[receiving record](../../../devtools/data/public_graph_xyz_receiving_648_610_20261108.json)
retains exact commands, negative controls, authoring mistakes, checksums,
notebook preservation and bounded memory measurements. Broader #378 and
installed/full-source/final-candidate acceptance remain separate.
