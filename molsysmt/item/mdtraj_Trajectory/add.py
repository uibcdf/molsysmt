from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest_item

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        digest_item(to_item, 'mdtraj.Trajectory')

    raise NotImplementedMethodError()

