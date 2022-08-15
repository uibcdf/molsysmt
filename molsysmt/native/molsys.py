from molsysmt._private.variables import is_all


class MolSys:

    def __init__(self):

        from .topology import Topology
        from .structures import Structures

        self.topology = Topology()
        self.structures = Structures()

    def extract(self, atom_indices='all', structure_indices='all'):

        if is_all(atom_indices) and is_all(structure_indices):

            return self.copy()

        else:

            tmp_item = MolSys()
            tmp_item.topology = self.topology.extract(atom_indices=atom_indices, structure_indices=structure_indices)
            tmp_item.structures = self.structures.extract(atom_indices=atom_indices, structure_indices=structure_indices)

            return tmp_item

    def add(self, item, selection='all', structure_indices='all', syntax='MolSysMT'):

        from molsysmt import convert, get_form, select

        if get_form(item) != 'molsysmt.MolSys':
            tmp_item = convert(item, to_form='molsysmt.MolSys', selection=selection,
                               structure_indices=structure_indices, syntax=syntax)
            self.topology.add(tmp_item.topology)
            self.structures.add(tmp_item.structures)
        else:
            atom_indices=select(item, selection=selection, syntax=syntax)
            self.topology.add(item.topology, selection=atom_indices)
            self.structures.add(item.structures, selection=atom_indices, structure_indices=structure_indices)

    def load_frames(self, selection='all', structure_indices='all', syntax='MolSysMT'):

        atom_indices = self.select(selection=selection, syntax=syntax)
        return self.structures.load_frames(atom_indices=atom_indices, structure_indices=structure_indices)

    def copy(self):

        tmp_item = MolSys()
        tmp_item.topology = self.topology.copy()
        tmp_item.structures = self.structures.copy()
        return tmp_item

