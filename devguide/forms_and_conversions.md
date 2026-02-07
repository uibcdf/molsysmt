# Forms and Conversions

## Form Adapters
Form adapters live under `molsysmt/form`. Each form module must define:
- `form_name`
- `form_type`
- `form_info`
- `_convert_to` mapping with callables

## Lazy Discovery
Forms are discovered lazily. Mapping from form directory to dependency lives in
`molsysmt/_depdigest.py` (see `SPEC_DEPENDENCIES.md`).

Do **not** add dependency-related variables to a form `__init__.py`.

## Conversion Rules
- Prefer composition of existing converters over duplicate logic.
- Keep attribute names and shapes consistent across forms.
- Respect `msm.config.show_all_capabilities` when exposing forms.
