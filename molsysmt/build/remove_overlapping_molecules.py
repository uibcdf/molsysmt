from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def remove_overlapping_molecules(molecular_system, selection, selection_2=None,
                                structure_index=0, threshold='3 angstroms', pbc=True,
                                syntax='MolSysMT'):

    from molsysmt import select, get, remove
    from molsysmt.pbc import has_pbc
    from molsysmt.structure import get_contacts

    if pbc:
        pbc=has_pbc(molecular_system)

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if selection_2 is None:
        atom_indices_2 = complementary_atom_indices(molecular_system, atom_indices)
    else:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)

    contact_map = get_contacts(molecular_system, selection=atom_indices, selection_2=atom_indices_2,
                               structure_indices=structure_index, threshold=threshold, pbc=pbc,
                               output_type='matrix')

    mask = np.any(contact_map[0], axis=1)
    atoms_to_be_removed = np.array(atom_indices)[mask].tolist()
    molecules_to_be_removed = get(molecular_system, element='atom', selection=atoms_to_be_removed, molecule_index=True)
    molecules_to_be_removed = np.unique(molecules_to_be_removed)
    atoms_to_be_removed = select(molecular_system, selection='molecule_index==@molecules_to_be_removed')
    if len(atoms_to_be_removed):
        output = remove(molecular_system, selection=atoms_to_be_removed)
    else:
        output = molecular_system

    return output

