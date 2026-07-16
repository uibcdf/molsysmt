"""Converting an OpenFF molecule into normalized native chemical-state storage."""

from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all


def _formal_charge_value(atom):
    charge = getattr(atom, 'formal_charge', None)
    try:
        return int(charge.m)
    except Exception:
        try:
            return int(charge)
        except Exception:
            return None


def _fractional_order_value(bond):
    value = getattr(bond, 'fractional_bond_order', None)
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


@arg_digest(form='openff.Molecule')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """Converting independent OpenFF atom and bond chemical fields."""

    import pandas as pd
    from molsysmt.native import Topology

    tmp_item = Topology(n_atoms=item.n_atoms)
    atoms = list(item.atoms)
    tmp_item.atoms['atom_id'] = [str(atom.molecule_atom_index) for atom in atoms]
    tmp_item.atoms['atom_name'] = [
        atom.name if atom.name else f'{atom.symbol}{atom.molecule_atom_index}'
        for atom in atoms
    ]
    tmp_item.atoms['atom_type'] = [atom.symbol for atom in atoms]

    atom_attributes = {
        'formal_charge': [_formal_charge_value(atom) for atom in atoms],
        'is_aromatic': [bool(atom.is_aromatic) for atom in atoms],
        'stereochemistry': [
            atom.stereochemistry if atom.stereochemistry is not None else pd.NA
            for atom in atoms
        ],
    }
    for attribute, values in atom_attributes.items():
        tmp_item._set_chemical_state_atom_attribute(attribute, values)

    bonds = list(item.bonds)
    if bonds:
        tmp_item._append_chemical_state_bonds(
            [[bond.atom1_index, bond.atom2_index] for bond in bonds],
            bond_id=[str(index) for index in range(len(bonds))],
            bond_order=[
                pd.NA if bond.bond_order is None else int(bond.bond_order)
                for bond in bonds
            ],
            fractional_bond_order=[_fractional_order_value(bond) for bond in bonds],
            bond_type=['covalent'] * len(bonds),
            is_aromatic=[bool(bond.is_aromatic) for bond in bonds],
            evidence=['explicit'] * len(bonds),
        )
    tmp_item._chemical_states[0].connectivity_completeness = 'complete'

    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract

        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
