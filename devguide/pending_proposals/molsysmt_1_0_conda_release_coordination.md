# MolSysMT 1.0 — Conda release coordination

**Status:** investigation report; scheduled as a parallel final-delivery track.
No code changed.
**Segment:** independent Conda publication coordination for the
[MolSysMT 1.0 Execution Plan](release_1_0_execution_plan.md); status in
[release_1_0_status.md](../release_1_0_status.md).
**Depends on:** the accepted C1 decision in
[rust_packaging_backend_design.md](rust_packaging_backend_design.md) — one MolSysMT wheel
with a private `molsysmt._rust` abi3 extension, distributed through the project's own Conda
channel.
**Investigated:** 2026-07-27, against the live `uibcdf` channel and the local sibling
checkouts.

> **Maintainer scheduling decision — 2026-07-28**
>
> Coordinated Conda publication is not on the critical path for scientific
> consolidation, Rust-only validation, the 1.0 source/tag decision, or
> manuscript work. It may proceed during manuscript writing and review.
> Installed-wheel validation remains required, but it may use controlled
> preinstalled sibling dependencies instead of waiting for every package to
> appear on the `uibcdf` channel. This report remains the acceptance plan for
> the eventual Conda delivery.

## 0. The one-line answer

The command that must eventually work

```bash
conda create -n molsysmt-release-test -c uibcdf -c conda-forge python=3.13 molsysmt
```

**cannot work today.** C2 is now complete, but four of the five required
packages are absent from the channel at the required versions, three of the required Git
tags exist only on local clones, and one dependency has no Python 3.13 build at all. Every
missing artefact is identified below, per step.

## 1. Package and version inventory

`molsysmt/pyproject.toml` requires (`requires-python = ">=3.11.0,<3.14.0"`):

| Package | Required by MolSysMT | Newest on `uibcdf` channel | Newest local Git tag | Tag pushed to origin? | Verdict |
|---|---|---|---|---|---|
| `pyunitwizard` | `>=0.22.0` | **0.21.1** | 0.22.0 (+9 commits) | **no** | **missing on channel** |
| `smonitor` | `>=0.11.6` | **0.11.4** | 0.11.6 (+14 commits) | **no** | **missing on channel** |
| `argdigest` | `>=0.9.3` | **0.9.2** | 0.9.3 (+5 commits) | **no** | **missing on channel** |
| `depdigest` | `>=0.10.0` | 0.10.0 | 0.10.0 (+5 commits) | yes | **satisfied** |
| `molsysviewer` | *unpinned* | 0.7.0 | 0.20.0 (+55, dirty) | yes | **13 minor versions behind** |
| `molsysmt` | — | 0.12.0 | 0.20.0 (+150, dirty) | yes | to be released as 1.0 |

Reproduce with:

```bash
for p in smonitor depdigest pyunitwizard argdigest molsysviewer molsysmt; do
  conda search -c uibcdf --override-channels "$p" | tail -n +3 | awk '{print $2}' | sort -uV
done
for r in pyunitwizard argdigest smonitor depdigest molsysviewer; do
  git -C ../$r describe --tags --abbrev=0
  git -C ../$r ls-remote --tags origin "refs/tags/$(git -C ../$r describe --tags --abbrev=0)"
done
```

### Why the tags exist but the packages do not

`.github/workflows/build_and_upload_conda_packages.yaml` triggers on
`release: types: ['released', 'prereleased']` — a **GitHub Release**, not a Git tag. Three
of the required tags were never pushed, so no Release could exist and no build was ever
triggered. **Creating and pushing a tag is not sufficient; a GitHub Release must be
published** (or the workflow dispatched manually).

## 2. Channel state

**Channel:** `uibcdf` on anaconda.org, label `main`, used with `conda-forge` at
`channel_priority: strict` (`ci-full.yaml`, `benchmarks.yml`, `build_and_upload_conda_packages.yaml`).
The build environment (`devtools/conda-envs/build_env.yaml`) also lists `ambermd`.

### Python coverage of what *is* published — two holes

