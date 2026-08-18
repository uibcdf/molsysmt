from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest()
def add_forbidden_z_region(molecular_system, selection='all', z0='0.0 nm', width='1.0 nm',
                           force_constant='5000 kilojoules_per_mole/nm**2', pbc=False, return_force=False,
                           syntax='MolSysMT', skip_digestion=False):
    """
    Adding repulsive boundary restraints preventing particles from entering a z-slab in OpenMM.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    z0 : object, default='0.0 nm'
        Argument z0.
    width : object, default='1.0 nm'
        Argument width.
    force_constant : object, default='5000 kilojoules_per_mole/nm**2'
        Argument force_constant.
    pbc : bool, default=False
        Whether to take periodic boundary conditions into account.
    return_force : object, default=False
        Argument return_force.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.CustomExternalForce
        The added barrier force instance.


    .. versionadded:: 1.0.0
    """

    from .add_forbidden_plane_region import add_forbidden_plane_region

    z0, unit = puw.get_value_and_unit(z0)
    point = [[0.0, 0.0, z0]]
    point = puw.quantity(point, unit)

    return add_forbidden_plane_region(molecular_system, selection=selection,
                                      force_constant=force_constant, point=point, normal_vector=[0,0,1],
                                      width=width, pbc=pbc, return_force=return_force, syntax=syntax,
                                      skip_digestion=True)

