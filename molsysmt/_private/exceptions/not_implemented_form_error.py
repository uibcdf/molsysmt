class NotImplementedFormError(NotImplementedError):
    """Exception raised when a method or a class does not support a specific item's form yet.

    This exception is raised when a method or a class should be able to work with an item's form,
    but it has not been implemented yet. For instance, a method gets the number of atoms of a
    molecular system, but the current version works over a pdb file but not yet over a mol file. In
    this case this exception should be rised when the input argument is a mol file.

    Parameters
    ----------
    form : str
        The item's form not supported yet by the class or method raising the exception.

    Raises
    ------
    NotImplementedFormError
        A message is printed out with the name of the not supported form, the name of the class or
        the method raising the exception, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotImplementedFormError
    >>> from molsysmt import get_form
    >>> def method_name(item):
    ...    input_form = get_form(item)
    ...    if input_form not in ['file:pdb', 'string:pdb_id', 'string:pdb_text']:
    ...       raise NotImplementedFormError(input_form)
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotImplementedFormError <developer:exceptions:NotImplementedFormError>`

    """

    def __init__(self, form):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The \"{form}\" form has not been implemeted yet in \"{caller_name}\". "
                f"Check {api_doc} for more information. "
                f"Write a new issue in {__github_issues_web__} asking for its implementation."
                )

        super().__init__(message)


