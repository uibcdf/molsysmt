# Docstrings

## Introduction

MolSysMT follows a unified and structured approach to documenting its API using
docstrings embedded in the source code. These docstrings are essential for both
human understanding and for automatically generating the API Reference section
of the documentation website.

We use the **NumPy docstring style**, extended with **Sphinx/MyST markup** to
allow cross-referencing, automatic documentation builds, and testable examples.
Every public function, method, or class must include a complete docstring,
which allows users and contributors to:

- Understand what the function does
- Learn how to call it and what arguments it expects
- Interpret the returned values
- See examples of usage
- Know when the function was added or modified

This document is divided by docstring sections:

- `Functions and Methods`: How to document callable elements with parameters, returns, and testable examples.
- `Classes`: How to document class constructors, attributes, and embedded methods.
- `Modules`: Guidelines for documenting whole modules and their role in the API.
- `Attributes`: How to document public attributes exposed in classes or modules.

Quick checklist:

- One-line summary in gerund with a trailing period.
- Section order: summary; optional extended description; Parameters; Returns (single section); Raises; Notes; See Also; Examples (doctest `>>>`); tutorial admonition; `.. versionadded::`.
- Types in lowercase; defaults described in text; reuse standard wording for `molecular_system`, `selection`, `structure_indices`, `syntax`, `skip_digestion`, `to_form`; selections/structure indices are 0-based and `'all'` selects everything.
- Mention units for physical quantities (nm, ps, radians, elementary charge) and prefer deterministic, minimal examples using bundled systems.

Each section includes usage instructions, conventions, and editorial rules.

Where applicable, you'll find blue boxes titled:

:::{admonition} Editorial guide
:class: important
- Use English, in technical and clear tone,clear, concise, and direct.    
- Avoid unnecessary jargon or verbosity, and colloquial language.    
- Use present tense and third person.    
:::

These rules are based on best practices, the specific needs of MolSysMT, and
aimed at maintaining a consistent and collaborative development style across
the project.


## Functions and Methods

This section describes how to write docstrings for functions and methods in
MolSysMT.

These are the most common elements in the library at the eye of the common user, particularly under the
`Tools` section in this documentation. Every public function must follow a consistent
structure, be fully documented, and include at least one example that can be
tested automatically.

The following is a example to illustrate the structure of a MolSysMT function docstring:

```python

@digest()
def add(to_molecular_system, from_molecular_system, selection='all', structure_indices='all',
        keep_ids=True, in_place=True, syntax='MolSysMT', skip_digestion=False):
    """
    Adding elements from one molecular system into another.

    This function adds selected elements from a source molecular system (`from_molecular_system`)
    into a target molecular system (`to_molecular_system`). Both systems must be compatible in
    terms of structure count: if the target system contains structural information (e.g., coordinates),
    the source must either match this number of structures or the user must explicitly provide
    `structure_indices` to specify which structures to use during the addition.

    Parameters
    ----------
    to_molecular_system : molecular system
        The target molecular system, in any of the :ref:`supported forms <Introduction_Forms>`.
        Elements from the source system will be added to this system by default. If `in_place=False`, 
        a copy will be returned instead of modifying this object directly.
    from_molecular_system : molecular system
        The source molecular system, in any of the :ref:`supported forms <Introduction_Forms>`.
        Selected elements from this system will be added to the target system.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atoms to be dded, specified as a list/tuple/array of 0-based atom indices,
        or as a string following one of the :ref:`supported selection syntaxes <Introduction_Selection>`.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Indices (0-based) of structures in the source system to use for copying structural attributes
        (e.g., coordinates) of the selected atoms.
    keep_ids : bool, default=True
        Whether to preserve the unique IDs of elements from the source system when adding them
        to the target system.
    in_place : bool, default=True
        If True, modifies `to_molecular_system` in place. If False, returns a new modified copy, leaving
        the original unchanged.
    syntax : str, default='MolSysMT'
        Selection syntax to interpret the `selection` string. See :ref:`Introduction_Selection` for options.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Returns
    -------
    molecular system or None
        If `in_place=True`, returns `None` and modifies `to_molecular_system` directly.
        If `in_place=False`, returns a new molecular system (same form as the input) with the added structures.

    Raises
    ------
    NotSupportedFormError
        If any molecular system is provided in an unsupported form.
    ArgumentError
        If any argument has an invalid or inconsistent value.

    Notes
    -----
    - All forms listed in :ref:`Introduction_Forms` are accepted for both source and target systems.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select` :
        Select elements from a molecular system.
    :func:`molsysmt.basic.merge` :
        Merge multiple molecular systems into one.
    :func:`molsysmt.basic.append_structures` :
        Append structures from one system to another.
    :func:`molsysmt.basic.concatenate_structures` :
        Concatenate multiple systems along the structural dimension.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys_A = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> molsys_B = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'])
    >>> msm.get(molsys_A, n_molecules=True)
    1
    >>> msm.add(molsys_A, molsys_B)
    >>> msm.get(molsys_A, n_molecules=True)
    2

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples: :ref:`Tutorial_Add`.

    .. versionadded:: 1.0.0
    """

    # Function implementation goes here

```

Each public function **must include** the following sections in this order:
As shown in the example above, a complete docstring for a function or method
should include the following sections:


- `One-line summary`: A short description in gerund form.
- `Extended description`: Optional, for added context or background.
- `Parameters`: A detailed list of input arguments.
- `Returns`: Output.
- `Raises`: Possible exceptions.
- `Notes`: Supplementary details and references.
- `See also`: Supplementary details and references.
- `Examples`: Minimal testable usage examples with `doctest` syntax.
- `Admonition with tutorial call`: 
- `Version added`: The version in which the function was introduced.

The structure described below also applies to methods of classes, with the
exception that the first argument (`self` or `cls`) is not documented
explicitly.

### One-line Summary

A concise sentence that explains what the function does.

Examples:

```python
"""
Adding elements of a molecular system into another molecular system.

