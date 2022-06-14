from molsysmt._private.digestion import digest_item

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'mdanalysis.Topology')
        digest_item(to_item, 'mdanalysis.Topology')

    raise NotImplementedMethodError()

