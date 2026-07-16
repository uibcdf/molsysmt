#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest

form='file:crd'


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """Reading the number of atoms from a CHARMM CRD header."""

    from molsysmt._private.files_and_directories import str_filename

    filename = str_filename(item)
    with open(filename, encoding='utf-8') as file:
        for line in file:
            stripped = line.strip()
            if not stripped or stripped.startswith('*'):
                continue
            return int(stripped.split()[0])

    from molsysmt._private.smonitor import FormatError

    raise FormatError('The CHARMM CRD header does not contain an atom count.')


# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
