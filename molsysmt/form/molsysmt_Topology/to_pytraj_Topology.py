from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest
import numpy as np

@digest(form='molsysmt.Topology')
def to_pytraj_Topology(item, atom_indices='all', digest=True):

    try:
        from pytraj import Topology
        from pytraj import Atom as pytraj_atom, Residue as pytraj_residue
    except:
        raise LibraryNotFound('pytraj')

    from molsysmt.physchem import mass as get_mass
    from molsysmt.physchem import charge as get_charge
    from molsysmt import pyunitwizard as puw

    n_atoms = item.atoms_dataframe.shape[0]

    atom_index_array = item.atoms_dataframe["atom_index"].to_numpy()
    atom_name_array = item.atoms_dataframe["atom_name"].to_numpy()
    atom_id_array = item.atoms_dataframe["atom_id"].to_numpy()
    atom_type_array = item.atoms_dataframe["atom_type"].to_numpy()

    group_index_array = item.atoms_dataframe["group_index"].to_numpy()
    group_name_array = item.atoms_dataframe["group_name"].to_numpy()
    group_id_array = item.atoms_dataframe["group_id"].to_numpy()
    group_type_array = item.atoms_dataframe["group_type"].to_numpy()

    chain_index_array = item.atoms_dataframe["chain_index"].to_numpy()
    chain_name_array = item.atoms_dataframe["chain_name"].to_numpy()
    chain_id_array = item.atoms_dataframe["chain_id"].to_numpy()
    chain_type_array = item.atoms_dataframe["chain_type"].to_numpy()

    bonds_atom1 = item.bonds_dataframe["atom1_index"].to_numpy()
    bonds_atom2 = item.bonds_dataframe["atom2_index"].to_numpy()

    mass_atom_array = puw.get_value(get_mass(item, digest=False))
    try:
        charge_atom_array = get_charge(molecular_system, digest=False)
    except:
        charge_atom_array = np.zeros(shape=[n_atoms])

    tmp_item = Topology()

    former_group_index = -1

    list_new_atoms = []

    for ii in range(n_atoms):

        atom_index = atom_index_array[ii]
        atom_name = atom_name_array[ii]
        atom_id = atom_id_array[ii]
        atom_type = atom_type_array[ii]
        atom_charge = charge_atom_array[ii]
        atom_mass = mass_atom_array[ii]

        group_index = group_index_array[ii]
        chain_index = chain_index_array[ii]

        new_group = (former_group_index!=group_index)

        if new_group:
            residue_name = group_name_array[ii]
            residue_id = group_id_array[ii]
            residue = pytraj_residue(residue_name, resid=group_index, icode=residue_id, chainID=chain_index)
            former_group_index = group_index

        atom = pytraj_atom(name=atom_name, type=atom_type, resid=group_index, mass=atom_mass, charge=atom_charge)

        list_new_atoms.append(atom)

        tmp_item.add_atom(atom, residue)

    bonds = np.column_stack([bonds_atom1, bonds_atom2])
    tmp_item.add_bonds(bonds)

    return tmp_item

