---
summary: The conda recipe omits four dependency floors, and the channel cannot satisfy two of them.
issue: uibcdf/molsysmt#193
status: resolved
opened: 2026-09-01
closed: 2026-09-01
severity: high
verification: measured
area: [build, deps]
guard: tests/test_distribution_manifests.py
normative:
blocked_by: []
supersedes: []
---

# The conda recipe and `pyproject.toml` declare different dependency contracts

**Reported:** 2026-09-01, from MolSysViewer, while auditing the release chain that ends
in MolSysViewer 1.0 and passes through this repository. Found by reading both manifests
side by side, then querying the channel.
**Status:** resolved on 2026-09-01. The recipe now matches the source manifest and a
mutation-verified guard rejects future divergence.

## What

`pyproject.toml` constrains five dependencies. `devtools/conda-build/meta.yaml` reproduces
one of them.

| dependency | `pyproject.toml` | `meta.yaml` `run:` |
|---|---|---|
| `argdigest` | `>=0.12.1` | `>=0.12.1` |
| `smonitor` | `>=0.13.0` | *(no bound)* |
| `pyunitwizard` | `>=0.24.0` | *(no bound)* |
| `depdigest` | `>=0.10.0` | *(no bound)* |
| `numpy` | `>=1.26,<3` | *(no bound)* |

Read from `pyproject.toml:23-35` and `devtools/conda-build/meta.yaml:14-26` on
`cc48b26d9`.

Two of the four omissions are reachable today, because the channel serves versions below
the declared floor:

```bash
$ curl -s https://api.anaconda.org/package/uibcdf/smonitor \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['versions'])"
['0.11.4', '0.12.0']

$ curl -s https://api.anaconda.org/package/uibcdf/pyunitwizard \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['versions'])"
['0.18.2', '0.21.0', '0.21.1', '0.23.0', '0.24.0', '0.25.0']

$ curl -s https://api.anaconda.org/package/uibcdf/depdigest \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['versions'])"
['0.4.0', '0.9.1', '0.10.0', '0.10.1']
```

`smonitor` is the sharp one: the newest build on the channel is `0.12.0`, **below** the
`>=0.13.0` this project declares. A conda install cannot satisfy the declared contract at
all, and does not report that, because the recipe asks for nothing.

`pyunitwizard` and `depdigest` each serve versions below their floor, so a solver may
legitimately select one. `numpy`'s divergence is an omitted **ceiling** rather than a
floor, which is the half that gets forgotten: the recipe permits the `3.x` that
`pyproject.toml` excludes.

## How

The two files are independent lists of the same contract, and nothing compares them. The
one that agrees, `argdigest`, is the one recently edited for the alias-collision floor —
which is the shape of the defect rather than an exception to it: a manifest stays correct
exactly as long as someone is looking at it.

The asymmetry between `argdigest` and `smonitor` is worth stating because it explains why
this has not been noticed. Both floors name versions absent from the channel. `argdigest`
is pinned in the recipe, so the conda build **fails observably** and this repository's own
release ledger tracks it as a known wait. `smonitor` is not pinned, so the same situation
**passes silently** and yields a package.

A source install is unaffected: `pip` and an editable checkout read `pyproject.toml`.
Which is also why a green suite says nothing here — the development environment resolves
from the source tree, never from the recipe.

## Why

`severity: high`, on three grounds.

A conda package is what people install and keep, and 1.0 is the release that makes that
permanent. Publishing 1.0 with this recipe ships a package whose installed dependency set
contradicts its own declared support contract.

The failure mode is silence, not a crash. Nothing in the `0.12.0 → 0.13.0` range of
smonitor adds public API that would raise on the older version; the range is corrections
to the catalog path — warning semantics, `stacklevel`, rebuilding catalog instances from
state. So an installation below the floor does not fail. It emits diagnostics that behave
differently from the ones this project tested, which in a scientific library is worse than
an import error.

The defect has a precedent with a known fix. MolSysViewer declared `argdigest` and
`molsysmt` without constraints in **both** its manifests and became unimportable under a
resolver-valid combination. It closed the defect by fixing both floors and adding a guard
that holds the two manifests to one contract, so neither can drift alone:
`tests/test_distribution_artifact.py::test_distribution_manifests_bound_the_shared_alias_contract`
in `uibcdf/molsysviewer#62`. This repository has no equivalent check; `tests/` contains no
reference to `meta.yaml` or the recipe.

## What is measured and what is assumed

**Measured** — the contents of both manifests at `cc48b26d9`, and the versions each
package publishes on the `uibcdf` channel, with the commands above (2026-09-01).

