from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest
import numpy as np

class MolSys:

    @digest()
    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0,
                skip_digestion=False):

        from .topology import Topology
        from .structures import Structures
        from .molecular_mechanics import MolecularMechanics

        self.topology = Topology(n_atoms=n_atoms, n_groups=n_groups, n_components=n_components,
                                 n_molecules=n_molecules, n_entities=n_entities, n_chains=n_chains,
                                 n_bonds=n_bonds, skip_digestion=True)
        self.structures = Structures(skip_digestion=True)
        self.molecular_mechanics = MolecularMechanics()

    @digest()
    def extract(self, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

        if is_all(atom_indices) and is_all(structure_indices):

            if copy_if_all:
                return self.copy()
            else:
                return self

        else:

            tmp_item = MolSys()
            tmp_item.topology = self.topology.extract(atom_indices=atom_indices, copy_if_all=True,skip_digestion=True)
            tmp_item.structures = self.structures.extract(atom_indices=atom_indices,
                                                          structure_indices=structure_indices, copy_if_all=True,
                                                          skip_digestion=True)
            tmp_item.molecular_mechanics = self.molecular_mechanics.copy()

            return tmp_item


    @digest()
    def remove(self, atom_indices=None, structure_indices=None, copy_if_None=False, skip_digestion=False):

        if (atom_indices is None) and (structure_indices is None):

            if copy_if_None:
                return self.copy()
            else:
                return self

        else:

            if atom_indices is not None:
                atom_indices_to_be_kept = np.setdiff1d(np.arange(self.topology.n_atoms), atom_indices)
            else:
                atom_indices_to_be_kept = 'all'

            if structure_indices is not None:
                structure_indices_to_be_kept = np.setdiff1d(np.arange(self.structures.n_structures), structure_indices)
            else:
                structure_indices_to_be_kept = 'all'

            tmp_item = self.extract(atom_indices=atom_indices_to_be_kept,
                                    structure_indices=structure_indices_to_be_kept, skip_digestion=True)

            return tmp_item

    @digest(form='molsysmt.MolSys')
    def add(self, item, atom_indices='all', structure_indices='all', keep_ids=True, skip_digestion=False):

        self.topology.add(item.topology, atom_indices=atom_indices, keep_ids=keep_ids, skip_digestion=True)
        self.structures.add(item.structures, atom_indices=atom_indices, structure_indices=structure_indices,
                           skip_digestion=True)

    @digest(form='molsysmt.MolSys')
    def append_structures(self, item, atom_indices='all', structure_indices='all', skip_digestion=False):

        self.structures.append_structures(item.structures, atom_indices=atom_indices, structure_indices=structure_indices,
                           skip_digestion=True)

    def copy(self):

        tmp_item = MolSys()
        tmp_item.topology = self.topology.copy()
        tmp_item.structures = self.structures.copy()
        tmp_item.molecular_mechanics = self.molecular_mechanics.copy()
        return tmp_item


    def add_missing_bonds(self, threshold='2 angstroms', selection='all', structure_indices=0, syntax='MolSysMT',
                          engine='MolSysMT', with_templates=True, with_distances=True, skip_digestion=False):

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(self, threshold=threshold, selection=selection, structure_indices=structure_indices,
                                   syntax=syntax, engine='MolSysMT', with_templates=True, with_distances=False,
                                   skip_digestion=True)

        self.topology.bonds['atom1_index'] = np.array(bonds, dtype=int)[:,0]
        self.topology.bonds['atom2_index'] = np.array(bonds, dtype=int)[:,1]

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):

        self.topology.rebuild_atoms(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):

        self.topology.rebuild_groups(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_components(self, redefine_ids=True, redefine_types=True):

        self.topology.rebuild_components(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_molecules(self, redefine_ids=True, redefine_types=True):

        self.topology.rebuild_molecules(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_chains(self, redefine_ids=True, redefine_types=True):

        self.topology.rebuild_chains(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_entities(self, redefine_ids=True, redefine_types=True):

        self.topology.rebuild_entities(redefine_ids=redefine_ids, redefine_types=redefine_types)