...
"""
```

```python
"""
Retrieving attribute values from a molecular system.

...
"""
```

```python
"""
Removing atoms or structures from a molecular system.

...
"""
```

:::{admonition} Editorial guide
:class: important
- The one-line summary starts with a verb in gerund form (e.g., "Adding", "Calculating", "Retrieving").    
- Always end with a period.    
- Keep it short and action-oriented.    
:::

### Extended Description

A paragraph (or more) that expands on the function’s purpose and clarifies special
behavior, or situates the function in the context of MolSysMT.

Examples:

```python
"""
...


This function adds selected elements from a source molecular system (`from_molecular_system`)
into a target molecular system (`to_molecular_system`). Both systems must be compatible in
terms of structure count: if the target system contains structural information (e.g., coordinates),
the source must either match this number of structures or the user must explicitly provide
`structure_indices` to specify which structures to use during the addition.


...
"""
```

```python
"""
...

This function retrieves values of one or more attributes from a molecular system (or from
a selected subset of it), optionally specifying the hierarchical `element` level. Attributes
to be returned are indicated via keyword flags in `**kwargs` (e.g., ``n_atoms=True``,
``coordinates=True``).

...
"""
```

```python
"""
...

This function returns a new molecular system after removing the atoms and/or structures
specified via `selection` and `structure_indices`. If `selection` is `None`, no atoms are
removed. If `structure_indices` is `None`, no structures are removed. Optionally,
the resulting system can be returned in a different form with `to_form`.

...
"""
```

:::{admonition} Editorial guide
:class: important
- Use present tense, e.g., “This function retrieves...”    
- Do not repeat the one-line summary verbatim.    
- Prefer short paragraphs over bullet points (unless describing multiple modes).    
:::


### Parameters

List all function arguments, including optional ones.

Each parameter must include:
  - name
  - type (lowercase, e.g. `str`, `tuple`, `molecular system`) -See the section on [object typing](#sec-object-typing)-
  - optional: default value in description (not in signature)
  - clear explanation of its use (1-3 lines if possible)

Examples:

```python
"""
...
    to_form : str or list of str, default 'molsysmt.MolSys'
        Target form (or list of forms) for the conversion output. When a list is given,
        the function returns a list with one converted output per requested form.
        See :ref:`Supported conversions <Introduction_Supported>`.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default='atom'
        Structural level on which the selection is applied. Returned indices correspond to this level.
    include_none : bool, default False
        Whether to consider attributes currently holding `None` as available.
        If `True`, an attribute that exists but is `None` will return `True`.
