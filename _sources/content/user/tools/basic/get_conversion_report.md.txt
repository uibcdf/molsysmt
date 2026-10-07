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

:::{seealso}
:class: dropdown

- {ref}`cookbook-native-sdf` for an SDF preflight workflow.
- {func}`molsysmt.basic.convert` for strict loss rejection and actual conversion.
:::
