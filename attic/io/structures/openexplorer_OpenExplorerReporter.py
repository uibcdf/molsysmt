from molsysmt._private.variables import is_all

def from_openexplorer_OpenExplorerReporter(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt import get_shape_from_box
    from molsysmt.native.trajectory import Trajectory
    from numpy import array

    tmp_item = Trajectory()

    if item.structure_id is not None:
        tmp_item.structure_id = array(item.structure_id, dtype=int)

    units = item.coordinates.unit
    tmp_item.coordinates = array(item.coordinates._value, dtype=float)
    if not is_all(atom_indices):
        tmp_item.coordinates = tmp_item.coordinates[:,atom_indices,:]
    if not is_all(structure_indices):
        tmp_item.coordinates = tmp_item.coordinates[structure_indices,:,:]
    tmp_item.coordinates = tmp_item.coordinates*units

    if item.box is not None:
        tmp_item.box = array(item.box._value, dtype=float)
        if not is_all(structure_indices):
            tmp_item.box = tmp_item.box[structure_indices,:,:]
        tmp_item.box = tmp_item.box*units
        tmp_item.box_shape = get_shape_from_box(tmp_item.box)


    tmp_item.n_structures = tmp_item.coordinates.shape[0]
    tmp_item.n_atoms = tmp_item.coordinates.shape[1]

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item

