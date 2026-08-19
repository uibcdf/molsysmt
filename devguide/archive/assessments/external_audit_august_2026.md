# External Audit — 19 August 2026

> **Document role:** Assessment. This is a dated snapshot taken at repository commit
> `b9a2098e4`. Every count, ratio and outcome below is an observation on that commit in
> the environment recorded at the end; none of it is normative, and none of it stays
> current by itself. The defects it found are tracked as issues, and those entries — not
> this page — carry the analysis and the state.

## What this was

An audit conducted from one vantage point: a reader who has just received the MolSysMT
methods paper, opens the repository for the first time, and checks whether it supports
what the paper will claim. Nothing was assumed from the developer guide. Claims were
taken from `README.md` and from the generated registries, and then run.

The method was: measure, then read. Every number here has the command that produced it,
in this document or in the entry it points to.

## The finding that frames the rest

**There is no paper.** `paper/main.tex` is the 2020 *Bioinformatics* template with its
placeholders in place: the abstract reads `\textbf{Summary:} Bla, bla, bla.`, the
Introduction and Implementation sections read `Text Text Text`, and the notes are in
Spanish inside the `.tex`.

So `README.md` is currently the paper. That is the reason five of the eight entries
opened by this audit are about the public presentation surface rather than about the
code: the code is in better shape than the page that describes it, and the page is what a
referee reads.

## What was verified and holds

This section exists because an audit that reports only defects misrepresents what it
looked at. Each item was run, not read.

**The form claims are exact.** `README.md` states 89 forms in a 75 / 3 / 11 tier split.
`molsysmt/_private/form_tier.py` classifies exactly 89 forms, 75 Tier 1, 3 Tier 2, 11
Tier 3. No rounding, no stale count.

**The numerics agree with an independent implementation.** Minimum-image distances over
a 5000-structure triclinic pentaalanine trajectory, four atom pairs, against MDTraj
computed from the same file: maximum absolute difference `1.55e-07` nm. The same call ran
in 0.212 s against MDTraj's 0.287 s.

