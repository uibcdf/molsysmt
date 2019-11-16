from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.composition import Composition as _molmodmt_Composition

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Composition : form_name,
    'molmodmt.Composition': form_name
}

def to_networkx_Graph(item, atom_indices='all', frame_indices='all'):

    from .api_networkx_Graph import extract_subsystem as extract_networkx_Graph
    from networkx import empty_graph

    G = empty_graph(item.n_atoms)

    for bond in item.bond:
        G.add_edge(bond.atom[0].index, bond.atom[1].index)

    tmp_item = extract_networkx_Graph(G, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pandas_DataFrame(item, atom_indices='all', frame_indices='all'):

    from pandas import DataFrame, Series

    tmp_item = DataFrame()

    tmp_item['atom.index'] = Series(atom.index for atom in item.atom).values
    tmp_item['atom.name'] = Series(atom.name for atom in item.atom).values
    tmp_item['atom.id'] = Series(atom.id for atom in item.atom).values
    tmp_item['atom.type'] = Series(atom.type for atom in item.atom).values
    tmp_item['atom.element'] = Series(atom.element for atom in item.atom).values

    tmp_item['group.index'] = Series(atom.group.index for atom in item.atom).values
    tmp_item['group.name'] = Series(atom.group.name for atom in item.atom).values
    tmp_item['group.id'] = Series(atom.group.id for atom in item.atom).values
    tmp_item['group.type'] = Series(atom.group.type for atom in item.atom).values

    tmp_item['component.index'] = Series(atom.component.index for atom in item.atom).values
    tmp_item['component.name'] = Series(atom.component.name for atom in item.atom).values
    tmp_item['component.id'] = Series(atom.component.id for atom in item.atom).values
    tmp_item['component.type'] = Series(atom.component.type for atom in item.atom).values

    tmp_item['chain.index'] = Series(atom.chain.index for atom in item.atom).values
    tmp_item['chain.name'] = Series(atom.chain.name for atom in item.atom).values
    tmp_item['chain.id'] = Series(atom.chain.id for atom in item.atom).values
    tmp_item['chain.type'] = Series(atom.chain.type for atom in item.atom).values

    #tmp_item['molecule.index'] = Series(atom.molecule.index for atom in item.atom).values
    #tmp_item['molecule.name'] = Series(atom.molecule.name for atom in item.atom).values
    #tmp_item['molecule.id'] = Series(atom.molecule.id for atom in item.atom).values
    #tmp_item['molecule.type'] = Series(atom.molecule.type for atom in item.atom).values

    tmp_item['entity.index'] = Series(atom.entity.index for atom in item.atom).values
    tmp_item['entity.name'] = Series(atom.entity.name for atom in item.atom).values
    tmp_item['entity.id'] = Series(atom.entity.id for atom in item.atom).values
    tmp_item['entity.type'] = Series(atom.entity.type for atom in item.atom).values

    tmp_item['bioassembly.index'] = Series(atom.bioassembly.index for atom in item.atom).values
    tmp_item['bioassembly.name'] = Series(atom.bioassembly.name for atom in item.atom).values
    tmp_item['bioassembly.id'] = Series(atom.bioassembly.id for atom in item.atom).values
    tmp_item['bioassembly.type'] = Series(atom.bioassembly.type for atom in item.atom).values

    tmp_item.set_index(tmp_item['atom.index'].values)

    return tmp_item

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def duplicate(item):

    return item.duplicate()

def select_with_Pandas(item, selection):

    from molmodmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item, selection)
    return atom_indices

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

