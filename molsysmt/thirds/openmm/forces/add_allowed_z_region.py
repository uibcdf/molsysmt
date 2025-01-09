from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_allowed_z_region(molecular_system, selection='all', z0='0.0 nm', width='1.0 nm',
                         force_constant='5000 kilojoules_per_mole/nm**2', pbc=False, return_force=False,
                         syntax='MolSysMT', skip_digestion=False):

    from .add_allowed_plane_region import add_allowed_plane_region

    z0, unit = puw.get_value_and_unit(z0)
    point = [[0.0, 0.0, z0]]
    point = puw.quantity(point, unit)

    return add_allowed_plane_region(molecular_system, selection=selection,
                                    force_constant=force_constant, point=point, normal_vector=[0,0,1],
                                    width=width, pbc=pbc, return_force=return_force, syntax=syntax,
                                    skip_digestion=True)
