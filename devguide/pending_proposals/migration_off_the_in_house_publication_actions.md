# Migrating MolSysMT's two publication pipelines off the in-house actions

**Status:** open. Two decisions, independent of each other, both with the
implementation sketched here and neither taken.
**Raised:** 2026-08-08, after auditing `uibcdf/action-sphinx-docs-to-gh-pages` and
`uibcdf/action-build-and-upload-conda-packages` and repairing both.
**Scope:** `.github/workflows/sphinx_docs_to_gh_pages.yaml`,
`.github/workflows/build_and_upload_conda_packages.yaml`, `devtools/conda-build/`, and
the GitHub Pages source setting of the repository.
**Not in scope:** the two actions themselves. They keep their users and their
maintenance; see §3.

## 0. The one-line answer

Both pipelines were built when their technique was the only one available. One of the two
has since been replaced by a native GitHub mechanism, and the other rests on a conda
feature that cannot work for a package with a compiled extension. Neither is broken today
in a way that a patch can fix, because in both cases the patch would have to be a
different pipeline.

The two cases are not symmetric and should not be decided together:

| | documentation | conda packages |
|---|---|---|
| What replaced it | a native GitHub Pages mechanism | nothing official; the ecosystem moved |
| Is our action at fault | no — the whole approach is superseded | no — `conda convert` cannot do what we ask |
| Urgency | low, it works | **blocking for 1.0 delivery** |
| Effort | one afternoon | one to three days, depending on the route |

## 1. Documentation: from a `gh-pages` branch to native Pages deployment

### 1.1 What happens today

`sphinx_docs_to_gh_pages.yaml` grants `contents: write`, and the action:

1. checks out the branch holding the documentation,
2. compiles it with Sphinx,
3. `git add -f docs/_build/html` and commits **the built site into the source branch**,
4. `git subtree split --prefix docs/_build/html` to extract that directory as its own
   commit, and
5. `git push origin <that commit>:gh-pages --force`.

GitHub Pages then serves the `gh-pages` branch. This was the standard technique for years
and there is nothing wrong with the implementation; it is the model that has aged.

### 1.2 What GitHub provides instead

Since 2022, Pages can take its source directly from a workflow run. The site is uploaded
as an artifact with `actions/upload-pages-artifact` and deployed with
`actions/deploy-pages`, authenticated through an OIDC token rather than repository write
access. Current majors at the time of writing: `upload-pages-artifact@v5`,
`deploy-pages@v5`, `configure-pages@v6`.

### 1.3 Why this is worth doing here, specifically

Four reasons, in descending order of weight:

1. **The workflow stops needing write access to the repository.** Today the documentation
   job holds `contents: write`, which is permission to push to *any* branch, granted so it
   can push to one. The native mechanism needs `pages: write` and `id-token: write`, and
   neither can modify the repository.

2. **The `gh-pages` branch stops existing, and it is not small.** It carries **1907
   commits**, each one a full snapshot of the built site, and the built site is currently
   **190 MB**. That branch is the one deliberate exception in
   [`git_history_bloat_cleanup.md`](git_history_bloat_cleanup.md), which says at line 87
   that it is separate and should be left untouched. With deployments as artifacts there is
   no branch to leave untouched: the history simply is not created. The repository is
   426 MiB packed today.

3. **Deployment history and rollback.** Deployments appear under the repository's
   Environments, with the URL of each and a one-click rollback. Today, recovering a
   previous version of the site means finding a commit in a force-pushed branch.

4. **It removes the failure mode we patched rather than fixed.** The action published
   whatever was in `docs/_build/html`. When Sphinx failed silently — which is what happened
   on every run since 2026-01-12 — a stale directory would have been published as new.
   v3.0.0 now refuses to publish when the directory is absent, but "the build failed and
   the previous output is still on disk" remains conceptually possible. With an artifact,
   what is deployed is what this run produced, or nothing.

### 1.4 The replacement workflow

```yaml
name: Documentation

on:
  release:
    types: ['released']
  workflow_dispatch:

env:
  SPHINXWORKING: True

permissions:
  contents: read

jobs:

  build:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v7
        with:
          fetch-depth: 0        # versioningit needs the tags

      - uses: actions/setup-python@v7
        with:
          python-version: 3.12

      - uses: mamba-org/setup-micromamba@v3
        with:
          environment-file: devtools/conda-envs/docs_env.yaml
          environment-name: docs
          condarc: |
            channels:
              - uibcdf
              - conda-forge
              - ambermd
            channel_priority: strict
          create-args: >-
            python=3.12

      - name: Install the package
        shell: bash -l {0}
        run: python -m pip install . --no-deps

      - name: Build the documentation
        shell: bash -l {0}
        working-directory: docs
        run: |
          set -euo pipefail
          sphinx-build -M html . _build -j auto

      - uses: actions/upload-pages-artifact@v5
        with:
          path: docs/_build/html

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v5
```

