class LibraryNotFoundError(NotImplementedError):
    """Exception raised when a library required by the user is not found.

    Some libraries are not considered as dependencies by Sabueso. These libraries are required if
    the user choose to execute a method with a not default engine. In this case, the user hat to
    install it previousy. It that's not the case, the method will raise this exceptions suggesting
    the manual installation.

    Parameters
    ----------
    argument : str
        The name of the not found library.

    Raises
    ------
    LibraryNotFoundError
        A message is printed out with the name of the class or the method raising the exception,
        the name of the not found library, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import LibraryNotFoundError
    >>> def method_name(item, engine='MolSysMT'):
    ...    if engine == 'OpenMM':
    ...       try:
    ...          import openmm
    ...       except:
    ...          raise LibraryNotFoundError('OpenMM')
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide \> Exceptions \> LibraryNotFoundError <developer:exceptions:LibraryNotFoundError>`

    """

    def __init__(self, library):

        from molsysmt import __github_issues_web__
        from inspect import stack

        all_stack_frames = stack()
        caller_stack_frame = all_stack_frames[1]
        caller_name = caller_stack_frame[3]

        api_doc = ''

        message = (
                f"The python library {library} was not found. "
                f"Although {library} is not considered a dependency, it needs "
                f"to be installed to execute the {caller_name} method the way you require. "
                f"If you still need help, open a new issue in {__github_issues_web__}."
                )

        super().__init__(message)


