def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    try:
        from pdbfixer.pdbfixer import PDBFixer
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound('pdbfixer')

    from molsysmt.tools.molsys_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text
    from io import StringIO

    tmp_item = molsysmt_MolSys_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, check=True)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

