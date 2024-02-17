from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSysOld')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSysOld
    from ..molsysmt_TopologyOld import merge as merge_molsysmt_TopologyOld
    from ..molsysmt_StructuresOld import merge as merge_molsysmt_StructuresOld
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

    output = MolSysOld()
    output.topology = merge_molsysmt_TopologyOld([ii.topology for ii in items], atom_indices=atom_indices,
                                                 skip_digestion=True)
    output.structures = merge_molsysmt_StructuresOld([ii.structures for ii in items],
            atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    output.molecular_mechanics = merge_molsysmt_MolecularMechanics([ii.molecular_mechanics for ii in items],
            atom_indices=atom_indices, skip_digestion=True)

    return output

