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

## Classes

## Modules

## Modules

## Attributes

(sec-object-typing)=
## Object typing

Parameters, Return, ... need to specify object types.

| type | comment |
|------|----------|
| `Any` | See [PEP 484](https://www.python.org/dev/peps/pep-0484/#the-any-type) |
| `bool` | boolean |
| `str` | string |
|  `list of str` |   |
|   |   |

## Other finnal editorial rules

- Avoid using bold text unnecessarily in descriptive parts of docstrings.
- You can use limited Markdown-style formatting inside docstrings
  (for example, `**bold**`, lists) as long as Sphinx parses it correctly.
- Avoid raw `.rst` constructs when they are not needed; rely on Sphinx roles
  such as `:ref:` and `:func:` for cross-references.
- Triple backticks for code blocks are fine in `.md` files, but docstrings in
  Python code must still use triple quotes `"""`.
- Cross-references (`:ref:`, `:func:`) work as in reStructuredText and should
  point to stable labels defined in the documentation.
- Use lowercase identifiers in prose to match attribute names
  (for example, `atom_id`, `group_id`).
- Early validation of arguments is always performed with the `@digest` decorator.
- There must be **exactly one blank line** between sections (`Parameters`,
  `Returns`, `Notes`, etc.).
- Do not leave blank lines **inside** the parameter block between arguments.
- Use `.. admonition:: Tutorial with more examples` inside docstrings to link
  to notebooks; the MyST format for admonitions is reserved for documentation
  pages and tutorials, not for docstrings.