Note what disappears along with the action: no `sphinx-apidoc` question, no `branch`
input, no `.nojekyll` step, no committer identity, no `gh-pages` creation branch, and the
`set -euo pipefail` we had to add lives here where it can be read.

### 1.5 Migration steps

1. Verify the domain first — this is the only step that can go wrong in a way a workflow
   run will not tell you. The Pages API currently reports `build_type: legacy`,
   `cname: null`, and `html_url: http://www.uibcdf.org/molsysmt/`. The custom domain is
   therefore inherited from the organisation site, not configured on this repository, and
   the switch should preserve it — but confirm it against the live URL rather than assume.
2. Land the workflow above.
3. Switch *Settings → Pages → Source* from "Deploy from a branch" to "GitHub Actions".
   Until this is done, the deploy job fails; after it is done, the old workflow would no
   longer publish. The two are exclusive, so they change together.
4. Run it once with `workflow_dispatch` and compare the published site against the current
   one before deleting anything.
5. Keep `gh-pages` until the new pipeline has published at least one release, then decide
   whether to delete it. Deleting it is what actually reclaims the history; keeping it is
   a harmless archive of what was published before the migration.

### 1.6 Risks and what to check

- **Size.** The site is 190 MB. Pages officially supports up to 1 GB and times a
  deployment out after 10 minutes, so there is room, but not unlimited room: the notebooks
  carry embedded outputs (`docs/content/showcase/nglview.ipynb` alone is 7.7 MB, per
  `git_history_bloat_cleanup.md`), so the number grows with the documentation. Worth
  measuring in the first run.
- **`sphinx.ext.githubpages`** already writes `.nojekyll`; the artifact is served as-is, so
  the extension becomes redundant but harmless. No change needed.
- **This is a repository-level setting**, so it cannot be tested on a branch. That is why
  step 4 exists.

### 1.7 Acceptance criteria

1. A `workflow_dispatch` run publishes a site whose front page and API reference match the
   current ones, at the same URL.
2. The workflow declares `contents: read` at top level; no job holds `contents: write`.
3. A deliberately broken build (for instance, an extension removed from `docs_env.yaml`)
   fails the workflow and **does not** change the published site.
4. The deployment appears in the repository's Environments with a working rollback.
5. `git_history_bloat_cleanup.md` is updated: `gh-pages` is no longer an exception to be
   left untouched, it is a branch that can be deleted.

## 2. Conda packages: from one host build to real per-platform builds

### 2.1 Why the current pipeline cannot work, restated

`build_and_upload_conda_packages.yaml` builds once on `ubuntu-latest` and asks the action
to produce `osx-64`, `osx-arm64` and `win-64` with `conda convert`. The conda-build
documentation is explicit that this cannot work for compiled code: *"it is not possible to
convert packages containing C extensions to other platforms"*. `conda convert` adapts file
paths; it does not compile anything. A `--force` flag exists and does not change the
outcome, it only stops the tool from refusing.

Since the Rust migration MolSysMT carries a mandatory `molsysmt._rust` abi3 extension
(`pyproject.toml:119-124`), so it is exactly the case the documentation excludes. The
official alternative it offers — make the package `noarch` — is not available to us.

This has never been observed because the workflow has not run since 2025-12-07, for
version 0.12.0, months before the extension existed. The evidence and the channel-level
consequences are recorded in
[`molsysmt_1_0_conda_release_coordination.md`](molsysmt_1_0_conda_release_coordination.md)
§2, which this section is the mechanical answer to.

### 2.2 Three routes

**Route A — a matrix of real runners, keeping `conda build`.**

Each platform builds on its own runner and uploads its own package; the `platform_*`
conversion inputs are switched off. The recipe still needs the fixes in §7 of the
coordination report — a Rust toolchain declared, Python build tools moved to `host:`.

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - {os: ubuntu-latest,   platform: linux-64}
      - {os: ubuntu-24.04-arm, platform: linux-aarch64}
      - {os: macos-13,        platform: osx-64}
      - {os: macos-latest,    platform: osx-arm64}
      - {os: windows-latest,  platform: win-64}
