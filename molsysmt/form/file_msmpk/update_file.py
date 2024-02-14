from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def update_file(item, skip_digestion=False):

    from molsysmt.native import MolSys
    from ..molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk
    from molsysmt import pyunitwizard as puw
    import pickle
    import bz2

    fff = bz2.BZ2File(item,'rb')
    tmp_item = pickle.load(fff)
    fff.close()


    molsys = MolSys()

    # Topology

    if 'atom_index' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['atom_index']=tmp_item.topology.atoms_dataframe['atom_index']

    if 'atom_name' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['atom_name']=tmp_item.topology.atoms_dataframe['atom_name']

    if 'atom_id' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['atom_id']=tmp_item.topology.atoms_dataframe['atom_id']

    if 'atom_type' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['atom_type']=tmp_item.topology.atoms_dataframe['atom_type']

    if 'group_index' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['group_index']=tmp_item.topology.atoms_dataframe['group_index']

    if 'group_id' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['group_id']=tmp_item.topology.atoms_dataframe['group_id']

    if 'group_name' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['group_name']=tmp_item.topology.atoms_dataframe['group_name']

    if 'group_type' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['group_type']=tmp_item.topology.atoms_dataframe['group_type']

    if 'component_index' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['component_index']=tmp_item.topology.atoms_dataframe['component_index']

    if 'component_name' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['component_name']=tmp_item.topology.atoms_dataframe['component_name']

    if 'component_id' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['component_id']=tmp_item.topology.atoms_dataframe['component_id']

    if 'component_type' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['component_type']=tmp_item.topology.atoms_dataframe['component_type']

    if 'chain_index' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['chain_index']=tmp_item.topology.atoms_dataframe['chain_index']

    if 'chain_name' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['chain_name']=tmp_item.topology.atoms_dataframe['chain_name']

    if 'chain_id' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['chain_id']=tmp_item.topology.atoms_dataframe['chain_id']

    if 'chain_type' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['chain_type']=tmp_item.topology.atoms_dataframe['chain_type']

    if 'molecule_index' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['molecule_index']=tmp_item.topology.atoms_dataframe['molecule_index']

    if 'molecule_name' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['molecule_name']=tmp_item.topology.atoms_dataframe['molecule_name']

    if 'molecule_id' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['molecule_id']=tmp_item.topology.atoms_dataframe['molecule_id']

    if 'molecule_type' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['molecule_type']=tmp_item.topology.atoms_dataframe['molecule_type']

    if 'entity_index' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['entity_index']=tmp_item.topology.atoms_dataframe['entity_index']

    if 'entity_name' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['entity_name']=tmp_item.topology.atoms_dataframe['entity_name']

    if 'entity_id' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['entity_id']=tmp_item.topology.atoms_dataframe['entity_id']

    if 'entity_type' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['entity_type']=tmp_item.topology.atoms_dataframe['entity_type']

    if 'occupancy' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['occupancy']=tmp_item.topology.atoms_dataframe['occupancy']

    if 'alternate_location' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['alternate_location']=tmp_item.topology.atoms_dataframe['alternate_location']

    if 'b_factor' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['b_factor']=tmp_item.topology.atoms_dataframe['b_factor']

    if 'formal_charge' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['formal_charge']=tmp_item.topology.atoms_dataframe['formal_charge']

    if 'partial_charge' in tmp_item.topology.atoms_dataframe:
        molsys.topology.atoms_dataframe['partial_charge']=tmp_item.topology.atoms_dataframe['partial_charge']

    if 'atom1_index' in tmp_item.topology.bonds_dataframe:
        molsys.topology.bonds_dataframe['atom1_index']=tmp_item.topology.bonds_dataframe['atom1_index']

    if 'atom2_index' in tmp_item.topology.bonds_dataframe:
        molsys.topology.bonds_dataframe['atom2_index']=tmp_item.topology.bonds_dataframe['atom2_index']

    if 'order' in tmp_item.topology.bonds_dataframe:
        molsys.topology.bonds_dataframe['order']=tmp_item.topology.bonds_dataframe['order']

    if 'type' in tmp_item.topology.bonds_dataframe:
        molsys.topology.bonds_dataframe['type']=tmp_item.topology.bonds_dataframe['type']

    # Structures

    if hasattr(tmp_item.structures, 'structure_id'):
        molsys.structures.structure_id=tmp_item.structures.structure_id

    if hasattr(tmp_item.structures, 'time'):
        value = tmp_item.structures.time
        if value is not None:
            quantity = puw.quantity(value, 'ps')
            molsys.structures.time = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'coordinates'):
        value = tmp_item.structures.coordinates
        if value is not None:
            quantity = puw.quantity(value, 'nm')
            molsys.structures.coordinates = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'velocities'):
        value = tmp_item.structures.velocities
        if value is not None:
            quantity = puw.quantity(value, 'nm/ps')
            molsys.structures.velocities = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'box'):
        value = tmp_item.structures.box
        if value is not None:
            quantity = puw.quantity(value, 'nm')
            molsys.structures.box = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'temperature'):
        value = tmp_item.structures.temperature
        if value is not None:
            quantity = puw.quantity(value, 'kelvin')
            molsys.structures.temperature = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'potential_energy'):
        value = tmp_item.structures.potential_energy
        if value is not None:
            quantity = puw.quantity(value, 'kJ/mol')
            molsys.structures.potential_energy = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'kinetic_energy'):
        value = tmp_item.structures.kinetic_energy
        if value is not None:
            quantity = puw.quantity(value, 'kJ/mol')
            molsys.structures.kinetic_energy = puw.standardize(quantity)

    if hasattr(tmp_item.structures, 'occupancy'):
        molsys.structures.occupancy=tmp_item.structures.occupancy

    if hasattr(tmp_item.structures, 'b_factor'):
        molsys.structures.b_factor=tmp_item.structures.b_factor

    if hasattr(tmp_item.structures, 'bioassembly'):
        molsys.structures.bioassembly=tmp_item.structures.bioassembly

    molsys.structures.n_atoms=tmp_item.structures.n_atoms
    molsys.structures.n_structures=tmp_item.structures.n_structures

    # New msmpk

    tmp_item = molsysmt_MolSys_to_file_msmpk(molsys, output_filename=item, skip_digestion=True)

    return tmp_item

