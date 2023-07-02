from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add_missing_bonds(molecular_system, threshold='2 angstroms', engine='MolSysMT', check=True):
    """
    To be written soon...
    """

    if check:

        digest_single_molecular_system(molecular_system)
        engine = digest_engine(engine)

    from molsysmt.basic import convert, get_form

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="ParmEd":

        raise NotImplementedError

    elif engine=="pytraj":

        raise NotImplementedError

    else:

        raise NotImplementedError

    raise NotImplementedError

