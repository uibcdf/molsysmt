from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids3(item, atom_indices='all'):

    if check:

        digest_item(item, 'nglview.NGLWidget')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item = molsysmt_Topolgy_to_string_aminoacids3(tmp_item)

    return tmp_item

