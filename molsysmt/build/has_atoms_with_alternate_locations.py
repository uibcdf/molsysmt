from molsysmt._private.digestion import digest
import numpy as np

@digest()
def has_atoms_with_alternate_locations(molecular_system):

    from molsysmt.basic import get

    occupancy = get(molecular_system, element='atom', occupancy=True)

    return np.allclose(occupancy,1.0)

