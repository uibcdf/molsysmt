<!--
SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.
Canonical source: https://github.com/uibcdf/ackredit/blob/main/standards/ACKREDIT_GUIDE.md
-->

# Ackredit Integration Guide

Source of truth for integrating **Ackredit** into a host library, following the
**MolSysSuite** standards.

## What is Ackredit

Ackredit records which algorithms, datasets and dependencies a run **actually reached**,
and turns that into a citation report with full provenance.

It exists against the alternative: asking users to cite a whole library because they
installed it. A run that never took the iterative branch should not cite the iterative
paper, and a list built from what a library *contains* cannot make that distinction.

## Why this matters in this library

- **Your work gets cited for what it did.** Papers, datasets and methods your library
  rests on are credited when the code that needs them runs, not when someone imports you.
- **Your users stop guessing.** They receive a bibliography in BibTeX, CSL-JSON, LaTeX or
  Markdown, covering your library and everything under it.
- **Provenance, not a list.** The report says which of your functions led to which
  citation, including citations that arrived through a library you call.
- **Nothing breaks without it.** Ackredit is an optional dependency, and the pattern in
  section 1 is what keeps your library working when it is absent.

## 1. Centralization File: `_ackredit.py`

Every host library should have a `_ackredit.py` file in its main package directory to centralize Ackredit's configuration and handle it as an optional dependency.

The single rule this file exists to enforce: **the host keeps working when Ackredit is absent**. Every name it exports must therefore have a fallback with the *same signature* as the real one, or the host will break precisely in the case the pattern was meant to protect.

### Template for `_ackredit.py`:

```python
"""Ackredit integration for this library.

Ackredit is an optional dependency. This module must import cleanly and expose the
same names whether or not it is installed.
"""

try:
    import ackredit
    from ackredit import (
        add_injection,
        bind,
        bound_items,
        credit_bound,
        register_item,
        report,
        scope,
        scoped_usage,
        track_item,
    )

    ACKREDIT_INSTALLED = True

except ImportError:
    ACKREDIT_INSTALLED = False
    ackredit = None

    def register_item(**item):
        pass

    def bind(target, items):
        pass

    def bound_items(target):
        return []

    def add_injection(target_module, items):
        pass

    def credit_bound(target):
        return []

    def track_item(item_id, used_by=None):
        pass

    def scoped_usage(target, credit_bound=False):
        def deco(fn):
            return fn

        return deco

    class scope:
        def __init__(self, name, credit_bound=False):
            self.name = name

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    def report(format="markdown", **kwargs):
        return "Ackredit is not installed."
```

Note what the fallbacks return: `bound_items` and `credit_bound` return an empty list, not `None`, so host code that iterates their result behaves identically in both modes. `scope` is a class, because it is used as a context manager.

## 2. Static Registration

In your host library's `__init__.py` or a dedicated setup file, register your items and bindings using the centralized `_ackredit.py`:

```python
from ._ackredit import bind, register_item

register_item(
    id="molsysmt:software",
    type="software",
    title="MolSysMT",
    authors=["Prada-Gracia, Diego", "Moreno-Vargas, Liliana M."],
    doi="10.5281/zenodo.1298752",
)

bind(target="molsysmt.basic.convert", items=["molsysmt:software"])
```

Copy the fields from the work's own record — its `CITATION.cff`, its DOI, its published
author list — and never write one from memory. In particular, **never write a truncation
as a name**. Putting `"et al."` at the end of the list makes BibTeX credit a person
surnamed "al." with the given name "et", and that reaches a manuscript. List the authors,
and let the bibliography style decide how many of them to print.

## 3. Dynamic Tracking

Use the decorators and tracking functions in your modules:

```python
from .._ackredit import scoped_usage, track_item


@scoped_usage(target="molsysmt.basic.convert")
def convert(item, to_form):
    track_item("molsysmt:software")
    # implementation...
```

`bind` declares what a target *may* require; it credits nothing on its own. When a function's citations do not depend on the code path taken, let the binding carry them instead of repeating the ids in the body:

```python
from .._ackredit import scoped_usage, track_item


@scoped_usage(target="molsysmt.basic.convert", credit_bound=True)
def convert(item, to_form, method="default"):
    # the bound items are credited on every call
    if method == "experimental":
        track_item("molsysmt:paper:2026:experimental")
```

## 4. Reporting

Expose a reporting function for the end user:

```python
from ._ackredit import report


def cite(format="markdown"):
    return report(format=format)
```

## 5. Advanced Features

