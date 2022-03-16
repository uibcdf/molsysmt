from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.group_indices import digest_group_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def to_string_aminoacids3(item, group_indices='all', check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            group_indices = digest_group_indices(group_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = to_molsysmt_Topology(item, check=False)
    tmp_item = molsysmt_Topology_to_string_aminoacids3(tmp_item, group_indices=group_indices, check=False)

    return tmp_item

