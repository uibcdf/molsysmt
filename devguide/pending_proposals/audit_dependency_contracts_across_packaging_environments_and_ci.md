---
summary: Audit dependency contracts across packaging, environments, and CI
issue: uibcdf/molsysmt#245
status: active
opened: 2026-09-25
closed:
verification: reproduced
area: [packaging, deps, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Audit dependency contracts across packaging, environments, and CI

**Reported:** 2026-09-25, after a staged wheel smoke installed outdated
PyUnitWizard sources and exposed a public minimum that was too low.
**Status:** Active; the read-only auditor and its route inventory are under
local verification before the next exact candidate is frozen.

## What

Establish a read-only audit of the dependency requirements that appear in
Python packaging, both Conda recipes, Conda environments, and controlled CI
source routes. The public dependency list in `pyproject.toml` owns names and
version floors; the audit inventory owns only secondary paths and exceptional
providers. A contributor, not a broadcaster, updates secondary files in the
same change.

## How

`devtools/scripts/audit_dependency_contract.py` reads the public metadata and
the route inventory in `devtools/dependency_contract.toml`. It checks the
Conda translation of `mmcif`, constraints in each recipe, runtime-bearing
environments, hard/soft form classification, controlled source SHA uniqueness,
and the workflows that install sources into `--no-deps` environments. A new
environment must be classified or explicitly excluded. Findings identify the
file and its missing or conflicting requirement. The fast release gate runs
the auditor. Focused mutation tests remove a floor, package, source install,
workflow pin, or inventory entry and require failure.

## Why

The initial pass found an absent `py-mmcif` dependency in the Rattler recipe,
unbounded hard dependencies in production/development/test environments, and
a benchmark workflow that installed MolSysMT without supplying the missing
hard dependencies. The earlier wheel smoke had a separate, stale set of
sibling SHAs. These are independent routes by which an apparently green
source test can disagree with an installable artifact.

## What is measured and what is assumed

**Reproduced:** the first local auditor invocation on 2026-09-25 produced
specific findings for the Rattler recipe, environment floors, and the
benchmark workflow; after addressing those paths, the same command passed.
`python -c 'import yaml; yaml.load(open("devtools/conda-build/meta.yaml"),
Loader=yaml.FullLoader)'` fails with `ConstructorError` because the current
recipe contains Jinja expressions. The original broadcaster uses that load.

**Assumed:** the pattern may be reusable by other MolSysSuite components.
That requires separate component evidence and central review; this local
experiment does not enact a suite-wide policy.

## What was refuted

- Reusing `devtools/requirements.yaml` as the sole public authority: it mixes
  hard, soft, build and development packages, lacks current floors, and would
  make standard Python package metadata a derivative surface.
- Re-running `broadcast_requirements.py`: it cannot parse the current recipe
  and would overwrite compiler, host and selector decisions.
- Checking only that wheel and Conda manifests match: both can agree on the
  wrong minimum. The PyUnitWizard 0.24.0 API gap requires separate minimum-
  version and installed-runtime evidence.

## Scope and exclusions

The first implementation belongs to MolSysMT. It audits static source
contracts and workflow routes; it does not rewrite files, solve Conda
environments, infer every API introduction date, or certify downloaded
package metadata. Built-artifact inspection and clean installation remain
separate release gates. MolSysViewer may adopt a corresponding pattern after
this one is stable; the suite repository owns any shared policy.

## Acceptance criteria

- The auditor passes on the maintained tree and fails on mutations of each
  materially distinct route.
- The fast release gate includes the auditor, and its operational procedure
  is documented in `devguide/dependency_contract_audit.md`.
- Existing controlled-source CI consumers use the single manifest; an
  independent hard-coded sibling SHA is rejected.
- The old broadcaster is not used as a repair mechanism. Retiring its files
  and relocating the active manifest are separate, reversible cleanup steps
  only after all references are accounted for.

The durable rule belongs in `devguide/dependency_contract_audit.md`; the
regression guard is `devtools/tests/test_audit_dependency_contract.py`.

## Dependencies and risks

The static parser intentionally understands only the current simple run-list
shape of the two recipes and fails on an unfamiliar entry. If a recipe gains
conditional runtime syntax, extend the parser and its mutation tests before
the audit can pass. An overly broad exception or a hard-coded output-shaped
test could make the gate vacuous; compare actual executed workflow steps and
the produced package metadata at release time.

## Provenance

MolSysMT candidate worktree, Python 3.13 development environment,
2026-09-25. The related hosted wheel failure is run `36102309653` and the
first staged package-pair build is recorded in `release_1_0_status.md`.
