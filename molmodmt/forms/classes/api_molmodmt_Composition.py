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

    tmp_item['molecule.index'] = Series(atom.molecule.index for atom in item.atom).values
    tmp_item['molecule.name'] = Series(atom.molecule.name for atom in item.atom).values
    tmp_item['molecule.id'] = Series(atom.molecule.id for atom in item.atom).values
    tmp_item['molecule.type'] = Series(atom.molecule.type for atom in item.atom).values

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

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_Pandas(item, selection):

    from molmodmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item._dataframe, selection)
    return atom_indices

###### Get

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_element_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molmodmt_Composition import get_bonded_atoms_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #tmp_indices = [trajectory_indices[ii] for ii in indices]
    #bonded_atoms_composition = _get(item.composition, indices=tmp_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #bonded_atoms = {}
    #for ii_composition, ii_bonded_composition in bonded_atoms_composition.items():
    #    bonded_atoms[traduction[ii_composition]]=[traduction[jj] for jj in ii_bonded_composition]

    #return bonded_atoms

def get_molecules_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## group

## chain

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.n_groups

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.n_chains

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return n_molecules

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return n_bonds

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_masses_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molmodmt_Composition import get_bonded_atoms_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #bonded_atoms_composition = _get(item.composition, indices=trajectory_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #bonded_atoms = {}
    #for ii_composition, ii_bonded_composition in bonded_atoms_composition.items():
    #    bonded_atoms[traduction[ii_composition]]=[traduction[jj] for jj in ii_bonded_composition]

    #return bonded_atoms

def get_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_graph_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molmodmt_Composition import get_molecules_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #molecules_composition = _get(item.composition, indices=trajectory_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #molecules = []
    #for tmp_molecule in molecules_composition:
    #    molecules.append([traduction[ii] for ii in tmp_molecule])

    #return molecules

