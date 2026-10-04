from molsysmt._private.smonitor import ArgumentError


def digest_engine(engine, caller=None):
    """Check the name of the engine.

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

    if caller == "molsysmt.physchem.get_cip_stereochemistry.get_cip_stereochemistry":
        if isinstance(engine, str) and engine.lower() == "rdkit":
            return "rdkit"
        raise ArgumentError("engine", value=engine, caller=caller)

    if (
        caller == "molsysmt.build.add_missing_hydrogens.add_missing_hydrogens"
        and isinstance(engine, str)
        and engine.lower() == "rdkit"
    ):
        return "RDKit"

    from molsysmt.supported.engines import lowercase_engines

    if isinstance(engine, str):
        try:
            return lowercase_engines[engine.lower()]
        except Exception:
            pass

    raise ArgumentError("engine", value=engine, caller=caller, message=None)
