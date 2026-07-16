from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from datetime import datetime
import pandas as pd

@arg_digest(form='molsysmt.MolSys')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', pdb_chain_id='chain_name',
                       skip_digestion=False):

    pdb_chain_id_column = 0
    if pdb_chain_id=='chain_name':
        pdb_chain_id_column = 1
    elif pdb_chain_id=='chain_id':
        pdb_chain_id_column = 0

    now = datetime.now()

    from molsysmt.pbc import get_lengths_and_angles_from_box

    tmp_item = ""

    description = "MOLECULAR SYSTEM"
    date = now.strftime('%d-%b-%y').upper()
    pdb_id = ''

    line = f"HEADER    {description:<40}{date:>9}   {pdb_id:<4}\n"
    tmp_item += line


    line = f"REMARK   1 Created by MolSysMT version 1.0 on {now.strftime('%d-%b-%Y').upper()} at {now.strftime('%H:%M:%S')}\n"
    tmp_item += line
    

    with_multiple_models = False

    if is_all(structure_indices):
        if item.structures.coordinates.shape[0]>1:
            with_multiple_models = True
            if item.structures.structure_id is not None:
                model_index = item.structures.structure_id
            else:
                model_index = list(range(item.structures.coordinates.shape[0]))
    else:
        if len(structure_indices)>1:
            with_multiple_models = True
            if item.structures.structure_id is not None:
                model_index = item.structures.structure_id[structure_indices]
            else:
                model_index = list(range(len(structure_indices)))

    if item.structures.box is not None and item.structures.box.shape[0] > 0:

        if is_all(structure_indices):
            lengths, angles = get_lengths_and_angles_from_box(item.structures.box[0])
        else:
            lengths, angles = get_lengths_and_angles_from_box(item.structures.box[structure_indices[0]])

        a,b,c = puw.get_value(lengths[0], to_unit='angstrom')
        alpha,beta,gamma = puw.get_value(angles[0], to_unit='degrees')

        line = f"CRYST1{a:>9.3f}{b:>9.3f}{c:>9.3f}{alpha:>7.2f}{beta:>7.2f}{gamma:>7.2f}\n"
        tmp_item += line

    if is_all(atom_indices):
        aux_df = item.topology.atoms.copy()
        source_atom_indices = aux_df.index.to_numpy()
    else:
        aux_df = item.topology.atoms.iloc[atom_indices].copy()
        source_atom_indices = aux_df.index.to_numpy()
        aux_df.reset_index(drop=True, inplace=True)

    pdb_serial_by_source_atom_index = {}
    for local_atom_index, atom in zip(source_atom_indices, aux_df.itertuples()):
        try:
            pdb_serial_by_source_atom_index[int(local_atom_index)] = int(str(atom.atom_id))
        except (TypeError, ValueError):
            pdb_serial_by_source_atom_index[int(local_atom_index)] = atom.Index + 1

    if is_all(structure_indices):
        structure_indices_to_write = list(range(item.structures.coordinates.shape[0]))
    else:
        structure_indices_to_write = list(structure_indices)

    for local_st_ii, st_ii in enumerate(structure_indices_to_write):

        if is_all(atom_indices):
            aux_coors = puw.get_value(item.structures.coordinates[st_ii, :, :], to_unit='angstroms')
        else:
            aux_coors = puw.get_value(item.structures.coordinates[st_ii, atom_indices, :], to_unit='angstroms')

        if with_multiple_models:
            line = f"MODEL     {model_index[local_st_ii]:>4}\n"
            tmp_item += line

        previous_chain_index = None

        for atom in aux_df.itertuples():

            if previous_chain_index is not None and atom.chain_index != previous_chain_index:
                tmp_item += "TER\n"

            previous_chain_index = atom.chain_index

            head = 'ATOM'

            atom_id = str(atom.atom_id)
            atom_name = atom.atom_name
            group_name = item.topology.groups.iloc[atom.group_index, 1]
            group_id = str(item.topology.groups.iloc[atom.group_index, 0])
            _raw_chain_id = item.topology.chains.iloc[atom.chain_index, pdb_chain_id_column]
            chain_id = str(_raw_chain_id) if not pd.isna(_raw_chain_id) else 'A'

            x,y,z = aux_coors[atom.Index, :]

            occupancy = 0.0
            temp_factor = 0.0

            element_symbol = atom.atom_type if atom.atom_type is not None else ''

            line = (
                f"{head[:6].ljust(6)}"
                f"{atom_id[:5].rjust(5)}"
                f"{' ':1}"
                f"{atom_name[:4].ljust(4)}"
                f"{' ':1}"
                f"{group_name[:3].rjust(3)}"
                f"{' ':1}"
                f"{chain_id[:1].rjust(1)}"
                f"{group_id[:4].rjust(4)}"
                f"{' ':1}"
                f"{' ':3}"
                f"{x:>8.3f}"
                f"{y:>8.3f}"
                f"{z:>8.3f}"
                f"{occupancy:>6.2f}"
                f"{temp_factor:>6.2f}"
                f"{' ':10}"
                f"{element_symbol[:2].rjust(2)}"
                f"\n"
            )
            tmp_item += line

        if with_multiple_models:
            tmp_item += "ENDMDL\n"

    bonds = item.topology._get_chemical_state_bonds()
    if bonds.shape[0] > 0:
        atom_index_in_output = set(int(ii) for ii in source_atom_indices)
        bonded_pairs_written = set()

        for bond in bonds.itertuples():
            atom1_index = int(bond.atom1_index)
            atom2_index = int(bond.atom2_index)

            if atom1_index not in atom_index_in_output or atom2_index not in atom_index_in_output:
                continue

            atom1_serial = pdb_serial_by_source_atom_index[atom1_index]
            atom2_serial = pdb_serial_by_source_atom_index[atom2_index]

            pair = tuple(sorted((atom1_serial, atom2_serial)))
            if pair in bonded_pairs_written:
                continue

            bonded_pairs_written.add(pair)
            tmp_item += f"CONECT{atom1_serial:>5}{atom2_serial:>5}\n"


    tmp_item += 'END\n'

    return tmp_item
