from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolecularMechanicsDict')
def to_molsysmt_MolecularMechanics(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native.molecular_mechanics import MolecularMechanics as molsysmt_MolecularMechanics

    if is_all(atom_indices):

        aux_item = item

    else:

        aux_item = item.copy()

        if 'formal_charge' in aux_item:
            if aux_item['formal_charge'] is not None:
                aux_item['formal_charge'] = item['formal_charge'][atom_indices]

        if 'partial_charge' in aux_item:
            if aux_item['partial_charge'] is not None:
                aux_item['partial_charge'] = item['partial_charge'][atom_indices]

    tmp_item = molsysmt_MolecularMechanics(**aux_item)

    return tmp_item
