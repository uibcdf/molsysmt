from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from copy import deepcopy

@digest(form='molsysmt.MolecularMechanics')
def merge(items, atom_indices='all'):

    output = items[0].copy()

    n_items = len(items)

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ValueError(atom_indices)

    list_formal_charge = []
    list_partial_charge = []

    for aux_item, aux_atom_indices in zip(items, atom_indices):

        if is_all(aux_atom_indices):

            list_formal_charge.append(aux_atom_indices.formal_charge)
            list_partial_charge.append(aux_atom_indices.partial_charge)

        else:

            if len(aux_atom_indices)>0:

                if aux_atom_indices.formal_charge is not None:
                    list_formal_charge.append(aux_atom_indices.formal_charge[aux_atom_indices])
                else:
                    list_form_charge.append(None)

                if aux_atom_indices.partial_charge is not None:
                    list_partial_charge.append(aux_atom_indices.partial_charge[aux_atom_indices])
                else:
                    list_partial_charge.append(None)

    if any([ii is None for ii in list_formal_charge]):
        output.formal_charge = puw.concatenate(list_formal_charge)
    else:
        output.formal_charge = None

    if any([ii is None for ii in list_partial_charge]):
        output.partial_charge = puw.concatenate(list_partial_charge)
    else:
        output.partial_charge = None

    pass

