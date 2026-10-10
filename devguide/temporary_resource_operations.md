# Temporary-resource ownership in MolSysMT

This is the component operating contract established by uibcdf/molsysmt#371.
Shared policy belongs to
[uibcdf/molsyssuite#104](https://github.com/uibcdf/molsyssuite/issues/104).
Follow the synchronized [suite guide](../MOLSYSSUITE_GUIDE.md#temporary-development-resources)
for ownership, retention and explicit disposal. This document does not replace it.

## Runtime ownership

| Operation | Owner and lifetime | Failure and disposal |
|---|---|---|
| Disk-backed result without a supplied path | The result handle owns its backing file until `cleanup()` or context exit. | Failed mapping construction retires the allocated file. Cleanup errors propagate. |
| Disk-backed result with a supplied path | The caller owns the file, including after closing the handle. | Construction and cleanup do not delete it. Mapping with write mode is an intentional write, not preservation of previous content. |
| `TLeap.run()` with no working directory | The wrapper owns its generated directory through input copying, child execution and output copying. | Success and failure retire it unless retention was explicitly requested. Cleanup errors propagate and the original working directory is restored. |
| Explicit `TLeap.run(working_directory=...)` or `keep_working_directory=True` | The caller owns or explicitly retains the directory. | The wrapper preserves it; the caller inspects and retires it after its final use. |
| `build_peptide(engine='LEaP')` | The builder owns intermediate files through execution and conversion to the requested output form. | Managed directory exit retires intermediates on preparation, child or conversion failure. |
| Eager compressed-CIF and remote-data parsing | The parsing operation owns its scratch, distinct from its returned in-memory data. | Existing managed contexts/finally blocks retire it; underlying removal failures remain visible. |
| Simulation to PDBFixer bridge | The converter owns an intermediate PDB through eager fixer construction. | Managed directory exit retires scratch on write/read failure or success; the in-memory fixer survives. Cleanup errors propagate. |
| `get_missing_bonds(engine='pytraj')` | The audit owns an intermediate PDB through eager topology loading and bond-pair materialization. | Write/read/extraction failures and success retire scratch. Returned pairs are independent; cleanup errors propagate. |
| Successful file-returning download or conversion | The returned file is a result, even when its path was generated in a temporary location. | Ownership passes to the caller. Do not delete it on successful return. Explicit outputs remain caller-owned. |

The LEaP wrapper still uses the process working directory while running; resource
custody does not establish concurrent-call safety. Preserve existing serialized
use of that wrapper.

## Development, tests and qualification

- Use managed disposable contexts for tool scratch, and place requested receipts
  outside them. Scientific-evidence certificates and archive/artifact input files
  are retained independently of temporary XML or extraction directories.
- The Bash LEaP check runs its child in its generated directory, using an absolute
  executable path. Its exit trap retires only that directory; child logs cannot
  overwrite the caller's `leap.log`. Failures and cleanup diagnostics stay visible.
- Pytest owns its fixture directories and can retain recent sessions for diagnosis.
  If `--basetemp` is used, supply a fresh exclusive task directory: pytest may clear
  that destination. Never point it at a shared environment or caller evidence.
- Benchmark file contexts own temporary HDF5/SQLite files through closed readers
  and queries. Caller-selected JSON outputs are evidence, not disposable scratch.
- Notebook code, saved outputs, run fingerprints, generated Viewer scenes and
  execution logs have distinct purposes. Preserve outputs and logs still needed
  for verification. A source-only review does not qualify notebook execution.
- Documentation clean commands require an explicitly reviewed generated destination.
  Do not invoke the legacy `docs/clean_api.py` against arbitrary caller directories,
  or discard authored API material based on the name `autosummary` alone.
- Local build trees, extracted packages and installed prefixes belong to the task
  that created them. Hosted workflows retain their required receipts/artifacts
  before runner retirement. Source review does not prove hosted/platform cleanup.
- Preserve the frozen release references, original artifacts, hashes and receipts
  under [the release ledger](release_1_0_status.md). This policy review does not
  authorize rebuilding, promotion or publication during the pause.

## Remaining bounded implementation exceptions

uibcdf/molsysmt#374 owns generated file-returning failure custody and standalone
temporal native-probe exceptions. Its two eager runtime PDB bridges now implement
the managed lifetimes listed above. Owners are dprada/LMMV; review on 2026-10-24 or before
the next affected invocation. Use an exclusive process scratch root selected
before interpreter startup, retain it through inspection, and retire it after
readers, children and loaded libraries end. Provide explicit output paths for
file writers when failed creation must be recoverable. These are interim
procedures, not claims that the original operations implement complete cleanup.

Remove the exceptions only after independent success/failure/caller-custody
guards establish the relevant lifetimes and report retirement errors. Windows
loaded-library lifetime requires its own evidence; Linux unlink behavior does
not establish it. The issue retains the precise operations and acceptance scope.
