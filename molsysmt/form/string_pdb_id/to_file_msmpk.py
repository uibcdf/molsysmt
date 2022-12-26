from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_file_msmpk(item, atom_indices='all', structure_indices='all', output_filename=None, digest=True):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)
    tmp_item = molsysmt_MolSys_to_file_msmpk(tmp_item, output_filename=output_filename, digest=False)

    return tmp_item

