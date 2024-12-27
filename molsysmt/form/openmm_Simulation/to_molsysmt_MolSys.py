from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.molsys import MolSys
    from . import to_molsysmt_Topology as openmm_Simulation_to_molsysmt_Topology
    from . import to_molsysmt_Structures as openmm_Simulation_to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = openmm_Simulation_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                                  skip_digestion=True)
    tmp_item.structures = openmm_Simulation_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                                      structure_indices=structure_indices,
                                                                      skip_digestion=True)

    return tmp_item

