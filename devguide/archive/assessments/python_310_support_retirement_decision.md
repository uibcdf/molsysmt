# Python 3.10 Support Retirement Decision

**Decision date:** 2026-07-13
**Status:** Accepted and applied

MolSysMT supports Python 3.11, 3.12, and 3.13. Python 3.10 was removed from the
package contract because it approaches upstream end of life and the project has
chosen to concentrate validation and release resources on the three maintained
versions.

The decision was applied to:

- `project.requires-python` and PyPI classifiers;
- Ruff's minimum target version;
- Conda recipe constraints and package build matrix;
- CI and developer documentation;
- documentation support badges.

Python 3.10 compatibility is no longer tested or promised. Incidental operation
on Python 3.10 does not constitute support.
