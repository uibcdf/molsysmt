from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
from networkx import Graph, to_dict_of_lists
import __main__
from molsysmt.element import _element_singular_to_plural as _plural_of_element

_large_list_length = 10000

# From atom

## From group

@digest(form=form)
def get_n_bonds_from_group(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_group(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)


@digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all'):

    if is_all(indices):
        return get_n_inner_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_group(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_inner_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)


@digest(form=form)
def get_formal_charge_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_group(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = puw.concatenate(output, type_value='numpy.ndarray', standardized=True)

    return output


@digest(form=form)
def get_partial_charge_from_group(item, indices='all'):

    if indices is None:
        return None

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_group(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output


@digest(form=form)
def get_n_aminoacids_from_group(item, indices='all'):

    group_types = get_group_type_from_group(item, indices=indices)

    return (group_types=='aminoacid').sum()


@digest(form=form)
def get_n_nucleotides_from_group(item, indices='all'):

    group_types = get_group_type_from_group(item, indices=indices)

    return (group_types=='nucleotide').sum()


@digest(form=form)
def get_n_ions_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()


@digest(form=form)
def get_n_waters_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()


@digest(form=form)
def get_n_small_molecules_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()


@digest(form=form)
def get_n_peptides_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()


@digest(form=form)
def get_n_proteins_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()


@digest(form=form)
def get_n_dnas_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()


@digest(form=form)
def get_n_rnas_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()


@digest(form=form)
def get_n_lipids_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()


@digest(form=form)
def get_n_oligosaccharides_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()


@digest(form=form)
def get_n_saccharides_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


# From component

@digest(form=form)
def get_atom_index_from_component(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'atom', 'component')


@digest(form=form)
def get_atom_id_from_component(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'id', 'component')


@digest(form=form)
def get_atom_name_from_component(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'name', 'component')


@digest(form=form)
def get_atom_type_from_component(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'type', 'component')


@digest(form=form)
def get_group_index_from_component(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'group', 'component')


@digest(form=form)
def get_group_id_from_component(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'id', 'component')


@digest(form=form)
def get_group_name_from_component(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'name', 'component')


@digest(form=form)
def get_group_type_from_component(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'type', 'component')


@digest(form=form)
def get_component_index_from_component(item, indices='all'):

    return _get_index_from_element(item, indices, 'component')


@digest(form=form)
def get_chain_index_from_component(item, indices='all'):

    return _get_supr_index_from_element(item, indices, 'chain', 'component')


@digest(form=form)
def get_chain_id_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'chain', 'id', 'component')


@digest(form=form)
def get_chain_name_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'chain', 'name', 'component')


@digest(form=form)
def get_chain_type_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'chain', 'name', 'component')


@digest(form=form)
def get_molecule_index_from_component(item, indices='all'):

    return _get_supr_index_from_element(item, indices, 'molecule', 'component')
    

@digest(form=form)
def get_molecule_id_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'molecule', 'id', 'component')


@digest(form=form)
def get_molecule_name_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'molecule', 'name', 'component')


@digest(form=form)
def get_molecule_type_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'molecule', 'type', 'component')

@digest(form=form)
def get_entity_index_from_component(item, indices='all'):

    return _get_supr_index_from_element(item, indices, 'entity', 'component')


@digest(form=form)
def get_entity_id_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'entity', 'id', 'component')


@digest(form=form)
def get_entity_name_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'entity', 'name', 'component')


@digest(form=form)
def get_entity_type_from_component(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'entity', 'type', 'component')


