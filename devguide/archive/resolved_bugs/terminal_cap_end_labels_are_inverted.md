---
summary: Terminal cap resources invert their documented peptide-end labels.
issue: uibcdf/molsysmt#547
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [build, attribute]
guard: tests/element/group/terminal_capping/test_terminal_end_semantics.py
normative:
blocked_by: []
supersedes: []
---

# Terminal-cap peptide-end semantics

## What

On main be2f3fb7cb6ac0e52170669edea165166899ad3c, N-terminal predicates return
False for ACE and True for NME/NHE/NH2. Their public help and native builders
already use the peptide-end convention: ACE protects N, the amide caps protect C.
The five new classification/resource assertions fail before the repair.

## How

The two JSON resources are labeled by their cap atom rather than the protected
peptide end. `build.get_missing_bonds` compensates for that inversion when
choosing C/N candidate atoms. Swap the two resource payloads byte for byte and
correct this consumer together. Update template-generation source paths and
provenance, leaving each cap's atoms/bonds and generated coordinates unchanged.

## Why

Public classification contradicts documentation. Changing only predicates or
tables would break bond candidates, so classification and chemical construction
must be received together. This is a name/consumer consistency repair, not a
new cap geometry or preparation model.

## Decision and evidence

Retain the existing public peptide-end meaning. The primary software
[CAMPARI input documentation](https://campari.sourceforge.net/V5/inputfiles.html)
also classifies ACE as N-terminal and NH2/NME as C-terminal. NHE/NH2 have the
same amide atom/bond pattern in the existing local resources. No scientific
algorithm is copied from that reference.

Guard coverage includes all four labels, negative/case-sensitive inputs, every
stored naming variant, source-preserving cap-to-peptide candidates for the three
C-terminal labels, separate chains, template-only systems and a focused template
generator with both methyl-carbon naming conventions. Existing native capping
builders remain in the receiving selection.

## What was refuted

This is not merely a misleading docstring: resource filenames and one consumer
encode the opposite interpretation. A facade-only swap would hide the disagreement.
No evidence requires changing existing cap topology payloads or regenerating
bundled binary systems.

## Scope and acceptance

Make all public cap classifications agree with peptide ends; preserve templates,
candidate bonds, units, source data and caller selections. Update user documentation,
course and generator references; run focused and neighboring tests. No template
coverage expansion or new chemical assignment is included.

## Provenance

Local Linux/Python 3.14.7, unchanged shared environment/backend. Initial command:
`python -m pytest --receptor=llm -n 2 tests/element/group/terminal_capping/test_terminal_end_semantics.py
tests/element/group/amino_acid/test_codes.py tests/element/group/amino_acid/test_name_examples.py`.
The shared initial run has eight failures/861 passes; five failures belong here,
two to #545 and one to #546. Final receiving passes; see below.

## Completed receiving — 2026-11-03

The [shared receipt](../../../devtools/data/group_label_receiving_545_547_20261103.json)
records hashes, original failures, exact source basis and scope. Both resource
payloads exchange paths byte for byte, and bundled ACE/NME coordinate templates
remain byte-identical. Executing the original consumer against the corrected
resources raises ValueError, independently confirming that a data-only repair
is unsafe. The corrected consumer retains the existing geometry/selection rules.

The broader native/group/peptide/sequence/FASTA selection passes **430 cases**,
zero omissions/failures, 103.77 seconds. Its 82 warnings comprise 63 explicitly
unassessed side-chain controls, 14 structural-attribute-drop notices and five
legacy-H5MSM warnings. The final focal guards pass **77 cases**, no warnings,
in 4.09 seconds. They also receive #545/#546; counts are shared, not additive.
The final focus includes four later literal J/X/U/O assertions absent from the
430-case run; runtime code is unchanged between these runs.

Documentation and changed-module doctests pass **570 cases**, zero omissions/
failures, 50.24 seconds. All 530 warnings are retained in the receipt: 514
Sphinx/MyST deprecations, nine legacy warnings, six headless plotting notices
and one intentional structural-drop control. The first documentation run fails
one source-boundary test because the new DDBJ footnote was not cited in text;
adding its in-text reference fixes the failure without suppressing a warning.

All 14 fast gates, Ruff lint/format (4,322 files), 246 public docstrings and
current developer-guide/index checks pass. The four modified notebooks retain
all code cells and stored outputs unchanged. This is source contract and bounded
construction receiving, not an installed-pair or new chemical-profile qualification.
The separately discovered legacy/protonation-label discrepancy remains #549.
Template-helper index-return documentation (#548) and NumPy atom-name container
admission (#550) are independent incoming contracts; they are not certified or
fixed by this peptide-end classification repair.
