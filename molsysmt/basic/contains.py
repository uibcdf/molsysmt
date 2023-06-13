from molsysmt._private.digestion import digest
import numpy as np

def _evaluation(condition, n_in_system):

    output = True

    if condition is not None:
        if type(condition)==bool:
            if condition==True and n_in_system==0:
                output = False
            elif condition==False and n_in_system>0:
                output = False
        elif type(condition)==int:
            if condition>n_in_system:
                output = False

    return output

@digest()
def contains(molecular_system, selection=None, syntax='MolSysMT', **kwargs):
    """
    Checking if a molecular system contains certain elements.

    Attributes from two molecular systems can be compared according to two rules: equality
    ('equal') and containment ('in').
    However, if no attributes are chosen to be compared, the entire input systems are
    compared. If you only want to include certain elements or structures in the comparison, make
    use of the input arguments ``selection``, ``structure_indices``, ``selection_2``, and
    ``structure_indices_2``.
    """

    from . import get

    atts_required = {}
    aux_atts = {}
    for key in kwargs.keys():
        atts_required[key] = kwargs[key]
        aux_atts[key] = True

    n_atts_required = len(atts_required)

    if n_atts_required:

        atts_values = get(molecular_system, selection=selection, syntax=syntax, **aux_atts)


        if n_atts_required==1:
            atts_values = [atts_values]

        for att, att_value in zip(aux_atts.keys(), atts_values):
            if not _evaluation(atts_required[att], att_value):
                return False

    else:

        n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax, n_atoms=True)

        if not n_atoms:
            return False

    return True

