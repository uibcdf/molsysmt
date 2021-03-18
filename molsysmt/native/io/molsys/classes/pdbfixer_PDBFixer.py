def from_pdbfixer_PDBFixer (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = pdbfixer_PDBFixer_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = pdbfixer_PDBFixer_to_molsysmt_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pdbfixer_PDBFixer (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import to_pdb as molsysmt_MolSys_to_pdb
    from pdbfixer.pdbfixer import PDBFixer
    from io import StringIO

    tmp_item = molsysmt_MolSys_to_pdb(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, output_filename='.pdb')
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