| Package (published version) | py3.11 | py3.12 | py3.13 |
|---|---|---|---|
| `smonitor` 0.11.4 | yes | yes | yes |
| `argdigest` 0.9.2 | yes | yes | yes |
| `depdigest` 0.10.0 | yes | yes | yes |
| `pyunitwizard` 0.21.1 | **no** | **no** | yes |
| `molsysviewer` 0.7.0 | yes | yes | **no** |

Two independent consequences, both blocking on their own:

- **`pyunitwizard` 0.21.1 is py3.13-only**, so even the already-published version cannot
  satisfy a 3.11 or 3.12 environment;
- **`molsysviewer` 0.7.0 has no py3.13 build**, so the closing command
  (`python=3.13 molsysmt`) is unsatisfiable *even ignoring every version gap*.

### Platform coverage

Probed with `argdigest 0.9.2`, which is representative of the publishing workflow:

| Platform | Published |
|---|---|
| `linux-64` | yes |
| `osx-64` | yes |
| `osx-arm64` | yes |
| `win-64` | yes |
| `linux-aarch64` | **no** |

The publishing workflow enables exactly `platform_linux-64`, `platform_osx-64`,
`platform_osx-arm64`, `platform_win-64`. **Linux aarch64 is required by C3 and is not
built by any current workflow.** Adding it also means cross-building or an ARM runner for
the Rust extension, which is a C3 decision, not a coordination one.

## 3. Are the recipes correct? (questions 3 and 4)

Recipes live at `devtools/conda-build/meta.yaml` in each repository, with a two-line
`build.sh` (`$PYTHON -m pip install --no-deps .`).

| Check | Result |
|---|---|
| Python 3.11/3.12/3.13 in the build matrix | Yes for all five — the workflow matrix is `["3.11","3.12","3.13"]` |
| Python constraint in the recipe | `molsysmt` and `pyunitwizard` pin `python >=3.11,<3.14`; **`argdigest`, `depdigest` and `smonitor` declare a bare `python`**, so they would build against any Python the environment offers |
| Version constraints on siblings | **None.** `molsysmt`'s recipe lists `argdigest`, `depdigest`, `smonitor`, `pyunitwizard`, `molsysviewer` with no version bounds, while `pyproject.toml` pins `>=0.9.3`, `>=0.10.0`, `>=0.11.6`, `>=0.22.0`. A Conda install would therefore accept `pyunitwizard 0.11.0` and fail at import time instead of at solve time |
| Correct requirement sections | `molsysmt` and `depdigest` use `requirements: build:` where `host:` is correct for a Python package; the others use `host:`. This matters once a compiled extension exists (see §7) |
| `test:` section | **Absent in all five recipes.** No import test, so a package that cannot even be imported would still upload successfully |
| Channels declared | `uibcdf` + `conda-forge`, strict priority, consistently across workflows |

**The missing version bounds are the most consequential defect here**: they let the solver
produce an environment that satisfies Conda and violates `pyproject.toml`.

## 4. Dependency graph and publication order (questions 6 and 8)

Runtime dependencies among the five, from the recipes:

```
smonitor      → (python only)
depdigest     → smonitor
pyunitwizard  → numpy, pint, smonitor, depdigest
argdigest     → beartype, pydantic, pyunitwizard, pyyaml, numpy, pandas
molsysviewer  → anywidget
molsysmt      → h5py, numpy, numba, pandas, networkx, tqdm, matplotlib,
                argdigest, depdigest, smonitor, pyunitwizard, molsysviewer
```

**No cycles, at runtime or at build time.** Build requirements are only
`python`/`pip`/`setuptools`/`versioningit` (plus `nodejs` for `molsysviewer`); no recipe
build-depends on a sibling, so the graph is a DAG and one linear pass suffices.

**Required publication order:**

1. `smonitor` 0.11.6
2. `depdigest` (already at 0.10.0 — republish only if its pinned version must move)
3. `pyunitwizard` 0.22.0
4. `argdigest` 0.9.3
5. `molsysviewer` (a release covering py3.13 — see §2)
6. `molsysmt` 1.0

