from molsysmt._private.digestion import digest_item

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'pytraj.Trajectory')
        digest_item(to_item, 'pytraj.Trajectory')

    raise NotImplementedMethodError()

