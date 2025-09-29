# MolSysMT Warning System — Developer Guide

This document explains how to **emit, categorize, filter, and test** warnings in MolSysMT. It covers the recommended categories, parametrized warnings, helpers, configuration, deprecations, and testing patterns.

> **Target Python**: 3.10+

---

## 1) Why custom warnings?

- We avoid noisy prefixes like `"[MolSysMT Warning]"`.  
- The **warning category** itself communicates origin and intent (and is filterable by users).

---

## 2) Categories

All categories inherit from `UserMolSysMTWarning`:

```python
# molsysmt/warnings.py (excerpt)
import warnings
from typing import Type, Iterable

class UserMolSysMTWarning(Warning):
    # Base class for user-facing warnings in MolSysMT.
    pass

class FileFormatWarning(UserMolSysMTWarning):
    # Parsing/metadata/IO-related warnings.
    pass

class SelectionWarning(UserMolSysMTWarning):
    # Selection string / subset resolution warnings.
    pass

class PerformanceWarning(UserMolSysMTWarning):
    # Potentially expensive operations / degraded performance.
    pass

class MolSysMTDeprecationWarning(DeprecationWarning):
    # API deprecations for MolSysMT.
    pass
```

---

## 3) Emitting warnings (two patterns)

### A. Simple message (most cases)

Use `warnings.warn` with an appropriate category:

```python
import warnings
from molsysmt.warnings import FileFormatWarning

warnings.warn(
    "Missing CRYST1 line; no box parsed.",
    FileFormatWarning,
    stacklevel=2,  # points at the caller line
)
```

**When to use**: the message is a one-off string; you don’t need to format complex parameters repeatedly.

### B. Parametrized warning class (centralized formatting)

Define a warning that builds its message in `__init__`:

```python
from typing import Iterable

class TopologyWarning(UserMolSysMTWarning):
    def __init__(
        self,
        n_bonds: int,
        chains: Iterable[str] | None = None,
        *,
        source: str = "struct_conn",
        context: str | None = None,
    ):
        self.n_bonds = n_bonds
        self.chains = tuple(chains) if chains else None
        self.source = source
        self.context = context

        msg = f"{n_bonds} covalent bond(s) reported by '{source}'"
        if self.chains:
            msg += f" between chains {list(self.chains)}"
        msg += " were added."
        if self.context:
            msg += f" (context: {self.context})"

        super().__init__(msg)
```

Usage:

```python
import warnings
from molsysmt.warnings import TopologyWarning

warnings.warn(TopologyWarning(n_bonds=3, chains=["A", "B"], context="read_cif()"), stacklevel=2)
```

**When to use**: the same warning is emitted in multiple places with varying parameters; centralizing formatting reduces duplication and keeps messages consistent.

---

## 4) Helpers: `warn` and `warn_once` (optional convenience)

We provide thin wrappers to standardize `stacklevel` and suppress duplication.

```python
from typing import Type

__WARNED_ONCE_CACHE__: set[tuple[Type[Warning], str]] = set()

def warn(message_or_warning: str | Warning,
         category: Type[Warning] | None = None,
         *,
         stacklevel: int = 2) -> None:
    import warnings
    if isinstance(message_or_warning, Warning):
        warnings.warn(message_or_warning, stacklevel=stacklevel)
    else:
        warnings.warn(message_or_warning, category or UserMolSysMTWarning, stacklevel=stacklevel)

def warn_once(message_or_warning: str | Warning,
              category: Type[Warning] | None = None,
              *,
              stacklevel: int = 2) -> None:
    import warnings
    if isinstance(message_or_warning, Warning):
        msg, cat = str(message_or_warning), type(message_or_warning)
    else:
        msg, cat = message_or_warning, category or UserMolSysMTWarning

    key = (cat, msg)
    if key in __WARNED_ONCE_CACHE__:
        return
    __WARNED_ONCE_CACHE__.add(key)
    warnings.warn(message_or_warning, cat, stacklevel=stacklevel)
```

**Examples**

```python
from molsysmt.warnings import warn, warn_once, SelectionWarning

warn("Unknown tokens in selection; ignoring.", SelectionWarning)

for _ in range(100):
    warn_once("Falling back to slow path; consider pre-alignment.", PerformanceWarning)
```

---

## 5) Choosing `stacklevel`

- Use `stacklevel=2` so the traceback points to **the caller** (your API’s surface), not the internal utility emitting the warning.
- If you wrap warnings in deeper helpers, you may need `stacklevel=3+`. Verify with a quick run to ensure the location shown is helpful to end users.

