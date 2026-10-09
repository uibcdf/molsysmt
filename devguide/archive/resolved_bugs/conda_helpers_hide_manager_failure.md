---
summary: Conda helpers hide manager failures and split paths with spaces.
issue: uibcdf/molsysmt#351
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [devtools, environment, governance]
guard: devtools/tests/test_conda_env_helpers.py
normative:
blocked_by: []
supersedes: []
---

# Conda helpers hide manager failures and split paths with spaces

**Reported:** 2026-10-09 during the developer-resource review coordinated by
uibcdf/molsyssuite#104.
**Status:** Resolved with checked argument-vector calls and a private-manager guard.

## What

On source `bd81edad5a85e861988cfa87eff50ec53a7c47d3`, both legacy environment
helpers return exit zero after a private manager exits 17. With a manager path
containing spaces, the shell instead tries the first path fragment; the helper
still returns zero. The manager may never execute while the operation looks
successful to its caller.

```bash
python -m pytest --noconftest -o addopts= --receptor=llm -p no:cacheprovider \
  devtools/tests/test_conda_env_helpers.py
```

The regression supplies its own executable, environment input, output receipt,
scratch directory and caller-owned sentinel. It never invokes real Conda/Mamba.

## How

`devtools/conda-envs/create_conda_env.py` and `update_conda_env.py` construct shell
strings, call `subprocess.call(..., shell=True)` and ignore its return code.
Whitespace splits executable, input and environment-name arguments. Ordinary
manager failure also does not reach the CLI outcome.

The repair uses `subprocess.run(argv, check=True)` in each existing route. It
retains Mamba preference, Python/YAML selection, update `--prune` and the managed
create directory. A failed call raises `CalledProcessError`; the CLI reports
failure, while the existing context removes create scratch on exceptional exit.
The helper does not promise to forward the manager's exact numeric exit code.

## Why

Developers and automation need a trustworthy result before relying on an
environment operation. Caller environment and evidence remain caller-owned;
generated input is disposable only after the manager has finished. This is a
developer-tool correction, with no molecular algorithm or runtime API change.

## What is measured and what is assumed

The twelve-case guard combines create via Conda, create via Mamba and update,
manager exits zero/17, and ordinary/space-containing paths and names. Against the
original source, nine cases fail and three ordinary-success controls pass.
After repair all twelve pass. The six existing development-archive checks also
pass: **18 selected local tests**, with scientific conftest disabled.

Executed assertions cover exact manager arguments, YAML Python substitution,
generated input existence during the child, removed create scratch afterwards,
unchanged original YAML, and retained caller prefix/sentinel/receipt. Source
inspection also retains the `temp_cd` finally restoring the caller directory.
Actual solver behavior, supported-manager option changes, OS deletion faults,
Windows/macOS execution and real environment mutation are not measured.

## What was refuted

This is not a solver or dependency-resolution failure: the recording executable
is private and deterministic. Three success controls already pass. The failing
outcome assertion sees helper exit zero after manager exit 17; the path cases
show the shell cannot find the truncated executable. Existing managed scratch
already cleans up on ordinary exits; its ownership is retained rather than
replaced with another temporary-resource abstraction.

## Scope and exclusions

Only the two owner-local legacy manager calls and their regression change.
Standard checked subprocess operations suffice; no shared tool, profile,
dependency, recipe, SDK/policy/guide pin, package or release change is needed.
No scientific suite, real manager, environment installation or package
build/upload/promotion runs. The accepted seven existing workspace findings in
uibcdf/molsyssuite#82 remain separate.

## Acceptance criteria and resolution

`devtools/tests/test_conda_env_helpers.py` is the durable guard: failure must
produce a nonzero helper result, arguments must remain intact, and resource and
caller custody assertions must pass. Nine assertions fail before repair and
all twelve cases pass afterwards, so the guard addresses this failure mechanism.
Affected Ruff lint/format checks pass. Developer-guide validation and exact
hosted administrative evidence are retained with the #104 receiving record.
Scientific/full-suite debt remains with dprada/LMMV and existing nightly/weekly/
manual recovery; administrative validation does not clear that debt or execute
the new regression. The authorized conditional skip avoids launching scientific
work for this developer-only correction.

## Provenance

Linux x86_64; Python 3.14.7 in `molsyssuite@uibcdf_3.14`, 2026-10-09.
The paused temporary root was absent on resume; the original source and test
reproduction were recovered and executed again. No historical cleanup
attribution is inferred from that absence. Primary editable clones and the
shared environment are preserved throughout this review.