@digest(form=form)
def get_n_atoms_from_component(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_component(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_component(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_component(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_components_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_component(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_component(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_component(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_bonds_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_component(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all'):

    if is_all(indices):
        return get_n_inner_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_component(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_inner_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_formal_charge_from_component(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_component(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_component(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_component(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_component(item, indices='all'):

    group_indices = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all'):

    group_indices = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'atom', 'molecule')


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'id', 'molecule')


@digest(form=form)
def get_atom_name_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'name', 'molecule')

@digest(form=form)
def get_atom_type_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'type', 'molecule')

@digest(form=form)
def get_group_index_from_molecule(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'group', 'molecule')


@digest(form=form)
def get_group_id_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'id', 'molecule')

@digest(form=form)
def get_group_name_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'name', 'molecule')

@digest(form=form)
def get_group_type_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'type', 'molecule')


@digest(form=form)
def get_component_index_from_molecule(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'component', 'molecule')

@digest(form=form)
def get_component_id_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'component', 'id', 'molecule')

@digest(form=form)
def get_component_name_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'component', 'name', 'molecule')

@digest(form=form)
def get_component_type_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'component', 'type', 'molecule')

@digest(form=form)
def get_chain_index_from_molecule(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'chain', 'molecule')

@digest(form=form)
def get_chain_id_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'chain', 'id', 'molecule')

@digest(form=form)
def get_chain_name_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'chain', 'name', 'molecule')

@digest(form=form)
def get_chain_type_from_molecule(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'chain', 'type', 'molecule')

@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all'):

    return _get_index_from_element(item, indices, 'molecule')


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all'):

    return _get_supr_index_from_element(item, indices, 'entity', 'molecule')


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'entity', 'id', 'component')


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'entity', 'name', 'component')


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all'):

    return _get_supr_attr_from_element(item, indices, 'entity', 'type', 'component')


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_component_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_chains_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_chain_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_entities_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_molecule(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all'):

    if is_all(indices):
        return get_n_inner_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_inner_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_formal_charge_from_molecule(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_molecule(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_molecule(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_molecule(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_molecule(item, indices='all'):

    group_indices = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all'):

    group_indices = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='saccharide').sum()


## chain

@digest(form=form)
def get_atom_index_from_chain(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'atom', 'chain')

@digest(form=form)
def get_atom_id_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'id', 'chain')

@digest(form=form)
def get_atom_name_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'name', 'chain')

@digest(form=form)
def get_atom_type_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'type', 'chain')

@digest(form=form)
def get_group_index_from_chain(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'group', 'chain')

@digest(form=form)
def get_group_id_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'id', 'chain')

@digest(form=form)
def get_group_name_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'name', 'chain')

@digest(form=form)
def get_group_type_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'group', 'type', 'chain')

@digest(form=form)
def get_component_index_from_chain(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'component', 'chain')

@digest(form=form)
def get_component_id_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'component', 'id', 'chain')

@digest(form=form)
def get_component_name_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'component', 'name', 'chain')

@digest(form=form)
def get_component_type_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'component', 'type', 'chain')

@digest(form=form)
def get_chain_index_from_chain(item, indices='all'):

    return _get_index_from_element(item, indices, 'chain')

@digest(form=form)
def get_molecule_index_from_chain(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'molecule', 'chain')

@digest(form=form)
def get_molecule_id_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'molecule', 'id', 'chain')

@digest(form=form)
def get_molecule_name_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'molecule', 'name', 'chain')

@digest(form=form)
def get_molecule_type_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'molecule', 'type', 'chain')

@digest(form=form)
def get_entity_index_from_chain(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'entity', 'chain')

@digest(form=form)
def get_entity_id_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'entity', 'id', 'chain')

@digest(form=form)
def get_entity_name_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'entity', 'name', 'chain')

@digest(form=form)
def get_entity_type_from_chain(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'entity', 'type', 'chain')