`molsysviewer` is independent of 1–4 and may be published in parallel, but must precede
`molsysmt`.

## 5. Tags and releases to create (question 7)

| Repository | Action | Note |
|---|---|---|
| `smonitor` | push tag `0.11.6`, publish GitHub Release | tag exists locally only; 14 commits sit after it — confirm the tag is the intended release point |
| `pyunitwizard` | push tag `0.22.0`, publish GitHub Release | tag exists locally only; 9 commits after it |
| `argdigest` | push tag `0.9.3`, publish GitHub Release | tag exists locally only; 5 commits after it |
| `depdigest` | none required | 0.10.0 already published; 5 commits after the tag are unreleased |
| `molsysviewer` | new tag + Release with a py3.13 build | channel is at 0.7.0, local tag is 0.20.0; decide the release version deliberately |
| `molsysmt` | tag `1.0.0` + Release, last | only after 1–5 and C3-C7 |

Because `version: "{{ environ['GIT_DESCRIBE_TAG'] }}"`, a Release built from a commit that
is not exactly on a tag produces a version string carrying the distance and hash. **Release
builds must run from the tagged commit**, and the "+N commits" columns above are a warning
that HEAD is not currently at the tag in four of the six repositories.

## 6. Pre-C2 development-environment snapshot (question 5)

On 2026-07-27 the development environment could not answer the clean-install
question because every sibling was an editable install pointing at a local
checkout:

```
molsysmt          0.20.0+149.gcb3341fd5.dirty   regular
pyunitwizard      0.22.0                        EDITABLE -> <workspace>/pyunitwizard
smonitor          0.11.6+0.gee38231.dirty       EDITABLE -> <workspace>/smonitor
argdigest         0.9.3                         EDITABLE -> <workspace>/argdigest
depdigest         0.10.0+2.g6e072b0             EDITABLE -> <workspace>/depdigest
molsysviewer      0.14.0+2.g6f85b96             EDITABLE -> <workspace>/molsysviewer
msm_rust_kernels  0.1.0                         EDITABLE -> <workspace>/molsysmt/experiments/rust_kernels
```

Reproduce with:

```bash
python -c "
import importlib.metadata as md, json
for p in ('molsysmt','pyunitwizard','smonitor','argdigest','depdigest','molsysviewer','msm_rust_kernels'):
    d = md.distribution(p)
    print(p, d.version, d.read_text('direct_url.json'))
"
```

The final line records the old pilot arrangement. C2 removed the separate
distribution and proved a non-editable local wheel containing
`molsysmt._rust`; C4/C5 must repeat the clean-install assertion for the
supported release artifacts.

## 7. Putting the abi3 wheel inside the Conda recipe (question 9)

The C1 design makes the extension part of the MolSysMT wheel, so **no separate Conda
package for the kernels is needed**. Two viable shapes:

**(a) Build the extension inside the recipe (preferred; one source of truth).**
`build.sh` already runs `pip install --no-deps .`, which with `setuptools-rust` in
`[build-system] requires` compiles the crate during the Conda build. The recipe must then
declare a Rust toolchain and move the Python build tools to `host:`:

```yaml
requirements:
  build:
    - {{ compiler('rust') }}          # or: rust
  host:
    - python >=3.11,<3.14
    - pip
    - setuptools >=68.0
    - setuptools-rust >=1.10
    - versioningit >=3.0
  run:
    - python >=3.11,<3.14
    ...
```

Consequence: the abi3 property becomes irrelevant *inside* Conda, because Conda already
builds one artefact per Python version. abi3 still matters for the wheels published
elsewhere and for C3.

**(b) Install a pre-built abi3 wheel in the recipe.** `build.sh` would
`pip install --no-deps <wheel>` from a build artefact. This removes the Rust toolchain from
the Conda build but makes the Conda package depend on an external artefact whose provenance
must then be pinned and verified. Only choose this if (a) proves impractical on some
platform.

Either way, the C3 wheel-inspection contract from the C1 decision applies: exactly one
`molsysmt/_rust.*` in the built package, and no package containing both an abi3 and a
CPython-specific extension.

