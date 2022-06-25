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


def digest_engine(engine):
    """ Check the name of the engine.

        Parameters
        ---------
        engine : str
            The name of the engine

        Raises
        ------
        BadCallError
            If the engine name is not valid.
    """
    if isinstance(engine, str):
        try:
            return engines_from_lowercase[engine.lower()]
        except KeyError:
            # TODO: create a wrong engine error
            raise WrongEngineError
    raise WrongEngineError
