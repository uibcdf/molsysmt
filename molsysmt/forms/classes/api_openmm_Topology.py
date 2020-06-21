from os.path import basename as _basename
from simtk.openmm.app import Topology as _simtk_openmm_app_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'openmm.topology':form_name,
    'openmm.Topology':form_name,
    'simtk.openmm.app.topology.Topology':form_name,
    _simtk_openmm_app_Topology:form_name
}

info=["",""]
with_topology=True
with_trajectory=False

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_openmm_Topology as molsysmt_DataFrame_from_openmm_Topology
    return molsysmt_DataFrame_from_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_Topology as molsysmt_Topology_from_openmm_Topology
    return molsysmt_Topology_from_openmm_Topology(item, atom_indices=atom_indices)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_openmm_Topology as molsysmt_MolSys_from_openmm_Topology
    return molsysmt_MolSys_from_openmm_Topology(item, atom_indices=atom_indices)

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import extract as extract_mdtraj_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology
    tmp_item = mdtraj_Topology.from_openmm(item)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from parmed.openmm import load_topology as openmm_Topology_to_parmed_Structure
    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from yank import Topography as yank_Topography
    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = yank_Topography(tmp_item)
    return tmp_item

def to_openmm_Modeller(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt import get
    from simtk.openmm.app import Modeller

    positions = get(trajectory_item, target='atom', indices=atom_indices,
                    frame_indices=frame_indices, coordinates=True)
    tmp_item = Modeller(item, positions[0])
    return tmp_item

def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all',
           frame_indices='all'):

    from molsysmt import get as _get
    from simtk.openmm.app import PDBFile
    from simtk.openmm.version import short_version
    from io import StringIO

    coordinates = _get(trajectory_item, target="atom", indices=atom_indices, frame_indices=frame_indices, coordinates=True)

    if atom_indices is 'all':
        tmp_item = item
    else:
        tmp_item = extract(item, atom_indices=atom_indices)

    tmp_io = StringIO()
    PDBFile.writeFile(tmp_item, coordinates[0], tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    filedata = filedata.replace('WITH OPENMM '+short_version, 'WITH OPENMM '+short_version+' BY MOLSYSMT')
    tmp_io.close()
    del(tmp_io)

    if output_filepath=='.pdb':
        return filedata
    else:
        with open(output_filepath, 'w') as file:
            file.write(filedata)
        pass


def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from simtk.openmm.app import Topology
        new_item = Topology()
        atom_indices_to_be_kept = atom_indices
        newAtoms = {}
        set_atom_indices = set(atom_indices_to_be_kept)
        for chain in item.chains():
            needNewChain = True
            for residue in chain.residues():
                needNewResidue = True
                for atom in residue.atoms():
                    if atom.index in set_atom_indices:
                        if needNewChain:
                            newChain = new_item.addChain(chain.id)
                            needNewChain = False;
                        if needNewResidue:
                            newResidue = new_item.addResidue(residue.name, newChain, residue.id, residue.insertionCode)
                            needNewResidue = False;
                        newAtom = new_item.addAtom(atom.name, atom.element, newResidue, atom.id)
                        newAtoms[atom] = newAtom
        for bond in item.bonds():
            if bond[0].index in set_atom_indices and bond[1].index in set_atom_indices:
                new_item.addBond(newAtoms[bond[0]], newAtoms[bond[1]])
        return new_item

def copy(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    tmp_item = to_mdtraj_Topology(item, selection='all', syntaxis='MDTraj')
    return tmp_item.select(selection)

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_molsysmt_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_molsysmt_Topology_with_MolSysMT(tmp_item, selection)


#### Get

## Atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    return indices

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    atom_id=[atom[ii].id for ii in indices]
    del(atom)
    return atom_id

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    atom_name=[atom[ii].name for ii in indices]
    del(atom)
    return atom_name

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    atom_type=[atom[ii].element.symbol for ii in indices]
    del(atom)
    return atom_type

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_indices = [atom[ii].residue.index for ii in indices]
    del(atom)
    return group_indices

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_ids = [atom[ii].residue.id for ii in indices]
    del(atom)
    return group_ids

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_names = [atom[ii].residue.name for ii in indices]
    del(atom)
    return group_names

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    chain_indices = [atom[ii].group.chain.index for ii in indices]
    del(atom)
    return chain_indices

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    chain_ids = [atom[ii].group.chain.id for ii in indices]
    del(atom)
    return chain_ids

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.topology import group_name_to_molecule_type
    group_names = get_group_name_from_atom(item, indices=indices)
    molecule_types = [group_name_to_molecule_type(ii) for ii in group_names]
    del(group_names, group_name_to_molecule_type)
    return molecule_types

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

    return len(indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_indices = [atom[ii].group.index for ii in indices]
    group_indices = list(set(group_indices))
    del(atom)
    return len(group_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    return indices

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    group=list(item.residues())
    group_ids = [group[ii].id for ii in indices]
    del(group)
    return group_ids

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    group=list(item.residues())
    group_names = [group[ii].name for ii in indices]
    del(group)
    return group_names

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    group=list(item.residues())
    chain_indices = [group[ii].chain.index for ii in indices]
    del(group)
    return chain_indices

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    group=list(item.residues())
    chain_ids = [group[ii].chain.id for ii in indices]
    del(group)
    return chain_ids

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.topology import group_name_to_molecule_type
    group=list(item.groups())
    group_names = [group[ii].name for ii in indices]
    molecule_types = [group_name_to_molecule_type(ii) for ii in group_names]
    del(group, group_names, group_name_to_molecule_type)
    return molecule_types

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    return len(indices)

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

def get_mass_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

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

def get_mass_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

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

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    chain=list(item.chains())
    chain_indices = [chain[ii].index for ii in indices]
    del(chain)
    return chain_indices

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    chain=list(item.chains())
    chain_ids = [chain[ii].id for ii in indices]
    del(chain)
    return chain_ids

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.topology import group_name_to_molecule_type
    chain=list(item.chains())
    molecule_types = []
    for ii in indices:
        group = list(chain[ii].groups())[0]
        molecule_types.append(group_name_to_molecule_type(group.name))
    del(chain, group)
    return molecule_types

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

    return len(indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

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

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.getNumAtoms()

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return get_n_groups_from_atom(item, 'all')

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

    from molsysmt.topology import is_aminoacid
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_aminoacids=0
    for group_name in group_names:
        if is_aminoacid(group_name): n_aminoacids+=1
    del(group_indices, group_names)
    return n_aminoacids

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_nucleotide
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_nucleotides=0
    for group_name in group_names:
        if is_nucleotide(group_name): n_nucleotides+=1
    del(group_indices, group_names)
    return n_nucleotides


def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_ion
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_ions=0
    for group_name in group_names:
        if is_ion(group_name): n_ions+=1
    del(group_indices, group_names)
    return n_ions

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_water
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_waters=0
    for group_name in group_names:
        if is_water(group_name): n_waters+=1
    del(group_indices, group_names)
    return n_waters

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

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    box = item.getPeriodicBoxVectors()

    if box is not None:
        box = _array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box.unit

    return box

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


