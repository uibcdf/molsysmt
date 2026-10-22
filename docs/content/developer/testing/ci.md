# Continuous Integration

MolSysMT uses GitHub Actions for source tests, static checks, documentation and
separate package qualification. A source run does not qualify installed artifacts.

## 1. Workflow Architecture

- **Push smoke checks**: `ci-smoke.yaml` runs the smoke suite on Ubuntu/Python
  3.14 for applicable pushes and pull requests; its path filters omit prose-only
  changes. Ruff, developer-guide and suite-governance workflows provide separate
  checks with their own triggers.
- **Pull-request full matrix**: `ci-full.yaml` runs the full suite on Linux and
  macOS arm64 with Python 3.11–3.14. Manual dispatch accepts an exact Viewer source
  commit. Intel macOS is outside this source matrix.
- **Scheduled full suite**: `ci-weekly.yaml` runs all four supported Python minors
  on Linux and at least weekly macOS arm64/Python 3.14. Its nightly route services
  skipped-commit backlog; the Python 3.13 job supplies coverage. A coverage-only
  run does not clear the full-matrix backlog.
- **Scientific evidence**: full-source qualification executes the registered
  evidence nodes and retains a certificate. Missing external oracles produce
  skips that prevent a passing zero-skip certificate. The evidence registry and
  environment define the actual oracle scope; passing regression or parity tests
  alone does not establish scientific accuracy.
- **Documentation deployment**: `sphinx_docs_to_gh_pages.yaml` builds and publishes
  on a released GitHub Release or explicit manual dispatch. Merging into `main`
  alone does not deploy the site. Local rendering and notebook execution remain
  distinct checks.
- **Package qualification**: installed-pair and package verification workflows
  record exact artifacts and hashes separately from source evidence. Their
  execution is not permission to publish or promote a release.

The workflow files under `.github/workflows/` are authoritative for matrices,
triggers, environment pins and commands. Inspect run results with GH Run Receptor
as described in the repository's `GH_RUN_RECEPTOR_GUIDE.md`.

## 2. CI Control Flags

Internal maintainers may use `[skip ci]` only under the
[direct-push checkpoint policy](https://github.com/uibcdf/molsysmt/blob/main/MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints).
Omit it by default; never use it on pull requests. Skipped source commits retain
full-suite backlog until the required Linux matrix succeeds. Administrative
checks and a marker do not waive exact-candidate release gates.
