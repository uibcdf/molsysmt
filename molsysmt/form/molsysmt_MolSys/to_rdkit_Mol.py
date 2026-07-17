"""Converting native molecular systems to chemistry-aware RDKit molecules."""

import re

import numpy as np
import pandas as pd

from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest


def _element_symbol(atom_type, atom_name, periodic_table):
    """Resolve an RDKit element symbol without silently inventing carbon."""

    candidates = []
    for value in (atom_type, atom_name):
        if value is None or pd.isna(value):
            continue
        token = str(value).strip().split('.', maxsplit=1)[0]
        match = re.match(r'([A-Za-z]{1,2})', token)
        if match:
            text = match.group(1)
            candidates.extend((text.capitalize(), text[0].upper()))
    for candidate in candidates:
        if periodic_table.GetAtomicNumber(candidate) > 0:
            return candidate
    return None


def _optional_atom_values(topology, name):
    if topology._has_chemical_state_atom_attribute(name, include_none=True):
        return topology._get_chemical_state_atom_attribute(name)
    return None


def _has_value(value):
    """Return whether a scalar optional-table value is present."""

    missing = pd.isna(value)
    return isinstance(missing, (bool, np.bool_)) and not bool(missing)


def _matches(value, expected):
    """Compare an optional-table scalar without coercing ``pd.NA`` to bool."""

    return _has_value(value) and bool(value == expected)


