"""Converting an OpenFF molecule into normalized native chemical-state storage."""

from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest


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


@dep_digest('rdkit')
def _bond_stereo_metadata(item):
    """Return OpenFF E/Z labels with the reference atoms chosen by RDKit."""

    molecule = item.to_rdkit()
    metadata = {}
    for bond in molecule.GetBonds():
        stereo = str(bond.GetStereo())
        if stereo not in {'STEREOE', 'STEREOZ'}:
            continue
        references = list(bond.GetStereoAtoms())
        if len(references) != 2:
            continue
        key = frozenset((bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()))
        metadata[key] = (stereo[-1], references[0], references[1])
    return metadata


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
        stereo_metadata = {}
        if any(bond.stereochemistry is not None for bond in bonds):
            stereo_metadata = _bond_stereo_metadata(item)
        stereo_rows = [
            stereo_metadata.get(
                frozenset((bond.atom1_index, bond.atom2_index)),
                (pd.NA, pd.NA, pd.NA),
            )
            for bond in bonds
        ]
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
            stereochemistry=[row[0] for row in stereo_rows],
            stereo_atom1_index=[row[1] for row in stereo_rows],
            stereo_atom2_index=[row[2] for row in stereo_rows],
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
