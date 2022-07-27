from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_pdb_text(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'string:pdb_text')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from ..string_pdb_text import extract

    try:
        tmp_item = item.component_0.get_structure_string()
    except:
        tmp_item = item.get_state()['_ngl_msg_archive'][0]['args'][0]['data']

    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
                       copy_if_all=False)

    return tmp_item



