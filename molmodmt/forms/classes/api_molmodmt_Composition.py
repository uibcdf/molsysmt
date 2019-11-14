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

    # atom.index
    serie = Series(atom.index for atom in item.atom)
    tmp_item['atom.index']= serie.values
    tmp_item.set_index(serie.values)
    del(serie)

    # atom.name
    serie = Series(atom.name for atom in item.atom)
    tmp_item['atom.name']= serie.values
    del(serie)

    # atom.id
    serie = Series(atom.id for atom in item.atom)
    tmp_item['atom.id']= serie.values
    del(serie)

    # atom.element
    serie = Series(atom.element for atom in item.atom)
    tmp_item['atom.element']= serie.values
    del(serie)

    # atom.type
    serie = Series(atom.type for atom in item.atom)
    tmp_item['atom.type']= serie.values
    del(serie)

    # atom.group.index
    serie = Series(atom.group.index for atom in item.atom)
    tmp_item['group.index']= serie.values
    del(serie)

    # atom.group.name
    serie = Series(atom.group.name for atom in item.atom)
    tmp_item['group.name']= serie.values
    del(serie)

    # atom.group.id
    serie = Series(atom.group.id for atom in item.atom)
    tmp_item['group.id']= serie.values
    del(serie)

    # atom.group.type
    serie = Series(atom.group.type for atom in item.atom)
    tmp_item['group.type']= serie.values
    del(serie)

    # atom.component.index
    serie = Series(atom.component.index for atom in item.atom)
    tmp_item['component.index']= serie.values
    del(serie)

    # atom.component.name
    serie = Series(atom.component.name for atom in item.atom)
    tmp_item['component.name']= serie.values
    del(serie)

    # atom.component.id
    serie = Series(atom.component.id for atom in item.atom)
    tmp_item['component.id']= serie.values
    del(serie)

    # atom.component.type
    serie = Series(atom.component.type for atom in item.atom)
    tmp_item['component.type']= serie.values
    del(serie)

    # atom.chain.index
    serie = Series(atom.chain.index for atom in item.atom)
    tmp_item['chain.index']= serie.values
    del(serie)

    # atom.chain.name
    serie = Series(atom.chain.name for atom in item.atom)
    tmp_item['chain.name']= serie.values
    del(serie)

    # atom.chain.id
    serie = Series(atom.chain.id for atom in item.atom)
    tmp_item['chain.id']= serie.values
    del(serie)

    # atom.chain.type
    serie = Series(atom.chain.type for atom in item.atom)
    tmp_item['chain.type']= serie.values
    del(serie)

    ## atom.molecule.index
    #serie = Series(atom.molecule.index for atom in item.atom)
    #tmp_item['molecule.index']= serie.values
    #del(serie)

    ## atom.molecule.name
    #serie = Series(atom.molecule.name for atom in item.atom)
    #tmp_item['molecule.name']= serie.values
    #del(serie)

    ## atom.molecule.id
    #serie = Series(atom.molecule.id for atom in item.atom)
    #tmp_item['molecule.id']= serie.values
    #del(serie)

    ## atom.molecule.type
    #serie = Series(atom.molecule.type for atom in item.atom)
    #tmp_item['molecule.type']= serie.values
    #del(serie)

    # atom.entity.index
    serie = Series(atom.entity.index for atom in item.atom)
    tmp_item['entity.index']= serie.values
    del(serie)

    # atom.entity.name
    serie = Series(atom.entity.name for atom in item.atom)
    tmp_item['entity.name']= serie.values
    del(serie)

    # atom.entity.id
    serie = Series(atom.entity.id for atom in item.atom)
    tmp_item['entity.id']= serie.values
    del(serie)

    # atom.entity.type
    serie = Series(atom.entity.type for atom in item.atom)
    tmp_item['entity.type']= serie.values
    del(serie)

    # atom.bioassembly.index
    serie = Series(atom.bioassembly.index for atom in item.atom)
    tmp_item['bioassembly.index']= serie.values
    del(serie)

    # atom.bioassembly.name
    serie = Series(atom.bioassembly.name for atom in item.atom)
    tmp_item['bioassembly.name']= serie.values
    del(serie)

    # atom.bioassembly.id
    serie = Series(atom.bioassembly.id for atom in item.atom)
    tmp_item['bioassembly.id']= serie.values
    del(serie)

    # atom.bioassembly.type
    serie = Series(atom.bioassembly.type for atom in item.atom)
    tmp_item['bioassembly.type']= serie.values
    del(serie)

    return tmp_item

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def duplicate(item):

    return item.duplicate()

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

