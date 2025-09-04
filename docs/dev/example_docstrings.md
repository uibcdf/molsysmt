```python
def function_name(param1, param2=None, *, option=True):
    """
    One-line summary in gerund form.

    Extended description of the function, its purpose, requirements,
    and special considerations. Use clear, concise sentences.
    Mention assumptions, constraints, or interactions between arguments.

    Parameters
    ----------
    param1 : type
        Short and precise description of the parameter.
    param2 : type, optional
        Default value is described here. Explain how the parameter modifies behavior.
    option : bool, default True
        Explain clearly the meaning of True/False.

    Returns
    -------
    return_type
        Description of the returned value. Be explicit about the type and structure.

    Raises
    ------
    NotSupportedFormError
        If the input molecular system is provided in an unsupported form.
    ValueError
        If the parameter values are inconsistent or invalid.

    Notes
    -----
    Add clarifications, implementation details, or links to background material.
    You can include cross-references like:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    See Also
    --------
    :func:`molsysmt.basic.select` : Select elements from a molecular system.
    :func:`molsysmt.basic.merge` : Merge multiple molecular systems into one.

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
```python

