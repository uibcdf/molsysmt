(Tutorial_Get_Conversion_Report)=
# Getting conversion reports

*Inspecting detected information loss before requesting a conversion.*

{func}`molsysmt.basic.get_conversion_report`, also available as
`msm.get_conversion_report`, inspects the source using the same preflight as
`msm.convert(..., strict=True)` and `msm.convert(..., return_report=True)`.
It reads source files as needed and returns a report without writing the
destination or changing the source's molecular data.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.basic.get_conversion_report`
:::

## Choosing the destination

Supply a supported form name or a filename, including a `pathlib.Path`.
The destination need not exist; an existing destination is never overwritten.
Supply a list of targets to receive a list of reports in the same order.
An empty target list returns an empty report list.

You can use the usual `selection`, `structure_indices` and `syntax` arguments
to inspect the requested subset. Structure indices are indices, not IDs.
The source may be any supported form or a composition of forms.

## Reading the report

Each immutable {class}`molsysmt.basic.ConversionReport` includes `from_form`,
`to_form`, `outcome`, `issues`, `audited_scopes` and `is_exhaustive`.
Use `is_lossy` to check whether any losses were detected. Issue records identify
the attribute, kind, scope and reason. `to_dict()` gives a serializable report.

An `equivalent` or `exact` outcome without exhaustive coverage does not prove
that every source detail survives. The report also does not prove that an
adapter exists, its optional dependencies are installed, or its writer accepts
every value. Request the actual conversion after reviewing the report.

Converter-specific options such as `ctfile_version` and `discard_properties`
remain arguments of `convert`; the report query does not interpret them. For
example, you can inspect SD property loss without first authorizing its discard,
but a later SDF conversion still requires explicit authorization.

## Retaining naming context

Group labels and their declared vocabulary are distinct information. Native
inventories, their supported typed dictionaries and H5MSM carry the versioned
`group_naming_schemes` declaration. PDB, other label-only representations and
coordinate-only projections do not. Their reports contain an `unsupported`
issue for `group_naming_schemes` in the `topology` scope when selected groups
have a declaration. `convert(strict=True)` rejects that loss before creating
or replacing the destination. Ordinary conversion retains its existing policy
of permitting loss; inspect its returned report when fidelity matters.

You can supply `from_naming_scheme` to audit a prospective source declaration
with the same spelling and meaning as in `convert`. Existing selected declarations
must agree with it. The query does not assign it to the source. An unknown
vocabulary is not inferred from a group label, Python class or file format.
Empty selections and undeclared selected groups do not invent a loss of known
metadata merely because another, unselected group has a declaration.

Known declarations can be lost even when the target keeps the same label. A
same-format foreign conversion with an explicit source interpretation therefore
does not inherit the exhaustive byte-copy claim of an ordinary file identity
conversion. This scope does not certify every foreign adapter or chemical method.
The executed {ref}`Tutorial_Group_Name_Code` demonstrates naming preflight.

## Retaining interaction evidence

Named analyses are represented information even when they contain no occurrences.
A target without their storage reports an `interactions` loss in that scope.
When an explicit source convention adds a previously missing declaration,
MolSysMT's existing lifecycle policy invalidates attached evaluated interaction
coverage on the independent result. Preflight reports this as `invalidation`,
including structures evaluated without occurrences. Strict conversion refuses
before publication; ordinary conversion keeps its existing invalidation policy.
The original source and its analysis snapshots stay unchanged.

Matching declarations do not invalidate analyses. Coverage outside the selected
structures, or an already unevaluated analysis, does not create an invalidation
loss in the selected output. The metadata preflight inspects coverage without
expanding interaction occurrence columns; other report scopes can still read
source data. Neither this query nor conversion recalculates interactions.

:::{seealso}
:class: dropdown

- {ref}`cookbook-native-sdf` for an SDF preflight workflow.
- {func}`molsysmt.basic.convert` for strict loss rejection and actual conversion.
:::
