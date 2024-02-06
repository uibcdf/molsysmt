from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest

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
    def add(self, item, atom_indices='all', structure_indices='all', skip_digestion=False):

        self.topology.add(item.topology, atom_indices=atom_indices, skip_digestion=True)
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

