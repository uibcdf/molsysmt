from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_structure_indices

def to_nglview_NGLWidget(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

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

    from molsysmt.tools.string_pdb_text import to_molsysmt_MolSys as string_pdb_text_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = string_pdb_text_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, check=False)

    return tmp_item

