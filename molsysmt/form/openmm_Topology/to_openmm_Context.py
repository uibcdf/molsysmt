from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Context(item, atom_indices='all', coordinates=None, digest=True):

    from . import to_openmm_System
    from ..openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item = to_openmm_System(item, atom_indices=atom_indices, coordinates=coordinates, digest=False)
    tmp_item = openmm_System_to_openmm_Context(tmp_item, digest=False)

    return tmp_item

