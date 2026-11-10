---
summary: Native terminal detection mistakes group ID labels for chemical sequence.
issue: uibcdf/molsysmt#686
status: resolved
opened: 2026-11-09
closed: 2026-11-10
severity: high
verification: reproduced
area: [build, chemistry]
guard: tests/chemical_states/test_get_peptide_termini.py
normative:
blocked_by: []
supersedes: []
---

# Native terminal detection mistakes group ID labels for chemical sequence

**Reported:** 2026-11-09, independent follow-up to the #679 selection correction.
**Status:** Reproduced on public `0c6f9c746`; scientific interpretation and repair
remain pending. This is not another source-selection-axis defect.

## What

Relabelling group IDs changes the group reported to lack C-terminal OXT even
though connectivity, coordinates, atom/group indices and chain membership stay
unchanged. IDs are labels, not positions or a chemical ordering declaration.

```python
import molsysmt as msm

source = msm.build.build_peptide('AlaValPro', engine='MolSysMT')
other = source.copy()
original = msm.build.get_missing_terminal_cappings(source)
msm.set(other, element='group', group_id=['3', '2', '1'])
renamed = msm.build.get_missing_terminal_cappings(other)
assert original == renamed == {2: ['OXT']}
```

Observed: `original == {2: ['OXT']}`, but `renamed == {0: ['OXT']}`.
The final assertion fails. Independent comparisons confirm byte-equivalent
coordinate values and equal stored bond tables before the two assessments.

## How

`build/get_missing_terminal_cappings.py` groups amino acids by chain, converts
`group_id` to integers and sorts them to select an endpoint. Its docstring
explicitly describes this algorithm; the problem is the chemical contract,
not a hidden departure from that prose. Full-chain context from #679 fixes
selection edges but does not make arbitrary labels a chemical sequence.

## Why

The public assessment can report the wrong group after a supported label-only
edit. Native terminal addition consumes that assessment, so later repair may
target the wrong end. That propagation is inspected in source; the measured
counterexample is the read-only assessment, not a claimed corrupt-output run.
This valid-input correctness defect belongs ahead of optional enhancements.

## What is measured and what is assumed

Measured on clean public `0c6f9c746dbd10b02dfe8474a5af280b857ace0d`:
the two different reports above, unchanged bond/coordinate content and unchanged
source files throughout a bounded single-CPU probe. The probe exits 1 at the
intended invariant. Runtime is about four seconds; this is not a performance
benchmark. Hashes of the private raw artifacts follow:

| Artifact | SHA-256 |
| --- | --- |
| `terminal-group-label-probe.json` | `d9335568f813a1d6647c3fbbeadacf1b661fc3b7fb1e219f0fafbefd7fd8f752` |
| `pre1-intake-677-679-680-id-probe.json` | `b46bd3dc28e748a368089f4efa070393e4f1596a4500910bab4fcb3ff35aba17` |
| `pre1-intake-677-679-680-id-probe-bounded.json` | `2864077391181106005e65f1192cbfe791ab16f93f20a0362cc8d1554f4d2e06` |
| `pre1-intake-677-679-680-id-probe.log` | `885698f2e1d5788c60d838aaf0c946542a4a9657cc9f3143bcfadc6ff2a1bd4e` |

## What was refuted

- This does not arise from numeric atom-versus-group selection or from a
  truncated selected chain: both calls assess the whole same chain.
- Coordinates, chemistry and chain membership do not change in the control.
- Requiring numeric or monotonically increasing ID labels would evade the
  invariant instead of fixing chemical terminal recognition.

## Scope and exclusions

Review native chemical-terminus recognition and its terminal-completion
consumers. Do not infer arbitrary peptide chemistry from matching labels,
invent sequence order for a branched/cyclic/unknown system, or introduce a
second chemical store in Topology. Reuse or extend state-dependent connectivity
tools in `chemical_states` if a reusable recognition operation is required.
No proposed implementation is selected by this report.

## Acceptance criteria

- The same declared peptide chemistry has the same terminal groups under
  arbitrary numeric, nonnumeric and permuted group ID labels.
- Reordered atom/group inventories and multiple chains preserve source maps.
- Explicitly incomplete, branched, cyclic, capped or ambiguous chemistry is
  handled by a documented scientifically defensible rule or a clear refusal;
  selection edges never become chemical termini.
- Assessment and addition agree on endpoint identity, preserve unrelated
  populations, and have a failing-before/passing-after public regression.
- Public documentation explains the recognition rule and limits; #679/#684
  selection/component controls remain passing.

## Provenance

Linux x86_64 shared development host, Python 3.14.7, existing development
environment and published PyUnitWizard 0.28.1 overlay. No installation, native
rebuild or source edit during the probe. One CPU, 2 GiB own-memory cap, no own
swap and host availability monitoring; no own OOM or reserve stop. No claim of
installed-package, other-platform or complete terminal-science qualification.

## Implementation under receiving — 2026-11-10

The public experimental `chemical_states.get_peptide_termini` now owns the shared observed-backbone rule. Terminal assessment, free N-side completion and explicit cap anchors delegate to it. Initial controls retain the original four label/cap/cycle failures. The first implementation exposed legacy two-column bond tables, an internal local-name shadow and fixture/converter keyword mistakes; these attempts remain recorded. Expanded state/form/group-permutation/H5MSM receiving and public documentation are still pending acceptance. No issue closure or milestone credit is claimed yet.

## Incomplete real source and explicit partial mode — 2026-11-10

The 1BRS source has one path in chains 0/1/2/5, but Barstar chains 3 and 4 each have two stored backbone fragments. Chain 3 has starts 326/389 and ends 388/412; chain 4 starts 413/475 and ends 474/498. Both jumps span source labels 63 to 66, and no ordered native chain declaration is stored. Relabelling those labels cannot supply missing chemical evidence. The old OXT-at-412 assertion used a sequence-label heuristic, not a stored-graph oracle.

The public recognizer defaults to a strict error. Explicit `on_ambiguous="report"` retains unassessed chains with reasons and no invented endpoints; other chains remain assessed. The legacy dictionary and local adder use that explicit mode and emit catalog warning MSM-WARN-BUILD-003 for every omitted chain. The native 1BRS adder therefore repairs four supported heavy atoms (5151 to 5155) without placing uncertain OXT, while PDBFixer retains its independent 5230-atom/6-OXT profile. Tests retain those independent observations and assert partial coverage instead of assuming algorithm parity. This does not silently interpret gaps as free fragment ends or weaken the new strict recognizer.

## Resolution and receiving — 2026-11-10

Native/addon source receiving on clean 68954e6aa passes 342 affected/route/inventory cases. Final clean b59ce29d5 passes 110 scientific cases over 71 registered nodes, including three newly declared analytical graph oracles; native/addon/docs and existing affected-test bytes match the earlier receiving exactly. Fourteen fast gates and six inspected HTML pages pass on f8c516abb, with identical product/docs bytes; six unchanged title-underline warnings remain. Both affected tutorial notebooks actually execute their seventeen code cells, plus private source/interpreter identity probes. Source warnings, failed iterations and the explicit 1BRS scope change remain in the [receiving record](../../../devtools/data/peptide_termini_receiving_686_20261110.json). This closes the label-dependent native endpoint defect, not completeness/protonation, general PDBFixer selection behavior or release qualification.
