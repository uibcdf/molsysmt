from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.native import MolSys
    from molsysmt.tools.string_pdb_text import to_molsysmt_Topology as string_pdb_text_to_molsysmt_Topology
    from molsysmt.tools.string_pdb_text import to_molsysmt_Structures as string_pdb_text_to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = string_pdb_text_to_molsysmt_Topology(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)
    tmp_item.trajectory = string_pdb_text_to_molsysmt_Structures(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