...
"""
```

:::{admonition} Editorial guide
:class: important
- List parameters in the order they appear in the function signature.
- Use lowercase for types (e.g., `str`, `bool`, `list`, `tuple`, `molecular system`).
- Include default values in the description, not in the signature.
- Do not leave blank lines between parameters.
- Always document all parameters, including `self` or `cls` for methods.
- Use `molecular system` type where applicable (see below)
- Use `PyUnitWizard` quantities where applicable (see below)
- Use `numpy.ndarray` instead of `ndarray`
- Use `pandas.DataFrame` instead of `DataFrame`
:::

Some parameters have standard descriptions that should be reused verbatim, if
possible, across functions. This ensures consistency and clarity. Those
parameters include: `molecular_system`, `to_form`, `selection`, `structure_indices`,
`syntax`, and `skip_digestion`. See below for their standard descriptions.

#### `molecular_system`

```python
"""
...
    molecular_system : molecular system
        Molecular system to analyze, in any of the :ref:`supported forms <Introduction_Forms>`.
...
"""
```


#### `selection`

- Can be: `str`, `list`, `tuple`, `numpy.ndarray`.
- Always indicate:
  - That it accepts **0-based** indices.
  - That `'all'` selects all relevant elements.
  - A reference to the supported selection syntaxes, for example
    ``:ref:`supported selection syntaxes <Introduction_Selection>``` when used
    inside docstrings.

#### `structure_indices`
- Same rules as for `selection`:
  - **0-based** indices.
  - `'all'` applies to all structures.
  - An optional reference to selection syntaxes (often placed in the `Notes`
    section).

#### `syntax`
- Always clarify that it is the selector used to interpret `selection`.
- Include a reference such as:

  ```text
  See :ref:`Introduction_Selection` for details.
  ```

#### `skip_digestion`
- Standard text for all functions:
  ```text
  Whether to skip MolSysMT’s internal argument digestion mechanism.

  MolSysMT includes a built-in digestion system that validates and normalizes
  function arguments. This process checks types, shapes, and values, and automatically
  adjusts them when possible to meet expected formats.

  Setting `skip_digestion=True` disables this process, which may improve performance
  in workflows where inputs are already validated. Use with caution: only set this to
  `True` if you are certain all input arguments are correct and consistent.
  ```

### Returns

- Describe return type and meaning
- Always use a single `Returns` section.  
- Let Sphinx automatically generate the "Return type" field; do not add it manually.  
- Return type and behavior, including any units if relevant.
   - Tipo de retorno + descripción clara
   - Si hay múltiples outputs, cada uno en su propia línea

Examples:

```python
Returns
-------
molecular system or None
    If `in_place=False`, returns a new molecular system.  
    If `in_place=True`, returns None and modifies the input in place.
```

```python
Returns
-------
bool
    True if the container is a non-empty list or tuple and all items are valid
    molecular systems. False otherwise.
```

- Only define a single **Returns** section.  
- Use syntax like:

  ```python
  Returns
  -------
  molecular system or None
      If `in_place=False`, returns a new molecular system.  
      If `in_place=True`, returns None and modifies the input in place.
  ```

- With PyData + napoleon, Sphinx will automatically generate a separate
  **Return type** field. Do **not** add one manually.
- If the function can return multiple types conceptually different, use different lines in the Returns section:

  ```python
  Returns
  -------
  Type1
      Justification for Type1.    
  Type2
      Justification for Type2.    
  ```

### Raises

- List exceptions the function may raise, with conditions.
- Consistently includes `NotSupportedFormError`, `ArgumentError`, `SyntaxError`.


### Notes

- Always use bullet points starting with `-`.
- Clarify internal assumptions and link to reference documentation (Forms,
  Selection syntaxes, Attributes).
- Add clarifications, implementation notes, or links to other docs, for example:

  ```python
  - Supported molecular-system forms are described in :ref:`Introduction_Forms`.
  - Selection syntaxes and valid query expressions are described in :ref:`Introduction_Selection`.
  ```

- For functions such as `concatenate_structures`, the `Notes` section should
  explicitly list which structural attributes are concatenated
  (`coordinates`, `velocities`, `box`, `time`).

- When applicable, also include clarifications such as:
  - `If element is not specified, it is inferred from the attribute definition.`
  - `If the attribute runs over structures, structure_indices must be defined accordingly.`
  - Any other important internal rule (for example, that `where_is_attribute`
    returns the last matching item).

### See Also

- Use infinitive verbs in descriptions (`Retrieve`, `Select`, `Remove`, etc.).
- Keep descriptions concise (ideally a single line).
- Cross-link functions that are conceptually related using `:func:` roles.
- `See Also` descriptions must be concise and in infinitive (no leading “to”):
  - ✅ `Retrieve attribute values from a molecular system`
  - ❌ `To get the attributes of...`

### Examples

- Include at least one `doctest`-style example using `>>>`
- Keep realistic and minimal
- Link to doctest section
- Always provide `doctest`-compatible examples using `>>>`.  
- Keep examples minimal but functional.  
- Prefer using `molsysmt.systems` or small peptide builders instead of external files.  
- Non-deterministic results must be avoided.
- Written in executable doctest format (with `>>>`).
- Always include at least one realistic use case.
- All examples inside docstrings must be written as `doctest` blocks (`>>>`)
  and are executed automatically by `pytest --doctest-modules`.
- **Do not duplicate** examples in `tests/` unless additional complex checks
  are required (for example, fixtures, multiple asserts, heavy inputs).
- Unit tests in `tests/` should cover logic and edge cases not suitable for
  doctest format.
- Examples should use small, realistic systems (for example, `alanine dipeptide`,
  `pentalanine`, or systems from `molsysmt.systems`).

### Admonition with tutorial call

- A closing `.. admonition:: User guide` block that links to the corresponding tutorial.
- Use Sphinx's `.. admonition::` directive

```python
.. admonition:: Tutorial with more examples

   See the following tutorial for a practical demonstration of how to use this function,
   along with additional examples:
   :ref:`User Guide > Tools > Basic > Add <Tutorial_Add>`.
```

```rst
.. admonition:: Tutorial with more examples

   See the following tutorial for a practical demonstration of how to use this function,
   along with additional examples:
   :ref:`Tutorial_<FunctionName>`.
```
### Version Added

Always indicate the version when the function was added at the end of the docstring.

```python
.. versionadded:: 1.0.0
```

## Classes and Constructors

Classes in MolSysMT (such as native containers `MolSys`, `Topology`, `Structures`, `MolecularMechanics`, and `MolSysBuilder`) must document constructor parameters in the class docstring under `Parameters`, and document instance fields under `Attributes`.

```python
class MolSys:
    """
    Unified molecular system container combining topology, structures, and mechanics.

    Parameters
    ----------
    topology : molsysmt.Topology, optional
        Topological graph and chemical metadata.
    structures : molsysmt.Structures, optional
        Spatial coordinates, simulation boxes, and time series.
    molecular_mechanics : molsysmt.MolecularMechanics, optional
        Force field parameters, force groups, and engine contexts.

    Attributes
    ----------
    topology : molsysmt.Topology
        Molecular topology instance.
    structures : molsysmt.Structures
        Molecular structures instance.
    molecular_mechanics : molsysmt.MolecularMechanics
        Molecular mechanics instance.

    .. versionadded:: 1.0.0
    """
```

:::{admonition} Editorial guide for classes
:class: important
- Document constructor parameters in the class-level docstring under `Parameters`.
- Document public instance attributes under `Attributes`.
- Do not repeat constructor parameters inside `__init__` docstrings unless `__init__` has custom private signature logic.
:::

## Properties and Class Attributes

Class properties decorated with `@property` should have a concise summary, an optional description, and a `Returns` section describing the return type and meaning:

```python
@property
def n_atoms(self):
    """
    Number of atoms in the molecular system.

    Returns
    -------
    int
        Total atom count.
    """
    return self._n_atoms
```

## Form Adapters and Converters

Form adapters under `molsysmt/form/<form_name>/` represent the interoperability layer. Each form converter (`to_<target_form>.py`) and operation (`extract.py`, `add.py`, `merge.py`, `copy.py`, `append_structures.py`, `is_form.py`, `has_attribute.py`) must document:

1. **One-line summary**: Stating source and target forms or operation in gerund.
2. **Parameters**: All arguments in the exact signature (including `atom_indices`, `structure_indices`, `selection`, `syntax`, `output_filename`, `skip_digestion`).
3. **Returns**: Target form instance or `None` if modifying in place.

```python
@arg_digest(form='file:pdb', to_form='molsysmt.MolSys')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to molsysmt.MolSys.

    Parameters
    ----------
    item : file:pdb
        Source item in file:pdb form to convert.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include in the converted system.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include in the converted system.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Converted molecular system representation.

    .. versionadded:: 1.0.0
    """
