---
summary: ruff excludes molsysmt/form, so 89 adapters are never linted
issue: uibcdf/molsysmt#170
status: open
opened: 2026-08-18
closed:
severity: medium
verification: reproduced
area: [ci, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: `ruff check molsysmt` returns green over files that do not compile

**Reported:** 2026-08-18, while investigating
[uibcdf/molsysmt#169](https://github.com/uibcdf/molsysmt/issues/169). Twenty-eight
files under `molsysmt/form` failed `ast.parse` and the mandated pre-commit lint
reported success.
**Status:** open, cause identified, not started.

## What

`pyproject.toml` excludes three directories from ruff:

```toml
[tool.ruff]
exclude = [
    "molsysmt/third_party",
    "molsysmt/molecular_dynamics",
    "molsysmt/form",
]
```

`molsysmt/form` holds the 89 form adapters. While 28 of them contained a syntax
error, the command every contributor is told to run before committing said:

```bash
$ ruff check molsysmt
All checks passed!

$ ruff check --no-cache molsysmt
All checks passed!
```

Pointed directly at one of the broken files, ruff finds the error:

```bash
$ ruff check --no-cache molsysmt/form/molsysmt_Topology/to_file_h5msm.py
...
Found 6 errors.
```

The exclusion is not a cache artifact and not a rule-selection issue: the files are
never read.

## How

`pyproject.toml`, `[tool.ruff] exclude`. An excluded path is skipped entirely, so
even `E999` (syntax error) is unreachable there.

The gap is widened by how the package loads. Form adapters are imported lazily —
`molsysmt/form/catalogue.py` reads `form.json` and imports nothing — so
`import molsysmt` succeeds with every adapter broken. The failure only appears when
a form is actually used. Between the linter that will not look and the import that
does not either, a broken adapter can reach a commit unremarked.

## Why

`severity: medium`. No library behaviour is wrong *because of* this; it is a
detector that does not detect. But the surface it fails to cover is the largest and
most mechanically edited in the repository — 89 adapters, routinely modified in
bulk by sweeps — and `AGENTS.md` names `ruff check molsysmt` as the check to run
before committing. A contributor who follows the rule exactly is told the code is
clean when it does not parse.

`molsysmt/third_party` is excluded on the same line and was also touched by the
batch that motivated #169.

## What is measured and what is assumed

Measured, on this checkout:

- 28 files under `molsysmt/form` failed `ast.parse`; 0 elsewhere in `molsysmt/`.
- `ruff check molsysmt` and `ruff check --no-cache molsysmt` both printed
  `All checks passed!` in that state.
- `ruff check --no-cache molsysmt/form/molsysmt_Topology/to_file_h5msm.py` reported
  6 errors.
- `import molsysmt` succeeded in the same state.

Assumed:

- That the exclusions were added to silence style noise in generated or vendored
  adapter code, not to skip syntax checking. The intent is not recorded in the file
  and no commit message explains it — this is a reading of the situation, not a fact.

## What was refuted

*Ruff's cache hid the errors.* No — `--no-cache` gives the same result.

*Ruff does not report syntax errors.* No — it reports six on the same file when the
path is given explicitly.

## Scope and exclusions

Covers whether the three excluded directories should be exempt from **syntax**
checking, which is separable from style checking.

Excludes which style rules should apply to adapter code. That is the question the
exclusion probably meant to answer, and narrowing it to specific rule codes rather
than whole directories is one available fix — but choosing the rule set is a
maintainer decision, not something this report settles.

## Acceptance criteria

- A syntactically invalid file anywhere under `molsysmt/` makes the mandated
  pre-commit lint fail. Whether that is achieved by removing the exclusions, by
  replacing them with per-rule ignores, or by adding a separate compile check
  alongside ruff, is open; any of the three satisfies this.
- A test that introduces a deliberate syntax error under `molsysmt/form` and asserts
  the check fails. Names the `guard` field.

## Dependencies and risks

Removing the exclusions outright will surface a large backlog of style findings in
89 adapters at once, which is why narrowing to specific rules is likely the
practical route. The risk of doing nothing is that the next bulk edit of the
adapters is unlinted, as the last one was.

## Provenance

Host: this development checkout, molsysmt at
`51102b03e`. Python 3.13.14. 2026-08-18.
