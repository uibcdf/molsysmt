---
summary: Course minimization examples discard independent results and pass an unsupported keyword.
issue: uibcdf/molsysmt#562
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [api, docs, tests, units]
guard: tests/molecular_mechanics/potential_energy_minimization/test_potential_energy_minimization.py
normative:
blocked_by: []
supersedes: []
---

# Course minimization result ownership

## What

All four Path Module 43 notebooks discard the default independent result;
Alzheimer/Enzyme also pass an unavailable tolerance keyword. Alzheimer Module 54
has the same result-ownership error. Later energy/view operations retain the
unminimized input while prose claims relaxation and sometimes physical stability.

## How

Source 1b359d441b899d26a06a6d927b809f770a09c462, Linux/Python
3.14.7/OpenMM 8.6.1. An executable guard parses each actual minimizer statement,
binds it to the public signature and runs it on bundled alanine dipeptide rather
than executing downloads or unqualified ligand/membrane preparation. All five
lesson cases fail: two unknown keywords and three unchanged continuation systems.
The four native CPU/Reference independent/in-place controls pass. Final red
result: 5 failed, 4 passed, exit 1, 5.48 s.

The preceding minimization test filename did not match pytest discovery. Recover
its energy-decrease purpose under a collected test filename with a bounded
fixture, without coupling a minimizer guard to hydrogen preparation/downloads.

## Why and acceptance

Rebind each lesson's continuing molecular-system variable to its independent
result. Preserve native in_place=True / None-return semantics in explicit tests.
Retain supported signatures and do not add tolerance or iteration knobs to make
legacy prose appear valid. Verify real coordinate displacement and finite energy
decrease for the bounded fixture, exact source preservation in independent mode,
noncanonical energy units and unit-policy preservation. The lesson guard must
fail an unused/forgotten result, not merely recognize assignment syntax.

Correct nearest/global-minimum, equilibrium and guaranteed-stability statements;
describe the implemented L-BFGS local optimization and its engine defaults.
Retain biological scenarios and anchors. Native model preparation, force-field
coverage and spatial assembly are prerequisites, not products of minimization.

## Scope and separate findings

The five course notebooks currently have no executed outputs. Do not fabricate
them by substituting bundled-system outputs for the biological preparations.
Execute the actual minimizer statements on a bounded input and the independent
Toolbox tutorial; qualify full scenarios separately. No runtime optimizer or
public signature is changed here. Existing engine Context independence is a
separate reproduced defect, uibcdf/molsysmt#588.

## Resolution and receiving — 2026-11-05

**Contract-tested / bounded execution.** The five lesson calls now retain their
independent result in the same continuing molecular-system variable. The four
Module 43 lessons also retain an original-system alias for before/after work and
select a single structure explicitly. No unnecessary copy is required to retain
that original in the native independent mode. Downstream energy/view references
receive the minimized result. The unavailable tolerance arguments are removed;
no tolerance, iteration counter or other public keyword has been introduced.

All biological scenarios, notebook anchors, original code-cell counts and
execution payloads are preserved. Scientific prose now identifies local L-BFGS
optimization and appropriate preparation/model prerequisites. It no longer
promises the nearest/global minimum, guaranteed force cancellation, equilibrium,
a universal energy/RMSD change or physical/binding stability. Challenges inspect
model-dependent changes instead of relying on invented stopping controls.
The engine's own defaults/constraint behavior are the basis, inspected at
[the primary OpenMM header](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/openmmapi/include/openmm/LocalEnergyMinimizer.h).

The executable optimizer AST and decorators are identical to the source base
after docstrings are excluded. Docstrings, Foundations, Toolbox, Cookbook and
relevant course lessons describe the same native ownership and unit behavior.
The existing engine-context exception is explicitly disclosed, not silently
repaired or relabeled as native success. No dependency floor, schema, compiled
kernel, scientific criterion or Ackredit event is changed by this correction.

### Guards and evidence

The former minimization test's filename was not collected by pytest. Its energy
reduction intent is recovered in the standard test filename using a small
bundled native fixture, separated from hydrogen preparation/downloads. Four
ordinary calls cover CPU/Reference and independent/in-place modes under an
angstrom/kcal unit policy. Controls require finite physical energies, a genuine
energy decrease, coordinate change greater than 1e-5 nm in this fixture, exact
stored-source preservation for independent output, in-place None return and
unit-policy preservation.

Five additional guards parse and bind the actual lesson minimizer statements,
then execute those statements with a bundled native system. They require the
continuing lesson variable to contain genuinely changed coordinates and lower
energy, and verify the later energy/view references. A discarded result or an
unused assignment cannot satisfy those conditions. The guard executes neither
the network preparation cells nor a viewer scene.

Final local receiving passes:

- 259 affected mechanics/digester tests, exit 0, 14.91 s.
- 29 cases with published support floors, exit 0, 9.63 s; runtime SMonitor stays
  active while its unrelated editable pytest entry point is excluded under #524.
- 569 documentation/governance/doctest cases, exit 0, 18.92 s.
- Focused nine-case ownership/course guard plus the function doctest, 10 passed,
  exit 0, 6.00 s.
- Executed five-cell Trp-Cage Toolbox tutorial, 11.4 s, demonstrating both modes.

Suites overlap. The documented native energies and coordinate changes are
bounded contract controls, not a scientific validation of every force field or
preparation protocol. Full downloaded protein/ligand/membrane scenarios remain
unqualified. Those five course sources already had no executed outputs, and no
bundled outputs are inserted in their place. The existing Cookbook executable
cells, outputs and metadata are unchanged. A new tutorial Markdown cell receives
an explicit schema ID after the schema guard correctly rejected the initial
missing ID; the final guard passes without reader-side repair.

### Corrected test assumptions and separate defects

A preliminary test used a top-level class alias not exported by the current
native API; it now checks the actual input class. Another compared nanometer
numbers obtained through different session-unit round trips bitwise; the source
ownership control now checks stored native coordinates exactly and continues
checking actual returned units and all policy fields except lazy backend
inventory. Coordinate-change assertions use a physical threshold rather than
accepting mere floating-point representation changes. These are test repairs,
not runtime/data changes to force a passing result.

Two independent findings have their own open reports: #588, source mutation
before existing Context/Simulation independent-copy failure, and #589, the final
project's incorrect two-selection reference buried-area call. The latter remains
visibly qualified in the project source. Correcting the minimizer statement does
not claim the entire project runs or proves binding. Neither finding is hidden
by an expected-failure marker or a release waiver.

[The receiving receipt](../../../devtools/data/course_minimization_receiving_562_20261105.json)
records commands, hashes, versions, preserved payloads and separate bug evidence.
Hosted, installed/platform and release qualification remain separate. Continue
with the source-ownership defect and #583/#584; PR #543 receiving and #587 remain
independent work. No tag, Release, promotion or new release matrix is launched.
