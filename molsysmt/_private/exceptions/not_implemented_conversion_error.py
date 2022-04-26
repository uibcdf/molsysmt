class NotImplementedConversionError(NotImplementedError):

    """Exception raised when the conversion between two forms was not implemented yet.

    This exception is raised when the conversion of a molecular system between two forms has not
    been implemented yet.

    Parameters
    ----------
    from_form : str
        The form of the molecular system to be converted.
    to_form : str
        The target form to which the molecular system needs to be converted.

    Raises
    ------
    NotImplementedFormError
        A message is printed out with the name of the two forms defining the not supported conversion, the name of the class or
        the method raising the exception, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import NotImplementedConversionError
    >>> def method_name(molecular_system, to_form):
    ...    from molsysmt.basic import get_form
    ...    from_form = get_form(molecular_system)
    ...    if from_form in ['string_pdb']:
    ...       if to_form in ['file_pdb']:
    ...          raise NotImplementedConversionError(from_form, to_form)
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> NotImplementedConversionError <developer:exceptions:NotImplementedConversionError>`

    """

    def __init__(self, from_form, to_form):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The conversion from {from_form} to {to_form} in \"{caller_name}\" has not been implemented yet. "
                f"Check {api_doc} for more information. "
                f"Write a new issue in {__github_issues_web__} asking for its implementation."
                )

        super().__init__(message)



