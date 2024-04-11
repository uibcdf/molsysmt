#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################
from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='mmtf.MMTFDecoder'


## From atom


@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atom_pairs_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bond_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atom_pairs_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_aminoacids_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_aminoacids_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From component


@digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_aminoacids_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_aminoacids_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_rnas_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From molecule


@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_amino_acids_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_nucleotides_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_ions_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_waters_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_small_molecules_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_lipids_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_oligosaccharides_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_saccharides_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_peptides_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_proteins_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_dnas_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From entity


@digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_aminoacids_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
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

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system

@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return item.num_models
    else:
        return len(structure_indices)

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_box_from_lengths_and_angles

    n_structures = get_n_structures_from_system(item, skip_digestion=True)

    if item.unit_cell is not None:

        cell_lengths = np.empty([n_structures,3], dtype='float64')
        cell_angles = np.empty([n_structures,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles, skip_digestion=True)
        box = puw.standardize(box)

    else:

        box = None

    if not is_all(structure_indices):
        if box is not None:
            box = box[structure_indices,:,:]

    return box

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    output = {}

    for bio_assembly in item.bio_assembly:

        aux = {'chain_indices': [], 'rotations': [], 'translations': []}

        for transformation in bio_assembly['transformList']:

            matrix_transformation = np.array(transformation['matrix']).reshape(-1,4)

            aux['chain_indices'].append(transformation['chainIndexList'])
            aux['rotations'].append(matrix_transformation[:3,:3])
            aux['translations'].append(puw.quantity(matrix_transformation[:3,3], unit='angstroms', standardized=True))

        output[bio_assembly['name']] = aux

    return output

@digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    return len(item.bio_assembly)

## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output




