# MolSysMT v1.0.0 — MDTraj Integration Stabilization

This checklist tracks the sequential sanitization of MDTraj-related forms to ensure robust Lazy Loading and perfect attribute parity.

## 🧪 Technical Strategy
1. **Absolute Imports**: Switch from `from . import to_X` to `from molsysmt.form.Form.to_X import to_X`.
2. **Type Robustness**: Methods must check if input is a path (str), a handler, or a memory object.
3. **Internal MDTraj Reference**: Verify all `.n_atoms`, `.seek()`, etc., against the source in `../mdtraj`.

## 1. Form: `mdtraj.Topology`
- [x] Audit `molsysmt/form/mdtraj_Topology/`.
- [x] Fix `to_molsysmt_Topology.py` (Verify it handles MDTraj Topology objects only).
- [x] Ensure `get.py` / `get_topological_attributes.py` are robust.

## 2. Form: `mdtraj.Trajectory`
- [x] Audit `molsysmt/form/mdtraj_Trajectory/`.
- [x] Fix `to_molsysmt_MolSys.py`.
- [x] Ensure physical units (nm, ps) are correctly attached in `get.py`.

## 3. Form: `mdtraj.HDF5TrajectoryFile` (Critical)
- [x] Audit `molsysmt/form/mdtraj_HDF5TrajectoryFile/`.
- [x] Fix `extract.py` (Ensure it doesn't fail on `None` filename or closed handles).
- [x] Fix `get.py` (Ensure it uses `._handle.root...` correctly for file handlers).

## 4. Cross-Form Logic (Shortcuts)
- [x] Fix `molsysmt/form/file_h5/to_mdtraj_Trajectory.py` (Already using `mdtraj.load()`).
- [x] Fix `molsysmt/form/file_h5/to_openmm_Topology.py`.

## 5. Final Validation
- [ ] Run `pytest tests/basic/get/test_get_tier1_parity.py` -> Must be GREEN.
