from molsysmt._private.digestion import digest

@digest(form='openmm.Modeller')
def copy(item, skip_digestion=False):

    from openmm.app import Modeller

    tmp_item = Modeller(item.topology, item.positions)

    return tmp_item

