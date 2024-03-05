from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from datetime import datetime

@digest(form='molsysmt.MolSys')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):

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

    if item.structures.box is not None:

        if is_all(structure_indices):
            lengths, angles = get_lengths_and_angles_from_box(item.structures.box[0])
        else:
            lengths, angles = get_lengths_and_angles_from_box(item.structures.box[structure_indices[0]])

        a,b,c = puw.get_value(lengths[0], to_unit='angstrom')
        alpha,beta,gamma = puw.get_value(angles[0], to_unit='degrees')

        line = f"CRYST1{a:>9.3f}{b:>9.3f}{c:>9.3f}{alpha:>7.2f}{beta:>7.2f}{gamma:>7.2f}\n"
        tmp_item += line

    if is_all(atom_indices):
        aux_df = item.topology.atoms
    else:
        aux_df = item.topology.atoms.iloc[atom_indices]
        aux_df.reset_index(drop=True, inplace=True)

    st_ii=0

    if is_all(atom_indices):
        aux_coors = puw.get_value(item.structures.coordinates[st_ii, :, :], to_unit='angstroms')
    else:
        aux_coors = puw.get_value(item.structures.coordinates[st_ii, atom_indices, :], to_unit='angstroms')

    if with_multiple_models:

        line = f"MODEL     {model_index[st_ii]:>4}"
        tmp_item += line

    for atom in aux_df.itertuples():

        head = 'ATOM'

        atom_id = atom.atom_id
        atom_name = atom.atom_name
        group_name = item.topology.groups.iloc[atom.group_index,1]
        group_id = item.topology.groups.iloc[atom.group_index,0]
        chain_id = item.topology.chains.iloc[atom.chain_index,1]

        x,y,z = aux_coors[atom.Index, :]

        occupancy = 0.0
        temp_factor = 0.0

        element_symbol = atom.atom_type

        line = (
            f"{head:<6}"
            f"{atom_id:>5}"
            f"{' ':1}"
            f"{atom_name:<4}"
            f"{' ':1}"
            f"{group_name:>3}"
            f"{' ':1}"
            f"{chain_id:>1}"
            f"{group_id:>4}"
            f"{' ':1}"
            f"{' ':3}"
            f"{x:>8.3f}"
            f"{y:>8.3f}"
            f"{z:>8.3f}"
            f"{occupancy:>6.2f}"
            f"{temp_factor:>6.2f}"
            f"{' ':10}"
            f"{element_symbol:>2}"
            f"\n"
        )
        tmp_item += line

    if with_multiple_models:

        line = f"ENDMDL"
        tmp_item += line


    tmp_item += 'END\n'

    return tmp_item

