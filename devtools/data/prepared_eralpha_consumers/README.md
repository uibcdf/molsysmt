# Prepared ERalpha consumer qualification

Dated local contract evidence for uibcdf/molsysmt#298. See the maintained
[checkpoint](../../../devguide/pending_proposals/apply_explicit_chemical_templates_with_atom_correspondence.md).
This is a declared fragment/ligand model, not full-receptor or docking validation.

## Reproducing

Run from the MolSysMT root with RDKit and the chosen consumer's dependencies.
Select a consumer checkout explicitly. Use a **fresh artifact directory** for
each run: public H5MSM writing intentionally refuses to overwrite a file.
Run consumers in separate processes. For example:

```bash
python devtools/qualify_prepared_eralpha_consumers.py \
    --consumer dockingmt --consumer-root ../dockingmt \
    --artifacts /tmp/eralpha-docking-new --output /tmp/eralpha-docking-new.json
python devtools/qualify_prepared_eralpha_consumers.py \
    --consumer pharmacophoremt --consumer-root ../pharmacophoremt \
    --artifacts /tmp/eralpha-pharmacophore-new --output /tmp/eralpha-pharmacophore-new.json
```

The driver checks input SHA-256, prepares fixed chemistry and H through public
provider operations, attaches three named analyses, recovers public H5MSM, checks
observed coordinates/identity, historical typed values, empty coverage and maps,
then invokes real consumer APIs under pm/fs/coulomb application units. Coordinate
and H5MSM files remain in the requested artifact directory; compact reports are
retained here. Assertion controls require ordinary Python without `-O`.

## Consumer adjustments and evidence

- `dockingmt.patch` targets main d419feeb70a09e9f27035fc5b759f38e1793fbeb:
  audit snapshots use supported history-bearing domains; the resolved aromatic
  H path receives a positive control. Ownership: uibcdf/dockingmt#42.
- `pharmacophoremt.patch` targets the frozen unpublished ERalpha pilot described
  in `qualification.json`, not published main. A repeat-H control distinguishes
  unchanged chemistry from appended history. Ownership: uibcdf/pharmacophoremt#39.

These are proposed owner-review patches; they were tested only in isolated copies.
They do not change either original consumer worktree. `qualification.json` records
baseline file hashes, patch hashes and complete affected-suite results; the two
`*-interface.json` files record bounded real-API outcomes and runtime versions.
The provider source HEAD is authoritative for this source run. Its editable
package version string may describe an earlier installed build and is retained
honestly; this is not a public distribution or installed-artifact qualification.

The decompressed fixture is staged into caller-owned storage because concurrent
input-adjacent CIF.GZ decompression is tracked by uibcdf/molsysmt#326. No new
provider API, chemistry implementation, dependency or compiled routine is added.

The patches use zero context. Check the recorded baseline file hashes before
owner review, then use `git apply --check --unidiff-zero <patch>` in the intended
consumer checkout; normal context matching is unavailable for these files.
