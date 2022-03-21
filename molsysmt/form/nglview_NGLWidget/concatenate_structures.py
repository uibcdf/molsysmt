from .is_nglview_NGLWidget import is_nglview_NGLWidget
from molsysmt._private.exceptions import WrongFormError, WrongStepError
from molsysmt._private.step import digest_step
from molsysmt._private.time import digest_time
from molsysmt._private.coordinates import digest_coordinates
from molsysmt._private.box import digest_box

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        try:
            is_nglview_NGLWidget(item)
        except:
            raise WrongFormError('nglview.NGLWidget')

        try:
            step = digest_step(step)
        except:
            raise WrongStepError()

        try:
            time = digest_time(time)
        except:
            raise WrongTimeError()

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

        try:
            box = digest_box(box)
        except:
            raise WrongBoxError()

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    from ..molsysmt_MolSys import append_structures as append_structures_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item)
    append_structures_molsysmt_MolSys(tmp_item, step=step, time=time, coordinates=coordinates, box=box)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

