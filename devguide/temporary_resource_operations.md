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
| RCSB file download | Each attempt owns a staging directory beside the destination through response/file close and publication. | Failed attempts retire staging without touching the destination. Only a complete response is published with `os.replace`; cleanup errors are visible. |
| PDB-ID or AlphaFold file conversion | The converter owns staging through download and extraction. | Download/extraction failure preserves the destination, including an existing default basename. Successful extraction is published without deleting the returned file. |
| Generated PDB-text or UniProt FASTA output | The writer owns the generated file until successful write and close. | Failure or interruption retires generated output. Explicit destinations are retained and may contain partial writes; cleanup errors propagate. |

Download/conversion staging requires a writable destination parent. Publishing
uses a same-filesystem replacement after handles close; it does not promise
power-loss durability, serialization of concurrent writers, preservation of an
old destination's inode/permissions, or rollback if directory retirement fails
after publication. The high-level conversion dispatcher still requires an
explicit filename for file targets; generated paths described here belong to
the corresponding form adapters.

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
- The temporal Rust probe compiles inside a parent-owned managed directory and
  loads the library only in a child. The parent waits for normal/failed exit or
  kills and reaps the child after communication failure or interruption before
  retiring that directory. Child temporary HDF5 files also live under this owned
  root. Compile/start/load/single-query/batch-query/cleanup errors remain visible.
  A successful JSON report is published only after directory retirement succeeds.
  Query timings stay inside the child and exclude compilation, process startup
  and IPC. Index-byte fields do not measure total process RAM. An abrupt kill of
  the owner cannot execute its Python cleanup scope.
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

## Verification scope

uibcdf/molsysmt#374 repairs the two eager runtime PDB bridges, generated
file-returning failure custody and temporal native-probe ownership. Its native
guards execute real Rust libraries and child lifetimes on Linux. They assert
child exit before directory retirement, rather than relying on unlinking a
loaded library. Windows/macOS execution and platform release qualification
are not claimed. Execute the addressable native guard on the corresponding
platform before claiming lifetime compliance there:

```bash
python -m pytest --receptor=llm -n12 devtools/tests/test_temporal_probe_lifecycle.py
```

The native cases require `rustc`; a dependency skip is not native-lifetime
evidence. Frozen-candidate qualification and release preservation remain
separate under uibcdf/molsysmt#334.
