from molsysmt.engine.engines import engines
from molsysmt._private.exceptions import ArgumentError

engines_from_lowercase = {ii.lower(): ii for ii in engines}

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

    if isinstance(engine, str):
        try:
            return engines_from_lowercase[engine.lower()]
        except:
            pass

    raise ArgumentError('engine', caller=caller, message=None)

