from molsysmt._private.smonitor import NotImplementedMethodError, experimental_module

@experimental_module('molsysmt.molecular_dynamics')
def run_NVT_equilibration (item, protocol=0, forcefield=['AMBER99SB-ILDN','TIP3P'],
                       contraint_HBonds=True, engine='OpenMM', verbose=True, *kwargs):
    """
    To be written soon...
    """

    raise NotImplementedMethodError(caller='molsysmt.molecular_dynamics.run_NVT_equilibration')

