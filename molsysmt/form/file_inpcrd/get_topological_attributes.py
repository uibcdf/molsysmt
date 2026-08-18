from molsysmt._private.argdigest import arg_digest
import types

form='file:inpcrd'

# system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:inpcrd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt._private.files_and_directories import str_filename
    filename = str_filename(item)
    with open(filename, 'r') as fff:
        fff.readline()  # title
        # Second line is 'NATOM' (inpcrd) or 'NATOM TIME' (restart)
        n_atoms = int(fff.readline().split()[0])
    return n_atoms


# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
