from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest_item

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        digest_item(to_item, 'mdtraj.Topology')

    raise NotImplementedMethodError()

