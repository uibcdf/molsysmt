from .multitool import get_form as _get_form
from .multitool import convert as _convert
from .utils.exceptions import *

def add_hydrogens(item, pH=7.4, engine="openmm", verbose=False):

    form_in = _get_form(item)

    if engine=="openmm":

        tmp_item = _convert(item,"openmm.Modeller")
        log_residues_changed = tmp_item.addHydrogens(pH=pH)

        if verbose:
            ii = 0
            for residue in item.topology.residues():
                if log_residues_changed[ii] is not None:
                    print('{}-{} to {}-{}'.format(residue.name, residue.index,
                                                   log_residues_changed[ii], residue.index))
                ii+=1
    else:
        raise NotImplementedError

    tmp_item = _convert(tmp_item, form_in)

    return tmp_item

