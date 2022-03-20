from .is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def to_openmm_System(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()


    from molsysmt.tools.form.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.form.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, check=False)

    return tmp_item

