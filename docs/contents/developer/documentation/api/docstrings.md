# Docstrings

MolSysMT uses the Numpy style to write its docstrings

## Function or Method

    """Checks if `atom_id` has the expected type and value.

    Parameters
    ----------
    atom_id : Any
        The `atom_id` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    WrongAtomIdError
        If the given `atom_id` has not the correct type or value.
    """

### Parameters

`syntax : str, default=X`

## Object typing

Parameters, Return, ... need to specify object types.

| type | comment |
|------|----------|
| `Any` | See [PEP 484](https://www.python.org/dev/peps/pep-0484/#the-any-type) |
| `bool` | boolean |
| `str` | string |
|  `list of str` |   |
|   |   |
