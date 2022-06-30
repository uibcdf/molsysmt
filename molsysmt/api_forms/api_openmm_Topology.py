from molsysmt._private.exceptions import *
from molsysmt.item.openmm_Topology.is_openmm_Topology import is_openmm_Topology as is_form
from molsysmt.item.openmm_Topology.extract import extract
from molsysmt.item.openmm_Topology.add import add
from molsysmt.item.openmm_Topology.append_structures import append_structures
from molsysmt.item.openmm_Topology.get import *
from molsysmt.item.openmm_Topology.set import *
from .form_attributes import form_attributes

form_name = 'openmm.Topology'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['box'] = True


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    return openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_molsysmt_MolSys as openmm_Topology_to_molsysmt_MolSys

    from molsysmt.basic import get

    coordinates, box = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                           coordinates=True, box=True)
    return openmm_Topology_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                              coordinates=coordinates, box=box, check=False)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    return openmm_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    return openmm_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return openmm_Topology_to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates, check=False)


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()
    return openmm_Topology_to_openmm_System(item, atom_indices=atom_indices,
                                            forcefield=forcefield, parameters=parameters,
                                            check=False)


def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_openmm_Context as openmm_Topology_to_openmm_Context

    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()
    return openmm_Topology_to_openmm_Context(item, atom_indices=atom_indices,
                                             forcefield=forcefield, parameters=parameters,
                                             check=False)


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation

    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()
    return openmm_Topology_to_openmm_Context(item, atom_indices=atom_indices,
                                             forcefield=forcefield, parameters=parameters,
                                             check=False)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.item.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return openmm_Topology_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates, check=False)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return openmm_Topology_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates, check=False)


def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_openmm_PDBFile as openmm_Topology_to_openmm_PDBFile

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return openmm_Topology_to_openmm_PDBFile(item, atom_indices=atom_indices, coordinates=coordinates, check=False)


def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Topology import to_nglview_NGLWidget as openmm_Topology_to_nglview_NGLWidget

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return openmm_Topology_to_nglview_NGLWidget(item, atom_indices=atom_indices, coordinates=coordinates, check=False)