These call the module directly, which is why the template imports `ackredit` as well as the individual names. Guard them with `ACKREDIT_INSTALLED`, because the fallback binds `ackredit` to `None`.

### Auto-Discovery of Dependencies

If your library uses external packages (like `mdtraj`) and you want Ackredit to track them automatically, enable the hooks early in your initialization — before your `__init__` imports the submodules that import those packages:

```python
from ._ackredit import ACKREDIT_INSTALLED, ackredit

if ACKREDIT_INSTALLED:
    ackredit.enable_import_hooks()
```

Discovery sees imports that happen after it is enabled; a package already loaded is not
discovered. Ackredit loads **numpy** itself through ArgDigest (until
`uibcdf/argdigest#15`), so discovery never sees numpy. For a package that may already be
loaded, register its citation and declare an injection: an injection is credited whether
its package was imported before the hooks or after.

```python
if ACKREDIT_INSTALLED:
    # "numpy:paper:2020" registered from the work's own record, as in Static Registration.
    ackredit.add_injection("numpy", ["numpy:paper:2020"])
```

### Session Persistence

For long-running scientific workflows, you can ensure no citation is lost even if the script crashes:

```python
from ._ackredit import ACKREDIT_INSTALLED, ackredit

if ACKREDIT_INSTALLED:
    ackredit.enable_persistence("ackredit_session.json")
```

## 6. Check that the integration is live

The `try`/`except ImportError` above is deliberately silent, so a host with Ackredit installed but mis-integrated looks exactly like a host without it: everything succeeds and nothing is ever recorded.

Do not let that state pass unnoticed. Expose the flag, and assert it where it matters:

```python
from ._ackredit import ACKREDIT_INSTALLED


# in the host's test suite, when ackredit is a test dependency
def test_ackredit_integration_is_active():
    assert ACKREDIT_INSTALLED
```

If `ACKREDIT_INSTALLED` is `False` while `pip show ackredit` succeeds, the import in `_ackredit.py` is raising `ImportError` for some other reason and being swallowed. Reproduce it by importing the names outside the `try` block.

By following this pattern, the host library remains functional even if Ackredit is not installed, while providing full citation support for users who have it.

## Required behavior (non-negotiable)

1.  **The host works without Ackredit.** Every name `_ackredit.py` exports has a fallback
    with the *same signature* as the real one. A fallback that has drifted breaks your
    library precisely in the case the pattern exists to protect.
2.  **Declare at import, credit at runtime.** `register_item` and `bind` say what *could*
    be cited and belong at import time. `track_item` says what *was* used and belongs in
    the code path that used it. Crediting at import is the behaviour Ackredit replaces.
3.  **Bind the unconditional, track the conditional.** If a citation depends on the path
    taken, call `track_item` on that branch. `credit_bound=True` is for the coarse case
    and credits on every call, which is why it is opt-in.
4.  **Never write a truncation as a name.** `"et al."`, `"and others"` and `"..."` are
    rendering decisions, not people. Written into `authors`, BibTeX turns them into a
    person and the bibliography credits someone who does not exist.
5.  **Do not silence the integration.** The `try`/`except ImportError` is deliberately
    quiet, so a host with Ackredit installed but mis-integrated is indistinguishable from
    one without it. Assert `ACKREDIT_INSTALLED` where it matters — section 6.

## SMonitor Integration

Ackredit's diagnostics are catalog-driven, so a host sees stable codes rather than
free-form messages, and nothing is swallowed. The ones a host is most likely to meet:

| code | when |
| --- | --- |
| `ACKREDIT-W004` | a `CITATION.cff` it found could not be parsed |
| `ACKREDIT-W005` | no citation information could be discovered for a package |
| `ACKREDIT-W006` | DOI metadata could not be fetched, so an item is reported with what is known |
| `ACKREDIT-W008` | a citation plugin from another package failed to load |
| `ACKREDIT-W011` | `pdflatex` is absent, so no PDF was produced |
| `ACKREDIT-E004` | a report format that does not exist was requested |

Each carries the typed facts of its occurrence, so a host can filter or report them
through its own SMonitor integration. `ackredit.dependency_info()` reports which optional
features the environment supports.

## Worked examples

The Ackredit repository carries two host libraries under `examples/` that integrate it
exactly as described here — `dummy_solver`, and `dummy_pipeline` which calls it, so
citations cross a library boundary. Their `_ackredit.py` is this document's template,
asserted byte-identical by the test suite, so what you read here is what runs there.
