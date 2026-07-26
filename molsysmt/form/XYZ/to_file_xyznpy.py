from molsysmt._private.arg_digestion import arg_digest
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest(form='XYZ')
def to_file_xyznpy(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from molsysmt._private.variables import is_all

    tmp_item = output_filename

    if is_all(structure_indices):
        selected_structure_indices = np.arange(item.shape[0], dtype=int)
    else:
        selected_structure_indices = np.asarray(structure_indices, dtype=int)
    if is_all(atom_indices):
        selected_atom_indices = np.arange(item.shape[1], dtype=int)
    else:
        selected_atom_indices = np.sort(np.asarray(atom_indices, dtype=int))
    selected = item[
        np.ix_(
            selected_structure_indices,
            selected_atom_indices,
            [0, 1, 2],
        )
    ]

    with open(tmp_item, 'wb') as fff:
        np.save(fff, selected.shape, allow_pickle=True)
        np.save(
            fff,
            puw.get_value(selected, to_unit='nm'),
            allow_pickle=True,
        )

    return tmp_item
