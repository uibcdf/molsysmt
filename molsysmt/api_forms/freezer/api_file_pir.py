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
from molsysmt.api_forms.common_gets import *
import numpy as np
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt._private_tools.files_and_directories import temp_filename

form_name='file:pir'
from_type='file'

is_form = {
        'file:pir': form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements']:
    has[ii]=True

def to_file_pir(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=False):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item, output_filename=output_filename)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all', output_filename=None):

    if output_filename is None:
        output_filename = temp_filename(extension='pir')

    if (atom_indices is 'all') and (structure_indices is 'all'):
        return NotImplementedError()
    else:
        raise NotImplementedError()

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', structure_indices='all'):

    return form_name

