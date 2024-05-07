from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import types
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt.attribute import bonds_are_required_to_get_attribute

form='string:pdb_id'


## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output



@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'atom')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'group')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From component


@digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'component')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From molecule


@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_aminoacids_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_aminoacids_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_aminoacids', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'molecule')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From entity


@digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'entity')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From chain


@digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'chain')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From bond


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'bond')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'bond')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'bond')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=type)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'bond')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'bond')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system


@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_oligosaccharides', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'system')
    tmp_item = to_molsysmt_Topology(item, get_missing_bonds=bonds_required, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
