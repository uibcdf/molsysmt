from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices
import numpy as np
from molsysmt import puw

def to_file_xyznpy(item, atom_indices='all', structure_indices='all', output_filename=None):

    if check:

        digest_item(item, 'XYZ')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    tmp_item = output_filename

    with open(tmp_item, 'wb') as fff:
        np.save(fff, item.shape, allow_pickle=True)
        np.save(fff, puw.get_value(item, to_unit='nm'), allow_pickle=True)

    return tmp_item

