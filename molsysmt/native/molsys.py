from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest
import numpy as np

class MolSys:

    def __init__(self):

        from .topology import Topology
        from .structures import Structures
        from .molecular_mechanics import MolecularMechanics

        self.topology = Topology(skip_digestion=True)
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
            tmp_item.topology = self.topology.extract(atom_indices=atom_indices, skip_digestion=True)
            tmp_item.structures = self.structures.extract(atom_indices=atom_indices,
                                                          structure_indices=structure_indices, skip_digestion=True)
            tmp_item.molecular_mechanics = self.molecular_mechanics.copy()

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

