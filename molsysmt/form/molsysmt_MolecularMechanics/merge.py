from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError, InternalAlgorithmError, FormatError
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
from copy import deepcopy

@arg_digest(form='molsysmt.MolecularMechanics')
def merge(items, atom_indices='all', skip_digestion=False):

    output = items[0].copy()

    n_items = len(items)

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ArgumentError("atom_indices", value=atom_indices, caller="molsysmt.form.molsysmt_MolecularMechanics.merge")

    list_formal_charge = []
    list_partial_charge = []
    list_atom_ff_type = []

    for aux_item, aux_atom_indices in zip(items, atom_indices):

        if is_all(aux_atom_indices):

            list_formal_charge.append(aux_item.formal_charge)
            list_partial_charge.append(aux_item.partial_charge)
            list_atom_ff_type.append(aux_item.atom_ff_type)

        else:

            if len(aux_atom_indices) > 0:

                fc = aux_item.formal_charge
                list_formal_charge.append(fc[aux_atom_indices] if fc is not None else None)

                pc = aux_item.partial_charge
                list_partial_charge.append(pc[aux_atom_indices] if pc is not None else None)

                aft = aux_item.atom_ff_type
                list_atom_ff_type.append(aft[aux_atom_indices] if aft is not None else None)

    if any([ii is None for ii in list_formal_charge]):
        output.formal_charge = None
    else:
        output.formal_charge = puw.utils.sequences.concatenate(list_formal_charge)

    if any([ii is None for ii in list_partial_charge]):
        output.partial_charge = None
    else:
        output.partial_charge = puw.utils.sequences.concatenate(list_partial_charge)

    if any([ii is None for ii in list_atom_ff_type]):
        output.atom_ff_type = None
    else:
        import numpy as np
        output.atom_ff_type = np.concatenate(list_atom_ff_type)

    return output

