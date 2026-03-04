from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology
    
    # We leverage OpenMM's PDB parser which is very robust for topology
    # PDBFileHandler has the file path in self.file.name if it's a file on disk
    
    if hasattr(item.file, 'name'):
        tmp_item = openmm_PDBFile_to_molsysmt_Topology(item.file.name, atom_indices=atom_indices, skip_digestion=True)
    else:
        # If it's a StringIO or buffer
        from openmm.app import PDBFile
        pdb = PDBFile(item.file)
        from molsysmt.form.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
        tmp_item = openmm_Topology_to_molsysmt_Topology(pdb.topology, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