## 8. Proving the installed package uses no local checkout (question 10)

The check must be positive evidence, not the absence of an error. Run **outside** any
repository directory (a `molsysmt/` subdirectory in the CWD shadows the installed package —
this was observed during the C1 spike):

```bash
cd /tmp && conda activate molsysmt-release-test
python - <<'EOF'
import importlib.metadata as md, pathlib, sys, molsysmt
prefix = pathlib.Path(sys.prefix).resolve()
for name in ('molsysmt','pyunitwizard','smonitor','argdigest','depdigest','molsysviewer'):
    d = md.distribution(name)
    loc = pathlib.Path(d.locate_file('')).resolve()
    assert prefix in loc.parents or loc == prefix, f'{name} resolves outside the env: {loc}'
    assert d.read_text('direct_url.json') is None, f'{name} is a direct/editable install'
    assert '+' not in d.version and 'dirty' not in d.version, f'{name} is not a released version: {d.version}'
import molsysmt._rust as r
assert pathlib.Path(r.__file__).resolve().is_relative_to(prefix)
print('clean install verified:', molsysmt.__version__)
EOF
```

Four independent signals: the file lives under `sys.prefix`, there is no
`direct_url.json` (editable/local installs always write one), the version carries no
`+N.gHASH`/`dirty` local segment, and the compiled extension also resolves inside the
prefix. Add `conda list --explicit` to the CI log so the exact provenance of every package
is recorded.

## 9. What can be tested now vs. what needs C2

| Test | Possible today | Needs |
|---|---|---|
| Channel inventory and version gaps (this document) | **yes** | — |
| Recipe review: python bounds, missing version pins, absent `test:` sections | **yes** | — |
| Publishing `smonitor`, `pyunitwizard`, `argdigest`, `molsysviewer` | **yes** | tags + Releases only; independent of MolSysMT |
| A clean env with the four siblings and *no* MolSysMT | **yes**, once published | §4 order |
| Adding version bounds to `molsysmt`'s recipe | **yes** | a documentation/recipe change |
| `conda create ... molsysmt` end to end | no | siblings published **and** a MolSysMT 1.0 release |
| Wheel carrying `molsysmt._rust` | **yes, locally** | C2 exact-commit artifact passes; C3 must reproduce it in CI |
| Conda package carrying `molsysmt._rust` | no | recipe update per §7 and C5 |
| "no local checkout" assertions on `molsysmt._rust` | **yes for the C2 local wheel** | C4/C5 must repeat against supported installed artifacts |
| abi3 wheels across the platform matrix | no | **C3** |
| Python 3.11/3.12/3.13 × NumPy range installed-wheel matrix | no | **C3/C4** |

**Nothing in §4's publication order is blocked by C2 or by Segment B.** The sibling
releases are the part of this work that can start immediately.

## 10. The closing path, step by step, with the missing artefact named

```bash
conda create -n molsysmt-release-test -c uibcdf -c conda-forge python=3.13 molsysmt
```

| Step | Solver needs | Status | Missing artefact |
|---|---|---|---|
| 1 | `python=3.13` | OK | — |
| 2 | `smonitor >=0.11.6` | **fails** | `smonitor-0.11.6-py3{11,12,13}_*` — tag unpushed, no Release |
| 3 | `depdigest >=0.10.0` | OK | — |
| 4 | `pyunitwizard >=0.22.0` | **fails** | `pyunitwizard-0.22.0-py3{11,12,13}_*` — tag unpushed; note 0.21.1 shipped py3.13 only, so the 3.11/3.12 builds must be restored |
| 5 | `argdigest >=0.9.3` | **fails** | `argdigest-0.9.3-py3{11,12,13}_*` — tag unpushed, no Release |
| 6 | `molsysviewer` (py3.13) | **fails** | any `molsysviewer` build for py3.13; the channel stops at 0.7.0/py3.12 |
| 7 | `molsysmt` 1.0 | **fails** | `molsysmt-1.0.0-py3{11,12,13}_*`; C2 already integrates `molsysmt._rust`, while the recipe and C3-C7 gates remain |
| 8 | verify no local checkout | not reachable | the §8 script, run in CI outside any repo directory |

