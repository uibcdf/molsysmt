# MolSysMT Roadmap

This document outlines the planned architectural evolutions and major features for MolSysMT.

## Architecture: Decorator-based Dependency Management

We have transitioned to a robust, introspection-friendly dependency management system using **Smart Decorators**.

**Status:** IMPLEMENTED (Phase 1)

**Achievements:**
- **Zero-Cost Startup:** Soft dependencies are no longer imported at startup.
- **Robustness:** Added `@requires` decorator and `check_dependency` to prevent crashes when libraries are missing.
- **Dynamic Discovery:** Redesigned `molsysmt.form` to load modules lazily and support user-defined visibility filtering.
- **Single Source of Truth:** Centralized dependency status in `molsysmt/config/dependencies.py`.

**Next Steps (Phase 2 - Coverage & Validation):**
- [ ] **Comprehensive Form Mapping:** Ensure every directory in `molsysmt/form/` that depends on a soft library is mapped in `molsysmt/config/dependencies.py`.
- [ ] **Full Decorator Coverage:** Sweep all conversion modules (`to_*.py`, `extract.py`) and apply `@requires` to all soft-dependency functions.
- [ ] **Automated Architecture Tests:** Create scripts to detect:
    - Top-level imports of soft dependencies.
    - Unmapped form directories.
- [ ] **Integration Tests:** Verify that `msm.config.show_all_capabilities` correctly filters the registry when libraries are missing.
- [ ] **Help Integration:** Update `msm.info()` and `msm.help()` to utilize decorator metadata for informing users about missing libraries.

---

## Planned Improvements
- [ ] Expansion of native topology and structure attributes.
- [ ] Integration with advanced MD analysis protocols.