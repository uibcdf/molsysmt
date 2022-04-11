from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        digest_item(item, 'nglview.NGLWidget')
        step = digest_step(step)
        time = digest_time(time)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    from ..molsysmt_MolSys import append_structures as append_structures_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, check=False)
    append_structures_molsysmt_MolSys(tmp_item, step=step, time=time, coordinates=coordinates, box=box, check=False)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, check=False)

    return tmp_item

