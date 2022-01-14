def to_openmm_Modeller(item, atom_indices='all', frame_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item):
            raise ItemWithWrongForm('molsysmt.MolSys')

    try:
        from openmm.app import Modeller
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound(openmm)

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.molsysmt_MolSys import get_coordinates_from_atom
    from molsysmt import puw

    tmp_topology = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices, check_form=False)
    tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices, check_form=False)
    tmp_positions = puw.convert(tmp_positions, to_form='openmm.unit')

    tmp_item = Modeller(tmp_topology, tmp_positions[0])

    return tmp_item

