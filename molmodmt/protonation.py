from .multitool import get_form as _get_form
from .multitool import convert as _convert
from .utils.exceptions import *

def add_hydrogens(item, pH=7.4, engine="openmm", verbose=False):

    form_in = _get_form(item)

    if engine=="openmm":

        tmp_item = _convert(item,"molmodmt.Modeller")
        log_residues_changed = tmp_item.addHydrogens(pH=pH)

        if verbose:
            ii = 0
            for residue in item.topology.residues():
                if log_residues_changed[ii] is not None:


    else:
        raise NotImplementedError

    return tmp_item
