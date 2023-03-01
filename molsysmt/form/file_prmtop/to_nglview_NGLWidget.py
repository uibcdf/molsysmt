from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_nglview_NGLWidget(item, atom_indices='all', coordinates=None):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

def _to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)

    return to_nglview_NGLWidget(item, atom_indices=atom_indices, coordinates=coordinates)

