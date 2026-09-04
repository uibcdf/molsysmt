# gh-run-receptor Guide (Canonical)

Source of truth for adopting **gh-run-receptor** in a client repository.

Metadata

- Source repository: `gh-run-receptor`
- Source document: `standards/GH_RUN_RECEPTOR_GUIDE.md`
- Source version: `gh-run-receptor@0.3.0`
- Last synced: 2026-09-04

## What gh-run-receptor is

gh-run-receptor is a read-only evidence receptor for GitHub Actions. It obtains structured
run evidence through the authenticated GitHub CLI, preserves GitHub's authoritative status
and conclusion, and renders a bounded report for either a human or an LLM.

It complements GitHub's native commands. It does not rerun, cancel, approve, upload,
publish, or deploy anything.

## Why a client repository adopts it

- Reduce repeated workflow output before passing it to a human or language model.
- Preserve run, attempt, job, platform, artifact, and evidence-completeness identity.
- Capture evidence once and replay it without another API request.
- Distinguish official GitHub state from profile interpretation such as `PARTIAL`.
- Retain a clear fallback to native GitHub inspection whenever evidence is incomplete or a
  workflow shape is unknown.

Measured MolSysMT examples reduced a competent diagnostic baseline from 5,138 to 296
`cl100k_base` tokens for a partial Conda failure, and a matrix-verification baseline from
143 to 39 tokens for a successful run. These are case measurements, not a universal rate.
For a status-only green query, native GitHub JSON was smaller and remains preferable.

## Supported integration level

Version `0.3.0` is a source preview with:

- `inspect`, `capture`, offline `replay`, and transition-only `watch`;
- `human`, `llm`, and JSON rendering;
- generic and initial Conda profiles;
- strict `bundle@1`, `model@1`, and `report@1` boundaries;
- dependency-free runtime on Python 3.11 through 3.13;
- installation as a GitHub CLI script extension;
- trusted default-branch repository configuration with exact workflow matching;
- offline `config check` and `config explain` commands;
- required-platform enforcement for the Conda profile.

CI, documentation, and release profiles; pattern matching; arbitrary rule keys; workflow
discovery; and the embedded GitHub Action are not implemented in `0.3.0`.

## Installation

The client requires Git, Python 3.11 through 3.13, and an authenticated GitHub CLI.
Install the exact preview tag:

```text
gh extension install uibcdf/gh-run-receptor --pin 0.3.0
gh run-receptor --version
```

Expected version output:

```text
0.3.0
```

Pinning is deliberate. A pinned script extension does not advance through an ordinary
upgrade. To change tags, remove and reinstall it explicitly:

```text
gh extension remove gh-run-receptor
gh extension install uibcdf/gh-run-receptor --pin NEW_VERSION
```

For development from a local checkout:

```text
gh extension install .
gh run-receptor --help
```

## Minimum use from a client

Inspect a completed or active run by numeric ID:

```text
gh run-receptor inspect RUN_ID --repo OWNER/REPO --receptor=llm
```

A full run URL also carries repository and hostname identity:

```text
gh run-receptor inspect https://github.com/OWNER/REPO/actions/runs/RUN_ID \
  --receptor=llm
```

Use `human` for an explanatory terminal view:

```text
gh run-receptor inspect RUN_ID --repo OWNER/REPO --receptor=human
```

If no receptor is supplied, an interactive terminal selects `human` and redirected output
selects `llm`. Automation should pass the receptor explicitly rather than depending on
terminal detection.

## Capture and replay

`inspect` captures and reports in one operation. Use `capture` when evidence should be
stored without interpreting the run, and `replay` to render that exact bundle later:

```text
gh run-receptor capture RUN_ID --repo OWNER/REPO --capture=full --output BUNDLE
gh run-receptor replay BUNDLE --receptor=llm
```

Capture policies:

| Policy | Behavior |
| --- | --- |
| `full` | Requests structured metadata and logs. Use for corpus work and difficult failures. |
| `adaptive` | Requests logs for completed unsuccessful runs. This is the normal inspection mode. |
| `metadata` | Requests structured resources without logs. Use when official state and job/artifact inventory are sufficient. |

Bundles separate hostname, repository, run, attempt, and policy. Members carry exact byte
counts and SHA-256 digests. A metadata bundle is never reused as if it satisfied a full
request.

## Monitoring without repeated output

```text
gh run-receptor watch RUN_ID --repo OWNER/REPO --receptor=llm
```

`watch` sends transition-only progress to stderr and one final report to stdout. It avoids
reprinting an unchanged job tree on every poll.

## Profiles

Use `generic` when no workflow-specific interpretation is wanted:

```text
gh run-receptor inspect RUN_ID --repo OWNER/REPO --profile=generic --receptor=llm
```

Use `conda` for a recognizable native-platform package matrix:

```text
gh run-receptor inspect RUN_ID --repo OWNER/REPO --profile=conda --receptor=llm
```

