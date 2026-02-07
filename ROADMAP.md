# MolSysMT Roadmap

This document outlines the planned architectural evolutions and major features for MolSysMT.

## Architecture: Decorator-based Dependency Management

We have transitioned to a robust, introspection-friendly dependency management system using **Smart Decorators**.

**Status:** IMPLEMENTED & OPTIMIZED

**Achievements:**
- **Zero-Cost Startup:** Soft dependencies are no longer imported at startup.
- **Robustness:** Added `@dep_digest` (via `depdigest`) to prevent crashes when libraries are missing.
- **Dynamic Discovery:** Redesigned `molsysmt.form` to load modules lazily and support user-defined visibility filtering.
- **Single Source of Truth:** Centralized dependency status in `molsysmt/_depdigest.py`.
- **Validation:** Added `scripts/validate_dependencies.py` to enforce architecture rules.
- **Coverage:** Extensive migration of form converters and extractors.
- **Integration Tests:** Verified runtime filtering logic.
- **Performance:** Optimized `argdigest` and `execfile` for fast imports.
- **Introspection:** Added `msm.supported.dependencies()` to report ecosystem status to users.

**Pending / Ongoing:**
- [ ] Integration of dependency metadata into automated API documentation (Sphinx).

---

## Planned Improvements
- [ ] Expansion of native topology and structure attributes.
- [ ] Integration with advanced MD analysis protocols.
