from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def merge(items, atom_indices='all', structure_indices='all'):

    from molsysmt.native import MolSys

    n_items = len(items)

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ValueError(atom_indices)

    if len(structure_indices)!=n_items:
        raise ValueError(structure_indices)

    output = MolSys()
    output.topology = merge_molsysmt_Topology([ii.topology for ii in items], atom_indices=atom_indices)
    output.structures = merge_molsysmt_Structures([ii.structures for ii in items],
            atom_indices=atom_indices, structure_indices=structure_indices)
    output.molecular_mechanics = merge_molsysmt_MolecularMechanics([ii.molecular_mechanics for ii in items],
            atom_indices=atom_indices, structure_indices=structure_indices)

    return output

