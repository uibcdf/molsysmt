from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'openmm.System')
        digest_item(to_item, 'openmm.System')

    raise NotImplementedMethodError()

