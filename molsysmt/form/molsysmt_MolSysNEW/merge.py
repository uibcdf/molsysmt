from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSysNEW')
def merge(items, atom_indices='all', structure_indices='all'):

    from molsysmt.native import MolSysNEW
    from ..molsysmt_TopologyNEW import merge as merge_molsysmt_TopologyNEW
    from ..molsysmt_StructuresNEW import merge as merge_molsysmt_StructuresNEW
    from ..molsysmt_MolecularMechanics import merge as merge_molsysmt_MolecularMechanics

    n_items = len(items)

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ValueError(atom_indices)

    if len(structure_indices)!=n_items:
        raise ValueError(structure_indices)

    output = MolSysNEW()
    output.topology = merge_molsysmt_TopologyNEW([ii.topology for ii in items], atom_indices=atom_indices)
    output.structures = merge_molsysmt_StructuresNEW([ii.structures for ii in items],
            atom_indices=atom_indices, structure_indices=structure_indices)
    output.molecular_mechanics = merge_molsysmt_MolecularMechanics([ii.molecular_mechanics for ii in items],
            atom_indices=atom_indices)

    return output

