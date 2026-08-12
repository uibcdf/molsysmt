---
summary: Built wheels omit the dynamic form catalogue
issue: uibcdf/molsysmt#145
status: active
opened: 2026-08-12
closed:
severity: high
verification: reproduced
area: [build, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Built Wheels Omit the Dynamic Form Catalogue

**Reported:** 2026-08-12, by the installed public-runtime jobs in the first exact-commit
1.0 candidate wheel campaign, GitHub Actions run `31572599515`.
**Status:** Active; the cause is reproduced from the generated Linux wheel and the
packaging contract is being repaired.

## What

All five platform wheels build and their private Rust extensions load, but a clean
installation cannot classify even a bundled H5MSM system. The public smoke fails on
Python 3.11, 3.12 and 3.13 with `ArgumentError` at the first `msm.convert()` call.

```bash
gh run view 31572599515 --log-failed
gh run download 31572599515 -n molsysmt-linux-x86_64-abi3 -D /tmp/molsysmt-wheel
python devtools/scripts/validate_installed_molsysmt.py
```

## How

`molsysmt/form/catalogue.py` discovers forms exclusively from the generated
`molsysmt/form/*/form.json` declarations. `pyproject.toml` sets
`include-package-data = false` and only declared `py.typed` and `molsysmt.data` as
package data. The generated wheel therefore contains the bundled H5MSM file but none of
the 89 form declarations. The catalogue is empty in an installed distribution, so
`get_form()` rejects every molecular-system form.

The correction must package every declaration and make the static wheel validator
compare the wheel contents against every declaration present in the source tree. A
single sentinel file is insufficient because a partially packaged catalogue would fail
only for selected forms.

## Why

This is high severity because source and editable installations work while every built
wheel is functionally unable to recognize supported forms. The binary extension and
static wheel checks still pass, creating a misleadingly healthy release artefact.

## What is measured and what is assumed

Measured from the Linux x86_64 artefact in run `31572599515`:

- `molsysmt/data/h5msm/1l2y.h5msm` is present and has the expected HDF5
  `type='h5msm'` attribute;
- `molsysmt/form/file_h5msm/form.json` is absent;
- no `molsysmt/form/*/form.json` entry is present;
- the public smoke fails identically on Python 3.11, 3.12 and 3.13.

No estimate is used in the diagnosis.

## What was refuted

- The H5MSM payload is not absent or corrupt: it is present in the wheel and opens with
  `h5py` with the expected type marker.
- The Rust abi3 extension is not implicated: its installation checks pass across the
  platform and Python matrices.
- The H5MSM detector is not failing on its contents: the catalogue cannot locate any
  detector because its declarations are missing.

## Scope and exclusions

This report covers inclusion and static validation of the generated form declarations,
plus the existing installed public-runtime smoke. It does not cover Conda recipes or
the independent availability of sibling packages on the `uibcdf` channel.

## Acceptance criteria

- A freshly built wheel contains every `molsysmt/form/*/form.json` declaration present
  in the source tree.
- `devtools/scripts/validate_rust_wheel.py` rejects a wheel missing any declaration.
- `devtools/scripts/validate_installed_molsysmt.py` passes from outside the checkout on
  Python 3.11, 3.12 and 3.13.
- The multiplatform abi3 build remains green.

## Dependencies and risks

The package-data glob must remain narrow: it should include generated `form.json` files,
not caches or arbitrary files under form packages. This work has no dependency on the
Conda publication track.

## Provenance

GitHub Actions run `31572599515`, candidate
`7cedab74a172f7391468ba239b1f87937898cc83`, Linux x86_64 wheel
`molsysmt-0.21.0+325.g7cedab74a-cp311-abi3-manylinux_2_28_x86_64.whl`, inspected on
2026-08-12. The failing installed smoke covered CPython 3.11, 3.12 and 3.13.
