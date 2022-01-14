def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item):
            raise ItemWithWrongForm('molsysmt.MolSys')

    try:
        from pdbfixer.pdbfixer import PDBFixer
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound('pdbfixer')

    from molsysmt.tools.molsys_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text
    from io import StringIO

    tmp_item = molsysmt_MolSys_to_string_pdb_text(item, atom_indices=atom_indices, frame_indices=frame_indices, check_form=True)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

