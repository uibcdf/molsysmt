from pandas import DataFrame as PandasDataFrame

class DataFrame(PandasDataFrame):

    def __init__(self):

        composition_columns = ['atom.index', 'atom.name', 'atom.id', 'atom.type',
                               'atom.formal_charge', 'atom.bonded_atom_indices',
                               'group.index', 'group.name', 'group.id', 'group.type',
                               'component.index', 'component.name', 'component.id', 'component.type',
                               'chain.index', 'chain.name', 'chain.id', 'chain.type',
                               'molecule.index', 'molecule.name', 'molecule.id', 'molecule.type',
                               'entity.index', 'entity.name', 'entity.id', 'entity.type',
                               'bioassembly.index', 'bioassembly.name', 'bioassembly.id', 'bioassembly.type']


        super().__init__(columns=composition_columns)

    def extract(self, atom_indices='all'):

        if type(atom_indices)==str:
            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()
        else:
            tmp_item = DataFrame()
            for column in self.columns:
                tmp_item[column]=self[column][atom_indices]
            return tmp_item

    def copy(self):

        item = DataFrame()
        for column in self.columns:
            item[column]=self[column]

        return item

    def _nan_to_None(self):

        list_columns_where_nan = ['group.type', 'component.name', 'component.type',
                                 'chain.name', 'chain.type', 'molecule.name', 'molecule.type',
                                 'entity.name', 'entity.type', 'bioassembly.name',
                                  'bioassembly.type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