Note that steps 2, 4, 5 and 6 are **not blocked by MolSysMT at all** — they are four
independent sibling releases.

## 11. Blockers

**Release-coordination blockers (no code):**

- B1. `smonitor` 0.11.6, `pyunitwizard` 0.22.0 and `argdigest` 0.9.3 tags exist only on
  local clones; nothing is published.
- B2. `pyunitwizard` 0.21.1 was published for py3.13 only — the 3.11/3.12 builds must be
  restored, or the matrix documented as narrower.
- B3. No `molsysviewer` build exists for py3.13; the channel is 13 minor versions behind
  the local tag.
- B4. In four of six repositories HEAD is several commits past the tag, so the release
  point must be chosen deliberately rather than built from HEAD.

**Recipe-quality blockers (small changes, no library code):**

- B5. `molsysmt`'s recipe declares its siblings with no version bounds while
  `pyproject.toml` pins them, so Conda can build an environment that violates the Python
  metadata.
- B6. No recipe has a `test:` section — an unimportable package would upload cleanly.
- B7. `argdigest`, `depdigest` and `smonitor` declare a bare `python` with no bounds.
- B8. `molsysmt` and `depdigest` use `requirements: build:` where `host:` is correct; this
  becomes load-bearing once a compiled extension exists.

**Blockers owned by other segments:**

- B9. `linux-aarch64` is required by C3 and no workflow builds it.
- B10. The Conda recipe has not yet been updated and validated to carry the
  C2-integrated `molsysmt._rust` extension.

## 12. Rollback plan for a bad build

Anaconda.org has no true "unpublish that keeps history" for a version, so the rollback is
label-based and additive:

1. **Immediately remove the bad artefact from the default label** so no new solve picks it:
   ```bash
   anaconda label --copy main broken-<pkg>-<version>       # preserve, then
   anaconda remove uibcdf/<pkg>/<version>/<file.tar.bz2>   # or:
   anaconda move --from-label main --to-label broken uibcdf/<pkg>/<version>/<file>
   ```
   Prefer `move`/relabel over `remove`: it preserves reproducibility for anyone who already
   installed it.
2. **Republish under a new patch version, never by re-uploading the same version.** Conda
   caches by name-version-build; re-uploading the same coordinates gives different users
   different bytes for the same identifier.
3. If only the build is wrong and the source is not, bump `build: number:` and re-upload —
   the solver prefers the higher build number.
4. **Record the bad version in this document and in the ledger's execution log**, with the
   reason and the replacement.
5. Because the siblings publish in dependency order (§4), a bad artefact low in the graph
   (`smonitor`) invalidates everything above it: re-verify `depdigest`, `pyunitwizard`,
   `argdigest` and `molsysmt` after replacing it.
6. Keep a `conda list --explicit` from the last known-good release-test environment so the
   previous state can be recreated exactly.

## 13. Acceptance criteria

1. `smonitor` 0.11.6, `pyunitwizard` 0.22.0 and `argdigest` 0.9.3 are published on `uibcdf`
   with py3.11, py3.12 and py3.13 builds for `linux-64`, `osx-64`, `osx-arm64` and
   `win-64`.
2. A `molsysviewer` release covering py3.13 is published.
3. `molsysmt`'s recipe declares sibling version bounds identical to `pyproject.toml`, and
   every recipe carries a `test:` section that at minimum imports the package.
4. `conda create -n t -c uibcdf -c conda-forge python=3.13 smonitor depdigest pyunitwizard
   argdigest molsysviewer` solves and imports with **no** MolSysMT present. This is
   independent of C2 and is the natural interim gate.
5. After the remaining C3-C7 gates and a MolSysMT 1.0 release, the closing command solves for python 3.11, 3.12
   and 3.13.
6. The §8 script passes in that environment, run outside any repository directory, and
   `conda list --explicit` is archived with the result.
7. Every step above is executed from a tagged commit, and the artefacts are recorded in the
   ledger's execution log.
