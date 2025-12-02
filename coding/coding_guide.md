

**Language policy:** Code comments, docstrings, and all documentation (markdown/guides/READMEs) must be written in English.

## forms

form_in
form_out

### Default form:

'molsysmt.MolSys'

## Atom indices

name variable: 'atom_indices'

Default: 'all'
None: all atoms
sorted list of integer

## Frame indices

name variable: 'structure_indices'

Default: None
'all': all atoms

frame is: structure_id, time, coordinates and box.

## Element IDs

In native MolSysMT objects (`molsysmt.Topology`, `molsysmt.MolSys`), all element IDs (`atom_id`, `group_id`, `component_id`, `molecule_id`, `chain_id`, `entity_id`) are stored as strings. Normalize any incoming numeric IDs to strings in converters and keep tests and docs aligned with this invariant.

## Getter outputs

Getter-style functions (e.g., `molsysmt.basic.get`, `element.get_*`) must return Python lists (or lists of lists) when returning multiple values. Do not return NumPy arrays for collections; coerce to lists to keep outputs consistent across forms.

# Docstrings

- Use NumPy-style docstrings with Sphinx/MyST roles for cross-references.
- Keep everything in English, concise, present tense, and third person.
- One-line summary in gerund with a trailing period.
- Standard section order: Summary; extended description (optional); Parameters; Returns (single section); Raises; Notes; See Also; Examples (doctest `>>>`); admonition with tutorial link; `.. versionadded::`.
- Types in lowercase (`str`, `bool`, `list`, `tuple`, `molecular system`, `numpy.ndarray`, `pandas.DataFrame`); defaults in the description, not the signature.
- Reuse standard wording for common parameters (`molecular_system`, `selection`, `structure_indices`, `syntax`, `skip_digestion`, `to_form`); selection/structure indices are 0-based, `'all'` selects everything, reference `Introduction_Selection`.
- Returns: one section only; include units where relevant; list multiple possible return types on separate lines.
- Raises: list exceptions and conditions (`NotSupportedFormError`, `ArgumentError`, `SyntaxError`, etc.).
- Notes: bullet list with internal assumptions and links to forms/selection docs.
- See Also: short infinitive descriptions with `:func:` roles.
- Examples: minimal, deterministic doctest blocks using `molsysmt.systems` or tiny fixtures; no duplicate heavy examples already covered by tests.
- Admonition: `.. admonition:: Tutorial with more examples` linking to the corresponding tutorial.
- End with `.. versionadded:: X.Y.Z`.
- Public functions normally carry `@digest` for argument validation.
