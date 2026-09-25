# Dependency contract audit

This is the maintained, repository-local route for changing a runtime
dependency. The public package contract is the `dependencies` list and
`requires-python` field in `pyproject.toml`. The form adapter's hard/soft
classification is owned separately by `molsysmt/_depdigest.py`. Exact source
SHAs used while a coordinated Conda pair is staged live in the controlled
source manifest named by `devtools/dependency_contract.toml`; those SHAs do
not define public version floors.

`devtools/dependency_contract.toml` inventories the secondary surfaces. It
contains paths, name translations (for example, Python `mmcif` to Conda
`py-mmcif`), and explicit source-provided exceptions, but no second copy of
the public dependency list. Every Conda environment in `devtools/conda-envs/`
must be classified as runtime-bearing or explicitly excluded with a reason.
The two maintained recipes and all workflows consuming the controlled-source
manifest are also inventoried. Main-branch smoke, weekly, benchmark, and docs
workflows share one audited routine Viewer source SHA; exact release-candidate
gates take the candidate SHA as an input instead.

## Updating a dependency

1. Decide whether it is a hard runtime requirement, a soft adapter/extra, or
   a build/test/docs-only tool. Do not infer the category from the environment
   where it happened to be installed.
2. For a hard runtime requirement, edit `pyproject.toml` first. Update
   `_depdigest.py` if the form classification changes. For a changed source
   candidate, update the controlled-source manifest or the explicit Viewer
   workflow input as appropriate.
3. Run `python devtools/scripts/audit_dependency_contract.py`. Update every
   secondary recipe and environment named by its findings in the same change.
   Do not weaken the public floor merely to make the auditor pass.
4. Run the focused tests with `pytest --receptor=llm -n 12` and the fast release
   gate. Before release, build packages and inspect their actual runtime
   metadata, then validate the exact installed Conda pair. The static audit
   does not replace those artifact and compatibility checks.

The auditor is intentionally read-only. The contributor changing a dependency
coordinates the secondary files; CI and the release gate prevent forgotten
copies from silently passing. `--root PATH` supports isolated fixture tests.
Its findings name the file and the missing or conflicting contract. It rejects
unclassified environments, a second hard-coded controlled SHA in a workflow,
and a missing source route for an environment that installs with `--no-deps`.

## Limits and retirement of the old broadcaster

Agreement is not compatibility. A wrong floor repeated perfectly in wheel and
Conda metadata still admits a broken installation; PyUnitWizard 0.24.0 versus
the `configure.has_active_policy()` call was one such case. Validate changed
minimum versions against the APIs they must supply, and keep clean installed
runtime tests as release evidence.

The legacy `devtools/requirements.yaml` and
`devtools/broadcast_requirements.py` were retired when this audit was adopted.
The broadcaster could not parse the current Jinja-based Conda recipe and
would overwrite hand-maintained host/build and platform choices. Its former
`devtools/requirements/` directory held one active source manifest; that file
now lives at `devtools/controlled_sources.txt`, and all active workflow
consumers use the new path. Historical archive references preserve the old
path as dated evidence, not as a current instruction.