---

## 6) Filtering and configuration (package & user)

We **don’t** force filters in `warnings.py`. Suggested defaults (opt-in) in `molsysmt/__init__.py`:

```python
# molsysmt/__init__.py
import warnings
from .warnings import UserMolSysMTWarning, MolSysMTDeprecationWarning

warnings.simplefilter("default", UserMolSysMTWarning)         # show user warnings at least once
warnings.simplefilter("default", MolSysMTDeprecationWarning)  # make deprecations visible
```

**User-side control** (in scripts or notebooks):

```python
import warnings
from molsysmt.warnings import PerformanceWarning, TopologyWarning

warnings.simplefilter("ignore", PerformanceWarning)  # silence performance warnings
warnings.simplefilter("always", TopologyWarning)     # always show topology warnings
warnings.simplefilter("error", FileFormatWarning)    # treat IO issues as errors
```

Common actions:
- `"ignore"`: hide a category
- `"default"`: show first occurrence per location (Python default behavior)
- `"once"`: show only once per process
- `"always"`: show every time
- `"error"`: convert to exceptions (useful in CI)

---

## 7) Deprecation policy

Use `MolSysMTDeprecationWarning` for API removals/renames. Provide guidance and a horizon:

```python
import warnings
from molsysmt.warnings import MolSysMTDeprecationWarning

warnings.warn(
    "Function `old_api()` is deprecated and will be removed in v2.0; use `new_api()` instead.",
    MolSysMTDeprecationWarning,
    stacklevel=2,
)
```

**Guidelines**
- Include the alternative API.
- Include a timeline (e.g., removal in vX.Y).
- Consider gating with an environment variable for early adopters (optional).

---

## 8) Message style guide

- **Actionable**: say what happened and what to do, if applicable.  
- **Compact**: one sentence when possible; link or reference docs for details.  
- **Context**: include small context (e.g., file, function) when it helps.  
- **No prefixes** like `[MolSysMT Warning]` — the category is the origin.

Examples:
- Good: *"Missing CRYST1 line; no box parsed. (file: my.pdb)"*  
- Good: *"3 covalent bond(s) reported by 'struct_conn' between chains ['A', 'B'] were added."*  
- Avoid: *"[MolSysMT Warning] Something happened."*

---

## 9) Testing warnings (pytest)

### A. Expect a warning

```python
import pytest
import warnings
from molsysmt.warnings import FileFormatWarning

def test_missing_cryst1_emits_warning():
    with pytest.warns(FileFormatWarning, match="Missing CRYST1"):
        # call the function that should warn
        parse_pdb("tests/data/no_cryst1.pdb")
```

### B. No warning expected

```python
def test_clean_file_no_warning(recwarn):
    parse_pdb("tests/data/clean.pdb")
    assert not recwarn  # no warnings captured
```

### C. Convert to errors in CI (optional)

In `pytest.ini`:

```ini
[pytest]
filterwarnings =
    error::molsysmt.warnings.FileFormatWarning
    default::molsysmt.warnings.UserMolSysMTWarning
    default::molsysmt.warnings.MolSysMTDeprecationWarning
```

Or in a specific test:

```python
def test_treat_file_issues_as_errors(monkeypatch):
    import warnings
    from molsysmt.warnings import FileFormatWarning
    warnings.simplefilter("error", FileFormatWarning)
    with pytest.raises(FileFormatWarning):
        parse_pdb("tests/data/bad_format.pdb")
```

---

## 10) Migration note (from `UserWarning` + text prefix)

**Before**  
```python
warnings.warn("[MolSysMT Warning] Added covalent bonds from struct_conn", UserWarning)
```

**After**  
```python
from molsysmt.warnings import TopologyWarning
import warnings

warnings.warn(TopologyWarning(n_bonds=1, chains=["A", "B"]))
```

No textual prefix is needed; the **category** is now `TopologyWarning`.

---

## 11) Quick reference (cheat sheet)

- **Pick a category**: `FileFormatWarning`, `SelectionWarning`, `PerformanceWarning`, `TopologyWarning`, `MolSysMTDeprecationWarning`.
- **Emit**: `warnings.warn("message", Category, stacklevel=2)` or `warnings.warn(CategoryClass(...), stacklevel=2)`.
- **Once only**: `warn_once("message", Category)` or `warn_once(CategoryClass(...))`.
- **Filter**: `warnings.simplefilter("ignore"|"default"|"once"|"always"|"error", Category)`.
- **Test**: `with pytest.warns(Category, match="..."):`.

---
