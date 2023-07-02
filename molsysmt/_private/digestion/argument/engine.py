from molsysmt._private.exceptions import ArgumentError

def digest_engine(engine, caller=None):
    """ Check the name of the engine.

        Parameters
        ---------
        engine : str
            The name of the engine

        caller: str, optional
            Name of the function or method that is being digested.
            For debugging purposes.

        Raises
        ------
        BadCallError
            If the engine name is not valid.
    """
    """ Checks if an engine has the correct type and value

        Parameters
        ----------
        element : str
            The name of the engine.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongEngineError
            A WrongEngineError is raised if the engine is not a string or its name is not valid.

    """

    from molsysmt.supported.engines import lowercase_engines

    if isinstance(engine, str):
        try:
            return lowercase_engines[engine.lower()]
        except:
            pass

    raise ArgumentError('engine', value=engine, caller=caller, message=None)

