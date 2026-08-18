from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from file:mol2 to file.pdb.

    Parameters
    ----------
    item : file:mol2
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pdb
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_file_pdb import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_file_pdb(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, skip_digestion=True)

    return tmp_item

