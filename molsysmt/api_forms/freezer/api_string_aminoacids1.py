from molsysmt._private_tools.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
from molsysmt.native.molecular_system import molecular_system_components

form_name='string:aminoacids1'
from_type='string'

is_form={
        'string:aminoacids1' : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements']:
    has[ii]=True

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from Bio.SeqUtils import seq3
    tmp_item=seq3(item)
    if molecular_system is not None:
        tmp_molecular_system=molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system=None

    return tmp_item, tmp_molecular_system

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_biopython_Seq import to_biopython_Seq as biopython_Seq_to_biopython_Seq
    from Bio.Seq import Seq as bio_Seq
    #from Bio.Alphabet.IUPAC import ExtendedIUPACProtein

    #tmp_item = bio_Seq(item, ExtendedIUPACProtein())
    tmp_item = bio_Seq(item)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    tmp_item, tmp_molecular_system = biopython_Seq_to_biopython_Seq(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices,
                                                                    structure_indices=structure_indices, copy_if_all=False)
    return tmp_item, tmp_molecular_system

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', structure_indices='all', id=None, name=None, description=None):

    from molsysmt.api_forms.api_biopython_Seq import to_biopython_SeqRecord as Seq_to_SeqRecord

    tmp_item, tmp_molecular_system = to_biopython_Seq(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = Seq_to_SeqRecord(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_fasta(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.api_forms.api_biopython_SeqRecord import to_fasta as SeqRecord_to_fasta

    tmp_item, tmp_molecular_system = to_biopython_SeqRecord(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = SeqRecord_to_fasta(tmp_item, molecular_system=tmp_molecular_system, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def to_pir(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None, id=None, style=None):

    from molsysmt.api_forms.api_biopython_SeqRecord import to_file_pir as SeqRecord_to_file_pir

    tmp_item, tmp_molecular_system = to_biopython_SeqRecord(item, molecular_system=molecular_system, id=id, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = SeqRecor_to_pir(tmp_item, molecular_system=tmp_molecular_system, output_filename=output_filename, style=style)

    return tmp_item, tmp_molecular_system

def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if item.startswith('aminoacids1:'):
        item = item.replace('aminoacids1:','')

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## atom

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as _get
    return _get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import get_molecule_index_from_atom as _get
    return _get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import get_entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## component

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_id_from_component as get
    return get(item, indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_name_from_component as get
    return get(item, indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_type_from_component as get
    return get(item, indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import get_molecule_id_from_molecule as get
    return get(item, indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import get_molecule_name_from_molecule as get
    return get(item, indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import get_molecule_type_from_molecule as get
    return get(item, indices)

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    raise NotImplementedError

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import get_entity_id_from_molecule as get
    return get(item, indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import get_entity_name_from_molecule as get
    return get(item, indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import get_entity_type_from_molecule as get
    return get(item, indices)

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    return None

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    return len(item)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_n_components_from_system as get
    return get(item, indices)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import get_n_molecules_from_system as get
    return get(item, indices)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import get_n_entities_from_system as get
    return get(item, indices)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

