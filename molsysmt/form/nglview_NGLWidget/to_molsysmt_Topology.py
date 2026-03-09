from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='nglview.NGLWidget')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):

    from .to_string_pdb_text import to_string_pdb_text
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.string_pdb_text.to_molsysmt_Topology import to_molsysmt_Topology as string_pdb_text_to_molsysmt_Topology

    tmp_item_pdb = to_string_pdb_text(item, skip_digestion=True)
    
    # string_pdb_text_to_molsysmt_Topology uses PDBFileHandler which is robust
    tmp_topology = string_pdb_text_to_molsysmt_Topology(tmp_item_pdb, get_missing_bonds=False, skip_digestion=True)

    if get_missing_bonds:
        # We try to get bonds using coordinates from the widget to ensure water is bonded
        from .get_structural_attributes import get_coordinates_from_atom
        coordinates = get_coordinates_from_atom(item, skip_digestion=True)
        
        from molsysmt.native import MolSys
        tmp_molsys = MolSys()
        tmp_molsys.topology = tmp_topology
        from molsysmt.native import Structures
        tmp_molsys.structures = Structures()
        tmp_molsys.structures.coordinates = coordinates
        
        from molsysmt.build import get_missing_bonds as _get_missing_bonds
        # We ensure get_missing_bonds can find the coordinates
        bonded_atoms = _get_missing_bonds(tmp_molsys, skip_digestion=True)
        if bonded_atoms is not None and len(bonded_atoms)>0:
            tmp_topology.add_bonds(bonded_atoms, skip_digestion=True)

    tmp_topology.rebuild_components(force=True)
    tmp_topology.rebuild_molecules(force=True)
    tmp_topology.rebuild_entities(force=True)

    return tmp_topology
