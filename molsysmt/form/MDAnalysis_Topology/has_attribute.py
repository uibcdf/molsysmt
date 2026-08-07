from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Topology')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from . import attributes

    output = attributes[attribute]

    if output and not include_none:
        if attribute == 'formal_charge':
            import pandas as pd

            output = (
                hasattr(molecular_system, 'formalcharges')
                and pd.Series(molecular_system.formalcharges.values).notna().any()
            )
        elif attribute in {
            'bond_type', 'bond_order', 'fractional_bond_order',
            'bond_is_aromatic', 'bond_evidence',
        }:
            from ._chemical_state import bond_table_from_topology

            column = {
                'bond_type': 'bond_type',
                'bond_order': 'bond_order',
                'fractional_bond_order': 'fractional_bond_order',
                'bond_is_aromatic': 'is_aromatic',
                'bond_evidence': 'evidence',
            }[attribute]
            bond_table = bond_table_from_topology(molecular_system)
            output = column in bond_table and bond_table[column].notna().any()
        elif attribute == 'connectivity_completeness':
            output = hasattr(molecular_system, 'bonds')

    return bool(output)
