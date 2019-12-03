
def DataFrame():

    from pandas import DataFrame

    tmp_item = DataFrame()

    composition_columns = ['atom.index', 'atom.name', 'atom.id', 'atom.type',
                           'group.index', 'group.name', 'group.id', 'group.type',
                           'component.index', 'component.name', 'component.id', 'component.type',
                           'chain.index', 'chain.name', 'chain.id', 'chain.type',
                           'molecule.index', 'molecule.name', 'molecule.id', 'molecule.type',
                           'entity.index', 'entity.name', 'entity.id', 'entity.type',
                           'bioassembly.index', 'bioassembly.name', 'bioassembly.id', 'bioassembly.type']

    return DataFrame(columns=composition_columns)