```

Crossed with the existing Python matrix (3.11, 3.12, 3.13) this is 15 jobs. The upload can
stay on our own action with every `platform_*` input false, or move to Anaconda's official
`anaconda/actions/upload-package`, published on 2026-06-26, which takes `token`, `channel`
and a `packages` glob.

`linux-aarch64` — required by C3 and built by no current workflow, per §2 of the
coordination report — comes free with this shape, since GitHub now hosts ARM Linux runners.

**Route B — `rattler-build`.**

`prefix-dev/rattler-build-action` installs `rattler-build` and builds from a `recipe.yaml`,
and is designed around exactly this platform matrix. It is not a fringe third-party
choice: since the May 2026 releases, conda-build itself routes v1 `recipe.yaml` recipes
through the `py-rattler-build` Python API. `setup-only: true` leaves the binary on `PATH`
so `rattler-build upload` can publish in the same job.

The cost is rewriting `devtools/conda-build/meta.yaml` as a v1 `recipe.yaml`, for MolSysMT
and eventually for the four sibling packages, so that the release track has one recipe
format rather than two.

**Route C — a conda-forge feedstock.**

Submit a recipe to `staged-recipes` and let conda-forge build the whole matrix. It removes
the pipeline entirely, adds migrators and a broader audience, and gives up publishing on
the `uibcdf` channel and controlling release timing. It also requires the sibling packages
to be on conda-forge, which is a much larger decision than this document.

### 2.3 Trade-offs

| | A: matrix + conda-build | B: rattler-build | C: conda-forge |
|---|---|---|---|
| Distance from today | smallest | medium | largest |
| Recipe rewrite | no | yes, v1 `recipe.yaml` | yes, feedstock |
| Covers `linux-aarch64` | yes | yes | yes |
| Keeps the `uibcdf` channel | yes | yes | no |
| Sibling packages affected | no | eventually | yes |
| Alignment with where conda is going | neutral | high | high |
| Who maintains the build matrix | us | us | conda-forge |

### 2.4 Recommendation

**Route A now, Route C as a separate conversation after 1.0.** A is the smallest change
that makes the published packages correct, it reuses the recipe we already have, and it
closes the `linux-aarch64` gap that C3 requires. B is where the ecosystem is heading and
is the natural follow-up, but doing it now couples the 1.0 delivery to a recipe-format
migration across five repositories. C is the outcome that usually pays off for a library
at 1.0 and deserves its own decision, not a footnote in a delivery plan.

Whichever is chosen, the recipe must gain a `test:` section that imports `molsysmt._rust`.
That single line is what distinguishes a real per-platform build from a relabelled Linux
binary, and its absence is why the current pipeline could have published broken packages
without failing.

### 2.5 Acceptance criteria

1. Every published package is built on a runner of its own platform. No `conda convert`
   step remains in the workflow.
2. `linux-64`, `linux-aarch64`, `osx-64`, `osx-arm64` and `win-64` are published for
   Python 3.11, 3.12 and 3.13.
3. The recipe carries a `test:` section that imports `molsysmt` and `molsysmt._rust`.
4. A fresh environment created from the channel on macOS ARM imports `molsysmt._rust`
   successfully — verified on a real machine or runner of that platform, not inferred.
5. Criteria 1-4 replace the platform-coverage assumption recorded in §2 of the
   coordination report.

## 3. What happens to the two in-house actions

**Neither is archived, and neither is at fault.**

`uibcdf/action-build-and-upload-conda-packages` is used by around 25 external repositories
— among them ACCESS-NRI, `numba/pixie`, `fermi-lat`, Stoner-PythonCode — and
`uibcdf/action-sphinx-docs-to-gh-pages` by a comparable number, including NSLS-II, LANL and
Stanford groups. For a pure-Python package the conda action does exactly what it claims,
and for a project without its own API reference the Sphinx action is still the shortest
path to a published site. Both received a substantive fix on 2026-08-08 (v2.0.0 and
v3.0.0) and both remain worth maintaining.

What changes is that **MolSysMT stops being one of their users**. That is a statement about
MolSysMT having outgrown them — a compiled extension, and a documentation site large enough
that a branch of snapshots is a liability — not about the actions being poor.

If both migrations are carried out, the honest follow-up is a line in each README pointing
at the native mechanism, so that a reader deciding today can make the same comparison
without having to run the audit again.

## 4. Related documents

- [`molsysmt_1_0_conda_release_coordination.md`](molsysmt_1_0_conda_release_coordination.md)
  — owns the channel state, the publication order and the release gate. §2 states the
  problem; §2 of this document is the mechanical answer to it.
- [`git_history_bloat_cleanup.md`](git_history_bloat_cleanup.md) — §1 removes the one
  exception that report deliberately left in place.
- [`../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md`](../pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md)
  — the warning inventory, which the `sphinx-apidoc` change of v3.0.0 already reduces and
  which the migration does not otherwise affect.
