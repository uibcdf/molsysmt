_multiple_conversion_shortcuts = {}


from .to_molsysmt_MolSys import file_prmtop_and_file_inpcrd_to_molsysmt_MolSys


_multiple_conversion_shortcuts[tuple(sorted(('file:prmtop','file:inpcrd')))]={
        'molsysmt.MolSys': file_prmtop_and_file_inpcrd_to_molsysmt_MolSys
        }

