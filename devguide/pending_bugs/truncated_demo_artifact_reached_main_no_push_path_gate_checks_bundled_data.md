---
summary: A truncated demo artifact reached main because no push-path gate checks bundled data.
issue: uibcdf/molsysmt#182
status: open
opened: 2026-08-19
closed:
severity: high
verification: reproduced
area: [tests, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: a truncated demo artifact reached `main`

**Reported:** 2026-08-19, during an external audit of the repository conducted as a
reader arriving from the forthcoming methods paper.
**Status:** open, and deliberately postponed on 2026-08-19 after an attempted fix showed
the restore target is not established. The regression is present on `main`.

## What

`molsysmt/data/h5msm/traj_pentalanine.h5msm` is the MolSysMT half of the paired
periodic-trajectory oracle used by the Scientific Truth Suite. A documentation commit
overwrote it with a 100-structure subset of itself. It should hold 5000.

```bash
$ python devtools/scripts/validate_demo_assets.py
AssertionError: ('traj_pentalanine.h5msm', [62, 7, 1, 1, 1, 1, 61, 100])

$ python -m pytest tests/scientific_truth/curated/pentalanine -q
E   molsysmt._private.smonitor.exceptions.ArgumentError: 'structure_indices' contains
    out-of-range structure indices [499, 999, 2499, 4999]; valid indices are in [0, 100).
ERROR ... ::test_pentalanine_artifacts_agree_on_coordinates_box_and_time
ERROR ... ::test_pentalanine_periodic_distances_agree_with_mdtraj
ERROR ... ::test_pentalanine_periodic_phi_dihedrals_agree_with_mdtraj
ERROR ... ::test_pentalanine_ca_least_rmsd_agrees_with_mdtraj
```

The two artifacts the suite calls a pair no longer are one:

```bash
$ python -c "
import molsysmt as msm, mdtraj as md
print(msm.get(str(msm.systems['pentalanine']['traj_pentalanine.h5msm']), n_structures=True))
print(md.load(str(msm.systems['pentalanine']['traj_pentalanine.h5'])).n_frames)"
100
5000
```

## How

The replacement is `3bee6f054`, *"docs(showcase,cookbook): update showcase notebooks,
cookbook recipes, and static 3D viewers"*, which touched exactly one file under
`molsysmt/data/`:

```bash
$ git show 3bee6f054 --stat -- molsysmt/data/
 molsysmt/data/h5msm/traj_pentalanine.h5msm | Bin 3494262 -> 175462 bytes

$ git show 3bee6f054^:molsysmt/data/h5msm/traj_pentalanine.h5msm > /tmp/prev.h5msm
$ python -c "import molsysmt as msm; print(msm.get('/tmp/prev.h5msm', n_structures=True))"
5000
```

**The gate that catches this is real and is not on the push path.**
`validate_demo_assets.py` compares every bundled H5MSM against the expected hierarchy in
`molsysmt/data/demo_manifest.json`, whose `traj_pentalanine.h5msm` row ends in `5000`. It
fails on this commit, precisely and with the right message. It runs only inside
`devtools/scripts/release_gate.py`, and the release gate runs only in `ci-full.yaml`,
whose sole trigger is `workflow_dispatch`. Nothing invokes it from `pytest`:

```bash
$ grep -rn 'validate_demo_assets' devtools/tests/ tests/ .github/workflows/
.github/workflows/ci-full.yaml:112:        run: python devtools/scripts/release_gate.py
```

So the detector exists, is correct, and had not been asked. The automatic detector is
`ci-weekly.yaml`, which runs the scientific-truth gate every Monday: the errors above
would have surfaced on 2026-08-24, five days after the write, against an accumulated
week of commits.

**A third, weaker defence is documentation only.**
[`tests/scientific_truth/curated/PROVENANCE.md`](../../tests/scientific_truth/curated/PROVENANCE.md)
opens with *"SHA-256 digests make silent replacement detectable"* and records
`3eda9e88…` for this artifact. Nothing reads that table:

```bash
$ grep -rn 'sha256\|PROVENANCE' tests/ --include='*.py'
$ python -c "
import hashlib; print(hashlib.sha256(open('molsysmt/data/h5msm/traj_pentalanine.h5msm','rb').read()).hexdigest())"
fec8c2acf5959f9f0f102b3f05f5409ded88bf57811b896086556ad5248157dc
```

`validate_demo_assets.py` checks the hierarchy, not the bytes, so the two are
complementary rather than redundant: a same-shape artifact regenerated with different
coordinates passes the manifest and fails the digest.

## Why

**The artifact is packaged, not only tested.** `molsysmt/data/` ships, so
`msm.systems['pentalanine']['traj_pentalanine.h5msm']` changed for anyone installing from
source at or after `3bee6f054`. A tutorial, benchmark, or downstream notebook that
assumed 5000 structures now silently sees 100.

**While it stands, four scientific-truth tests are not evidence.**
`scientific_evidence_matrix.md` presents that suite as the governed independent evidence
behind the 1.0 contract. A test that errors during fixture setup is not weaker evidence
than one that passes; it is none, and the generated matrix does not distinguish the two.

**The class matters more than the instance.** Bundled data is the one input category with
a real gate that no push-path job runs. The same commit shape — a documentation pass that
executes notebooks and writes back into `molsysmt/data/` — can replace any catalog
artifact, and the project's whole verification strategy assumes those artifacts are
fixed.

The severity is `high` and carries `scientific-integrity`: the release gate would have
stopped this before a release, so it cannot reach users through a published artifact, but
it did reach `main` and it did disable part of the scientific record.

## What is measured and what is assumed

Measured, with the commands above: the structure counts (100 against 5000), the byte
sizes, the current SHA-256 and its disagreement with `PROVENANCE.md`, the manifest
assertion failure, the four fixture errors, the identity of the commit, the absence of
any `pytest`-reachable invocation of `validate_demo_assets.py`, and the trigger of every
workflow that could run it.

Assumed: that a documentation notebook executed during that pass produced the truncated
file. The commit contents make no other source plausible, but the specific notebook has
not been identified. Identifying it is part of the fix — a restored artifact with the
writer still in place is restored until the next documentation pass.

Measured 2026-08-19, during an attempted restore, and decisive for the shape of the fix:
the pre-truncation revision does not match the recorded digest either.

```bash
$ git show 3bee6f054^:molsysmt/data/h5msm/traj_pentalanine.h5msm > /tmp/prev.h5msm
$ python -c "
import hashlib; print(hashlib.sha256(open('/tmp/prev.h5msm','rb').read()).hexdigest())"
d882572a520fe0cb7dbd4c3254e8f38171d4c788d739ab81ee387acd495433b6
```

That file is 3,494,262 bytes and holds 5000 structures, so it satisfies
`demo_manifest.json`. It is not the file `PROVENANCE.md` was written against. Either the
artifact was replaced more than once, or the digest was recorded against a revision that
is not `3bee6f054^`.

Not established: whether any other catalog artifact has drifted. `validate_demo_assets.py`
reports only this one, and `traj_pentalanine.h5` still matches its recorded digest, but
the digest table as a whole has never been executed and no row other than these two was
checked by hand. Given the finding above, the other rows are now more suspect than they
looked, not less.

## What was refuted

*No guard existed.* This was the audit's first reading and it is wrong.
`validate_demo_assets.py` encodes the expectation exactly and fails on the right file
with the right numbers. The defect is when it runs, not whether it exists — a distinction
worth keeping, because "add a check" is the wrong fix and "run the check we have" is the
right one.

*The H5MSM artifact was always a 100-structure subset and the test constants are stale.*
Refuted by the previous revision: it holds 5000, the manifest expects 5000, and the
constants `[0, 499, 999, 2499, 4999]` address them correctly.

*The weekly job makes this harmless.* It makes it recoverable, not harmless. Five days of
latency on `main` is what let a second commit land on top of it.

*Restoring `3bee6f054^` closes this.* **Refuted on 2026-08-19 by attempting it.** The
restore produces a 5000-structure artifact that passes `validate_demo_assets.py` and
whose digest is `d882572a…`, not the `3eda9e88…` recorded in `PROVENANCE.md`. So the
first question is not how to restore the file but *which file is the artifact*, and the
guard in criterion 3 cannot be written until that is answered — a hash test is worthless
if the hash it enforces was never the hash of anything in the tree. The working tree was
returned to its committed state and the entry postponed rather than closed on a guess.

## Scope and exclusions

Covers restoring the artifact, identifying and stopping whatever regenerated it, putting
the existing demo-asset gate on the push path, and executing the `PROVENANCE.md` digests.

Excludes the general CI trigger policy, which is
[#185](https://github.com/uibcdf/molsysmt/issues/185); this entry needs only that the
bundled-data check runs when bundled data changes. Excludes replacing the curated
trajectory with a better oracle: that is a separate decision and must not be taken while
restoring, or the restoration cannot be verified against the recorded digest.

## Acceptance criteria

1. The correct artifact is identified, `molsysmt/data/h5msm/traj_pentalanine.h5msm` holds
   it with 5000 structures, and `PROVENANCE.md` records that artifact's actual digest.
   **This criterion originally read "hashes to `3eda9e88…` again". That was false** — see
   *What was refuted* — and it is the reason this entry is not a one-line restore.
2. `python devtools/scripts/validate_demo_assets.py` and
   `python -m pytest tests/scientific_truth` both pass.
3. A `pytest` test walks every row of `tests/scientific_truth/curated/PROVENANCE.md`,
   hashes the named file, and fails on a mismatch, a missing file, or a curated artifact
   with no row. This is the `guard`, and it is reachable without the release gate.
4. A push that changes anything under `molsysmt/data/` runs the demo-asset gate.
5. The documentation build cannot write into `molsysmt/data/`, or the notebook that did
   writes elsewhere.

## Dependencies and risks

Restoring the file re-adds 3.3 MB to a repository already carrying the history problem
described in
[`../pending_proposals/git_history_bloat_cleanup.md`](../pending_proposals/git_history_bloat_cleanup.md).
Restoring from `3bee6f054^` rather than regenerating would keep that to one blob
revision, because the object is already in history — but per *What was refuted* that
revision is not known to be the recorded artifact, so the choice is not yet available.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `b9a2098e4`, mdtraj 1.11.1, h5py via the
installed environment, NumPy 2.4.6.
