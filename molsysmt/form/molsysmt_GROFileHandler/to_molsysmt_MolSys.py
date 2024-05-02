from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.GROFileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                       skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.build import get_missing_bonds as _get_missing_bonds
    from molsysmt.pbc import get_box_from_lengths_and_angles

    tmp_item = MolSys()

    tmp_item.topology.reset_atoms(n_atoms=item.entry.n_atoms)
    tmp_item.topology.reset_groups(n_groups=item.entry.n_groups)
    tmp_item.topology.reset_chains(n_chains=1)

    tmp_item.topology.atoms.atom_id = item.entry.atom_ids
    tmp_item.topology.atoms.atom_name = item.entry.atom_names
    tmp_item.topology.atoms.group_index = item.entry.atom_group_index
    tmp_item.topology.atoms.chain_index = np.zeros(shape=[item.entry.n_atoms], dtype=int)

    tmp_item.topology.rebuild_atoms(redefine_ids=False, redefine_types=True)

    tmp_item.topology.groups.group_id = item.entry.group_ids
    tmp_item.topology.groups.group_name = item.entry.group_names

    tmp_item.topology.rebuild_groups(redefine_ids=False, redefine_types=True)

    tmp_item.topology.chains.iloc[0,0] = 0
    tmp_item.topology.chains.iloc[0,1] = 'A'

    tmp_item.structures.append(coordinates=item.entry.coordinates, box=item.entry.box,
                               velocities=item.entry.velocities)

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

