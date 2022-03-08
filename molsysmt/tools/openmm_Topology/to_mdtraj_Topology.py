from molsysmt.tools.pdbfixer_PDBFixer.is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private_tools.exceptions import LibraryNotFoundError
from molsysmt._private_tools.atom_indices import digest_atom_indices

def to_mdtraj_Topology(item, atom_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    try:
        from mdtraj.core.topology import Topology as mdtraj_Topology
    except:
        raise LibraryNotFoundError('MDTraj')

    from molsysmt.tools.openmm_Topology import extract as extract_openmm_Topology

    tmp_item = extract_openmm_Topology(item, atom_indices=atom_indices, copy_if_all=False, check=False)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    return tmp_item


