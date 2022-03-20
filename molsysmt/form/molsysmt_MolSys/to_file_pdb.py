from .is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

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

    if output_filename is None:
        raise ValueError('The value different from None is required for the argument "output_filename"')

    from molsysmt.tools.form.molsys_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.form.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, check=False)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, atom_indices=atom_indices, output_filename=output_filename, check=False)

    return tmp_item