**The stability contract is honest.** `devtools/data/public_api_stability.json`
classifies 123 symbols `stable`, 57 `experimental`, 9 `outside-contract`. The audit
looked for surfaces classified more favourably than the evidence supports and found the
opposite: `build`, `hbonds`, `get_sasa`, `get_secondary_structure` and `get_rmsf` are all
correctly marked experimental. The problem is that the README does not repeat this
(#186), not that the registry overstates.

**The scientific-evidence design is the strongest thing in the repository.**
`tests/scientific_truth/README.md` separates analytic, external and metamorphic evidence
and states that cross-form agreement is parity, not truth, unless one side is
independently established. Rule 5 forbids deriving an expected value from a MolSysMT path
that shares the implementation under test. `scientific_evidence_matrix.md` reports 43
stable APIs, 43 validated, 0 partial, 0 gaps, and a cross-check confirmed that no stable
compute symbol is missing from it.

**Conversion fidelity is audited rather than assumed.** `msm.convert(..., return_report=True)`
returns a `ConversionReport` with `outcome='lossy'` and a per-attribute issue list naming
what the destination form cannot represent. The audit found no comparable facility in the
tools MolSysMT interoperates with.

**Lazy loading works.** `import molsysmt` completes in 0.37 s despite 2,565 modules in
the package.

**Errors name the cause and the remedy.** A misspelled selection field returns
`ArgumentError: The selection could not be parsed with the 'MolSysMT' syntax: name
'atom_nme' is not defined`, with documentation and issue links appended.

**The lint gate is clean.** `ruff check molsysmt` passes on the project's configured
ruleset.

**Governance beyond the norm.** A machine-readable stability registry, a form support-tier
protocol, a twelve-validator release gate, a normative reporting protocol enforced by
`validate_devguide.py`, generated queue indexes, a deprecation policy, and a document
policy that distinguishes *Implemented*, *Contract-tested*, *Parity-tested*,
*Scientifically validated* and *Benchmarked* and forbids using them interchangeably.
Filing the eight entries below through that machinery, rather than around it, was
frictionless — which is the strongest thing that can be said about a process.

Two figures are quoted here as dated observations and are **not current**: 4,834 test
functions under `tests/`, and 80.9% line / 68.6% branch coverage recorded in
`devtools/tests/coverage.json`, whose timestamp is 2026-03-27.

## What was found

Eight entries, each with its own document and issue. The analysis lives there.

| # | Entry | Severity |
|---|---|---|
| [#182](https://github.com/uibcdf/molsysmt/issues/182) | A truncated demo artifact reached `main` because no push-path gate checks bundled data | high, scientific-integrity |
| [#183](https://github.com/uibcdf/molsysmt/issues/183) | `gc.collect()` in public structure functions costs 40x the computation | high |
| [#185](https://github.com/uibcdf/molsysmt/issues/185) | No test workflow runs on a push to `main`, and the CI badge names a missing workflow | high |
| [#184](https://github.com/uibcdf/molsysmt/issues/184) | `solvate` rejects multi-structure systems with an internal merge error | medium |
| [#186](https://github.com/uibcdf/molsysmt/issues/186) | The README presents experimental surfaces as headline capabilities | medium |
| [#187](https://github.com/uibcdf/molsysmt/issues/187) | Stable public docstrings describe parameters with autogenerated placeholders | medium |
| [#188](https://github.com/uibcdf/molsysmt/issues/188) | `supported.forms()` and `info()` return only styled tables | proposal |
| [#189](https://github.com/uibcdf/molsysmt/issues/189) | The generated form layer is 84% of the codebase | proposal |

Three of them compose into one story and are worth reading in that order: **#185** is why
nothing tested the commit, **#182** is what got through, and the shipped artifact is the
cost. The gate that catches #182 exists, is correct, and had not been asked.

**#183 is the one that changes a paper claim.** The README offers precompiled kernels
with no warm-up. Both halves are true and neither reaches the user: `get_center` spends
191.8 ms, of which 4.3 ms is the work. The project's own competitor baseline from
2026-05-22 recorded `center_molsysmt_public` at 0.280 s against `center_molsysmt_jit` at
0.0082 s and `center_mdtraj` at 0.0016 s. The measurement existed for three months and
was read as public-API overhead in general. It is one call, repeated 37 times across the
package.

## Findings already tracked, not re-filed

**Repository weight.** `.git` is 563 MB and the working tree carries 428 MB of `docs/`,
of which 319 MB is 49 files under `docs/_static/views`. A reader cloning from the paper
downloads roughly a gigabyte. The theme is
[`../../pending_proposals/git_history_bloat_cleanup.md`](../../pending_proposals/git_history_bloat_cleanup.md),
whose 2026-07-07 diagnosis measured `.git` at 439 MB and attributed the bloat to binary
molecular-data assets rather than to web artifacts. Both halves of that have moved: the
total is up 124 MB, and the largest current working-tree contributor is regenerated
documentation HTML.

**The weekly suite is red.** `ci-weekly.yaml` failed on 2026-08-03 and 2026-08-10 in
`Setup conda env` and on 2026-08-17 with three cross-repo unit-policy failures on all
three Python versions, 9,989 passing. The failure itself belongs to
[`../../pending_proposals/pyunitwizard_global_standards_conflict.md`](../../pending_proposals/pyunitwizard_global_standards_conflict.md);
that it is the only automatic signal and has been red for three weeks is recorded in #185.

**The Sphinx warning population.** Confirmed still open as
[`../../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md`](../../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md);
not re-measured here.

## What the audit got wrong

Recorded because the corrections changed the fixes, and because a report that only lists
what it found right is not evidence of anything.

**"No guard existed for the truncated artifact."** Wrong. `validate_demo_assets.py`
encodes the expectation in `molsysmt/data/demo_manifest.json` and fails with the exact
file and the exact numbers. The defect is *when* it runs, not whether it exists — and the
right fix is to run the check the project already has, not to add one. The issue was
retitled before its document was written.

**"No CI runs at all."** Wrong. `Ruff` and `Developer guide integrity` run on nearly
every push and pass, `CI smoke` ran on the 2026-08-12 to 08-17 commits that omitted
`[skip ci]`, and the weekly job runs the full suite plus the scientific-truth gate. The
accurate statement is narrower and worse: the test signal is opt-out by default, and the
default is exercised on 107 of the last 109 commits.

**A miscount of `[skip ci]` commits.** The first measurement counted matching *lines*
from `git log --pretty=%s%b`, not commits. Re-measured per commit, the figure was
unchanged at 100 of the last 100 — but the method was wrong and would not have been
noticed if it had agreed less exactly.

**"90 of 278 tool notebooks render as empty pages."** Withdrawn. `nb_execution_mode` is
`off` and 90 notebooks carry no stored outputs, but those pages are Markdown reference
tables with no code to execute. The concern was retracted before it was written down
anywhere but here.

## The assessment

The engineering and the governance are in the top decile of published scientific
software, and the validation design is better than that. What is missing is the last mile
that turns the work into a citable artifact: a manuscript, a test signal connected to the
act of committing, and a front page that repeats the project's own stability
classification instead of contradicting it by omission.

The four concrete defects are days of work. What is not days of work, and should be said
in the paper rather than discovered by a referee, is that 84% of the codebase is a
materialised adapter matrix (#189) and that 2,902 of 2,990 commits are by one author.
Neither is a defect. Both are load-bearing facts about what a reader is being asked to
adopt.

## Provenance

Conducted 2026-08-19 at repository commit `b9a2098e4` on Linux 7.0.0-28-generic x86_64,
20-core Intel Xeon E5-2630 v4, Python 3.13.14, MolSysMT `0.21.0+325.g7cedab74a`, NumPy
2.4.6, pandas 2.3.3, mdtraj 1.11.1, MDAnalysis 2.10.0, with OpenMM available. GitHub
Actions history read through `gh` on the same date; run identifiers are recorded in the
entries so the outcomes stay checkable after the history scrolls.
