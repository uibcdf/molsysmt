from molsysmt.tools.nglview_NGLWidget.is_nglview_NGLWidget import is_nglview_NGLWidget
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def to_openmm_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_nglview_NGLWidget(item)
        except:
            raise WrongFormError('nglview.NGLWidget')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.tools.nglview_NGLWidget import to_string_pdb_text as nglview_NGLWidget_to_string_pdb_text
    from molsysmt.tools.string_pdb_text import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    tmp_item = nglview_NGLWidget_to_string_pdb_text(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices,
                                                    check=False)
    tmp_item = string_pdb_text_to_openmm_Topology(tmp_item, check=False)

    return tmp_item

