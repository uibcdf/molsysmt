# MolSysMT Logging and Warning Redirection — Developer Guide

This document explains how MolSysMT integrates Python `warnings` with the `logging` system, how the redirection works, and how developers should use it.

---

## 1) Motivation

- Standard Python warnings show filename and line number, which can be noisy for end users.
- With `logging.captureWarnings(True)`, all warnings are routed into the logging system.
- This allows us to:
  - Format them consistently with MolSysMT logs
  - Redirect them to files or other handlers
  - Control visibility with logging levels

---

## 2) Implementation overview

Defined in `molsysmt/logging_setup.py`:

- Creates or gets a logger named `molsysmt`
- Attaches a `StreamHandler` (stderr by default) with formatter:

```
MOLSYSMT %(levelname)s | %(message)s
```

- Captures warnings:
  - `logging.captureWarnings(True)` redirects `warnings.warn(...)` to logger `py.warnings`
  - The `py.warnings` logger shares the same handler and formatter as `molsysmt`
  - Optionally, `warnings.formatwarning` is redefined so messages become:

```
CategoryName: message
```

(without filename:lineno prefix)

---

## 3) How developers should emit warnings

Continue to use Python's `warnings.warn` with the custom MolSysMT warning classes:

```python
import warnings
from molsysmt.warnings import TopologyWarning, FileFormatWarning

warnings.warn(TopologyWarning(n_bonds=3, chains=["A", "B"], context="read_cif()"))
warnings.warn("Missing CRYST1 line; no box parsed.", FileFormatWarning)
```

These will be redirected to logging and formatted consistently.

---

## 4) Logger configuration

Developers can call:

```python
from molsysmt.logging_setup import setup_logging
setup_logging(level="INFO", capture_warnings=True, simplify_warning_format=True)
```

This configures both `molsysmt` and `py.warnings` loggers.

---

## 5) Testing logging output

With pytest:

```python
import warnings
import logging
import pytest
from molsysmt.logging_setup import setup_logging
from molsysmt.warnings import FileFormatWarning

def test_warning_redirect_to_logging(caplog):
    setup_logging(level="WARNING")

    with caplog.at_level(logging.WARNING, logger="py.warnings"):
        warnings.warn("Missing CRYST1 line", FileFormatWarning)

    assert any("FileFormatWarning: Missing CRYST1 line" in rec.message for rec in caplog.records)
```

---

## 6) Good practices

- **Always** use MolSysMT warning classes (`TopologyWarning`, `FileFormatWarning`, etc.)
- **Do not** print or log warnings manually; always use `warnings.warn`
- **Rely on the redirection** to logging for consistent formatting
- For new warning categories, inherit from `UserMolSysMTWarning`

---

## 7) Example output

Code:

```python
import warnings
from molsysmt.logging_setup import setup_logging
from molsysmt.warnings import TopologyWarning

setup_logging()

warnings.warn(TopologyWarning(n_bonds=3, chains=["A", "B"]))
```

Output:

```
MOLSYSMT WARNING | TopologyWarning: 3 covalent bond(s) reported by 'struct_conn' between chains ['A', 'B'] were added.
```
