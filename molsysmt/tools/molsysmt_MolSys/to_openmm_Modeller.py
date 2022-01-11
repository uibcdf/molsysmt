def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.exceptions import ItemWithWrongForm, LibraryNotFound
    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.molsysmt_MolSys import get_coordinates_from_atom
    from molsysmt import puw
    try:
        from openmm.app import Modeller
    except:
        raise LibraryNotFound(openmm)

    if not is_molsysmt_MolSys(item):
        raise ItemWithWrongForm('molsysmt.MolSys')

    tmp_topology = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_positions = puw.convert(tmp_positions, to_form='openmm.unit')

    tmp_item = Modeller(tmp_topology, tmp_positions[0])

    return tmp_item

