from molsysmt._private.smonitor import NotImplementedMethodError

def run_NVT_equilibration (item, protocol=0, forcefield=('AMBER99SB-ILDN','TIP3P'),
                       contraint_HBonds=True, engine='OpenMM', verbose=True, *kwargs):
    """
    To be written soon...

    Parameters
    ----------
    item : molecular system
        Argument item.
    protocol : object, default=0
        Argument protocol.
    forcefield : str, default=('AMBER99SB-ILDN', 'TIP3P')
        Force field parameter identifier or name.
    contraint_HBonds : object, default=True
        Argument contraint_HBonds.
    engine : object, default='OpenMM'
        Argument engine.
    verbose : object, default=True
        Argument verbose.
    """

    raise NotImplementedMethodError(caller='molsysmt.molecular_dynamics.run_NVT_equilibration')
