# MolSysMT Roadmap

This document outlines the planned architectural evolutions and major features for MolSysMT.

## Architecture: Decorator-based Dependency Management

We have transitioned to a robust, introspection-friendly dependency management system using **Smart Decorators**.

**Status:** IMPLEMENTED (Phase 1 & Phase 2)

**Achievements:**
- **Zero-Cost Startup:** Soft dependencies are no longer imported at startup.
- **Robustness:** Added `@requires` decorator and `check_dependency` to prevent crashes when libraries are missing.
- **Dynamic Discovery:** Redesigned `molsysmt.form` to load modules lazily and support user-defined visibility filtering.
- **Single Source of Truth:** Centralized dependency status in `molsysmt/config/dependencies.py`.
- **Validation:** Added `scripts/validate_dependencies.py` to enforce architecture rules (Zero Top-Level Imports).
- **Coverage:** Extensive migration of form converters (`to_*.py`) and extractors (`extract.py`) to the `@requires` standard.

**Pending / Ongoing:**
- [ ] **100% Extract Coverage:** Continue applying `@requires` to `extract.py` in remaining forms (MDTraj, Parmed, Pytraj, etc.) as they are touched.
- [ ] **Integration Tests:** Add runtime tests to verify filtering behavior (e.g. mocking a missing library).
- [ ] **Help Integration:** Update `msm.info()` and `msm.help()` to utilize decorator metadata for informing users about missing libraries.

---

## Planned Improvements
- [ ] Expansion of native topology and structure attributes.
- [ ] Integration with advanced MD analysis protocols.