# `msm.info()` tables lost their zebra striping in the built documentation

**Reported:** 2026-08-03, while comparing a notebook against its compiled page.

**Status:** **RESOLVED (archived 2026-08-03).** Verified on a real rebuilt page,
not predicted. `docs/conf.py:79` sets `nb_execution_mode = "off"`, so the
documentation renders the *stored* outputs; re-executing the remaining notebooks
is documentation work, not an open defect. See *Verification* and *Remaining*.

**Severity:** presentation only. No incorrect result and no hidden failure. It
affects every documentation page that displays an `msm.info()` table, which is
the first table most readers of the documentation ever see.

## Symptom

In a Jupyter notebook, the output of `msm.info()` renders with alternating light
and dark rows. In the HTML compiled by Sphinx it renders flat. The notebook and
the page therefore no longer agree, and the same build shows striping on some
tables and not on others.

The published sites still show the striping because they were built before the
change: `https://www.uibcdf.org/molsysviewer/` is served from a `gh-pages` build
dated 2026-01-11.

## Cause

`msm.info()` returns a `pandas` **`Styler`**, not a `DataFrame`
(`molsysmt/basic/info.py:423`, `tmp_df.style.hide(axis='index')`, in place since
2021). A `Styler` emits a table carrying **no class at all**:

```html
<style type="text/css"> </style>
<table id="T_6e2f9">
```

A plain `DataFrame` emits `<table border="1" class="dataframe">`.

Nothing in MolSysMT changed. What changed is where the striping came from:

- **JupyterLab** stripes with a class-agnostic rule, so a `Styler` is covered:
  ```css
  .jp-RenderedHTMLCommon tbody tr:nth-child(odd)  { background: var(--jp-layout-color0); }
  .jp-RenderedHTMLCommon tbody tr:nth-child(even) { background: var(--jp-rendermime-table-row-background); }
  ```
- **MyST-NB** used to ship the same idea in `myst_nb/static/mystnb.css`, under a
  comment that states its provenance:
  ```css
  /* Pandas tables. Pulled from the Jupyter / nbsphinx CSS */
  div.cell_output tbody tr:nth-child(odd) { background: #f5f5f5; }
  ```
  This block is present in v1.2.0 and v1.3.0 and **removed in v1.4.0**, the
  version currently installed. v1.4.0 is the dark-mode rework; of the pandas
  table rules not even the comment survives. The only remaining `tbody` selector
  is `tbody span.pasted-inline img`.
