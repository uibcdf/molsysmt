# Atom-correspondence provider delivery

**Role:** operational handoff for uibcdf/molsysmt#223.
**Reference:** bc21428312b6945c9c8926611721713c5ca3fbd2; source-level qualification,
not a new public package or installed-pair admission.

## Delivered public tools

| Operation | Public entry point | Result axis |
| --- | --- | --- |
| Explicit naming constraints | `msm.build.project_atom_names(..., return_report=True)` | Identity atom map and declared label changes |
| Typed nonpolar-H aggregation | `msm.build.merge_nonpolar_hydrogens(..., typing_scheme='autodock4', return_report=True)` | Reduced native system and source/projection map |
| Native export | `msm.convert(..., to_form='string:pdbqt_text', return_atom_map=True)` or file output | Actual written atom order and payload hash |
| Known-source pose import | `msm.form.file_pdbqt.read_poses` / `msm.form.string_pdbqt_text.read_poses` | Reader-native output against the declared source and completed export map |
| Typed stage composition | `msm.basic.compose_atom_maps` / `msm.compose_atom_maps` | Original-to-current direct/representative maps with absent origins |

The handler also supplies `read_poses`. Historical top-level
`msm.form.read_pdbqt_poses` and `msm.form.compose_atom_maps` spellings are absent
from the current source contract. Select the correct entry points for the
provider revision actually installed. The maintained public tutorials own
full API signatures and examples; this document owns handoff/receiving steps.

## Consumer receiving sequence

1. Keep the original fixed-state system and completed preparation reports.
   Select chemical typing/charges explicitly; projection does not select them.
2. Apply name constraints before template-sensitive assignment when needed.
   Keep the returned native object and its label transformation.
3. Consume the reduced native object returned by H aggregation, including
   its derived assignment binding and report. Extracting retained atoms alone
   does not perform charge transfer.
4. Export that prepared object through the native writer with a completed map.
   Keep its actual bytes, serial/ROOT/tree order, rounding evidence and map.
   A map from these bytes cannot be attached to another serializer's payload.
5. Read real returned poses against that known chemical source and export map.
   All models are checked; missing coordinates are not taken from old source
   structures. Missing-atom policies are explicit.
6. Compose actual generation, naming, projection, export and pose stages in
   their performed order. Generated atoms retain absent earlier origins;
   merged H atoms retain representative identity without inheriting a coordinate.

DockingMT owns production adoption and retirement under uibcdf/dockingmt#49,
including explicit presentation compatibility and its numeric Vina-output
coherence check. Its qualified profile at fb6382f6bf617467f4a3fb1dbc4fc28dc2815b71
uses the earlier provider 128a0bbb94e6804f5663e58a45313c77de1cc30d. New namespace
and stage-composition receiving must retain its own version evidence.

## Scope and evidence

The four-module provider selection passed 138 tests in 11.29 seconds on
2026-10-24 with twelve workers and Pytest Receptor, without failures/skips/warnings:

```bash
python -m pytest tests/basic/test_compose_atom_maps.py tests/build/test_merge_nonpolar_hydrogens.py tests/build/test_project_atom_names.py tests/form/file_pdbqt/test_known_source_poses.py --receptor=llm -n 12
```

Correspondence is declared, not authenticated or discovered chemically.
H5MSM 0.5 still excludes MolecularMechanics; maps remain typed sidecars.
General full-system permutation is owned separately by uibcdf/molsysmt#369.
No historical scientific search, external production migration, release or
biological preparation validation is implied by this provider completion.
