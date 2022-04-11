from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'string:aminoacids3')
        digest_item(to_item, 'string:aminoacids3')

    raise NotImplementedMethodError()

