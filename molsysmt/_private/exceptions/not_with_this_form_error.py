class NotWithThisFormError(ValueError):
    """Exception raised when a method or a class can not accept a specific item's form -by no means-.

    This exception is raised when a method or a class should be able to work with an item's form,
    but it has not been implemented yet. For instance, the method used to get the value of the
    dihedral angle defined by four atoms can not work over a GROMACS topology file (.top). In this
    case the method will raise a 'NotWithTisFormError' exception.

    Parameters
    ----------
    form : str
        The item's form not accepted by the method or class raising the exception.

    Raises
    ------
    NotWithThisFormError
        A message is printed out with the name of the not supported form, the name of the class or
        the method raising the exception, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotWithThisFormError
    >>> from molsysmt import get_form
    >>> def method_name(item):
    ...    input_form = get_form(item)
    ...    if input_form not in ['file:top', 'file:prmtop']:
    ...       raise NotWithThisFormError(input_form)
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotWithThisFormError <developer:exceptions:NotWithThisFormError>`

    """

    def __init__(self, form):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"\"{caller_name}\" does not work with {form} items. "
                f"Check {api_doc} for more information. "
                f"If you still need help, open a new issue in {__github_issues_web__}."
                )

        super().__init__(message)


