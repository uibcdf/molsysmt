from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5msm')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=True):

    from . import attributes
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    output = attributes[attribute]

    if not include_none:
        if attribute in {
            'velocities',
            'temperature',
            'potential_energy',
            'kinetic_energy',
        }:
            tmp_item = to_molsysmt_H5MSMFileHandler(
                molecular_system, skip_digestion=True
            )
            try:
                dataset = tmp_item.file['structures'].get(attribute)
                output = dataset is not None and dataset.shape[0] > 0
            finally:
                tmp_item.close()
        elif attribute == 'total_energy':
            tmp_item = to_molsysmt_H5MSMFileHandler(
                molecular_system, skip_digestion=True
            )
            try:
                structures = tmp_item.file['structures']
                output = all(
                    name in structures and structures[name].shape[0] > 0
                    for name in ('potential_energy', 'kinetic_energy')
                )
            finally:
                tmp_item.close()
        elif attribute == 'isotope':
            tmp_item = to_molsysmt_H5MSMFileHandler(
                molecular_system, skip_digestion=True
            )
            try:
                atoms = tmp_item.file['topology']['atoms']
                output = 'isotope' in atoms and bool((atoms['isotope'][:] != 0).any())
            finally:
                tmp_item.close()
        elif attribute == 'b_factor':
            tmp_item = to_molsysmt_H5MSMFileHandler(molecular_system, skip_digestion=True)
            output = ('b_factor' in tmp_item.file['structures']) and (tmp_item.file['structures']['b_factor'].shape[0] > 0)
            tmp_item.close()
        elif attribute == 'structure_chemical_state_index':
            from .get_structural_attributes import (
                get_structure_chemical_state_index_from_system,
            )

            values = get_structure_chemical_state_index_from_system(
                molecular_system, skip_digestion=True
            )
            output = len(values) > 0 and all(value is not None for value in values)
        elif attribute in {
            'formal_charge', 'atom_is_aromatic', 'n_unpaired_electrons',
            'n_implicit_hydrogens', 'allows_implicit_hydrogens',
            'atom_stereochemistry',
            'bond_id', 'bond_type', 'bond_order', 'fractional_bond_order',
            'bond_is_aromatic', 'bond_is_conjugated', 'bond_stereochemistry',
            'bond_stereo_atom_indices', 'bond_donor_atom_index',
            'bond_acceptor_atom_index', 'bond_joins_components', 'bond_evidence',
        }:
            tmp_item = to_molsysmt_H5MSMFileHandler(
                molecular_system, skip_digestion=True
            )
            try:
                from molsysmt.form.molsysmt_H5MSMFileHandler import (
                    has_attribute as handler_has,
                )

                output = handler_has(
                    tmp_item, attribute, include_none=False, skip_digestion=True
                )
            finally:
                tmp_item.close()

    return output
