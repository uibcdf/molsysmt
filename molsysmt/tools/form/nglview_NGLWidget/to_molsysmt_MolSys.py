from molsysmt.tools.nglview_NGLWidget.is_nglview_NGLWidget import is_nglview_NGLWidget
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices

def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

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

    from molsysmt.native.molsys import MolSys
    from molsysmt.tools.nglview_NGLWidget import to_molsysmt_Topology as nglview_NGLWidget_to_molsysmt_Topology
    from molsysmt.tools.nglview_NGLWidget import to_molsysmt_Structures as nglview_NGLWidget_to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = nglview_NGLWidget_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                               structure_indices=structure_indices,
                                                               check=False)
    tmp_item.structures = nglview_NGLWidget_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                                   structure_indices=structure_indices,
                                                                   check=False)
    return tmp_item

