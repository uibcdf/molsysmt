---
summary: Large molecular strings enter unbounded filename extension detection.
issue: uibcdf/molsysmt#149
status: resolved
opened: 2026-08-13
closed: 2026-08-13
severity: high
verification: measured
area: [form, convert, performance]
guard: tests/form/test_catalogue_extension_detection.py
normative:
blocked_by: []
supersedes: []
---

# Known source forms and bounded detection of large molecular strings

**Status:** proposed from a MolSysViewer integration benchmark  
**Owner:** MolSysMT (`get_form()` and `convert()`)

## What was observed

MolSysViewer generated a 95,000-atom PDB string for an endpoint-isolation
benchmark and converted it with:

```python
msm.convert(pdb_text, to_form="molsysmt.MolSys")
```

Before parsing began, generic form detection spent more than seven minutes in
`get_form() -> _detect() -> catalogue.form_of_extension()`. The extension
helper lowercases and splits the complete coordinate-rich payload on `.`, as if
the in-memory PDB text were a possible path. `skip_digestion=True` does not
bypass this because `convert()` always discovers `from_form` itself.

The direct known-form converter avoids the unrelated work, but importing
`molsysmt.form.string_pdb_text.to_molsysmt_MolSys` is not a suitable public
integration contract.

## Why two changes are appropriate

1. Generic detection should be fast for ordinary users who do not know the
   source form. A large molecular content string must not first be tokenized as
   a filename.
2. Infrastructure that knows a representation by construction should be able
   to declare it explicitly, avoiding heuristic detection and private imports.

The first fixes the default path. The second provides a deterministic expert
path. Neither replaces the other.

## Proposed changes

### Bounded, content-aware string detection

Refine `get_form()` so likely content is considered before extension lookup.
At minimum:

- line-bearing molecular text does not enter whole-string extension parsing;
- extension matching examines a bounded filename suffix rather than splitting
  the complete input;
- compact identifiers, paths and compressed extensions retain their behavior;
- the selected form plugin still confirms the candidate with `is_form()`;
- preliminary classification does not copy or tokenize the complete payload.

The exact heuristic remains a MolSysMT design decision. Structural bounds are
more important than a machine-specific timing threshold.

### Public explicit source-form hint

Extend `convert()` with an optional argument consumed by `convert()` itself:

```python
msm.convert(
    pdb_text,
    from_form="string:pdb_text",
    to_form="molsysmt.MolSys",
)
```

Required semantics:

- `from_form=None` preserves autodetection;
- a supplied form is canonicalized and validated against the form catalogue;
- its plugin may verify compatibility, but no global detector sweep or
  extension heuristic runs;
- an incorrect declaration fails observably and never falls back silently;
- multiple inputs receive explicit, unambiguous homogeneous/heterogeneous
  semantics or are rejected until those semantics are designed;
- `skip_digestion` remains independent and does not become an implicit trust
  flag.

Because `convert()` accepts `**kwargs`, the new argument must be explicit so it
cannot be forwarded accidentally to a converter.

## Acceptance evidence

1. A large generated PDB string resolves as `string:pdb_text` without full
   payload extension processing.
2. Extension classification has bounded auxiliary memory for content with many
   decimal points.
3. Explicit `from_form` reaches the expected converter without global
   `get_form()`.
4. A false source declaration raises a diagnostic error.
5. Existing IDs, paths, compressed paths and short molecular strings retain
   their classifications.
6. Multiple-input behavior is covered explicitly.
7. Detection time and parser time are reported separately for small and
   protein-scale fixtures.

Mutation checks should remove the content-before-extension branch, ignore the
explicit source hint, and permit a false declaration to fall back. Each
mutation must make its corresponding test fail.

## Downstream adoption

Once released, MolSysViewer will replace its benchmark-only private converter
import with public `msm.convert(..., from_form="string:pdb_text")`. Production
callers should provide the hint only where a validated protocol or constructor
guarantees the representation; arbitrary user inputs remain on autodetection.

This proposal does not introduce ViewerJSON or change the scientific object
held by MolSysViewer. It only improves how an existing MolSysMT conversion
identifies its input representation.

## Resolution — 2026-08-13

The pre-1.0 defect is resolved at the default boundary. Multiline molecular
content is rejected before extension matching, and path matching now copies
only slices bounded by the longest registered extension. The form adapter still
confirms any extension-index candidate through `is_form()`.

The guard uses an approximately one-megabyte, decimal-rich candidate and
observes every slice: no slice can exceed the longest extension plus its dot.
It also proves that multiline content is neither lowercased nor sliced, and
protects compact IDs, ordinary paths, and compressed compound extensions.

The explicit `from_form=` expert path was deliberately separated rather than
silently expanding this bug fix. It remains open as uibcdf/molsysmt#151 in
`devguide/pending_proposals/add_an_explicit_source_form_hint_to_convert.md` and
does not block 1.0.