@digest(form=form)
def get_n_atoms_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_component_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_molecule_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_chains_from_chain(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_entities_from_chain(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_chain(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_bonds_from_chain(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_chain(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all'):

    if is_all(indices):
        return get_n_inner_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_chain(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_inner_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_formal_charge_from_chain(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_chain(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_chain(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_chain(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_chain(item, indices='all'):

    group_indices = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all'):

    group_indices = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## From entity

@digest(form=form)
def get_atom_index_from_entity(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'atom', 'entity')

@digest(form=form)
def get_atom_id_from_entity(item, indices='all'):

    return get_inf_attr_from_element(item, indices, 'atom', 'id', 'entity')

@digest(form=form)
def get_atom_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_entity(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'group', 'entity')

@digest(form=form)
def get_group_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_entity(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'component', 'entity')

@digest(form=form)
def get_component_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_entity(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'chain', 'entity')

@digest(form=form)
def get_chain_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_index_from_entity(item, indices='all'):

    return _get_inf_index_from_element(item, indices, 'molecule', 'entity')

@digest(form=form)
def get_molecule_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_index_from_entity(item, indices='all'):

    return _get_index_from_element(item, indices, 'entity')

@digest(form=form)
def get_n_atoms_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_component_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_molecule_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_chains_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_chain_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_entities_from_entity(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_bonds_from_entity(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_entity(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all'):

    if is_all(indices):
        return get_n_inner_bonds_from_system(item)
    else:
        atom_indices = get_atom_index_from_entity(item, indices=indices)
        output = []
        for aux_indices in atom_indices:
            aux_val = get_n_inner_bonds_from_atom(item, indices=aux_indices)
            output.append(np.sum(aux_val))
        return np.array(output)

@digest(form=form)
def get_formal_charge_from_entity(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_entity(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_entity(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_entity(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_entity(item, indices='all'):

    group_indices = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all'):

    group_indices = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## From system

@digest(form=form)
def get_n_aminoacids_from_system(item):

    group_types = get_group_type_from_group(item)
    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_system(item):

    group_types = get_group_type_from_group(item)
    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_system(item):

    molecule_types = get_group_type_from_group(item)
    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_system(item):

    molecule_types = get_group_type_from_group(item)
    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_system(item):

    molecule_types = get_group_type_from_group(item)
    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='saccharide').sum()

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_coordinates_from_atom(item, structure_indices=structure_indices)

@digest(form=form)
def get_velocities_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_velocities_from_atom(item, structure_indices=structure_indices)

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_shape_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = get_shape_from_box(tmp_box)

    return output

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_lengths_and_angles_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output, _ = get_lengths_and_angles_from_box(tmp_box)

    return output

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_lengths_and_angles_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    _, output = get_lengths_and_angles_from_box(tmp_box)

    return output

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_volume_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    if tmp_box is None:
        output=None
    else:
        output = get_volume_from_box(tmp_box)

    return output

@digest(form=form)
def get_occupancy_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_occupancy_from_atom(item, indices='all', structure_indices=structure_indices)

@digest(form=form)
def get_b_factor_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_b_factor_from_atom(item, indices='all', structure_indices=structure_indices)

@digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_alternate_location_from_atom(item, indices='all', structure_indices=structure_indices)

@digest(form=form)
def get_formal_charge_from_system(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_system(item, indices)
    charges = get_formal_charge_from_atom(item, atom_indices)
    output = np.sum(charges)

    return output

@digest(form=form)
def get_partial_charge_from_system(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_system(item, indices)
    charges = get_partial_charge_from_atom(item, atom_indices)
    output = np.sum(charges)

    return output

@digest(form=form)
def get_bonded_atoms_from_system(item):

    return get_bonded_atoms_from_atom(item)

@digest(form=form)
def get_bond_index_from_system(item):

    return get_bond_index_from_atom(item)

@digest(form=form)
def get_inner_bonded_atoms_from_system(item):

    return get_inner_bonded_atoms_from_atom(item)

@digest(form=form)
def get_inner_bond_index_from_system(item):

    return get_inner_bond_index_from_atom(item)

## bond

@digest(form=form)
def get_bond_index_from_bond(item, indices='all'):

    return _get_index_from_element(item, indices, 'bond')


@digest(form=form)
def get_n_bonds_from_bond(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_bonds_from_system(item)
    else:
        output = indices.shape[0]

    return output


# Auxiliary methods

def _get_index_from_element(item, indices, element):

    from molsysmt.element import _element_singular_to_plural as _plural

    if indices is None:
        return None

    if is_all(indices):
        aux_get = getattr(__main__, f'get_n_{_plural_of_element[element]}_from_system')
        n_aux = aux_get(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output.tolist()

def _get_inf_index_from_element(item, indices, inf_element, base_element):

    if indices is None:
        return None

    aux_get = getattr(__main__, f'get_{base_element}_index_from_{inf_index}')
    target_index = aux_get(item)

    if len(target_index)>_large_list_length:

        serie = pd.Series(target_index_from_atom)
        groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
        if is_all(indices):
            output = [ii.tolist() for ii in groups_serie]
        else:
            output = [groups_serie[ii].tolist() for ii in indices]

    else:

        indice_dict = {}

        for idx, num in enumerate(target_index):
            try:
                indice_dict[num].append(idx)
            except:
                indice_dict[num] = [idx]

        if is_all(indices):
            output = [indice_dict[ii] for ii in indice_dict.keys()]
        else:
            output = [indice_dict[ii] for ii in indices]

    return output


@digest(form=form)
def get_inf_attr_from_element(item, indices, inf_element, attribute, base_element):

    if indices is None:
        return None

    get_1 = getattr(__main__, f'get_{inf_element}_index_from_{base_element}')
    target_indices = get_1(item)
    get_2 = getattr(__main__, f'get_{inf_element}_{attribute}_from_{inf_element}')

    if len(aux_indices)>0:
        aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
        aux_vals = get_2(item, indices=aux_unique_indices)
        aux_output = aux_vals[aux_indices]
        output = []
        ii = 0
        for aux in target_indices:
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].to_lists())
            ii = jj
        del(aux_unique_indices, aux_vals, aux_output)
    else:
        output = []

    del(target_indices)

    return output


def _get_supr_index_from_element(item, indices, supr_element, base_element):

    if indices is None:
        return None

    get_1 = getattr(__main__, f'get_atom_index_from_{base_element}')
    get_2 = getattr(__main__, f'get_{supr_element}_index_from_atom')

    atom_index_from_target = get_1(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_2(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output


def _get_supr_attr_from_element(item, indices, supr_element, attr, base_element):

    if indices is None:
        return None
    
    aux_element = attr.split('_')[0]
    get_1 = getattr(__main__, f'get_{supr_element}_index_from_{base_element}')
    get_2 = getattr(__main__, f'get_{supr_element}_{attr}_from_{base_element}')

    aux_indices = get_1(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_2(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del(aux_indices, aux_unique_indices, aux_vals, aux_new_indices)

    return output.tolist()

def _get_n_elements(item, indices, element):

    if indices is None:
        return 0

    if is_all(indices):
        aux_get = getattr(__main__, f'get_n_{_plural_of_element[element]}_from_system')
        output = aux_get(item)
    else:
        output = indices.shape[0]

    return output


def _get_n_sup_from_element(item, indices, supr_element, base_element):

    if indices is None:
        return 0

    if is_all(indices):
        aux_get = getattr(__main__, f'get_n_{_plural_of_element[supr_element]}_from_system')
        output = aux_get(item)
    else:
        aux_get = getattr(__main__, f'get_{supr_element}_index_from_{base_element}')
        output = aux_get(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


def _get_n_group_type_from_element(item, indices, group_type, element):

    aux_get = getattr(__main__, f'get_group_index_from_{element}')
    group_indices = aux_get(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (group_types==group_type).sum()

    return output


def _get_n_molecule_type_from_element(item, indices, molecule_type, element):

    aux_get = getattr(__main__, f'get_molecule_index_from_{element}')
    molecule_indices = aux_get(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    output = (molecule_types==molecule_type).sum()

    return output