```

## Atomic Attribute Extractors

Inside form adapter files like `get_topological_attributes.py` and `get_structural_attributes.py`, individual attribute getters (`get_<attribute>_from_<element>`) must document their arguments and return value types:

```python
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting Cartesian coordinates for selected atoms and structures.

    Parameters
    ----------
    item : object
        Molecular system item in the current form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to extract coordinates for.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    numpy.ndarray
        Coordinates array of shape `(n_structures, n_atoms, 3)` in nanometers.
    """
```

(sec-object-typing)=
## Standard Object Typing

Use lowercase identifiers for standard types and explicit package qualifiers for external types:

| Type Expression | Meaning and Usage |
| :--- | :--- |
| `molecular system` | Any object or file path recognized by MolSysMT in any supported form. |
| `quantity` | Physical quantity carrying units managed by PyUnitWizard. |
| `numpy.ndarray` | NumPy multidimensional array (specify shape when possible, e.g. `(n_structures, n_atoms, 3)`). |
| `pandas.DataFrame` | Pandas DataFrame tabular structure. |
| `pathlib.Path` | Pathlib filesystem path object. |
| `str` | Character string. |
| `int` | Integer value. |
| `float` | Floating point scalar. |
| `bool` | Boolean flag. |
| `list of str` / `list of int` | Homogeneous lists of strings or integers. |
| `tuple of int` | Fixed-length tuple of integers. |
| `dict` | Key-value dictionary. |

## Canonical Physical Units

MolSysMT defines canonical internal physical units registered in `puw.fast_track`. All docstrings documenting physical dimensions must state these units:

- **Lengths, Coordinates, Box dimensions**: `nanometers` (`nm`).
- **Angles and Dihedrals**: `degrees` or `radians` (explicitly documented).
- **Time and Timesteps**: `picoseconds` (`ps`).
- **Atomic Masses**: `daltons` (`Da`).
- **Temperature**: `kelvin` (`K`).
- **Potential and Interaction Energy**: `kJ/mol`.
- **Forces**: `kJ/(mol*nm)`.
- **Partial and Net Electric Charges**: `elementary charge` units (`e`).

## Standard Reusable Parameters Vocabulary

Reuse the standard description verbatim for these universal parameters:

| Parameter | Type | Standard Description |
| :--- | :--- | :--- |
| `molecular_system` | `molecular system` | Molecular system to query or manipulate, in any of the :ref:`supported forms <Introduction_Forms>`. |
| `selection` | `str, list, tuple, or numpy.ndarray, default='all'` | Selection of atoms or elements (0-based indices or query string following :ref:`supported syntaxes <Introduction_Selection>`). |
| `structure_indices` | `str, list, tuple, or numpy.ndarray, default='all'` | Structure indices (0-based) to include or process. |
| `syntax` | `str, default='MolSysMT'` | Selection syntax used to evaluate `selection`. See :ref:`Introduction_Selection`. |
| `skip_digestion` | `bool, default=False` | Whether to skip MolSysMT's internal argument digestion and validation mechanism. |
| `to_form` | `str or list of str, default='molsysmt.MolSys'` | Target form (or list of forms) for the conversion output. |
| `in_place` | `bool, default=False` | Whether to modify `molecular_system` in place or return a new copy. |
| `element` | `{'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default='atom'` | Structural hierarchical element level at which the query is applied. |
| `redefine_indices` | `bool, default=False` | Whether to recalculate element indices locally prior to querying. |
| `redefine_types` | `bool, default=False` | Whether to re-infer element classifications from constituent components. |
| `keep_ids` | `bool, default=True` | Whether to preserve original element IDs during merging or addition. |
| `engine` | `str, default='OpenMM'` | Target simulation engine backend. |
| `platform` | `str, default='CPU'` | Compute platform name (`'Reference'`, `'CPU'`, `'CUDA'`, `'OpenCL'`). |
| `output_filename` | `str or pathlib.Path` | Output file path for serialization. |
| `definition` | `str, default='collantes'` | Reference parameter dataset used for property calculation. |

## General Editorial and Formatting Invariants

- Always use English in technical, active, and direct tone.
- Avoid bold text in descriptive paragraphs unless strictly necessary.
- Exactly one blank line between docstring sections (`Parameters`, `Returns`, `Notes`, etc.).
- Do not leave blank lines between parameters within the `Parameters` block.
- Use `.. admonition:: Tutorial with more examples` inside docstrings to link to notebooks.
- Every public function must conclude with `.. versionadded:: 1.0.0`.
