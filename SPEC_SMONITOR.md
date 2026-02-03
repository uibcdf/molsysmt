# SPEC_SMONITOR.md — Centralized Diagnostic & Telemetry System

**Version:** v0.1 (Draft)  
**Status:** CONCEPT  
**Author:** UIBCDF Development Team  
**Project Name:** `monitor`

## 1. Motivation & Vision

Currently, the UIBCDF ecosystem (MolSysMT, TopoMT, ArgDigest, DepDigest, PyUnitWizard) operates as a collection of independent modules. While each handles its own logging, warnings, and errors, the resulting output is often fragmented, redundant, or lacks global context.

**Monitor** is designed to be the **Central Nervous System** of the suite. Its mission is to capture, coordinate, and present all internal events (logs, warnings, exceptions, and telemetry) in a unified, traceable, and user-friendly manner.

### Core Goals:
1.  **Orchestration**: Provide a single point of configuration for the diagnostic behavior of all sibling libraries.
2.  **Traceability**: Maintain a "call-chain" context (e.g., knowing that an error in `PyUnitWizard` originated from an `@arg_digest` call inside `msm.convert`).
3.  **Aesthetics & Clarity**: Leverage modern terminal formatting (like `rich`) to produce beautiful, readable, and informative reports.
4.  **Symmetry**: Follow the design patterns established by `arg_digest` and `dep_digest` for developer familiarity.

---

## 2. Architecture

The library is structured into four main layers:

```
monitor/
  core/
    manager.py      # The global engine (Singleton dispatcher)
    decorator.py    # The @signal decorator logic
    context.py      # Call-stack and execution metadata (The Breadcrumbs)
  emitters/
    log.py          # Integration with Python's standard logging
    warn.py         # Interceptor for warnings.warn()
    error.py        # Exception enhancement and coordination logic
  handlers/
    console.py      # Rich terminal output (colors, tables, source code)
    file.py         # Standard logging output to disk
    json.py         # Structured data for automated audits and telemetry
  config/
    discovery.py    # Auto-resolves _monitor.py in project roots
```

---

## 3. Public API

### 3.1 The `@signal` Decorator
The primary way to connect a function to the diagnostic system.

```python
from smonitor import signal

@signal
def my_function(item, selection='all'):
    # This function is now monitored. 
    # Any log, warning, or error inside (even in dependencies) will be tagged with this context.
    ...
```

### 3.2 Global Configuration
A single call to rule them all.

```python
import smonitor

smonitor.configure(
    level='INFO',          # Global verbosity
    theme='rich',          # Use colors, tables, and enhanced formatting
    capture_warnings=True, # Intercept all warnings.warn()
    trace_depth=3,         # How many levels of parent-calls to show
    show_traceback=True    # Enhanced error context
)
```

---

## 4. Key Features

### 4.1 Nested Traceability (The "Breadcrumb" Trail)
When an event occurs, `monitor` reports the path of execution:
`[molsysmt.convert] -> [arg_digest] -> [pyunitwizard] | ERROR: Invalid Unit`

### 4.2 Standardized Warning Redirection
Instead of messy Python warnings, `monitor` intercepts them and presents them as organized, high-value entries:
`MOLSYSMT | WARNING (selection.py:42): Selection string is ambiguous. Hint: Use 'atom_name:...'`

### 4.3 Telemetry & Health Reports
The system can produce a summary of the session or health statistics on demand:
```python
smonitor.report()
# Output:
# Functions called: 124
# Warnings issued: 2 (1 in molsysmt, 1 in argdigest)
# Errors encountered: 0
# Peak memory: 450MB
```

### 4.4 Symmetry with the "Digest" family
`monitor` will automatically find a `_monitor.py` file in the project root to load library-specific diagnostic rules, hints, and formatting preferences.

---

## 5. Integration Strategy

To implement `monitor` across the UIBCDF suite:

1.  **Phase 1: Base Library**: Build the core manager, the `@signal` decorator, and the context tracker.
2.  **Phase 2: Emitter Injection**: Replace standard `logging` and `warnings` calls in `argdigest`, `depdigest`, etc., with `monitor.emit()`.
3.  **Phase 3: MolSysMT Adoption**: Use `monitor` as the primary engine for `msm.config.setup_logging()`.
4.  **Phase 4: Automated Documentation**: Integrate with Sphinx to show which functions are monitored and what signals they emit.

---

## 6. Future Ideas

- **Live Dashboard**: A tiny web or terminal dashboard showing real-time execution signals and library health.
- **AI-Agent Instructions**: Export signals as machine-readable instructions for LLM agents to better debug the library state.
- **Performance Profiling**: Combine diagnostics with time-tracking to identify bottlenecks in the call-stack without heavy external profilers.

---

> **Tagline:** `smonitor` — The precision telemetry system for the scientific Python stack.