@arg_digest(form='molsysmt.MolSys')
@dep_digest('rdkit')
def to_rdkit_Mol(
    item,
    atom_indices='all',
    structure_indices='all',
    skip_digestion=False,
):
    """Converting the resolved native chemical state and conformers to RDKit."""

    from rdkit import Chem
    from molsysmt._private.smonitor import NotCompatibleConversionError
    from molsysmt.form.molsysmt_MolSys.extract import extract

    source = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    topology = source.topology
    periodic_table = Chem.GetPeriodicTable()

    formal_charge = _optional_atom_values(topology, 'formal_charge')
    aromatic = _optional_atom_values(topology, 'is_aromatic')
    radicals = _optional_atom_values(topology, 'n_unpaired_electrons')
    allows_implicit = _optional_atom_values(topology, 'allows_implicit_hydrogens')
    stereochemistry = _optional_atom_values(topology, 'stereochemistry')

    editable = Chem.RWMol()
    for atom_index, row in topology.atoms.iterrows():
        symbol = _element_symbol(row['atom_type'], row['atom_name'], periodic_table)
        if symbol is None:
            raise NotCompatibleConversionError(
                'molsysmt.MolSys',
                'rdkit.Mol',
                {'atom_type'},
                caller='molsysmt.form.molsysmt_MolSys.to_rdkit_Mol',
                message=(
                    f'Atom {atom_index} has no atom_type or atom_name from which '
                    'an element can be resolved safely.'
                ),
            )
        atom = Chem.Atom(symbol)
        atom.SetProp('_MolSysMTAtomID', str(row['atom_id']))
        if not pd.isna(row['atom_name']):
            atom.SetProp('_MolSysMTAtomName', str(row['atom_name']))
        isotope = row.get('isotope', pd.NA)
        if not pd.isna(isotope):
            atom.SetIsotope(int(isotope))
        if formal_charge is not None and not pd.isna(formal_charge.iloc[atom_index]):
            atom.SetFormalCharge(int(formal_charge.iloc[atom_index]))
        if radicals is not None and not pd.isna(radicals.iloc[atom_index]):
            atom.SetNumRadicalElectrons(int(radicals.iloc[atom_index]))
        if allows_implicit is not None and not pd.isna(allows_implicit.iloc[atom_index]):
            atom.SetNoImplicit(not bool(allows_implicit.iloc[atom_index]))
        if aromatic is not None and not pd.isna(aromatic.iloc[atom_index]):
            atom.SetIsAromatic(bool(aromatic.iloc[atom_index]))
        editable.AddAtom(atom)

    bond_type_by_order = {
        0: Chem.BondType.ZERO,
        1: Chem.BondType.SINGLE,
        2: Chem.BondType.DOUBLE,
        3: Chem.BondType.TRIPLE,
        4: Chem.BondType.QUADRUPLE,
        5: Chem.BondType.QUINTUPLE,
        6: Chem.BondType.HEXTUPLE,
    }
    fractional_bond_type = {
        1.5: Chem.BondType.ONEANDAHALF,
        2.5: Chem.BondType.TWOANDAHALF,
        3.5: Chem.BondType.THREEANDAHALF,
        4.5: Chem.BondType.FOURANDAHALF,
        5.5: Chem.BondType.FIVEANDAHALF,
    }
    bond_rows = []
    for _, row in topology._get_chemical_state_bonds().iterrows():
        atom1 = int(row['atom1_index'])
        atom2 = int(row['atom2_index'])
        relationship = row.get('bond_type', pd.NA)
        if _matches(relationship, 'dative'):
            donor = row.get('donor_atom_index', pd.NA)
            acceptor = row.get('acceptor_atom_index', pd.NA)
            if not pd.isna(donor) and not pd.isna(acceptor):
                atom1, atom2 = int(donor), int(acceptor)
            rdkit_bond_type = Chem.BondType.DATIVE
        elif _matches(row.get('is_aromatic', pd.NA), True):
            rdkit_bond_type = Chem.BondType.AROMATIC
        elif not pd.isna(row.get('bond_order', pd.NA)):
            rdkit_bond_type = bond_type_by_order.get(
                int(row['bond_order']), Chem.BondType.UNSPECIFIED
            )
        elif not pd.isna(row.get('fractional_bond_order', pd.NA)):
            rdkit_bond_type = fractional_bond_type.get(
                float(row['fractional_bond_order']), Chem.BondType.UNSPECIFIED
            )
        else:
            rdkit_bond_type = Chem.BondType.UNSPECIFIED
        editable.AddBond(atom1, atom2, rdkit_bond_type)
        bond_rows.append((atom1, atom2, row))

    molecule = editable.GetMol()
    try:
        Chem.SanitizeMol(molecule)
    except Exception as error:
        raise NotCompatibleConversionError(
            'molsysmt.MolSys',
            'rdkit.Mol',
            {'chemical_state'},
            caller='molsysmt.form.molsysmt_MolSys.to_rdkit_Mol',
            message=f'RDKit could not sanitize the converted chemical graph: {error}',
        ) from error

    if stereochemistry is not None:
        desired_stereochemistry = {}
        for atom_index, desired in enumerate(stereochemistry):
            if not _has_value(desired) or desired not in {'R', 'S'}:
                continue
            desired_stereochemistry[atom_index] = desired
            molecule.GetAtomWithIdx(atom_index).SetChiralTag(
                Chem.ChiralType.CHI_TETRAHEDRAL_CW
            )
        if desired_stereochemistry:
            Chem.AssignStereochemistry(molecule, cleanIt=True, force=True)
            for atom_index, desired in desired_stereochemistry.items():
                atom = molecule.GetAtomWithIdx(atom_index)
                observed = (
                    atom.GetProp('_CIPCode') if atom.HasProp('_CIPCode') else None
                )
                if observed != desired:
                    atom.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CCW)
            Chem.AssignStereochemistry(molecule, cleanIt=True, force=True)

    for atom1, atom2, row in bond_rows:
        bond = molecule.GetBondBetweenAtoms(atom1, atom2)
        if bond is None:
            continue
        is_conjugated = row.get('is_conjugated', pd.NA)
        if not pd.isna(is_conjugated):
            bond.SetIsConjugated(bool(is_conjugated))
        stereo = row.get('stereochemistry', pd.NA)
        stereo_atom1 = row.get('stereo_atom1_index', pd.NA)
        stereo_atom2 = row.get('stereo_atom2_index', pd.NA)
        stereo_map = {
            'E': Chem.BondStereo.STEREOE,
            'Z': Chem.BondStereo.STEREOZ,
            'cis': Chem.BondStereo.STEREOCIS,
            'trans': Chem.BondStereo.STEREOTRANS,
        }
        if (
            _has_value(stereo)
            and stereo in stereo_map
            and not pd.isna(stereo_atom1)
            and not pd.isna(stereo_atom2)
        ):
            bond.SetStereoAtoms(int(stereo_atom1), int(stereo_atom2))
            bond.SetStereo(stereo_map[stereo])

    Chem.AssignStereochemistry(molecule, cleanIt=False, force=True)

    mechanics = source.molecular_mechanics
    partial_charge = None if mechanics is None else mechanics.partial_charge
    if partial_charge is not None:
        for atom, charge in zip(molecule.GetAtoms(), partial_charge):
            if not pd.isna(charge):
                atom.SetDoubleProp('_MolSysMTPartialCharge', float(charge))

    if source.structures is not None and source.structures.coordinates is not None:
        from molsysmt import pyunitwizard as puw

        coordinates = np.asarray(
            puw.get_value(source.structures.coordinates, to_unit='angstrom'),
            dtype=np.float64,
        )
        structure_ids = source.structures.structure_id
        for structure_index, positions in enumerate(coordinates):
            conformer = Chem.Conformer(molecule.GetNumAtoms())
            conformer.SetPositions(positions)
            if structure_ids is not None:
                try:
                    conformer.SetId(int(structure_ids[structure_index]))
                except (TypeError, ValueError):
                    conformer.SetProp(
                        '_MolSysMTStructureID', str(structure_ids[structure_index])
                    )
            molecule.AddConformer(conformer, assignId=False)

    Chem.AssignStereochemistry(molecule, cleanIt=False, force=True)
    Chem.SetDoubleBondNeighborDirections(molecule)

    return molecule
