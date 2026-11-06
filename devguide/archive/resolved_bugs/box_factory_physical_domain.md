---
summary: Box factory accepts degenerate dimensions and returns nonfinite cells for incompatible angles.
issue: uibcdf/molsysmt#605
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [pbc, molsysviewer]
guard: tests/pbc/get_box_from_lengths_and_angles/test_get_box_from_lengths_and_angles.py
normative:
blocked_by: []
supersedes: []
---

# Box factory accepts degenerate dimensions and returns nonfinite cells for incompatible angles

## What

Box factory accepts degenerate dimensions and returns nonfinite cells for incompatible angles. This native scientific boundary is required by the molecular-tools
work under #421 / PR #543 and uibcdf/molsysviewer#264.

## How

Factory [2,3,4] nm and [10,10,170] degrees returns a matrix with NaN. Zero lengths and [0,90,90] angles return singular matrices; negative lengths are accepted. Orthogonal [2,3,4]/[90,90,90] is a finite determinant-24 control. Public native reproduction: `/tmp/msv-box-domain-probe-20261106.log`, source ed09f6453. This is distinct from #465 default angles and #358 units/documentation.

## Why and acceptance

Define and enforce the public physical domain or provide supported native validation for consumers. Retain valid unit/shared-angle/empty-axis semantics and add scientific invalid-input tests. The GUI cell editor remains required, pending this owner contract; no formula/private scientific helper is copied into the addon.

Native scientific fixes and tests belong to the owning team. This contribution
records the observation and bounded consumer admission, not a native repair.
Owner integration, exact-source/installed qualification and postponed human
acceptance remain separate. Neither 1.0 publication is authorized.

## Owner correction and local receiving — 2026-11-06

The native owner receives this report from PR #543 head
`8ab2f5474b2e04c68d31ef2854a238984b645fc8` and reproduces the public failures on
main `a91a4fd1b748a0f47ad9f5167554cf7ca0f4ae04`. The expanded guard records
49 failures and 29 positive/shape/unit controls passing before the correction,
with six original numerical warnings retained in its JUnit/evidence record.
The same nonphysical inputs also affect the analytical volume helper, and the
shape factory accepts nonpositive/nonfinite edges or anisotropic vectors under
a scalar shape label.

Shared private PBC validation now requires finite positive lengths. Angles in
radians must lie in `(0, pi)`, satisfy strict triangle inequalities and sum to
less than `2*pi`: the positive-Gram domain for three independent vectors.
There is no length-valued epsilon or dependence on presentation units. The box
factory then checks finite entries and a positive diagonal in its canonical
lower-triangular matrix after the existing six-decimal nm rounding. A physical
declaration that collapses at that precision rejects explicitly. A representable
`1e-6 nm` cube remains accepted; a global dimensional determinant cutoff is not
introduced. Raw-vector handedness and wrapping conventions are unchanged.

The shape factory validates one finite positive scalar edge. The unrounded
analytical-volume route reuses the physical declaration checks, retaining its
existing formula and explicit rejection if float64 cannot resolve a finite
positive volume. Existing public signatures, ArgDigest boundaries and Rust
construction kernels remain unchanged. No optional provider or new attribution
boundary is introduced. The shared predicates are internal to supported general
PBC tools, not a new public speculative validator.

All PBC and PBC scientific-truth tests pass: **430 cases**, zero failures/errors/
skips, five retained legacy-format warnings. This includes unit policies,
shared/per-structure angles, empty axes, valid canonical/triclinic matrices and
the new nonphysical/rounding guards. Source inputs are not modified. Public
docstrings, three tutorials, the solvation cookbook and Common Core Module 20
describe the domain/precision boundary without changing notebook code, outputs,
IDs or metadata. Final doctest/governance and source delivery remain pending;
this is not an installed-platform or release qualification.

Evidence uses the existing Linux/Python 3.14.7 development environment,
published Pytest Receptor 1.2.1 and 12 workers. Original and corrected JUnit
records are `.pytest_cache/pre1-review-20261106/605-before.xml` and
`605-receiving.xml`. No environment or compiled backend was changed. The
[execution packet](../../pre_1_0_robustness_audit_20261106.md) remains under #334.

## Owner resolution and final source receiving — 2026-11-06

The completed correction retains the general positive-length/positive-Gram
contract above and the canonical factory's existing six-decimal nm rounding.
The final receiving includes all constructor, empty/shared-angle, volume and
shape controls. Raw cell validation is separately corrected under #619; a
scalar factory's positive diagonal must not be imposed on arbitrary row-vector
inputs. Public signatures and scientific formulas are unchanged.

Implemented in `3eb720444b97f77f9325acf52f55114ece0b5f9e`. The joint native/composition/PBC/
vector/distance/interactions/H5MSM selection passes **5,435 cases**, with zero
failures/errors/skips. The final PBC/docstring/documentation and evidence-runner
profile passes **1,195 cases**, including the final strengthened trajectory
fixtures. The scientific certificate passes **97 cases across 64 registered
nodes**, with zero skips. All **82 Rust unit tests** pass. These scopes overlap
and are local receiving, not installed/platform or release qualification.

The [portable phase-two receipt](../../../devtools/data/pre_1_0_robustness_phase2_receiving_20261106.json)
records exact source/backend identities, original failures, retained warnings,
test chronology and limitations. The initial integrated command used a
nonexistent test path and executed zero cases; it is preserved as unsuccessful
evidence, with the controlled exit-4 diagnostic and corrected-path exit-0 run.
All eight edited notebooks preserve code, outputs, IDs and metadata; only
Markdown changes. Human autosummary edits remain outside these commits.

The native extension is deliberately rebuilt from the delivered Rust sources;
its SHA-256 is `2f1f69f6e0539bd31ee419ec3b7a4deaab20f09045ce3e6504369c9130438525`.
No environment or optional dependency is replaced. Public source verification
and issue synchronization follow this prepared closeout; Viewer graphical
receiving, installed artifacts and the release gate remain separately due.
