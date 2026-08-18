from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest()
def add_allowed_z_region(molecular_system, selection='all', z0='0.0 nm', width='1.0 nm',
                         force_constant='5000 kilojoules_per_mole/nm**2', pbc=False, return_force=False,
                         syntax='MolSysMT', skip_digestion=False):
    """
    Adding repulsive restraints confining particles within an allowed z-coordinate interval in OpenMM.

    Parameters
    ----------
    system : openmm.System
        Target OpenMM system to modify.
    atom_indices : list of int
        Atom indices to confine.
    z_min : quantity
        Minimum allowed z-coordinate in nanometers.
    z_max : quantity
        Maximum allowed z-coordinate in nanometers.
    k : quantity
        Harmonic confining constant in `kJ/(mol*nm^2)`.

    Returns
    -------
    openmm.CustomExternalForce
        The added confining force instance.

    .. versionadded:: 1.0.0
    """

    from .add_allowed_plane_region import add_allowed_plane_region

    z0, unit = puw.get_value_and_unit(z0)
    point = [[0.0, 0.0, z0]]
    point = puw.quantity(point, unit)

    return add_allowed_plane_region(molecular_system, selection=selection,
                                    force_constant=force_constant, point=point, normal_vector=[0,0,1],
                                    width=width, pbc=pbc, return_force=return_force, syntax=syntax,
                                    skip_digestion=True)
