---
summary: Clarify the numeric selection axis in native terminal-capping composition.
issue: uibcdf/molsysmt#679
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [build, selection, chemistry]
guard: tests/build/add_missing_terminal_cappings/test_selection_axis.py
normative:
blocked_by: []
supersedes: []
---

# Terminal-capping selection axis

Reproduced without Viewer on native `ca76d93b4`, Python 3.14.7. A native
AlaValPro peptide has forty atoms and three groups. Attaching ACE/NME with
`selection='all'` returns fifty-two atoms and five groups. The equivalent list
of all atom indices raises an out-of-range **group** index error. The explicit
expression `group_index in [0, 1, 2]` returns the same successful result. All
three controls preserve source coordinates; successful native legacy output
retains its `atoms_ff` omission warning. No atomicity defect is inferred.

The composition passes one selection first to group-level heavy completion and
later to atom-level `basic.select`. Numeric positions change meaning between
those calls. The public help does not define that mixed hierarchy clearly.
Choose/document one public axis and resolve internal populations explicitly;
receive lists/arrays/masks versus equivalent expressions, partial groups and
components, ensembles, invalid requests and source preservation. Do not derive
identity from equal counts or names. Generation maps/evidence remain separate
in #558.

The addon consumer under uibcdf/molsysviewer#264/#315 resolves selected atoms
through public `basic.get(..., group_index=True)` and supplies an explicit group
expression to the native function. This is named hierarchy selection, not a
scientific repair or a guessed atom map. Its independent result and reviewed
scene replacement retain native ownership. The expert wrapper is unchanged.
The original native reproduction, full traceback and before/after source hashes
are retained privately with the consumer receiving packet.


## Reproduction and implementation — 2026-11-09

The owner guards reproduce integer-axis rejection, Boolean rejection, untyped
invalid-input errors and empty-selection reconstruction. Resolve atom indices
once on the source and project explicit group populations through local repair;
atom insertion preserves that group axis while reordering atoms. Requested caps
operate on selected covalent components, resolved after repair from those groups.
Never transport the old atom positions through expansion. Native terminal
assessment now inspects whole selected chains before filtering the report, so
an internal selected group cannot become a spurious terminus. Unrelated unknown
chain membership is outside the local context. Public assessment retains its
group-index selection contract, now explicitly documented.

Twenty-eight directed controls pass after an independent #684 component-versus-
molecule defect is repaired. They include masks, syntax-independent numeric
axes, a single internal atom, empty/invalid requests, two structures, alternate
units, multiple components, atom reordering and an actual MDTraj form. Broader
existing tests, public documentation and clean receiving remain due. Initial
fixture assumptions about bound pandas table types and a nonexistent native
get_n_structures convenience method are corrected; these are not provider bugs.


## Resolution — 2026-11-09

Public addition resolves source atoms once and carries explicit groups through atom sorting, then resolves selected covalent components. Empty selection copies without reconstruction, invalid inputs preserve source, local completion is group-scoped and explicit ACE/NME is component-scoped. The public group assessment uses full selected-chain context before filtering. Numeric/expression/mask, two structures, alternate units, multiple components and real MDTraj forms pass. The existing addon audit expectation is corrected and its whole 63-case module passes on unchanged native code.

Clean c643a728f receives 170 expanded placement/repair/writer/doctest controls,
sixteen tiny benchmark/evidence controls, fourteen fast gates and five inspected
HTML pages. Failures remain distinct, including corrected fixture assumptions.
The [core receipt](../../../devtools/data/incoming_core_receiving_677_679_680_684_20261110.json)
and [consumer receipt](../../../devtools/data/terminal_audit_consumer_receiving_679_20261110.json)
retain exact source identities and limits. This adds no weighted milestone bonus
and does not qualify installed/platform/final-candidate or addon GUI behavior.
