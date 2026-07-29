# Residue left by the Numba-to-Rust migration: code comments, cross-references, and one missing test

**Status:** completed and archived on 2026-07-29.
**Found:** 2026-07-28, while bringing the developer guide up to date after Segments
B–E closed.
**Scope:** `rust/README.md`, doc comments in `rust/src/`, one comment in
`molsysmt/_private/rust_backend.py`, and one missing test under `tests/`.
**Relates to:**
[`numba_migration_inventory.md`](../numba_migration_inventory.md),
[`rust_numba_divergence_contract.md`](../rust_numba_divergence_contract.md),
[`release_1_0_status.md`](../release_1_0_status.md).

## Why this document exists

The developer-guide pass of 2026-07-28 archived four bug reports and four proposals
whose subject was the Numba implementation, and relabelled the three Numba
migration documents as historical evidence. That work was deliberately confined to
`devguide/`.

Doing it surfaced four items that cannot be fixed inside `devguide/` because they
live in code, in code comments, or in the test suite. They are recorded here rather
than fixed silently, so that the documentation cleanup is not mistaken for a
complete cleanup.

None of these affects shipped behaviour. Item 1 is a genuine coverage gap; items
2–4 are accuracy problems in text that a developer will read and believe.

## Resolution

All four items were completed as lifecycle stage F4 work:

1. a Python integration test now asserts size-one target-row broadcasting for
   both `set_dihedral_angles` and `set_mic_dihedral_angles` over three structures;
2. live source references point to the archived migration records;
3. comments describe Numba only as the implementation replaced during migration;
4. `rust/README.md` describes the production `rust/` crate, private
   `molsysmt._rust` extension, Rust-only runtime, and current two-layer test model.

Verification passed with seven focused Python tests, all 80 Rust unit tests,
Ruff, the course validator, and the developer-guide validator.

## Item 1 — the dihedral broadcast contract has no test

**The gap.** `set_dihedral_angles` documents its `angles` argument as compatible
with shape `(n_structures, n_quartets)`, and both the vacuum and the periodic Rust
kernels broadcast a size-1 structure axis accordingly. Nothing in `tests/` asserts
this. A search for `broadcast` across the suite returns no test, and the existing
tests in `tests/lib/test_advanced_pbc_and_mic_kernels.py` and
`tests/lib/test_remaining_advanced_structure_kernels.py` pass full-shape arrays.

**Why the gap exists.** The behaviour used to be pinned by a parity test against
the Numba oracle — specifically, a test asserting that Rust broadcasts *where Numba
read out of bounds*. Segment D removed the oracle, and the assertion went with it.
This is the general hazard of a divergence test: it is defined relative to a second
implementation, so it does not survive that implementation's deletion.

**Verified current behaviour** (2026-07-28, against the installed extension): with
`angles` of shape `(1, n_quartets)` applied to a three-structure system, both
`set_dihedral_angles` and `set_mic_dihedral_angles` broadcast, and both reach the
requested angle to `2.2e-16`. Neither raises.

**Implemented fix.** One test asserts that a size-1 structure axis broadcasts
identically on the vacuum and periodic paths. The history is in
[`archive/resolved_bugs/dihedral_angles_broadcast_mismatch_pbc.md`](../archive/resolved_bugs/dihedral_angles_broadcast_mismatch_pbc.md).

**Worth checking at the same time:** whether any *other* deliberate divergence was
pinned only by a parity assertion and lost its guard the same way. The candidates
are listed in [`rust_numba_divergence_contract.md`](../rust_numba_divergence_contract.md);
the three known to retain Rust-side unit tests are the SASA orthogonality check,
the principal-axes sign convention, and the triclinic minimum image.

## Item 2 — dangling references to relocated bug reports

Four bug reports moved from `devguide/pending_bugs/` to
`devguide/archive/resolved_bugs/` on 2026-07-28. These references still point at
the old paths:

| File | Reference |
| --- | --- |
| `rust/README.md` | all four reports, cited by name |
| `rust/src/dihedral_ops.rs` | `devguide/pending_bugs/dihedral_angles_broadcast_mismatch_pbc.md` (twice) |
| `rust/src/sasa.rs` | `devguide/pending_bugs/sasa_is_orthogonal_typo.md` (twice) |
| `rust/src/axes.rs` | `devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md` (twice) |
| `rust/src/pbc.rs` and `rust/README.md` | `devguide/pending_bugs/wrap_to_mic_triclinic_not_minimum_image.md` |
| `molsysmt/_private/rust_backend.py` | `devguide/pending_bugs/dihedral_angles_broadcast_mismatch_pbc.md` |

Mechanical path updates. They are listed individually because a reader who follows
a broken path is likely to conclude the bug is untracked rather than that the link
moved.

## Item 3 — code comments written against a live oracle

Several Rust doc comments describe the Numba implementation in the present tense,
as an "upstream" that a reader could go and inspect. It no longer exists in the
repository. Examples:

- `rust/src/dihedral_ops.rs`: *"which reports that its periodic twin does **not**
  broadcast"*, and *"Upstream this kernel indexes `angles[ii, aa]` directly"*;
- `rust/src/sasa.rs`: *"Upstream returns false for both because it tests `b[2][2]`"*,
  and *"the parity gate for this kernel is a tolerance"* — there is no parity gate;
- `rust/README.md`: *"Three cases so far, all reported"*, framing the divergences as
  open reports against a live implementation.

The technical content is correct and worth keeping: it explains why a kernel is
written the way it is. Only the tense and the framing are wrong. The proposed
rewording keeps every explanation and changes "upstream does X" to "the Numba
implementation this replaced did X", with a pointer to the archived report.

`rust/src/sasa.rs` needs one substantive touch rather than a reword: the comment on
`orthogonal_vs_triclinic_branch_on_a_cubic_box` justifies a `1e-9` parity tolerance
against Numba. That tolerance no longer exists. The test itself remains valuable —
it bounds the divergence between the kernel's own orthogonal and triclinic
branches — so the test should stay and its justification should be restated in
those terms.

## Item 4 — `rust/README.md` describes a superseded layout

`rust/README.md` refers to the pilot branch `experiment/rust-numba-pilot` and to
the crate directory `experiments/rust_kernels/`. Neither exists on `main`: the
crate is at `rust/` and ships as the private `molsysmt._rust` extension. The same
stale locations appeared in the proposals archived on 2026-07-28, where they are
now explicitly marked historical.

## Acceptance criteria

1. One test asserts the dihedral broadcast contract on both paths, and fails if
   either kernel stops broadcasting.
2. No file outside `devguide/archive/` refers to a bug report by a path that does
   not resolve.
3. No code comment describes the Numba implementation as present or inspectable.
4. `rust/README.md` describes the crate's actual location and packaging.
5. `ruff check molsysmt`, `cargo test --manifest-path rust/Cargo.toml
   --no-default-features`, and the fast release gate all still pass.

## Explicitly out of scope

- Re-running or re-validating any migration gate. Segments B–E are closed on exact
  commits with recorded evidence; nothing here disputes that evidence.
- Deleting `devtools/scripts/audit_numba_surface.py` or its baselines. The ratchet
  now guards zero and should keep running.
- The two open editorial items in Common Core notebooks 12 and 17. Those are course
  content, tracked in
  [`../resolved_bugs/course_module_numbering_overlaps.md`](../resolved_bugs/course_module_numbering_overlaps.md)
  and owned by lifecycle stage F4.
