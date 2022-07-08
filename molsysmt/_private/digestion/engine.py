from ..exceptions import WrongEngineError

engines = [
    'Amber',
    'Biopython',
    'PDBFixer',
    'OpenMM',
    'MDTraj',
    'LEaP',
    'Modeller',
    'MolSysMT',
    'OpenPocket',
    'NGLView',
]

engines_from_lowercase = {ii.lower(): ii for ii in engines}


def digest_engine(engine, caller=""):
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
    if isinstance(engine, str):
        try:
            return engines_from_lowercase[engine.lower()]
        except KeyError:
            raise WrongEngineError(engine, caller)
    raise WrongEngineError(engine, caller)