- **pydata-sphinx-theme** does stripe notebook outputs, but only through
  `table.dataframe`:
  ```css
  .bd-content div.cell_output table.dataframe tbody tr:nth-child(odd) { ... }
  ```
  This comes from the accessibility table redesign (PR #1757, 2024-05-13), whose
  `table-colors` mixin carries the `nth-child` rules, and was narrowed further by
  PR #2059, *"Remove hover striping from all but `.dataframe` tables"*. A `Styler`
  table matches neither `.dataframe` nor `.table`, so no rule applies.

The `Styler` contributes no CSS of its own: `.hide(axis='index')` produces an
empty `<style>` block.

## Evidence

Same build, same theme, same stylesheets:

| page | table markup | striped |
|---|---|---|
| `content/user/tools/basic/info.html` | `<table id="T_6e2f9">` (×8) | no |
| `content/user/tools/build/get_missing_bonds.html` | `<table border="1" class="dataframe">` | yes |

The stylesheet is the whole difference, and both repositories show it:

| artifact | file | rule present |
|---|---|---|
| MolSysMT `gh-pages`, 2026-01-12 | `_static/mystnb.8ecb98da…css` | yes |
| MolSysMT `docs/_build`, 2026-08-03 | `_static/mystnb.11b39860…css` | no |
| MolSysViewer `gh-pages`, 2026-01-11 | `_static/mystnb.8ecb98da…css` | yes (line 251) |
| MolSysViewer `docs/_build`, 2026-03-03 | `_static/mystnb.11b39860…css` | no |

MolSysViewer is already rebuilt without the striping and merely not yet
published. The two hashes match across both repositories, so this is one
upstream file change, not a per-repository configuration drift.

Scope: 62 of the documentation notebooks store `Styler` tables; only 2 store
`class="dataframe"` output.

## Contributing factor

`devtools/conda-envs/docs_env.yaml` and `development_env.yaml` pin neither
`myst-nb` nor `pydata-sphinx-theme`, so an environment update moves the
documentation's appearance without any change in this repository. This is how the
change arrived unnoticed, but it is not what made it possible: the markup was
already relying on a rule no longer guaranteed to exist. Pinning was considered
and rejected — it would have frozen the symptom instead of removing the
dependency on that rule.

## Resolution

`molsysmt/basic/info.py` now tags the returned `Styler`:

```python
return tmp_df.style.hide(axis='index').set_table_attributes('class="dataframe"')
```

This is not a workaround for the theme. `class="dataframe"` is what **pandas
itself** emits from `DataFrame.to_html()`; the `Styler` is the one object in the
library that omits it, which is why no downstream stylesheet can reach it.
Setting it returns `info()` to the markup contract every consumer already
assumes, in one place, for the whole MolSysSuite.

It also repairs dark mode, which was worse than merely unstriped. PST applies

```css
html[data-theme=dark] .bd-content div.cell_output .text_html:not(:has(table.dataframe))
  { background-color: var(--pst-color-text-base); color: var(--pst-color-on-background); }
```

as a fallback to non-`dataframe` HTML output, and `info()` sits exactly in
`<div class="output text_html">`. It was being painted as an inverted light box.
Carrying the class makes the `:not(:has(...))` stop matching, so the table takes
the real table styling instead. Resolved against the built stylesheet:

| theme | odd row | even row | text |
|---|---|---|---|
| light | `#f3f4f5` | `#fff` | `#14181e` |
| dark | `#29313d` | `#222832` | `#fff` |

Those are the same values every `table.dataframe` in the build already uses, so
the mixed-output consistency requirement follows from the same rule rather than
from a coincidence.

**Notebook rendering is unaffected**: `jupyterlab`, `notebook` and `nbconvert` as
installed define no `.dataframe` rule at all, and JupyterLab's striping comes
from the class-agnostic `.jp-RenderedHTMLCommon tbody tr:nth-child(...)`. The
class is inert there.

`info()` is the only producer of a `Styler` in MolSysMT, so the surface is one
line. Guarded by `test_info_styler_table_carries_the_dataframe_class` in
`tests/basic/test_info.py`, which asserts the class in both `to_html()` and
`_repr_html_()` — separate code paths in pandas — and that the hidden row index
survives.

### Verification

`docs/content/user/tools/basic/info.ipynb` was re-executed with `-f` and the
documentation rebuilt with `make html` (build succeeded; 445 warnings, the
accepted baseline). All **8** of its tables now emit

```html
<table id="T_22d51" class="dataframe">
```

nested as `.bd-content` → `div.cell_output` → `div.output.text_html`, which is
exactly the path PST's selector requires. The stylesheet linked by that page is
still `mystnb.11b39860…css` — the version *without* the pandas rule — so the
striping now comes from the theme alone and no longer depends on anything MyST-NB
could drop again. Confirmed visually by the maintainer in both the light and the
dark theme.

Diffing the notebook with the uuids normalized shows the re-execution changed
nothing else of substance: only the ids, the new class, and the removal of a
stale `display_data` output on the `import molsysmt as msm` cell that held an
orphan widget reference (`model_id`) with an empty `text/plain`.

### On the added borders

The compiled table is heavier than the one on the published sites: PST's
`table.dataframe` block also draws an outer border, vertical rules between cells
(`td~td, th~th { border-left }`), and a heading band underlined with
`--pst-color-primary`. The old appearance was lighter because *no* theme rule
reached the table at all — only the MyST-NB zebra. That lightness was an
inconsistency, not a design: `get_missing_bonds.html` renders a genuine
`class="dataframe"` table and has always carried those rules.

Overriding them in `docs/_static/custom.css` was considered and declined. The
current look is what pydata-sphinx-theme intends for a pandas table (the
accessibility redesign, PR #1757), and leaving it untouched keeps every repository
in the suite looking the same without any of them maintaining CSS.

### Rejected

- **CSS in `docs/_static/custom.css`.** Would have restyled the stored outputs
  without re-executing anything, but it treats the symptom in one repository and
  leaves a rule to maintain against upstream. Rejected in favour of fixing the
  markup.
- **Pinning `myst-nb<1.4`.** Forfeits the dark-mode rework that is the reason the
  hard-coded `#f5f5f5` was dropped upstream. Rejected as a patch.

### Remaining — documentation work, not a defect

**61** of the 62 notebooks holding `msm.info()` output still carry pre-fix stored
outputs, so their pages render unstriped until re-executed. Nothing is wrong with
them: they simply predate the fix. Until the sweep runs, pages such as
`get_missing_bonds.html` show a `Styler` table and a `DataFrame` table side by
side in the two different styles — which is the inconsistency this report closes,
visible mid-migration.

`docs/execute_notebooks.py` will not flag them: see the blind spot below.

## On the Styler `id` — considered and deliberately left alone

`Styler` derives the table `id` from `uuid4`: three calls on identical data give
`T_79a73`, `T_eb203`, `T_bf84f`. A single notebook holds many of them —
`docs/content/user/tools/basic/info.ipynb` has 8 tables and 290 occurrences of
`T_xxxxx` — and the `<style>` block that id identifies is empty, so it buys
nothing. Making it stable was considered and rejected on two counts.

**No library-side value can be both stable and unique.** `info()` cannot know how
many times it appears on a page.

- `set_uuid('')` gives every table `T_`, `T__row0_col0`, … — duplicate HTML ids on
  any page with more than one table.
- A uuid hashed from the table content collides too: **5 of the 62 notebooks hold
  two tables with identical content**, and not by accident — `copy.ipynb` shows
  `info()` before and after copying, which is the point of the page. Also
  `get_distances.ipynb`, `get_dihedral_angles.ipynb`, `get_missing_bonds.ipynb`.

`uuid4` at least guarantees valid HTML today, so any of these would trade valid
markup for tidier diffs. (`to_html(exclude_styles=True)` does drop the ids, but it
is a `to_html()` argument that `_repr_html_()` never uses — so it does not reach
the notebook, which is where the outputs are stored — and it strips the table
attributes as well, including the `dataframe` class this report is about.)

**And the churn is already bounded.** `docs/execute_notebooks.py:84-99` only
re-executes a notebook whose mtime, or last commit time, is newer than its
`.nbconvert.last_run`. Fresh ids therefore appear only in notebooks that were
edited, which have a real diff anyway.

### One blind spot worth recording

That mechanism keys off changes to the **notebook**, never to the library. The
`info()` change in this report marks nothing as stale, so the pages would be
rebuilt from outputs predating it. Landing it needs an explicit force:

```
cd docs && python execute_notebooks.py -fr content index.ipynb -n <workers>
```

`index.ipynb` sits at the `docs/` root and carries an `msm.info()` table, so
`-fr content` alone misses it. Do not force from `docs/` itself: `_build/` is not
excluded by the script's filter and holds executed copies of every notebook.

This is general, not specific to this bug: any future change to a `_repr_html_`
or to an output format is invisible to the staleness check.

## Acceptance

- An `msm.info()` table in a compiled page renders with alternating rows in both
  the light and the dark theme, with contrast that survives a theme switch.
- The check is performed on the built HTML, not on the notebook.
- A page mixing `Styler` and `DataFrame` output renders both consistently.
- The notebook rendering in JupyterLab is unchanged.
