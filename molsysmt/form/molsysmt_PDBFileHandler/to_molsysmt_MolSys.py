from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=False,
                       skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.build import get_missing_bonds as _get_missing_bonds
    from molsysmt.pbc import get_box_from_lengths_and_angles

    tmp_item = MolSys()

    atom_id_array = []
    atom_name_array = []
    group_index_array = []
    group_id_array = []
    group_name_array = []
    chain_index_array = []
    chain_name_array = []

    occupancy_array = []
    alternate_location_array = []
    coordinates_array = []

    group_index = -1
    former_group_id = None

    chain_index = -1
    former_chain_name = None
    aux_dict_chain = {}

    group_id_bck = []
    group_name_bck = []

    for atom_record in item.entry.coordinate.model[0].record:

        atom_id_array.append(int(atom_record.serial))
        atom_name_array.append(atom_record.name)

        group_id_bck.append(int(atom_record.resSeq))
        group_name_bck.append(atom_record.resName)

        if former_group_id!=atom_record.resSeq:
            group_id_array.append(int(atom_record.resSeq))
            group_name_array.append(atom_record.resName)
            group_index += 1
            former_group_id = atom_record.resSeq

        group_index_array.append(group_index)

        if former_chain_name!=atom_record.chainId:
            if atom_record.chainId in aux_dict_chain:
                chain_index = aux_dict_chain[atom_record.chainId]
            else:
                chain_index += 1
                aux_dict_chain[atom_record.chainId]=chain_index
                chain_name_array.append(atom_record.chainId)

        chain_index_array.append(chain_index)

    atom_id_array = np.array(atom_id_array, dtype=int)
    atom_name_array = np.array(atom_name_array, dtype=str)
    group_index_array = np.array(group_index_array, dtype=int)
    chain_index_array = np.array(chain_index_array, dtype=int)
    group_id_array = np.array(group_id_array, dtype=int)
    group_name_array = np.array(group_name_array, dtype=str)
    chain_name_array = np.array(chain_name_array, dtype=str)

    for model in item.entry.coordinate.model:

        tmp_occupancy = []
        tmp_alternate_location = []
        tmp_coordinates = []

        for atom_index, atom_record in enumerate(model.record):

            if atom_id_array[atom_index]!=atom_record.serial:
                raise ValueError
            if atom_name_array[atom_index]!=atom_record.name:
                raise ValueError
            if group_id_bck[atom_index]!=int(atom_record.resSeq):
                raise ValueError
            if group_name_bck[atom_index]!=atom_record.resName:
                raise ValueError

            tmp_occupancy.append(atom_record.occupancy)
            tmp_alternate_location.append(atom_record.altLoc)
            tmp_coordinates.append([atom_record.x, atom_record.y, atom_record.z])

        occupancy_array.append(tmp_occupancy)
        alternate_location_array.append(tmp_alternate_location)
        coordinates_array.append(tmp_coordinates)

    occupancy_array = np.array(occupancy_array, dtype=float)
    alternate_location_array = np.array(alternate_location_array, dtype=str)
    coordinates_array = np.array(coordinates_array, dtype=float)

    n_models = coordinates_array.shape[0]

    alt_atoms_dict = []
    atoms_to_be_removed_with_alt_loc = []

    for model_index in range(n_models):

        alt_atom_indices = np.where(alternate_location_array[model_index]!=' ')[0]

        aux_dict = {}

        if len(alt_atom_indices):

            alt_atom_names = atom_name_array[alt_atom_indices].to_numpy()
            alt_group_index = tmp_item.atoms["group_index"][alt_atom_indices].to_numpy()
            alt_chain_index = tmp_item.atoms["chain_index"][alt_atom_indices].to_numpy()
            for aux_atom_index, aux_atom_name, aux_group_index, aux_chain_index in zip(alt_atom_indices,
                                                                                 alt_atom_names, alt_group_index,
                                                                                 alt_chain_index):
                aux_key = tuple([aux_atom_name, aux_group_index, aux_chain_index])
                if aux_key in aux_dict:
                    aux_dict[aux_key].append(aux_atom_index)
                else:
                    aux_dict[aux_key]=[aux_atom_index]

        aux_atoms_to_be_removed=[]
        for same_atoms in aux_dict.values():
            alt_occupancy = occupancy[model_index][same_atoms]
            alt_loc = alternate_location[model_index][same_atoms]
            if np.allclose(alt_occupancy, alt_occupancy[0]):
                chosen = np.where(alt_loc=='A')[0][0]
            else:
                chosen = np.argmax(alt_occupancy)
            chosen = same_atoms.pop(chosen)
            aux_atoms_to_be_removed += same_atoms

        atoms_to_be_removed_with_alt_loc.append(aux_atoms_to_be_removed)
        alt_atoms_dict.append(aux_dict)

    if not all(len(ii)==0 for ii in atoms_to_be_removed_with_alt_loc):

        if n_models==1:

            atom_id_array = np.delete(atom_id_array, atoms_to_be_removed_with_alt_loc[0])
            atom_name_array = np.delete(atom_name_array, atoms_to_be_removed_with_alt_loc[0])
            group_index_array = np.delete(group_index_array, atoms_to_be_removed_with_alt_loc[0])
            chain_index_array = np.delete(chain_index_array, atoms_to_be_removed_with_alt_loc[0])
            coordinates_array[0] = np.delete(coordinates_array[0], atoms_to_be_removed_with_alt_loc[0])

        else:

            raise NotImplementedError

    n_atoms = atom_id_array.shape[0]
    n_groups = group_name_array.shape[0]
    n_chains = chain_name_array.shape[0]

    tmp_item.topology.reset_atoms(n_atoms=n_atoms)
    tmp_item.topology.reset_groups(n_groups=n_groups)
    tmp_item.topology.reset_chains(n_chains=n_chains)

    tmp_item.topology.atoms.atom_id = atom_id_array
    tmp_item.topology.atoms.atom_name = atom_name_array
    tmp_item.topology.atoms.group_index = group_index_array
    tmp_item.topology.atoms.chain_index = chain_index_array

    tmp_item.topology.rebuild_atoms(redefine_ids=False, redefine_types=True)

    tmp_item.topology.groups.group_id = group_id_array
    tmp_item.topology.groups.group_name = group_name_array

    tmp_item.topology.rebuild_groups(redefine_ids=False, redefine_types=True)

    tmp_item.topology.chains.chain_name = chain_name_array

    tmp_item.topology.rebuild_chains(redefine_ids=True, redefine_types=False)

    del(atom_id_array, atom_name_array, group_index_array, chain_index_array,
        group_id_array, group_name_array, chain_name_array, occupancy_array,
        alternate_location_array, alt_atom_indices, aux_dict)

    coordinates_array = puw.quantity(coordinates_array, 'angstroms')

    cryst1 = item.entry.crystallographic_and_coordinate_transformation.cryst1
    if cryst1 is not None:
        box_lengths = puw.quantity([[cryst1.a, cryst1.b, cryst1.c] for _ in range(n_models)], 'angstroms')
        box_angles = puw.quantity([[cryst1.alpha, cryst1.beta, cryst1.gamma] for _ in range(n_models)], 'degrees')
        box = get_box_from_lengths_and_angles(box_lengths, box_angles, skip_digestion=True)
        del(box_lengths, box_angles)
    else:
        box = None

    tmp_item.structures.append(coordinates=coordinates_array, box=box)

    del(coordinates_array, box)

    if get_missing_bonds:

        bonds = _get_missing_bonds(tmp_item)
        bonds = np.array(bonds)
        tmp_item.topology.reset_bonds(n_bonds=bonds.shape[0])
        tmp_item.topology.bonds.drop(['order', 'type'], axis=1, inplace=True)
        tmp_item.topology.bonds.atom1_index=bonds[:,0]
        tmp_item.topology.bonds.atom2_index=bonds[:,1]

        del(bonds)

        tmp_item.topology.rebuild_components()
        tmp_item.topology.rebuild_molecules()
        tmp_item.topology.rebuild_chains(redefine_ids=False, redefine_types=True)
        tmp_item.topology.rebuild_entities()

    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

