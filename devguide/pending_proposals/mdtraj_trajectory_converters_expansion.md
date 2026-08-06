# Expansion of `mdtraj.Trajectory` Form Converters (`file:*` and `string:*`)

**Raised:** 2026-08-06, during documentation review of `docs/content/user/tools/basic/convert.ipynb`.

## Context & Motivation

In `docs/content/user/tools/basic/convert.ipynb`, under section `## Supported conversions`, the tutorial illustrates how to query available conversion paths using `mdtraj.Trajectory` as the example source form:

```python
msm.supported.conversions(from_form='mdtraj.Trajectory', to_form_type='string')
msm.supported.conversions(from_form='mdtraj.Trajectory', to_form_type='file', as_rows='to')
```

Currently, the direct and transitive conversion routes from `mdtraj.Trajectory` to `string:*` (e.g. `string:pdb_text`, `string:amino_acids_3`, `string:fasta`) and `file:*` (e.g. `file:pdb`, `file:xtc`, `file:dcd`, `file:gro`, `file:h5msm`, `file:mmcif`) are minimal. Consequently, the interactive pandas/Styler output tables returned by `msm.supported.conversions()` show very few rows, giving a sparse impression of MolSysMT's conversion capabilities.

Adding and registering missing converters for `mdtraj.Trajectory` will not only expand actual conversion features for MDTraj users but will also enrich the tutorial tables in `convert.ipynb`.

## Proposal

1. **Implement & Register Converters for `mdtraj.Trajectory`**:
   - Add direct/transitive conversion support from `mdtraj.Trajectory` to target file forms (`file:pdb`, `file:dcd`, `file:xtc`, `file:gro`, `file:h5msm`, `file:mmcif`).
   - Add direct/transitive conversion support from `mdtraj.Trajectory` to target string forms (`string:pdb_text`, `string:amino_acids_1`, `string:amino_acids_3`, `string:fasta`).

2. **Ensure Transitive Dispatch Visibility**:
   - Verify that form routes delegating through intermediate native forms (`molsysmt.MolSys`, `molsysmt.Topology`, `molsysmt.Structures`) populate the capability matrix queried by `msm.supported.conversions()`.

3. **Documentation Enrichment**:
   - Re-execute `docs/content/user/tools/basic/convert.ipynb` once the converters are available so that the resulting tables present a comprehensive multi-path capability matrix.

## Acceptance Criteria

- `msm.supported.conversions(from_form='mdtraj.Trajectory', to_form_type='string')` displays multiple active target string forms.
- `msm.supported.conversions(from_form='mdtraj.Trajectory', to_form_type='file', as_rows='to')` displays multiple active target file forms.
- Regression tests added in `tests/form/mdtraj_Trajectory/` covering conversions to `file:*` and `string:*`.