**Measured** — the smonitor `0.12.0 → 0.13.0` range contains no new public API:
`git -C smonitor diff --stat 0.12.0..0.13.0 -- smonitor/` touches seven files, all
corrections plus one version-lookup performance change.

**Assumed** — that a solver presented with the current recipe would in fact select a
version below the floor rather than the newest available. Not exercised: no clean-channel
resolution was run, because doing so is part of the fix's acceptance rather than of the
report. For `smonitor` the assumption is not load-bearing — the newest available build is
already below the floor, so every resolution violates it.

**Not established** — whether any code path in this repository behaves incorrectly under
`smonitor 0.12.0`, `pyunitwizard 0.23.0` or `depdigest 0.9.1`. The report is about a
declared contract that one packaging path does not enforce, which stands whatever the
runtime consequence turns out to be.

## What was refuted

**"The recipe is deliberately loose so conda-forge can solve."** Refuted by `argdigest`,
which carries its floor in the recipe. The recipe is willing to pin; four entries simply
were not updated when their floors were introduced in `pyproject.toml`.

**"It is a documentation problem."** Refuted by the channel query. A missing floor for
`pyunitwizard` is not a stale note: the channel serves `0.18.2`, six minor versions below
the declared floor, and nothing stops a solver reaching it.

**"Publishing smonitor 0.13.0 closes it."** It closes the reachability of that one row and
leaves the mechanism intact. The next floor introduced in `pyproject.toml` drifts the same
way, silently, because nothing compares the files.

## Scope and exclusions

**In scope:** the agreement between `pyproject.toml` and `devtools/conda-build/meta.yaml`,
and a check that keeps them agreeing.

**Out of scope:** whether each floor is correct — that is each floor's own question;
publishing `smonitor 0.13.0` to the channel, which is that repository's release work and
only removes this defect's reachability, not the defect; and `argdigest 0.12.1`, which is
already tracked as a known wait by this project's release ledger.

**Deliberately not proposed:** upper bounds on the unconstrained dependencies. This report
asks the recipe to say what `pyproject.toml` already says, and nothing more.

## Acceptance criteria

1. Every constraint in `pyproject.toml` appears in the conda recipe, including the `numpy`
   ceiling.
2. A test fails when a floor is added, changed or removed in one manifest and not the
   other. This is the `guard`, and it is what distinguishes fixing the four rows from
   fixing the mechanism. `uibcdf/molsysviewer#62`'s guard is a working pattern for it,
   including the recipe parser.
3. The guard is mutation-verified: drop one floor from the recipe and it goes red.
4. A conda build against the channel either resolves within the declared contract, or
   fails naming the dependency it cannot satisfy. Silence is the defect.

Note the ordering consequence of criterion 4: with the recipe corrected, the conda build
cannot succeed until `smonitor 0.13.0` is published, exactly as it already cannot succeed
without `argdigest 0.12.1`. That is the contract becoming visible, not a new blocker — but
it should be known before the fix lands rather than discovered by a red build.

## Dependencies and risks

No `blocked_by`: the fix is local to this repository.

The risk in fixing it is the one just named — the conda build stops producing a package
until the channel catches up. Given that the alternative is a 1.0 package installing an
unsupported dependency set, that is the correct trade.

## Provenance

Read and measured on 2026-09-01. MolSysMT at `cc48b26d9` (`0.21.0-553`), working tree
carrying three unrelated modifications. Sibling checkouts: smonitor `0.13.0-2`,
pyunitwizard `0.25.0-1`, depdigest `0.10.1-10`, argdigest `0.12.0-13`. Channel contents
read from `api.anaconda.org` the same day. Linux, Python 3.13.14.

## Resolution

The Conda recipe now carries the same runtime constraints as `pyproject.toml` for
NumPy, ArgDigest, DepDigest, SMonitor and PyUnitWizard. The guard parses every runtime
requirement from both manifests and compares their specifiers; it is not limited to a
second hand-maintained list of the four original omissions. Five mutation cases remove
each current constraint from the recipe and prove that the guard detects the drift.

The live channel changed after this report was opened: ArgDigest 0.12.1 and SMonitor
0.13.0 are now published for Python 3.11--3.13. `conda build --check` renders the
corrected recipe, and a dry-run resolution of its runtime dependencies succeeds for
Python 3.12, selecting the declared floors or newer compatible versions.

The equivalent Python 3.13 resolution fails explicitly because the channel has no
Python 3.13 MolSysViewer artifact. That is not manifest drift and is tracked separately
as uibcdf/molsysmt#195; importantly, it is now a named solver failure rather than an
unsupported dependency set accepted silently.
