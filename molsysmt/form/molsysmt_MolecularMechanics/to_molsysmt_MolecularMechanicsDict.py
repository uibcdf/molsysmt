from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolecularMechanics')
def to_molsysmt_MolecularMechanicsDict(item, atom_indices='all', skip_digestion=False):

    tmp_item = item.to_dict()

    if not is_all(atom_indices):

        if tmp_item['formal_charge'] is not None:
            tmp_item['formal_charge'] = tmp_item['formal_charge'][atom_indices]
    
        if tmp_item['partial_charge'] is not None:
            tmp_item['partial_charge'] = tmp_item['partial_charge'][atom_indices]

    return tmp_item
