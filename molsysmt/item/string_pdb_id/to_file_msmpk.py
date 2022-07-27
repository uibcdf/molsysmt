from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_msmpk(item, atom_indices='all', structure_indices='all', output_filename=None):

    if check:

        digest_item(item, 'string:pdb_id')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_file_msmpk(tmp_item, output_filename=output_filename)

    return tmp_item

