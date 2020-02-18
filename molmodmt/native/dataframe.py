from pandas import DataFrame as PandasDataFrame

class DataFrame(PandasDataFrame):

    def __init__(self):

        composition_columns = ['atom.index', 'atom.name', 'atom.id', 'atom.type', 'atom.formal_charge', 'atom.bonded_atom_indices',
                               'group.index', 'group.name', 'group.id', 'group.type',
                               'component.index', 'component.name', 'component.id', 'component.type',
                               'chain.index', 'chain.name', 'chain.id', 'chain.type',
                               'molecule.index', 'molecule.name', 'molecule.id', 'molecule.type',
                               'entity.index', 'entity.name', 'entity.id', 'entity.type',
                               'bioassembly.index', 'bioassembly.name', 'bioassembly.id', 'bioassembly.type']


        super().__init__(columns=composition_columns)

