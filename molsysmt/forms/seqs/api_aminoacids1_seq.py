from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='aminoacids1:seq'

is_form={
    'aminoacids1:seq' : form_name,
    'aminoacids1' : form_name
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_bonds=False
with_parameters=False
with_simulation=False

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids3_seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from Bio.SeqUtils import seq3
    tmp_item=seq3(item.replace('aminoacids1:',''))
    return 'aminoacids3:'+tmp_item

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_biopython_Seq import extract as extract_biopython_Seq
    from Bio.Seq import Seq as bio_Seq
    from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    tmp_item = bio_Seq(item.replace('aminoacids1:',''), ExtendedIUPACProtein())
    tmp_item = extract_biopython_Seq(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', frame_indices='all', id=None, name=None, description=None):

    from molsysmt.forms.classes.api_biopython_Seq import to_biopython_SeqRecord as Seq_to_SeqRecord
    tmp_item=to_biopython_Seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item=Seq_to_SeqRecord(tmp_item)
    return tmp_item

def to_fasta(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.classes.api_biopython_SeqRecord import to_fasta as SeqRecord_to_fasta
    tmp_item=to_biopython_SeqRecord(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return SeqRecord_to_fasta(tmp_item, output_filename)

def to_pir(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None, id=None, style=None):

    from molsysmt.forms.classes.api_biopython_SeqRecord import to_pir as SeqRecord_to_pir
    tmp_item= to_biopython_SeqRecord(item, id=id, atom_indices=atom_indices, frame_indices=frame_indices)
    return SeqRecor_to_pir(tmp_item, output_filename=output_filename, style=style)

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    return item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as _get
    return _get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_index_from_atom as _get
    return _get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_id_from_component as get
    return get(item, indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_name_from_component as get
    return get(item, indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_type_from_component as get
    return get(item, indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_id_from_molecule as get
    return get(item, indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_name_from_molecule as get
    return get(item, indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_type_from_molecule as get
    return get(item, indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_id_from_molecule as get
    return get(item, indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_name_from_molecule as get
    return get(item, indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_type_from_molecule as get
    return get(item, indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_n_components_from_system as get
    return get(item, indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_n_molecules_from_system as get
    return get(item, indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_n_entities_from_system as get
    return get(item, indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

