---
summary: Source checkout calculations can report another installed MolSysMT version
issue: uibcdf/molsysmt#657
status: open
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [packaging]
guard:
normative:
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
