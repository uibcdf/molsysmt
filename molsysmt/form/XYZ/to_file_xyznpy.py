from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

@digest(form='XYZ')
def to_file_xyznpy(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    tmp_item = output_filename

    with open(tmp_item, 'wb') as fff:
        np.save(fff, item.shape, allow_pickle=True)
        np.save(fff, puw.get_value(item, to_unit='nm'), allow_pickle=True)

    return tmp_item

