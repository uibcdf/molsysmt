from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError, WrongStepError
from molsysmt._private_tools.step import digest_step
from molsysmt._private_tools.time import digest_time
from molsysmt._private_tools.coordinates import digest_coordinates
from molsysmt._private_tools.box import digest_box

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

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

    from molsysmt.tools.molsysmt_MolSys.extract import extract

    tmp_item = extract(item)
    tmp_item.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

