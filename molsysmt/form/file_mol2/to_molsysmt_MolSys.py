from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:mol2')
@dep_digest('parmed')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    import pandas as pd

    import numpy as np

    from molsysmt import pyunitwizard as puw
    from molsysmt.native import MolSys, MolecularMechanics, Structures
    from molsysmt.form.parmed_Structure.to_molsysmt_Topology import (
        to_molsysmt_Topology,
    )
    from molsysmt._private.variables import is_all
    from ._reader import read_mol2, _format_error

    structure, metadata = read_mol2(item)
    topology = to_molsysmt_Topology(structure, skip_digestion=True)
    topology.atoms['atom_type'] = [str(atom.type) for atom in structure.atoms]

    atom_id_to_index = {str(atom.number): atom.idx for atom in structure.atoms}
    bond_rows = []
    seen_pairs = set()
    for raw_bond in metadata['bonds']:
        try:
            atom1 = atom_id_to_index[raw_bond['atom1_id']]
            atom2 = atom_id_to_index[raw_bond['atom2_id']]
        except KeyError as error:
            _format_error(
                item,
                f'bond {raw_bond["bond_id"]!r} references unknown atom '
                f'{error.args[0]!r}.',
            )
        pair = tuple(sorted((atom1, atom2)))
        if pair in seen_pairs:
            _format_error(item, f'duplicate bond for atom pair {pair}.')
        seen_pairs.add(pair)

        token = raw_bond['token']
        row = {
            'atom1_index': atom1,
            'atom2_index': atom2,
            'bond_id': str(raw_bond['bond_id']),
            'bond_type': 'covalent',
            'evidence': 'explicit',
        }
        if token in {'1', '2', '3', '4'}:
            row['bond_order'] = int(token)
        elif token == 'ar':
            row['fractional_bond_order'] = 1.5
            row['is_aromatic'] = True
        elif token == 'am':
            row['fractional_bond_order'] = 1.25
            row['is_aromatic'] = False
        else:
            _format_error(
                item,
                f'unsupported bond token {token!r} at line '
                f'{raw_bond["line_number"]}; MolSysMT will not invent its chemistry.',
            )
        bond_rows.append(row)

    topology._set_chemical_state_bonds(pd.DataFrame(bond_rows))
    topology._chemical_states[0].connectivity_completeness = 'complete'
    topology.rebuild_components()
    topology.rebuild_molecules()
    topology.rebuild_entities()
    if topology.n_molecules == 1:
        topology.molecules.loc[0, 'molecule_id'] = metadata['molecule_name']
        topology.molecules.loc[0, 'molecule_name'] = metadata['molecule_name']

    structures = Structures()
    coordinates = getattr(structure, 'coordinates', None)
    if coordinates is not None:
        coordinates = puw.standardize(
            puw.quantity(
                np.asarray(coordinates, dtype=np.float64)[None, :, :],
                'angstrom',
            )
        )
        box = None
        if structure.box is not None:
            from molsysmt.pbc import get_box_from_lengths_and_angles

            box_values = np.asarray(structure.box, dtype=np.float64)
            box = get_box_from_lengths_and_angles(
                puw.quantity(box_values[:3], 'angstrom'),
                puw.quantity(box_values[3:], 'degree'),
                skip_digestion=True,
            )
        structures.append(
            structure_id=np.asarray([0], dtype=np.int64),
            coordinates=coordinates,
            box=box,
            skip_digestion=True,
        )
    partial_charge = None
    if metadata['charge_type'] != 'NO_CHARGES':
        partial_charge = [float(atom.charge) for atom in structure.atoms]

    output = MolSys()
    output.topology = topology
    output.structures = structures
    output.molecular_mechanics = MolecularMechanics(
        partial_charge=partial_charge
    )
    if not is_all(atom_indices) or not is_all(structure_indices):
        from molsysmt.form.molsysmt_MolSys.extract import extract

        output = extract(
            output,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
    return output
