from molsysmt.tools.pdbfixer_PDBFixer.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices

def to_mdtraj_Topology(item, atom_indices='all', check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from molsysmt.tools.pdbfixer_PDBFixer import to_openmm_Topology as pdbfixer_PDBFixer_to_mdtraj_Topology
    from molsysmt.tools.openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    tmp_item = pdbfixer_PDBFixer_to_openmm_Topology(item, atom_indices=atom_indices, check=False)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item, check=False)

    return tmp_item

