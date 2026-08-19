---
summary: supported.forms() and info() return only styled tables, with no programmatic result.
issue: uibcdf/molsysmt#188
status: open
opened: 2026-08-19
closed:
verification: measured
area: [api, basic]
guard:
normative:
blocked_by: []
supersedes: []
---

# Proposal: the introspection surface should return data, not only a rendering

**Raised:** 2026-08-19, during an external audit, on the first attempt to enumerate the
supported forms from a script.
**Status:** proposed. No decision recorded yet on the shape of the return value.

## What

Every function in `molsysmt.supported`, and `molsysmt.info`, returns a
`pandas.io.formats.style.Styler` and nothing else. A `Styler` renders in a notebook and
is opaque everywhere else:

```bash
$ python -c "
import molsysmt as msm
print(len(msm.supported.forms()))"
TypeError: object of type 'Styler' has no len()
```

```bash
$ python -c "
import molsysmt as msm, inspect
for name in ('forms', 'conversions', 'syntaxes', 'dependencies'):
    f = getattr(msm.supported, name)
    print(f'{name:14} -> {type(f()).__name__}')
print('info           ->', type(msm.info(msm.systems['Trp-Cage']['1l2y.h5msm'])).__name__)"
forms          -> Styler
conversions    -> Styler
syntaxes       -> Styler
dependencies   -> Styler
info           -> Styler
```

The proposal is that each of these gains an `output_type` argument, defaulting to the
current styled table so nothing in a notebook or in the documentation changes, and
accepting at least a plain object — a list for `forms`, a `DataFrame` or dictionary for
the rest — so the same call can be used from a script, a test, or a downstream library.

## How

`molsysmt.get` already establishes the pattern and the vocabulary: `output_type` with
`'values'` and `'dictionary'`. Reusing it here costs no new concept.

The data exists in every case; only the wrapper is lost. `Styler.data` holds the
underlying frame today, which means the fix is a return-path decision rather than a
recomputation, and it also means the current situation is worse than it looks: callers
who need the data reach through `.data` into pandas' rendering object, which is not a
stable interface and is not documented as one.

Ordering, applied to `msm.supported.forms` first: it is the entry point for the
capability the project leads with, and it is the one a downstream library needs.

## Why

**89 forms is the headline claim and there is no supported way to ask for the list.**
`README.md` builds its central table on the count. A user, a test, or a sibling package
that wants to iterate the forms — to check availability, to build a compatibility matrix,
to parametrise a suite — has to import pandas and read a private-by-convention attribute
of a rendering helper.

**The internal code does not use these functions.** `molsysmt/_private/form_tier.py`
holds `FORM_TIERS`, and the audit had to read that module directly to verify the README's
75/3/11 tier split, because the public function that reports the same information cannot
be counted. A public introspection API that the project's own verification cannot use is
not doing its job.

**It is a notebook-first assumption on a surface that is not notebook-only.** The rest of
the library is deliberately usable from scripts; `get` returns values, `select` returns
indices, `convert` returns objects. Introspection is the one corner where the return type
assumes a display.

Related but distinct: [#128](https://github.com/uibcdf/molsysmt/issues/128) asks for
`MolSys.info()` to shortcut `basic.info()`. That is about dispatch; this is about what
comes back.

## What is measured and what is assumed

Measured: the five return types above; the `TypeError` from `len()`; the presence of
`.data` on the returned `Styler`; the signatures, none of which accepts an output
argument.

Assumed — *estimate*: that `output_type` defaulting to the styled table preserves every
current caller. The documentation notebooks display the result of a bare call, and no
in-repository caller was found that depends on the return value being a `Styler`
specifically, but the course and cookbook notebooks were not exhaustively checked.

## What was refuted

*`msm.supported.forms()` has an undocumented plain mode.* It does not; its only
parameter is `form_type`, which filters rows.

*The information is available elsewhere in public form.* Not equivalently.
`msm.get_form` names the form of one object, and `_private.form_tier` is private. There
is no public enumeration.

## Scope and exclusions

Covers `molsysmt.supported.forms`, `conversions`, `syntaxes`, `dependencies`, and
`molsysmt.info`.

Excludes any change to what those tables contain, and excludes their rendering, which is
good and should stay the default. Excludes `msm.view` and other genuinely display-only
entry points. Excludes the docstring quality of these functions, which is
[#187](https://github.com/uibcdf/molsysmt/issues/187) — though `forms` is one of the
affected symbols, and the two fixes meet in the same signature.

## Acceptance criteria

1. Each named function accepts `output_type` and returns a plain Python or pandas object
   when asked, with the styled table as the default.
2. A test enumerates the supported forms through the public API and compares the result
   with `molsysmt/_private/form_tier.FORM_TIERS`, so the public count and the private
   registry cannot diverge silently.
3. `devguide/support_tier_protocol.md` points at the public call rather than the private
   module for the question *"which forms are supported"*.

## Dependencies and risks

Low. The main risk is a documentation notebook that renders the result of a bare call
and would be unaffected by an added keyword with a preserving default.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `b9a2098e4`, pandas 2.3.3.