Omitting `--profile` enables conservative auto-detection. Current Conda detection requires
at least two recognized platform names and a workflow identity containing `conda` or
`rattler`. An exact reviewed repository rule is preferable in automation.

The initial Conda profile reports observed platform outcomes and calls an artifact reusable
only when its platform job succeeded and a matching artifact exists. It does not yet prove
ABI validation, upload, or channel publication.

## Repository workflow rules

Place the version 1 configuration at `.github/gh-run-receptor.yaml`:

```yaml
schema_version: 1
workflows:
  - match:
      path: .github/workflows/build_and_upload_conda_packages.yaml
    profile: conda
    settings:
      expected_platforms:
        - linux-64
        - linux-aarch64
        - osx-64
        - osx-arm64
        - win-64
```

Version `0.3.0` supports exactly one identity per rule: an exact `path`, positive numeric
`id`, or exact display `name`. Path has precedence over ID, and ID over name, if more than
one distinct rule matches the observed workflow. Rules select only `generic` or `conda`.
The only configurable setting is `expected_platforms`, whose values are `linux-64`,
`linux-aarch64`, `osx-64`, `osx-arm64`, and `win-64`.

Unknown fields, duplicates, globs, YAML tags, anchors, multiline scalars, flow mappings,
and unsupported profile or platform values are errors. This strict subset prevents a
misspelling or future-looking inert rule from appearing to protect a workflow.

Before committing a client rule, run:

```text
gh run-receptor config check
gh run-receptor config explain .github/workflows/build_and_upload_conda_packages.yaml
```

`config check` and `config explain` inspect an explicit local candidate. Remote `inspect`,
`capture`, and `watch` do not trust the current checkout: they fetch the file from the
target repository's default branch and store its path, branch, Git blob SHA, and content
SHA-256 in `config.json`. Replay uses that captured policy offline. If the default branch
has no configuration, existing conservative auto-detection remains active.

An explicit CLI `--profile` overrides the repository profile. A matched rule's settings
remain visible, but settings that do not apply to the explicit profile cannot change its
assessment. A successful GitHub run missing a required Conda platform is receptor `FAIL`
with exit code 1; the report still retains GitHub's authoritative `conclusion=success`.

## Reading the result safely

Every report retains both layers:

```text
PARTIAL conclusion=failure status=completed | OWNER/REPO | run=123 attempt=1
```

`conclusion=failure` is the GitHub source fact. `PARTIAL` says that the profile found
independently reusable successful work alongside that failure. It never means success.

Preliminary exit codes:

| Code | Meaning |
| ---: | --- |
| 0 | Completed GitHub success and successful receptor processing |
| 1 | GitHub failure or required profile expectation failure |
| 2 | Cancelled, timed out, stale, action-required, or another non-success terminal state |
| 3 | Pending or in progress |
| 4 | Evidence incomplete for the requested operation |
| 5 | Acquisition, configuration, normalization, or rendering error |
| 64 | CLI usage error |

Shell or agent automation must inspect the report as well as the exit code when it needs to
distinguish these cases. Never coerce codes 2 through 5 into success.

## Required fallback

Use native GitHub inspection when:

- the receptor reports `INCOMPLETE`, `UNKNOWN`, or `RECEPTOR_ERROR`;
- a decision requires evidence outside the captured dimensions;
- a new workflow shape has not been covered by a profile or sanitized fixture;
- only a minimal `status/conclusion` query is needed.

Typical fallback commands:

```text
gh run view RUN_ID --repo OWNER/REPO
gh run view RUN_ID --repo OWNER/REPO --log-failed
gh run view RUN_ID --repo OWNER/REPO --json status,conclusion,jobs
```

Keep raw logs local. Do not paste a full log into an LLM merely because the compact report
could not decide; narrow the missing question first.

## Security and repository policy

- Treat workflow logs, artifacts, configuration, and pull-request content as untrusted.
- Do not commit raw captures, tokens, private logs, or unsanitized evidence bundles.
- Use a reviewed allow-list when converting a public capture into a test fixture.
- Do not let a pull request define the rules used to certify that same pull request.
- Preserve unknown jobs, conclusions, and unmatched failures rather than filtering them
  away.
- Never describe a tag or a successful subset as proof that publication completed.

## Client repository checklist

For adoption at the current level:

1. Pin a verified gh-run-receptor tag.
2. Copy this guide to `GH_RUN_RECEPTOR_GUIDE.md` and record it in the repository's required
   external-tooling guides.
3. Use `--receptor=llm` explicitly in agent-facing commands.
4. Add `.github/gh-run-receptor.yaml` only for settings supported by the pinned version.
5. Run `config check` and test each workflow path with `config explain`.
6. Start with known archived runs before relying on live development runs.
7. Confirm that live JSON reports show `configuration.matched: true` and the expected
   default-branch source.
8. Record unsupported workflow shapes in gh-run-receptor, not as silent local filters.
9. Preserve `gh run view` as the fallback for incomplete evidence.
