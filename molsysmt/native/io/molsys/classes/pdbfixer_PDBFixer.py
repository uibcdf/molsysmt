def from_pdbfixer_PDBFixer (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology, _ = pdbfixer_PDBFixer_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = pdbfixer_PDBFixer_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import to_file_pdb as molsysmt_MolSys_to_file_pdb
    from pdbfixer.pdbfixer import PDBFixer
    from io import StringIO

    tmp_item, _ = molsysmt_MolSys_to_file_pdb(item, atom_indices=atom_indices, frame_indices=frame_indices, output_filename='.pdb')
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

