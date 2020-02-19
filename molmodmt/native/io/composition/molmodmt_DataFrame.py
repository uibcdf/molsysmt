
def from_molmodmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from numpy import arange

    atoms = []
    groups = []
    components = []
    chains = []
    entities = []
    molecules = []
    bioassemblies = []
    bonds = []

    n_atoms = item.shape[0]

    # atoms, group, chain, entity, molecule

    atom_index_array = item["atom.index"].to_numpy()
    atom_name_array = item["atom.name"].to_numpy()
    atom_id_array = item["atom.id"].to_numpy()
    atom_type_array = item["atom.type"].to_numpy()

    group_index_array = item["group.index"].to_numpy()
    group_name_array = item["group.name"].to_numpy()
    group_id_array = item["group.id"].to_numpy()
    group_type_array = item["group.type"].to_numpy()

    component_index_array = item["component.index"].to_numpy()
    component_name_array = item["component.name"].to_numpy()
    component_id_array = item["component.id"].to_numpy()
    component_type_array = item["component.type"].to_numpy()

    chain_index_array = item["chain.index"].to_numpy()
    chain_name_array = item["chain.name"].to_numpy()
    chain_id_array = item["chain.id"].to_numpy()
    chain_type_array = item["chain.type"].to_numpy()

    entity_index_array = item["entity.index"].to_numpy()
    entity_name_array = item["entity.name"].to_numpy()
    entity_id_array = item["entity.id"].to_numpy()
    entity_type_array = item["entity.type"].to_numpy()

    molecule_index_array = item["entity.index"].to_numpy()
    molecule_name_array = item["entity.name"].to_numpy()
    molecule_id_array = item["entity.id"].to_numpy()
    molecule_type_array = item["entity.type"].to_numpy()

    bioassembly_index_array = item["bioassembly.index"].to_numpy()
    bioassembly_name_array = item["bioassembly.name"].to_numpy()
    bioassembly_id_array = item["bioassembly.id"].to_numpy()
    bioassembly_type_array = item["bioassembly.type"].to_numpy()

    former_group_index = -1
    former_component_index = -1
    former_chain_index = -1
    former_entity_index = -1
    former_molecule_index = -1
    former_bioassembly_index = -1

    iterator = zip(atom_index_array, atom_name_array, atom_id_array, atom_type_array,
            group_index_array, group_name_array, group_id_array, group_type_array,
            component_index_array, component_name_array, component_id_array, component_type_array,
            chain_index_array, chain_name_array, chain_id_array, chain_type_array,
            entity_index_array, entity_name_array, entity_id_array, entity_type_array,
            molecule_index_array, molecule_name_array, molecule_id_array, molecule_type_array,
            bioassembly_index_array, bioassembly_name_array, bioassembly_id_array, bioassembly_type_array)

    for atom_index, atom_name, atom_id, atom_type, group_index, group_name, group_id, group_type,\
    component_index, component_name, component_id, component_type, chain_index, chain_name,\
    chain_id, chain_type, entity_index, entity_name, entity_id, entity_type, molecule_index,\
    molecule_name, molecule_id, molecule_type, bioassembly_index, bioassembly_name, bioassembly_id,\
    bioassembly_type in iterator:

        new_group = (former_group_index!=group_index)
        new_component = (former_component_index!=component_index)
        new_molecule = (former_molecule_index!=molecule_index)
        new_chain = (former_chain_index!=chain_index)
        new_entity = (former_entity_index!=entity_index)
        new_bioassembly = (former_bioassembly_index!=bioassembly_index)

        atom = elements.Atom(index=atom_index, id=atom_id, name=atom_name, type=atom_type)
        atoms.append(atom)

        if new_group:
            group = elements.group_init_wizard(index=group_index, id=group_id, name=group_name, type=group_type)
            groups.append(group)
            former_group_index = group_index

        if new_component:
            component = elements.component_init_wizard(index=component_index, id=component_id, name=component_name, type=component_type)
            components.append(component)
            former_component_index = component_index

        if new_molecule:
            molecule = elements.molecule_init_wizard(index=molecule_index, id=molecule_id, name=molecule_name, type=molecule_type)
            molecules.append(molecule)
            former_molecule_index = molecule_index

        if new_chain:
            chain = elements.chain_init_wizard(index=chain_index, id=chain_id, name=chain_name, type=chain_type)
            chains.append(chain)
            former_chain_index = chain_index

        if new_entity:
            entity = elements.entity_init_wizard(index=entity_index, id=entity_id, name=entity_name, type=entity_type)
            entities.append(entity)
            former_entity_index = entity_index

        if new_bioassembly:
            bioassembly = elements.bioassembly_init_wizard(index=bioassembly_index, id=bioassembly_id, name=bioassembly_name, type=bioassembly_type)
            bioassemblies.append(bioassembly)
            former_bioassembly_index = bioassembly_index

        atom.group = group
        group.atom.append(atom)
        group.atom_indices.append(atom_index)
        group.n_atoms+=1

        atom.component = component
        component.atom.append(atom)
        component.atom_indices.append(atom_index)
        component.n_atoms+=1

        atom.chain = chain
        chain.atom.append(atom)
        chain.atom_indices.append(atom_index)
        chain.n_atoms+=1

        atom.molecule = molecule
        molecule.atom.append(atom)
        molecule.atom_indices.append(atom_index)
        molecule.n_atoms+=1

        atom.entity = entity
        entity.atom.append(atom)
        entity.atom_indices.append(atom_index)
        entity.n_atoms+=1

        atom.bioassembly = bioassembly
        bioassembly.atom.append(atom)
        bioassembly.atom_indices.append(atom_index)
        bioassembly.n_atoms+=1

        if new_group:

            group.component = component
            component.group.append(group)
            component.group_indices.append(group_index)
            component.n_groups+=1

            group.chain = chain
            chain.group.append(group)
            chain.group_indices.append(group_index)
            chain.n_groups+=1

            group.molecule = molecule
            molecule.group.append(group)
            molecule.group_indices.append(group_index)
            molecule.n_groups+=1

            group.entity = entity
            entity.group.append(group)
            entity.group_indices.append(group_index)
            entity.n_groups+=1

            group.bioassembly = bioassembly
            bioassembly.group.append(group)
            bioassembly.group_indices.append(group_index)
            bioassembly.n_groups+=1

        if new_component:

            component.chain = chain
            chain.component.append(component)
            chain.component_indices.append(component_index)
            chain.n_components+=1

            component.molecule = molecule
            molecule.component.append(component)
            molecule.component_indices.append(component_index)
            molecule.n_components+=1

            component.entity = entity
            entity.component.append(component)
            entity.component_indices.append(component_index)
            entity.n_components+=1

            component.bioassembly = bioassembly
            bioassembly.component.append(component)
            bioassembly.component_indices.append(component_index)
            bioassembly.n_components+=1

        if new_molecule:

            molecule.entity = entity
            entity.molecule.append(molecule)
            entity.molecule_indices.append(molecule_index)
            entity.n_molecules+=1

            molecule.bioassembly = bioassembly
            bioassembly.molecule.append(molecule)
            bioassembly.molecule_indices.append(molecule_index)
            bioassembly.n_molecules+=1

        if new_chain:

            chain.entity = entity
            entity.chain.append(chain)
            entity.chain_indices.append(chain_index)
            entity.n_chains+=1

            chain.bioassembly = bioassembly
            bioassembly.chain.append(chain)
            bioassembly.chain_indices.append(chain_index)
            bioassembly.n_chains+=1

        if new_entity:

            entity.bioassembly = entity
            bioassembly.entity.append(entity)
            bioassembly.entity_indices.append(entity_index)
            bioassembly.n_entities+=1

    del(atom_index_array, atom_name_array, atom_id_array, atom_type_array)
    del(group_index_array, group_name_array, group_id_array, group_type_array)
    del(component_index_array, component_name_array, component_id_array, component_type_array)
    del(molecule_index_array, molecule_name_array, molecule_id_array, molecule_type_array)
    del(chain_index_array, chain_name_array, chain_id_array, chain_type_array)
    del(entity_index_array, entity_name_array, entity_id_array, entity_type_array)
    del(bioassembly_index_array, bioassembly_name_array, bioassembly_id_array, bioassembly_type_array)

    tmp_item = Composition()

    tmp_item.bioassembly = bioassemblies
    tmp_item.n_bioassemblies = len(bioassemblies)
    tmp_item.bioassembly_indices = arange(tmp_item.n_bioassemblies)

    tmp_item.entity = entities
    tmp_item.n_entities = len(entities)
    tmp_item.entity_indices = arange(tmp_item.n_entities)

    tmp_item.molecule = molecules
    tmp_item.n_molecules = len(molecules)
    tmp_item.molecule_indices = arange(tmp_item.n_molecules)

    tmp_item.chain = chains
    tmp_item.n_chains = len(chains)
    tmp_item.chain_indices = arange(tmp_item.n_chains)

    tmp_item.component = components
    tmp_item.n_components = len(components)
    tmp_item.component_indices = arange(tmp_item.n_components)

    tmp_item.group = groups
    tmp_item.n_groups = len(groups)
    tmp_item.group_indices = arange(tmp_item.n_groups)

    tmp_item.atom = atoms
    tmp_item.n_atoms = len(atoms)
    tmp_item.atom_indices = arange(tmp_item.n_atoms)

    tmp_item.bond = bonds
    tmp_item.n_bonds = len(bonds)
    tmp_item.bond_indices = arange(tmp_item.n_bonds)
    #tmp_item.bonded_atom_indices

    tmp_item.dataframe = item.copy()

    return tmp_item

