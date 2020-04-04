from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native import DataFrame

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
     DataFrame : form_name,
    'molsysmt.DataFrame': form_name
}

info=["",""]

def to_molsysmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.composition.classes import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Composition
    return molsysmt_DataFrame_to_molsysmt_Composition(item, atom_indices=atom_indices, frame_indices=frame_indices)

def extract_subsystem(item, atom_inices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.iloc(atom_indices)

def duplicate(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item, selection)
    return atom_indices

###### Get

## Atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item['atom.index'].to_list()
    else:
        output = item['atom.index'][indices].to_list()

    return output

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item['atom.id'].to_list()
    else:
        output = item['atom.id'][indices].to_list()

    return output

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item['atom.name'].to_list()
    else:
        output = item['atom.name'][indices].to_list()

    return output

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item['atom.type'].to_list()
    else:
        output = item['atom.type'][indices].to_list()

    return output

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.shape[0]
    else:
        output = len(indices)

    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['group.index'].to_list()
    else:
        output_list = item['group.index'][indices].to_list()

    return output_list

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['group.id'].to_list()
    else:
        output_list = item['group.id'][indices].to_list()

    return output_list

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['group.name'].to_list()
    else:
        output_list = item['group.name'][indices].to_list()

    return output_list

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['group.type'].to_list()
    else:
        output_list = item['group.type'][indices].to_list()

    return output_list

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['component.index'].to_list()
    else:
        output_list = item['component.index'][indices].to_list()

    return output_list

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['component.id'].to_list()
    else:
        output_list = item['component.id'][indices].to_list()

    return output_list

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['component.name'].to_list()
    else:
        output_list = item['component.name'][indices].to_list()

    return output_list

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['component.type'].to_list()
    else:
        output_list = item['component.type'][indices].to_list()

    return output_list

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['chain.index'].to_list()
    else:
        output_list = item['chain.index'][indices].to_list()

    return output_list

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['chain.id'].to_list()
    else:
        output_list = item['chain.id'][indices].to_list()

    return output_list

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['chain.name'].to_list()
    else:
        output_list = item['chain.name'][indices].to_list()

    return output_list

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['chain.type'].to_list()
    else:
        output_list = item['chain.type'][indices].to_list()

    return output_list

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['molecule.index'].to_list()
    else:
        output_list = item['molecule.index'][indices].to_list()

    return output_list

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['molecule.id'].to_list()
    else:
        output_list = item['molecule.id'][indices].to_list()

    return output_list

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['molecule.name'].to_list()
    else:
        output_list = item['molecule.name'][indices].to_list()

    return output_list

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['molecule.type'].to_list()
    else:
        output_list = item['molecule.type'][indices].to_list()

    return output_list

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['entity.index'].to_list()
    else:
        output_list = item['entity.index'][indices].to_list()

    return output_list

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['entity.id'].to_list()
    else:
        output_list = item['entity.id'][indices].to_list()

    return output_list

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['entity.name'].to_list()
    else:
        output_list = item['entity.name'][indices].to_list()

    return output_list

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['entity.type'].to_list()
    else:
        output_list = item['entity.type'][indices].to_list()

    return output_list

def get_bioassembly_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['bioassembly.index'].to_list()
    else:
        output_list = item['bioassembly.index'][indices].to_list()

    return output_list

def get_bioassembly_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['bioassembly.id'].to_list()
    else:
        output_list = item['bioassembly.id'][indices].to_list()

    return output_list

def get_bioassembly_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['bioassembly.name'].to_list()
    else:
        output_list = item['bioassembly.name'][indices].to_list()

    return output_list

def get_bioassembly_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['bioassembly.type'].to_list()
    else:
        output_list = item['bioassembly.type'][indices].to_list()

    return output_list

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item['bioassembly.type'].to_list()
    else:
        output_list = item['bioassembly.type'][indices].to_list()

    return output_list

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from numpy import unique

    df=item

    if indices is 'all':
        output_list = df.loc[df['molecule.type'] == 'water']['group.index'].to_list()
    else:
        output_list = df.loc[df['molecule.type'][indices] == 'water']['group.index'].to_list()

    output_list = unique(output_list)

    return output_list.shape[0]

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from numpy import unique

    df=item

    if indices is 'all':
        output_list = df.loc[df['molecule.type'] == 'ion']['group.index'].to_list()
    else:
        output_list = df.loc[df['molecule.type'][indices] == 'ion']['group.index'].to_list()

    output_list = unique(output_list)

    return output_list.shape[0]

## group

## chain

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.shape[0]

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item['group.index'].iloc[-1]+1

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return item['component.index'].iloc[-1]+1

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item['chain.index'].iloc[-1]+1

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return item['molecule.index'].iloc[-1]+1

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return item['entity.index'].iloc[-1]+1

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    mask=(item['group.type']=='aminoacid').to_numpy()
    serie_indices=item['group.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    mask=(item['group.type']=='nucleotide').to_numpy()
    serie_indices=item['group.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='ion').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='water').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='cosolute').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='small_molecule').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='peptide').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='protein').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='dna').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='rna').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_masses_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_graph_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

