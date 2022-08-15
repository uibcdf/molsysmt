from molsysmt._private.digestion import digest

@digest(form='file:h5')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_file_pdb(tmp_item, output_filename=output_filename)

    return tmp_item

