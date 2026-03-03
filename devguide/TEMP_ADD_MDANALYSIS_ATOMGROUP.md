# MolSysMT v1.0.0 — New Form: MDAnalysis.AtomGroup

This checklist tracks the implementation of the `MDAnalysis.AtomGroup` form.

## 🏗️ Scaffolding
- [ ] Create directory `molsysmt/form/MDAnalysis_AtomGroup/`.
- [ ] Implement `is_form.py` (Must recognize MDAnalysis AtomGroup objects).
- [ ] Implement `__init__.py` with metadata and lazy conversion mapping.

## 🔄 Converters
- [ ] Implement `to_molsysmt_Topology.py`.
- [ ] Implement `to_molsysmt_MolSys.py`.
- [ ] Implement `to_MDAnalysis_Universe.py` (Useful for round-trip).

## 🔍 Getters & Methods
- [ ] Implement `get.py` (Delegating or native extraction).
- [ ] Implement `has_attribute.py`.
- [ ] Implement `extract.py`.

## 🧪 Validation
- [ ] Create a test case in `tests/form/MDAnalysis_AtomGroup/`.
- [ ] Verify with Tier 1 Contract Tests.
