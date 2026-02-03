# MolSysMT Roadmap

This document outlines the planned architectural evolutions and major features for MolSysMT.

## Architecture: Decorator-based Dependency Management

We have transitioned to a robust, introspection-friendly dependency management system using **Smart Decorators**.

**Status:** IMPLEMENTED & OPTIMIZED

**Achievements:**
- **Zero-Cost Startup:** Soft dependencies are no longer imported at startup.
- **Robustness:** Added `@requires` decorator and `check_dependency` to prevent crashes when libraries are missing.
- **Dynamic Discovery:** Redesigned `molsysmt.form` to load modules lazily and support user-defined visibility filtering.
- **Single Source of Truth:** Centralized dependency status in `molsysmt/config/dependencies.py`.
- **Validation:** Added `scripts/validate_dependencies.py` to enforce architecture rules (Zero Top-Level Imports).
- **Coverage:** Extensive migration of form converters (`to_*.py`) and extractors (`extract.py`) to the `@requires` standard.
- **Integration Tests:** Verfied runtime filtering logic with `tests/test_dependencies_architecture.py`.
- **Performance:** Optimized `argdigest` integration to eliminate import-time bottlenecks.

**Pending / Ongoing:**
- [ ] **Help Integration:** Update `msm.info()` and `msm.help()` to utilize decorator metadata for informing users about missing libraries.

---

## Planned Improvements
- [ ] Expansion of native topology and structure attributes.
- [ ] Integration with advanced MD analysis protocols.