# =======================
# PIR File Format
# =======================

"""
PIR File Format
===============

This format was introduced for the Protein Information Resource (PIR), a project of the National
Biomedical Research Foundation (NBRF).

The Protein Information Resource. Nucleic Acids Res. 2000 Jan 1; 28(1): 41–44.
doi: 10.1093/nar/28.1.41 https://doi.org/10.1093/nar/28.1.41
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC102418/

Modeller use PIR as alignment native file.
https://salilab.org/modeller/9v7/manual/node445.html

Other source information:
    http://emboss.sourceforge.net/docs/themes/seqformats/NbrfFormat.html
    https://biopython.org/DIST/docs/api/Bio.SeqIO.PirIO-module.html
    https://salilab.org/modeller/manual/node496.html

- This is EBI format, diferent from modeller, is the default.


"""
from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='file:pir'

is_form = {
        'file:pir': form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements']:
    has[ii]=True

def rewrite_to_style(filename, style=None):

    if style == 'modeller':
        fff = open(filename,"r")
        content = fff.readlines()
        fff.close()

        fff = open(filename,"w")
        fff.writelines(content[0])
        fff.write("sequence:::::::::")
        fff.writelines(content[1:])
        fff.close()

        pass
    else:
        pass

def to_file_pir(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=False):

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

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

