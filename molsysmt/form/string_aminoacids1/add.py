from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'string:aminoacids1')
        digest_item(to_item, 'string:aminoacids1')

    raise NotImplementedMethodError()

