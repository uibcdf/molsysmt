# MolSysMT Infrastructure Audit & Remediation Plan

**Date:** February 6, 2026
**Status:** Review Complete
**Target:** Standardization with SMonitor, ArgDigest, DepDigest, and PyUnitWizard.

---

## 1. Comprehensive Audit Findings

### 1.1 SMonitor (Diagnostics & Telemetry)
**Status:** 🔴 **Critical Violations**

*   **Infrastructure**: ✅ Correctly configured (`_smonitor.py`, `catalog.py`, `meta.py` exist). `__init__.py` activates the system.
*   **Telemetry**: ❌ **Total Blackout**. No usage of `@signal` was found in the codebase. MolSysMT execution flow is invisible to the diagnostic breadcrumb system.
*   **String Hardcoding**: ❌ **Violated**. Multiple instances of `warnings.warn("Literal string...")` found in conversion modules (e.g., `form/file_bcif`, `form/openmm_Topology`).
*   **Catalog**: ⚠️ Incomplete. Lacks entries for specific IO warnings found in the code.

### 1.2 DepDigest (Dependency Management)
**Status:** 🟢 **Excellent**

*   **Adoption**: ✅ Extensive use of `@dep_digest` in `molsysmt.form`.
*   **Lazy Loading**: ✅ Correctly implemented. Imports happen inside decorated functions (e.g., `to_mdtraj_Trajectory`).
*   **Configuration**: ✅ `_depdigest.py` is well-defined with hard/soft split and custom exception class (`LibraryNotFoundError`).

### 1.3 ArgDigest (Argument Auditing)
**Status:** 🟡 **Good but Improvable**

*   **Adoption**: ✅ Key API functions like `convert` are decorated.
*   **Architecture**: ✅ Uses the scalable `package` style with individual digester modules in `_private/arg_digestion/argument/`.
*   **Integration**: ⚠️ Exception handling in digesters (e.g., `digest_selection`) manually raises `ArgumentError` instead of leveraging SMonitor's catalog for rich hints.

### 1.4 PyUnitWizard (Units & Quantities)
**Status:** 🟢 **Correct**

*   **Configuration**: ✅ `_pyunitwizard.py` establishes standard units and default forms/parsers.
*   **Usage**: ✅ Consistent use of the alias `puw` internally.

---

## 2. Remediation Plan

This plan aims to bring MolSysMT to the same level of architectural maturity as its underlying infrastructure libraries.

### Phase 1: "Turn on the Lights" (Telemetry)
**Goal:** Make MolSysMT visible in SMonitor's execution trace.

*   ✅ **Action 1.1**: Instrument `molsysmt.basic` API.
*   ✅ **Action 1.2**: Instrument complex converters in `molsysmt.form`.

### Phase 2: "Clean the Noise" (Hardcoded Warnings)
**Goal:** Enforce "Zero String Hardcoding" and centralize messages.

*   ✅ **Action 2.1**: Expand the Catalog.
*   ✅ **Action 2.2**: Refactor Code.

### Phase 3: "The Error Bridge" (ArgDigest ↔ SMonitor)
**Goal:** Richer user feedback for argument errors.

*   ✅ **Action 3.1**: Refactor `molsysmt.exceptions.ArgumentError` to support SMonitor codes.
*   ✅ **Action 3.2**: Update Digesters.
*   ✅ **Action 3.3**: Architectural cleanup: Move exceptions/warnings to `_private/smonitor/`.
*   ✅ **Action 3.4**: Update documentation (User and Developer guides).

### Phase 4: Final Polish and Legacy Cleanup

*   [ ] **Action 4.1**: Remove or deprecate `molsysmt/config/logging_setup.py` if redundant with `SMonitor`.
*   [ ] **Action 4.2**: Final audit of `_private/` to ensure no diagnostic logic remains outside `_private/smonitor/`.
*   [ ] **Action 4.3**: Update `topomt` and `elasnetmt` to match these standards.

