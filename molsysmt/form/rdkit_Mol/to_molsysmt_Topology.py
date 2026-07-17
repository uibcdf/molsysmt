"""Converting an RDKit molecule into normalized native chemical-state storage."""

from molsysmt._private.arg_digestion import arg_digest
import pandas as pd


_RDKIT_BOND_STEREOCHEMISTRY = {
    'STEREOE': 'E',
    'STEREOZ': 'Z',
    'STEREOCIS': 'cis',
    'STEREOTRANS': 'trans',
}


def _rdkit_atom_stereochemistry(atom):
    if atom.HasProp('_CIPCode'):
        value = atom.GetProp('_CIPCode')
        if value in {'R', 'S', 'r', 's'}:
            return value
    return 'unspecified'


def _rdkit_bond_metadata(bond):
    """Return independent canonical values supplied by one RDKit bond."""

    import pandas as pd

    bond_type_name = str(bond.GetBondType()).upper()
    numeric_order = float(bond.GetBondTypeAsDouble())
    is_aromatic = bool(bond.GetIsAromatic())
    is_dative = bond_type_name.startswith('DATIVE')

    if is_aromatic or not numeric_order.is_integer():
        bond_order = pd.NA
        fractional_order = numeric_order
    else:
        bond_order = int(numeric_order)
        fractional_order = pd.NA

    stereochemistry = _RDKIT_BOND_STEREOCHEMISTRY.get(str(bond.GetStereo()))
    stereo_atoms = list(bond.GetStereoAtoms())
    if stereochemistry is None or len(stereo_atoms) != 2:
        stereochemistry = pd.NA
        stereo_atoms = [pd.NA, pd.NA]

    donor = bond.GetBeginAtomIdx() if is_dative else pd.NA
    acceptor = bond.GetEndAtomIdx() if is_dative else pd.NA
    return {
        'bond_id': str(bond.GetIdx()),
        'bond_order': bond_order,
        'fractional_bond_order': fractional_order,
        'bond_type': 'dative' if is_dative else 'covalent',
        'is_aromatic': is_aromatic,
        'is_conjugated': bool(bond.GetIsConjugated()),
        'stereochemistry': stereochemistry,
        'stereo_atom1_index': stereo_atoms[0],
        'stereo_atom2_index': stereo_atoms[1],
        'donor_atom_index': donor,
        'acceptor_atom_index': acceptor,
        'evidence': 'explicit',
    }


@arg_digest(form='rdkit.Mol')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """Converting RDKit atom and bond chemistry without collapsing semantics."""

    from rdkit import Chem
    from molsysmt.native import Topology
    from molsysmt._private.variables import is_all

    Chem.AssignStereochemistry(item, cleanIt=False, force=True)
    tmp_item = Topology(n_atoms=item.GetNumAtoms())

    atoms = list(item.GetAtoms())
    tmp_item.atoms['atom_id'] = [
        atom.GetProp('_MolSysMTAtomID')
        if atom.HasProp('_MolSysMTAtomID')
        else str(atom.GetIdx())
        for atom in atoms
    ]
    tmp_item.atoms['atom_name'] = [
        atom.GetProp('_MolSysMTAtomName')
        if atom.HasProp('_MolSysMTAtomName')
        else (
            atom.GetPDBResidueInfo().GetName().strip()
            if atom.GetPDBResidueInfo() is not None
            else f'{atom.GetSymbol()}{atom.GetIdx()}'
        )
        for atom in atoms
    ]
    tmp_item.atoms['atom_type'] = [atom.GetSymbol() for atom in atoms]
    tmp_item.atoms['isotope'] = pd.array(
        [atom.GetIsotope() or pd.NA for atom in atoms], dtype='UInt16'
    )

    atom_attributes = {
        'formal_charge': [atom.GetFormalCharge() for atom in atoms],
        'is_aromatic': [atom.GetIsAromatic() for atom in atoms],
        'n_unpaired_electrons': [atom.GetNumRadicalElectrons() for atom in atoms],
        'n_implicit_hydrogens': [atom.GetNumImplicitHs() for atom in atoms],
        'allows_implicit_hydrogens': [not atom.GetNoImplicit() for atom in atoms],
        'stereochemistry': [_rdkit_atom_stereochemistry(atom) for atom in atoms],
    }
    for attribute, values in atom_attributes.items():
        tmp_item._set_chemical_state_atom_attribute(attribute, values)

    bonds = list(item.GetBonds())
    if bonds:
        metadata = [_rdkit_bond_metadata(bond) for bond in bonds]
        tmp_item._append_chemical_state_bonds(
            [[bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()] for bond in bonds],
            **{
                field: [row[field] for row in metadata]
                for field in metadata[0]
            },
        )
    tmp_item._chemical_states[0].connectivity_completeness = 'complete'

    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract

        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
