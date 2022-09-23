from molsysmt._private.exceptions import *

def to_file_gro(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filepath=None):

    from molsysmt.api_items.api_openmm_GromacsGroFile import to_file_gro as openmm_GromacsGroFile_to_file_gro
    from molsysmt.native.io.topology import to_openmm_GromacsGroFile as molsysmt_Topology_to_openmm_GromacsGroFile

    tmp_item, tmp_molecular_system = molsysmt_Topology_to_openmm_GromacsGroFile(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_GromacsGroFile_to_file_gro(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

