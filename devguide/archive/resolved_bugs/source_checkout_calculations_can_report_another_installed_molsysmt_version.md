---
summary: Source checkout calculations can report another installed MolSysMT version
issue: uibcdf/molsysmt#657
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [packaging]
guard: tests/test_runtime_version.py
normative: devguide/dependency_contract_audit.md
blocked_by: []
supersedes: []
---

# Source checkout producer version can describe another installed distribution

## What

During #604's bounded source pilot, imported owner code based on `aff8a48ff`
reported `molsysmt.__version__ == '0.23.0+201.g3502232d8.dirty'`, inherited
from the separately installed development distribution. New scientific result
`software['molsysmt']` faithfully copied that string, but the string did not
identify the source actually imported through the controlled `PYTHONPATH` route.

## How

The root bootstrap in `molsysmt/__init__.py` prefers
`importlib.metadata.version('molsysmt')` whenever distribution metadata exists.
It only tries a package-local `_version` if no installed distribution is found.
A controlled source overlay can therefore combine source code and unrelated
installed metadata. Inspect import origin and distribution metadata separately:

```python
import importlib.metadata as metadata
import molsysmt as msm
print(msm.__file__)
print(msm.__version__)
print(metadata.version('molsysmt'))
```

The private `pairwise-604-pilot` source manifest and resource receipt retain the
exact imported file population and source base independently of the observed
version string. The root/version bootstrap was not modified by #604.

## Why

Detached analysis provenance and optional scientific software credits should not
silently imply that an installed version identifies overridden developer source.
This is currently a source-overlay provenance issue, not evidence that a clean
canonical installed package reports another package's version, that numeric
results differ, or that an immutable artifact hash is wrong.

## Proposed acceptance

Choose an explicit source/install identity contract without adding an unbounded
Git/network lookup to scientific hot paths. Retain supported installed-version
behavior and define how source overrides expose their independent source identity
or explicitly unknown source version. Test mismatched source/install metadata in
a fresh subprocess and keep original stored producer metadata when reading files.
Review any broader version/attribution consumers before changing the bootstrap.

## Current mitigation and exclusions

Source receiving retains the actual Git commit, dirty state, complete file hashes
and import origins independently of package version. The #604 receipt explicitly
records the observed version mismatch. Do not call that version an exact source
commit or infer installed-package qualification from the overlay. Runtime bootstrap
repair is a separate owned task; no tag, metadata rewrite or publication is made.

## Implemented resolution and receiving

The root now prefers its package-local generated stamp, then metadata whose
file inventory locates the actual imported initializer, otherwise `0+unknown`.
It does not execute Git or add a runtime build dependency. A broken generated
module's own import failure remains visible. The maintained contract is
[Identifying imported MolSysMT builds](../../dependency_contract_audit.md#identifying-imported-molsysmt-builds).
This build label is not a fingerprint of mutable source: exact source commits,
changes, import origins and file hashes remain separate receiving evidence.

`tests/test_runtime_version.py` uses fresh-process controls around the actual
initializer: foreign metadata, matching metadata with and without file records,
generated versions taking precedence, absent/invalid stamps and broken stamp
imports. A real clustering calculation checks cached producer/version credit
even when the metadata lookup is changed independently. Existing interaction
tests verify that reading and rewriting preserves original producer versions.
Bootstrap stubs isolate version selection; they do not establish installed or
cross-provider qualification.

Private attempts under `.pytest_cache/external-reference-421/` retain commands,
JUnit, logs, complete before/after source manifests and monitored resources:

- `runtime-version-657-baseline`: six failures and three passes with the old
  bootstrap, including a borrowed foreign version and the guessed fallback.
- `runtime-version-657-directed`: nine passes after the correction.
- `runtime-version-657-integrated`: collection failed because the expanded
  test module omitted its `pytest` import; this is a test-fixture error, not a
  numerical or producer regression. The original failed attempt is retained.
- `runtime-version-657-integrated-fixed`: 172 passes, including 13 version
  controls, existing provenance/H5MSM/Ackredit tests, diagnostics/unit-policy
  checks and native Viewer integration-route controls. Peak cgroup memory was
  403,202,048 bytes; host availability stayed above 16 GB decimal. The capped
  process tree used one CPU, at most 2 GiB RAM and no swap; no resource stop,
  source-input change or Viewer-export change occurred.

The User Guide's installation, interaction result and cookbook pages explain
explicit unknown versions and original producer preservation. Module 04 adds a
linked source-identity note with every existing code cell/output unchanged.
Final clean-source checks are recorded below; issue closure follows verified public delivery.

No new public callable, scientific method, quantity, optional backend,
dependency floor or schema is introduced. ArgDigest/DepDigest are not applicable
to this private standard-library bootstrap. Existing SMonitor initialization,
PyUnitWizard policy and producer Ackredit integration remain in their owning
paths and retain their directed tests. This block does not qualify another
installed artifact, interpreter/platform matrix, renderer or release candidate.

The repository-wide Ruff format check initially found two earlier #604 formatting
omissions in the method digester and pairwise helper. Formatting them preserves
both ASTs exactly; all 4,564 Python files now satisfy the format check and Ruff
lint passes. The affected geometry tests are included in final receiving.

## Final source checkpoint

Clean implementation `bbb5eb7c71ced43fa1cee7b49f835ddda3b0550d` passes all
172 affected tests and fourteen fast gates. The four rendered User Guide/course
pages contain the explicit unknown-version explanation and working links;
the full HTML build retains exactly the same six baseline warnings. Every
original course code cell, execution count and output is unchanged.

The [portable receiving record](../../../devtools/data/runtime_version_receiving_657_20261108.json)
retains the original six failing baseline controls, first nine directed passes,
the expanded fixture collection error and both successful 172-case runs.
All 8,602 source and 2,463 Viewer-export input hashes agree before/after final
receiving. The scientific tests peak at 408,023,040 bytes; all three capped
runs preserve more than 13 GB decimal host availability without an OOM,
pressure or reserve stop. The runtime honestly reports `0+unknown` for this
unstamped owner checkout. Provider versions and import origins are retained
independently; none is relabeled as an installed-artifact qualification.

Incoming uibcdf/molsysmt#659 independently reports a clustering/unit-boundary
failure and takes the next correctness priority. It remains separate from this
provenance fix and the already closed #604 feature delivery. Existing #256,
remaining graphical, platform, installed and exact-candidate holds remain.
