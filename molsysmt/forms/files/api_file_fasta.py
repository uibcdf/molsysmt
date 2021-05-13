from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='file:fasta'

is_form = {
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements']:
    has[ii]=True

def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', frame_indices='all'):

    from Bio.SeqIO import read as Bio_SeqRecord_reader
    from molsysmt.forms.classes.api_Bio_SeqRecord import extract as extract_Bio_SeqRecord

    tmp_item=Bio_SeqRecord_reader(item,'fasta')
    tmp_item=extract_Bio_SeqRecord(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_molecular_system=molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_file_crd(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=False):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return NotImplementedError()
    else:
        raise NotImplementedError()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

###### Get

