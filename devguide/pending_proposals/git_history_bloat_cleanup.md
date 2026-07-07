# Proposal: reduce molsysmt git-history bloat

**Status:** pending (diagnosis done; remediation not started).

## Diagnosis (measured 2026-07-07)

`molsysmt/.git` is **~439 MB** while the current working tree of the heavy
directories (`molsysmt/data` + `molsysmt/demo` + `sandbox`) is only **~102 MB**.
So roughly **~340 MB is historical dead weight** — old revisions of large binary
assets that were committed and later removed or replaced. Binary blobs do not
delta-compress, so every re-commit of a large file stores a full new copy that
lives in history forever.

The bloat is **committed binary molecular-data assets**, not build/web artifacts
(unlike molsysviewer, whose bloat was the regenerated `viewer.js.map`).

Accumulated packed size across all history, by bucket:

| Bucket | MB in history |
|--------|---------------|
| `molsysmt/*.msmpk` (packed systems) | 129 |
| `molsysmt/*.gz` | 58 |
| `molsysmt/*.dcd` (trajectories) | 53 |
| `molsysmt/*.h5` (HDF5 trajectories) | 33 |
| `docs/*.ipynb` (notebooks w/ embedded outputs) | 24.5 |
| `sandbox/*` (`.msmh5` + `.h5` + `.ipynb`) | ~23 |

### Concrete culprits

1. **Large binaries no longer in HEAD but still in history (pure dead weight):**
   - `molsysmt/data/msmpk/popc_membrane.msmpk` — **81.8 MB** in history, **absent
     from HEAD**.
   - `molsysmt/demo/membrane/membrane.msmpk` — **40.7 MB** in history, **absent
     from HEAD**.
   - Those two alone are ~122 MB of history that nothing checks out anymore.
   - `molsysmt/data/dcd/popc_membrane.dcd` — 4.5 MB in HEAD but 40 MB across
     history → re-committed / replaced multiple times.

2. **`sandbox/` is not gitignored** and has **24 tracked files** (e.g.
   `sandbox/traj.msmh5` 11 MB, `sandbox/Test_2nzt.ipynb` 4.6 MB,
   `sandbox/micro_traj_eq.h5` 4.6 MB). Scratch files that should never have been
   committed.

3. **Notebook output bloat:** `docs/*.ipynb` carry heavy embedded outputs
   (`docs/content/showcase/nglview.ipynb` alone is 7.7 MB).

### What is legitimate vs avoidable

- **Legitimate (keep):** `molsysmt/data/*` and `molsysmt/demo/*` fixtures that
  tests and documented examples actually load. These must stay in the tree; the
  problem is only their *historical churn*, not their present existence.
- **Avoidable:** `sandbox/` scratch, notebook embedded outputs, and the history of
  binaries that were removed or replaced.

## Remediation plan (three tiers, increasing effort/risk)

### Tier 1 — going-forward hygiene (low risk, no history rewrite)

- Add `sandbox/` to `.gitignore` and `git rm --cached` its 24 tracked files.
- Adopt `nbstripout` (pre-commit hook) so docs/sandbox notebooks stop committing
  embedded outputs.
- Result: stops future growth; reclaims ~0 existing space.

### Tier 2 — history purge of dead-weight binaries (big reclaim, rewrites history)

Reclaim the ~340 MB by purging removed/replaced binaries from history with
`git-filter-repo`, e.g.:

```bash
git filter-repo --invert-paths \
  --path molsysmt/data/msmpk/popc_membrane.msmpk \
  --path molsysmt/demo/membrane/membrane.msmpk \
  --path-glob 'sandbox/*'
```

**Preconditions / safeguards (learned from the molsysviewer .map purge on
2026-07-07):**
- Back up first: `git bundle create <backup>.bundle --all` and copy any
  uncommitted working-tree files.
- **Verify before purging any path** that *no test or documented example at any
  referenced commit* loads it. Files still present in HEAD and used by tests
  (e.g. `data/h5/dimer.h5`, current `data/dcd/*`) must **not** be `--invert-paths`
  purged — only genuinely dead paths (absent from HEAD) or `sandbox/*`.
- filter-repo removes `origin`; re-add it afterward.
- **Force-push** rewrites history → every collaborator must
  `git fetch && git reset --hard origin/main` (or re-clone). Announce to the team.
- `gh-pages` (published site) is a separate branch; leave it untouched.

### Tier 3 — structural (largest, project decision)

For large data fixtures that *are* needed, move them out of plain git:
- **git-LFS** for `molsysmt/data/**` binaries, or
- an **external data-download** mechanism (fetch on demand / packaged separately),
  so future large-fixture changes don't inflate the core repo.

## Suggested order

Tier 1 now (safe). Tier 2 as a deliberate, announced maintenance window after
verifying the path list against tests. Tier 3 only if data fixtures keep growing.

## Reference

Companion cleanup already done in molsysviewer (2026-07-07): purged
`molsysviewer/viewer.js.map` from history, `.git` 607 MB → 63 MB, force-pushed;
stopped tracking/packaging the map going forward. Same tooling and safeguards
apply here.
