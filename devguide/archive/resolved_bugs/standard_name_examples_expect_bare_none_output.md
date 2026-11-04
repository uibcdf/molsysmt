---
summary: Standard-name examples expect displayed output from bare None returns.
issue: uibcdf/molsysmt#546
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: low
verification: reproduced
area: [docs, attribute]
guard: tests/element/group/amino_acid/test_name_examples.py
normative:
blocked_by: []
supersedes: []
---

# Executing standard-name examples

## What and how

The public amino-acid `get_standard_name` examples correctly describe None for
ALA/HOH but expect its text from bare Python expressions, which display nothing.
The four-example guard fails with two doctest mismatches on main be2f3fb7c.

Receive exactly the two `print(...)` changes and the four-example guard already
proposed in PR #543, head b41810c26c36984a68781e7706f3e933e8589c66. No other addon
change is integrated by this repair. The runtime body and mappings are unchanged.

## Why and scope

Executable native help should show the actual output. Preserve all four examples
and the existing None convention for canonical/unmapped names. The correction
does not turn name lookup into a molecular transformation or change catalogue
membership. It composes with #545 without duplicating its code lookup logic.

## Acceptance and provenance

The real four examples must execute without doctest failures, and public helper
and documentation checks must pass. Local Linux/Python 3.14.7; the shared initial
run recorded in #547's report reproduces this guard failure. Final receiving passes; see below.

## Completed receiving — 2026-11-03

The guard copied from PR #543 executes all four unchanged semantic examples;
the two None cases now use print. The helper runtime body is byte-for-byte
unchanged by this repair. No remaining addon contribution is merged here.
The user tutorial explains the None convention, and its existing printed
examples/code/output remain unchanged.

The final shared focus passes **77 cases**, broader native/sequence receiving
**430**, and documentation/doctests **570**, all without failures or omissions.
Counts, commands, original failures and scope are recorded in the
[cap receiving record](terminal_cap_end_labels_are_inverted.md) and the
[shared receipt](../../../devtools/data/group_label_receiving_545_547_20261103.json).
The first documentation selection's unrelated new citation warning was corrected
and the complete selection rerun. All 14 fast gates and applicable style/docstring
checks pass. Issue closure refers only to native help; PR #543 retains its own
review/integration and exact-head gates.
