# Public GitHub Release titles

Follow the [canonical release-title rule](../MOLSYSSUITE_GUIDE.md#github-release-titles)
and [suite release policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md#github-release-titles).
The public component release title/name is exactly its canonical `X.Y.Z` version,
matching the tag and package/project version. Put descriptions in the body/notes.

Before publishing or intentionally editing a release, check **Release title**
in the web form, pass `--title X.Y.Z` to GitHub CLI, or set API `name` to the same
canonical value as `tag_name`. Generating release notes does not remove this check.
The existing governance policy-release/archive namespaces and documented bounded
exception route retain their separate meanings.

Accepted decision: [uibcdf/molsyssuite#119](https://github.com/uibcdf/molsyssuite/issues/119),
coordinated with [uibcdf/moli#68](https://github.com/uibcdf/moli/issues/68).
