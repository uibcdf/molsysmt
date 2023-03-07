from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Context(item, atom_indices='all', coordinates=None):

    from . import to_openmm_System
    from ..openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item = to_openmm_System(item, atom_indices=atom_indices, coordinates=coordinates)
    tmp_item = openmm_System_to_openmm_Context(tmp_item)

    return tmp_item

def _to_openmm_Context(item, atom_indices='all', structure_indices='all'):

    return to_openmm_Context(item, atom_indices=atom_indices)


