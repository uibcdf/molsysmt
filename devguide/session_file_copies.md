# Session-owned file copies

**Role:** normative. Defines the file-path branch of public copying, alongside
the [resident native copy contract](native_copy.md). Introduced by
[uibcdf/molsysmt#450](https://github.com/uibcdf/molsysmt/issues/450).

## Public behavior

`msm.copy(source)` uses each supported form's copy protocol. Resident copying
is unchanged. A supported file path without `output_filename` receives an
independent temporary path, with the same suffix and file form, owned by the
creating Python process. An explicit destination is caller-owned and persistent.
It must be a filename distinct from the source, including filesystem aliases.
Existing distinct destinations can be overwritten. A composite source without
a destination copies its members separately; one explicit filename cannot
address a composite.

Raw file copying preserves bytes and format version without materializing a
native molecular system. SDF/PDBQT retain their existing validation. Copying
does not add missing format write capabilities, implement live-handle ownership,
or migrate H5MSM. See the [user workflow](../docs/content/user/cookbook/copying_disk_systems.md).

## Ownership boundary

The private `files_and_directories.file_copy_destination` context resolves and
validates the destination. `copy_file` uses it for raw copying; validating adapters
use it around their own writer. Automatic reservations belong to
`_private.session_files`, which securely creates a private per-process directory
in Python's platform temporary location and unique same-suffix files. Temporary
files retain private writable permissions even for read-only sources. Python's
TMPDIR/TEMP/TMP selection applies; the filesystem can be RAM-backed. File copying
consumes additional filesystem space and does not impose a process-RSS budget.

Ownership is retained independently of path-string lifetime or garbage collection.
Forked children detach inherited ownership and locks. Concurrent reservations are
serialized without serializing the file copies. Failed automatic writes retire
their reservation; a failing composite retires already completed owned members.
Explicit destinations are never registered for automatic removal. If an existing
automatic path is selected explicitly, ownership is relinquished before writing,
after destination validation, including through a resolved path alias. An explicit
write failure therefore leaves the caller responsible for that destination.

## Lifetime and cleanup

Paths remain usable through the creating process's session. Use an explicit
persistent destination for saved sessions or consumers that outlive that process.
Normal interpreter exit attempts to unlink only registered paths. The directory
is removed only if empty: unregistered caller files, including persistent outputs
placed inside it, survive. Cleanup does not wait on a busy registry lock and
retains failed unlinks for any subsequent cleanup attempt. Locked files and abrupt
termination can leave leftovers; unconditional removal is not promised.

No public early-cleanup or path-reference-count lifetime is introduced. The
independently managed `PersistentResultHandle` keeps its existing explicit
array-resource lifecycle; it is not converted into a session-owned path.

## Guards

- [Public/direct file-copy contracts](../tests/basic/test_file_copy.py): independent
  paths, source protection, H5MSM domains, legacy bytes and filesystem path protocol.
- [Actual lifecycle subprocesses](../tests/basic/test_file_copy_lifecycle.py): normal
  exit, persistence, promotion, failure rollback, concurrency, read-only sources,
  busy-lock shutdown and fork isolation.
- [Shared adapters](../tests/form/test_raw_file_copy.py): raw copying and validating
  SDF/PDBQT routes, including failed temporary reservations.
