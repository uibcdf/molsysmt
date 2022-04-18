def is_file(form, check=True):

    from .file_inpcrd import is_file_inpcrd
    from .file_prmtop import is_file_prmtop
    from .file_pdb import is_file_pdb
    from .file_mmtf import is_file_mmtf

    output = False

    if is_file_pdb(form):
        output = True
    elif is_file_mmtf(form):
        output = True
    elif is_file_inpcrd(form):
        output = True
    elif is_file_prmtop(form):
        output = True

    return output

