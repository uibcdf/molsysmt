<!--
SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.
Canonical source: https://github.com/uibcdf/pytest-receptor/blob/main/standards/PYTEST_RECEPTOR_GUIDE.md
Report changes in: https://github.com/uibcdf/pytest-receptor/issues
-->

# Pytest Receptor consumer guide

Pytest Receptor is a pytest plugin that renders the same test session for a human, a
coding agent, or a CI log without changing the session's outcome. MolSysSuite consumers
use it to keep development output compact while retaining pytest's exit status, counts,
failure evidence, warnings, skips, and actionable rerun commands.

This file is the integration contract for repositories that use Pytest Receptor. Detailed
option and artifact references remain in the
[`uibcdf/pytest-receptor`](https://github.com/uibcdf/pytest-receptor) documentation.

## Required consumer behavior

1. Declare `pytest-receptor` in the development or test environment that invokes it. Do
   not make it a runtime dependency unless the shipped product itself runs pytest.
2. Use `--receptor=llm` for a local coding agent that can read the checkout after the run,
   and `--receptor=ci` for an ephemeral hosted log. Plain pytest remains unchanged because
   `--receptor=human` is the default and registers no receptor plugin.
3. Use the command's exit status as the result. Never infer success from a word, a missing
   section, an artifact, or a truncated log.
4. Do not combine a compact profile with `--tb=line` or `--tb=no`; those options discard
   traceback structure before the receptor can render it. `-q` and `--no-header` are
   redundant but harmless.
5. Keep the repository's ordinary test selection, coverage, JUnit, xdist, and other
   required gates. Pytest Receptor changes presentation, not which tests constitute the
   gate.
6. If the project invokes pytest through `python -m pytest`, `uv run pytest`, or another
   wrapper, set `receptor_rerun_command` so printed `rerun:` commands work verbatim.
7. Treat unexpected suppression, misleading grouping, missing actionable evidence, or any
   disagreement with native pytest as a provider issue. Do not silently normalize it in
   every consumer.

Installation alone changes nothing. Add the package through the repository's normal
development dependency route; for an isolated environment the published forms are:

```bash
conda install -c uibcdf pytest-receptor
pip install pytest-receptor
```

## Choosing a profile

```bash
pytest                         # unchanged native pytest
pytest --receptor=llm          # local agent; compact with recoverable overflow
pytest --receptor=ci           # hosted log; all causes retained inline
pytest --receptor=human        # explicit native-pytest passthrough
```

Use `llm` when the reader shares the filesystem. It may hold back detail only when a run
spreads across more than ten distinct root causes, in which case it points to
`.pytest_cache/d/receptor/last-run.txt`. The previous report is removed when the next run
starts, and no report is available when pytest's cache provider is disabled.

Use `ci` when the runner will disappear and its log is the durable evidence. It does not
hold back root causes or print an unreachable local report path. It may be combined with
the repository's required JUnit or structured artifact output.

Use `human`, or omit `--receptor`, when a person needs pytest's native terminal format or
when diagnosing an interaction involving the receptor itself. `human` is a true
passthrough, not a more verbose compact profile.

Both compact profiles support xdist. For example:

```bash
python -m pytest --receptor=llm -n 12 tests/
```

Long runs emit at most five progress lines on stderr after a silent warm-up. Progress is a
pace signal, not a hang detector: a stuck test cannot emit a completion threshold.

## Exit status and authority

Pytest Receptor never changes pytest's exit status. Its first compact line refines that
numeric result with labels such as `PASS`, `FAIL`, `COLLECTION_ERROR`, `USAGE_ERROR`, or
`NO_TESTS`, but the process status remains authoritative. A receptor rendering failure is
reported as `RECEPTOR_ERROR` while preserving pytest's status and making native evidence
available.

CI must therefore run the command directly under the shell's normal failure handling. Do
not pipe it through a command that hides the status, grep for a verdict, or declare a job
successful because an artifact exists. A failed test run may produce a complete artifact;
artifact completeness and test success are separate facts.

## Evidence artifacts

The compact text is normally enough. When a consumer needs structured evidence, opt in to
the versioned JSONL stream:

```bash
mkdir -p .pytest-receptor
pytest --receptor=ci --receptor-events=.pytest-receptor/events.jsonl
```

`--receptor-events=PATH` requires `llm` or `ci`, and its destination directory must already
exist. The stream uses schema `pytest-receptor.events@1`, is bounded to 50 MiB by default,
and finalizes with outcome, counts, completeness, integrity digest, and any declared
evidence truncation. Read it through the supported API rather than ad hoc line parsing:

```python
from pytest_receptor import read_artifact

artifact = read_artifact(".pytest-receptor/events.jsonl")
if artifact.complete:
    outcome = artifact.final.data["outcome"]
```

The plugin creates artifacts owner-only and refuses symlink destinations, but redaction is
only a conservative safety net. Tests can emit arbitrary sensitive values. Choose the
path, upload policy, visibility, and retention accordingly; Pytest Receptor performs no
network upload and no cleanup.

An absent or incomplete `session_finish` means incomplete evidence, not a failed or passed
session. Preserve the command's exit status and use native CI records such as JUnit when
they are part of the repository's required gate.

## When to use native pytest

Repeat the same selection without a compact profile when:

- the receptor and pytest disagree about exit status, outcome, counts, or completeness;
- `RECEPTOR_ERROR` appears or the plugin itself is being diagnosed;
- a third-party pytest plugin's required report appears to be missing or altered;
- the compact report is not sufficient to act and its referenced full report does not
  resolve the question; or
- an untested plugin combination or terminal interaction needs comparison with pytest's
  native output.

Native pytest is the comparison surface, not a routine second run after every failure.
Record both commands, versions, exits, and sanitized outputs when the comparison exposes a
problem. Do not weaken the consumer's normal test gate merely because the compact renderer
has a limitation.

## Reporting missing or limiting behavior

Open the owning bug or proposal in
[`uibcdf/pytest-receptor`](https://github.com/uibcdf/pytest-receptor/issues). Include the
consumer repository, exact command, Pytest Receptor/pytest/xdist versions, expected and
observed behavior, exit status, and the smallest sanitized evidence that preserves the
problem. A disagreement with pytest about outcome or counts is a high-priority defect.

If a consumer must keep a workaround, open or retain a consumer-local issue that links the
provider issue and states the removal condition. Apply the suite's
`component:<consumer>` relationship label in the provider repository when available. Do
not expose credentials, private data, or unredacted test output in either issue.

MolSysSuite contributors share responsibility for improving sibling components. A missing
profile, insufficient diagnostic, incompatible plugin, or limiting artifact contract is
feedback for Pytest Receptor even when the immediate work occurs elsewhere.

## Synchronization contract

This canonical file belongs to `uibcdf/pytest-receptor`. Registered consumers receive an
exact, read-only root copy named `PYTEST_RECEPTOR_GUIDE.md` through MolSysSuite's central
guide synchronizer. Consumer repositories must reference that copy from `AGENTS.md` and
exclude it from Ruff formatting or lint discovery with the repository's vendored-guide
configuration.

Never edit a consumer copy. Propose content changes in the provider, validate them there,
then update the central registry and resynchronize all registered copies byte for byte.
