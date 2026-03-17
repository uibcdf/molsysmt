from molsysmt._private.arg_digestion import arg_digest
import types

form='file:dcd'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """Read n_atoms from the DCD file header."""
    import struct
    from molsysmt._private.files_and_directories import str_filename
    filename = str_filename(item)
    with open(filename, 'rb') as f:
        header_len = struct.unpack('i', f.read(4))[0]
        f.seek(4 + header_len + 4)
        title_len = struct.unpack('i', f.read(4))[0]
        f.seek(title_len + 4, 1)
        f.read(4)  # n_atoms block length
        n_atoms = struct.unpack('i', f.read(4))[0]
    return n_atoms

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
