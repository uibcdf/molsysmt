from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_atoms_with_alternate_locations(molecular_system):

    from molsysmt.basic import select

    atom_indices = select(molecular_system, element='atom', selection='occupancy<1.0',
            syntax='MolSysMT')

    return atom_indices

