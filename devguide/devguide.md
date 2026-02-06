# Agreements

**Language policy:** All repository-facing text (code comments, docstrings, READMEs, guides, notebooks) must be written in English. User-facing replies can be in Spanish, but anything stored in the repo stays in English.

## Basic

pip install --no-deps --editable .

## Get

- n_atoms is always an integer even when there is no topological info.
- n_structures is None when the form has no structural info. If the form can store structures n_structures is always an integer (0, if there are no structures in the form).
- if time, box, etc... (structural attributes) are not present in an object... the output is a list with as many Nones as structure_indices.
- Element IDs in native structures (`atom_id`, `group_id`, `component_id`, `molecule_id`, `chain_id`, `entity_id`) are stored as strings; normalize any incoming numeric IDs to strings.
- Public getters (for example, `molsysmt.basic.get` or element-specific getters) must return Python lists (or lists of lists when nested), not NumPy arrays, for collections of values. Ensure converters and helpers coerce outputs accordingly.

## Iterator

- Coordinates is always a numpy.ndarray with shape (n_frames, n_atoms, 3), even with n_frames=1.
- Box is always a numpy.ndarray with shape (n_frames, 3, 3), even with n_frames=1.

## Form

### Structural Iterator

- Coordinates is always a numpy.ndarray with shape (n_frames, n_atoms, 3), even with n_frames=1.
- Box is always a numpy.ndarray with shape (n_frames, 3, 3), even with n_frames=1.

## Native

- if time, box, etc... (structural attributes) are not present in an object... the output is a list with as many Nones as structures in the object.
if there are no structures... all attributes are equal to None.

## Docstrings

- Follow NumPy-style docstrings with Sphinx/MyST roles; keep them concise, in English, present tense, and third person.
- One-line summary in gerund with a trailing period; order sections as: summary; optional extended description; Parameters; Returns (single section); Raises; Notes; See Also; Examples (doctest `>>>`); tutorial admonition; `.. versionadded::`.
- Types in lowercase (`str`, `bool`, `list`, `tuple`, `molecular system`, `numpy.ndarray`, `pandas.DataFrame`); defaults in the description. Reuse standard text for `molecular_system`, `selection`, `structure_indices`, `syntax`, `skip_digestion`, `to_form`; selections/structure indices are 0-based and `'all'` covers everything.
- Always state units for physical quantities (nm, ps, radians, elementary charge). Examples must be deterministic and minimal, preferably using `molsysmt.systems`.
## Testing

- Prefer reusing shared molecular systems defined in `tests/conftest.py` instead of constructing ad hoc fixtures inside individual tests; add new reusable systems there so other tests can share them and keep runtime down.
- Only keep on-the-fly downloads (for example, PDB ID strings) in tests whose explicit purpose is to validate conversion or detection from those remote forms (`string_pdb`, `string_pdb_id`, etc.).
- When adding fixtures in `conftest.py`, assert that created systems are not `None` so failures surface early.

## smonitor Integration

- The catalog is the single source of truth for messages and hints: `molsysmt/_private/smonitor/catalog.py`.
- Legacy classes in `_private/warnings` and `_private/exceptions` are kept for compatibility but should emit smonitor events.
- Project metadata (docs/issues URLs) live in `molsysmt/_private/smonitor/meta.py`.
- More details: `devguide/smonitor.md`.
