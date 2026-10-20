(Tutorial_Capability_Reports)=
# Querying capabilities

*Inspecting forms, conversion routes, syntax directions and dependency status.*

`msm.supported` reports library capabilities without loading a molecular system.
Its default output is a styled notebook table. Use `output_type='dataframe'` or
`'dictionary'` in scripts; `forms` also offers a plain name list. These reports
remain experimental and follow the current form registry and visibility policy.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

- {func}`molsysmt.supported.forms`
- {func}`molsysmt.supported.conversions`
- {func}`molsysmt.supported.syntaxes`
- {func}`molsysmt.supported.dependencies`
:::

## Enumerating forms

```python
import molsysmt as msm

names = msm.supported.forms(output_type='list')
assert 'molsysmt.MolSys' in names
files = msm.supported.forms('file', output_type='dataframe')
assert (files['Type'] == 'file').all()
assert set(files['Form']).issubset(names)
```

Forms retain their original `Form`, `Type`, `Dependency` and `Info` fields, sorted
by type and form name ignoring case. Plain outputs contain raw metadata; only
the styled table turns `Info` into HTML links. Editing returned metadata does
not edit the adapter's declaration.

## Inspecting routes

```python
routes = msm.supported.conversions(
    from_form=['molsysmt.MolSys'], to_form=['molsysmt.Topology'],
    output_type='dataframe')
assert bool(routes.loc['molsysmt.MolSys', 'molsysmt.Topology'])
```

`as_rows='from'` puts source forms on rows; `'to'` transposes the report. Existing
type and viewer filters work with every output. Empty filters retain the other
requested axis. Repeated filter names are deduplicated. An unknown explicit form
name retains false entries, as in the visual report.

A true entry means that an adapter declares that route. It does not certify that
every input contains the required attributes or that its optional engine is
installed. Self routes keep the existing false diagonal; this report is not a
replacement for conversion admission or fidelity checks.

## Inspecting other capabilities

```python
syntaxes = msm.supported.syntaxes(output_type='dataframe')
assert {'Syntax', 'Selection input', 'Translation output'}.issubset(syntaxes)
dependencies = msm.supported.dependencies(output_type='dataframe')
assert 'Library' in dependencies
```

Syntax rows preserve registry order and distinguish selection input from
translation output. Dependency rows come from DepDigest and are sorted by status,
type and library. Reporting a dependency does not execute its scientific tools.

## Retaining table axes

All four reports offer the same dictionary structure: `index`, `columns`, `data`.
Both axes and row order are explicit, including empty conversion matrices.

```python
import pandas as pd

record = msm.supported.conversions(
    from_form=['molsysmt.MolSys'], to_form=['molsysmt.Topology'],
    output_type='dictionary')
pd.testing.assert_frame_equal(pd.DataFrame(**record), routes)
```

Programmatic outputs do not construct a `Styler`. The default styled output
continues to work unchanged. Existing `msm.info(..., output_type='dataframe')`
and `'dictionary'` remain system-summary operations; its dictionary output keeps
its existing list-of-records contract.

:::{seealso}
:class: dropdown

- {ref}`Introduction_Forms`
- {ref}`Tutorial_Info`
- {ref}`Cookbook_Form_Teleportation`
:::
