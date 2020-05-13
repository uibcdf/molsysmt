from molsysmt.utils.exceptions import *
from os.path import basename as _basename
from mdtraj.core.topology import Topology as _mdtraj_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

info=["",""]
with_topology=True
with_trajectory=False

## To other form

def to_aminoacids3_seq(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = 'aminoacids3:'+''.join([ r.name.title() for r in item.residues ])
    return tmp_item

def to_aminoacids1_seq(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as aminoacids3_to_aminoacids1

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = to_aminoacids3_seq(tmp_item)
    tmp_item = aminoacids3_to_aminoacids1(tmp_item)
    return tmp_item

def to_molsysmt_DataFrame(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_mdtraj_Topology as molsysmt_DataFrame_from_mdtraj_Topology
    tmp_item = molsysmt_DataFrame_from_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item.to_openmm()

def to_yank_Topography(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_yank_Topography as opennn_Topology_to_yank_Topography
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = opennn_Topology_to_yank_Topography(tmp_item)
    return tmp_item

def to_parmed_Structure(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_form)
    return tmp_item

def to_parmed_GromacsTopologyFile(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile
    tmp_item = to_parmed_Structure(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return GromacsTopologyFile.from_structure(tmp_item)

def to_top(item, output_filepath=None, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .api_parmed_GromacsTopologyFile import to_top as parmed_GromacsTopologyFile_to_top
    tmp_item = to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return parmed_GromacsTopologyFile_to_top(tmp_item, output_filepath=output_filepath)

def to_pandas_DataFrame(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

# Select

def select_with_MDTraj(item, selection):
    return item.select(selection)

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import dataframe_select
    tmp_item = to_pandas_DataFrame(item)
    atom_indices = dataframe_select(tmp_item, selection)
    del(tmp_item)
    return atom_indices

# Extract

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from mdtraj.core.topology import Topology
        from mdtraj.utils import ilen

        atom_indices_to_be_kept = set(atom_indices)
        newTopology = Topology()
        old_atom_to_new_atom = {}

        for chain in item._chains:
            newChain = newTopology.add_chain()
            for group in chain._groups:
                resSeq = getattr(group, 'resSeq', None) or group.index
                newResidue = newTopology.add_group(group.name, newChain,
                                                     resSeq, group.segment_id)
                for atom in group._atoms:
                    if atom.index in atom_indices_to_be_kept:
                        try:  # OpenMM Topology objects don't have serial attributes, so we have to check first.
                            serial = atom.serial
                        except AttributeError:
                            serial = None
                        newAtom = newTopology.add_atom(atom.name, atom.element,
                                                       newResidue, serial=serial)
                        old_atom_to_new_atom[atom] = newAtom

        bondsiter = item.bonds
        if not hasattr(bondsiter, '__iter__'):
            bondsiter = bondsiter()

        for bond in bondsiter:
            try:
                atom1, atom2 = bond
                newTopology.add_bond(old_atom_to_new_atom[atom1],
                                     old_atom_to_new_atom[atom2],
                                     type=bond.type,
                                     order=bond.order)
            except KeyError:
                pass
                # we only put bonds into the new topology if both of their partners
                # were indexed and thus HAVE a new atom

        # Delete empty groups
        newTopology._groups = [r for r in newTopology._groups if len(r._atoms) > 0]
        for chain in newTopology._chains:
            chain._groups = [r for r in chain._groups if len(r._atoms) > 0]

        # Delete empty chains
        newTopology._chains = [c for c in newTopology._chains
                               if len(c._groups) > 0]
        # Re-set the numAtoms and numResidues
        newTopology._numAtoms = ilen(newTopology.atoms)
        newTopology._numResidues = ilen(newTopology.groups)

        return newTopology

# Merge

def merge_two_items(item1, item2, in_place=False):

    if in_place:
        item1.join(item2)
        pass
    else:
        tmp_item=item1.copy()
        return tmp_item.join(item2)

# Duplicate

def copy(item):

    return item.copy()

########################
### Get
########################

## Atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_atom (item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group(item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group(item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component(item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component(item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

