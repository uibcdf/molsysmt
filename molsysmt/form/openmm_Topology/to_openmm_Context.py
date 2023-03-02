from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Context(item, atom_indices='all', coordinates=None):

    from . import to_openmm_System
    from ..openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item = to_openmm_System(item, atom_indices=atom_indices, coordinates=coordinates)
    tmp_item = openmm_System_to_openmm_Context(tmp_item)

    return tmp_item

def _to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()
    return to_openmm_Context(item, atom_indices=atom_indices,
                                             forcefield=forcefield, parameters=parameters)


