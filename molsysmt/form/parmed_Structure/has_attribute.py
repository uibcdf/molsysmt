from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='parmed.Structure')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if output and not include_none:
        if attribute == 'formal_charge':
            output = any(
                getattr(atom, 'formal_charge', None) is not None
                for atom in molecular_system.atoms
            )
        elif attribute == 'atom_is_aromatic':
            output = any(
                getattr(atom, 'aromatic', None) is not None
                for atom in molecular_system.atoms
            )
        elif attribute in {
            'bond_type', 'bond_order', 'fractional_bond_order',
            'bond_is_aromatic', 'bond_evidence',
        }:
            from ._chemical_state import bond_table_from_structure

            column = {
                'bond_type': 'bond_type',
                'bond_order': 'bond_order',
                'fractional_bond_order': 'fractional_bond_order',
                'bond_is_aromatic': 'is_aromatic',
                'bond_evidence': 'evidence',
            }[attribute]
            bond_table, _ = bond_table_from_structure(molecular_system)
            output = column in bond_table and bond_table[column].notna().any()
        elif attribute == 'connectivity_completeness':
            output = hasattr(molecular_system, 'bonds')

    return bool(output)
