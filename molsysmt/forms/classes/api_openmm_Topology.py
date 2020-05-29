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

    tmp_io = StringIO()
    PDBFile.writeFile(item, coordinates[0], tmp_io)
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
        atom_indices_to_be_kept = atom_indices
        newAtoms = {}
        set_atom_indices = set(atom_indices_to_be_kept)
        for chain in item.chains():
            needNewChain = True
            for group in chain.groups():
                needNewResidue = True
                for atom in group.atoms():
                    if atom.index in set_atom_indices:
                        if needNewChain:
                            newChain = newTopology.addChain(chain.id)
                            needNewChain = False;
                        if needNewResidue:
                            newResidue = newTopology.addResidue(group.name, newChain, group.id, group.insertionCode)
                            needNewResidue = False;
                        newAtom = newTopology.addAtom(atom.name, atom.element, newResidue, atom.id)
                        newAtoms[atom] = newAtom
        for bond in item.bonds():
            if bond[0].index in set_atom_indices and bond[1].index in set_atom_indices:
                newTopology.addBond(newAtoms[bond[0]], newAtoms[bond[1]])
        return newTopology

def copy(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    tmp_item = to_mdtraj_Topology(item, selection='all', syntaxis='MDTraj')
    return tmp_item.select(selection)

#### Get

def get_n_atoms_from_atom(item, indices='all', frame_indices='all'):

    return len(indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    atom_name=[atom[ii].name for ii in indices]
    del(atom)
    return atom_name

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    return indices

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    atom_id=[atom[ii].id for ii in indices]
    del(atom)
    return atom_id

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    atom_type=[atom[ii].element.symbol for ii in indices]
    del(atom)
    return atom_type

def get_n_groups_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_indices = [atom[ii].group.index for ii in indices]
    group_indices = list(set(group_indices))
    del(atom)
    return len(group_indices)

def get_group_name_from_atom(item, indices='all', frame_indices='all'):

    group_indices = get_group_index_from_atom (item, indices=indices)
    group=list(item.groups())
    group_names = [group[ii].name for ii in group_indices]
    del(group, group_indices)
    return group_names

def get_group_index_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_indices = [atom[ii].group.index for ii in indices]
    del(atom)
    return group_indices

def get_group_id_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    group_ids = [atom[ii].group.id for ii in indices]
    del(atom)
    return group_ids

def get_chain_index_from_atom(item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    chain_indices = [atom[ii].group.chain.index for ii in indices]
    del(atom)
    return chain_indices

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms())
    chain_ids = [atom[ii].group.chain.id for ii in indices]
    del(atom)
    return chain_ids

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    pass

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    pass

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_aminoacid
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_aminoacids=0
    for group_name in group_names:
        if is_aminoacid(group_name): n_aminoacids+=1
    del(group_indices, group_names)
    return n_aminoacids

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_nucleotide
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_nucleotides=0
    for group_name in group_names:
        if is_nucleotide(group_name): n_nucleotides+=1
    del(group_indices, group_names)
    return n_nucleotides

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_water
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_waters=0
    for group_name in group_names:
        if is_water(group_name): n_waters+=1
    del(group_indices, group_names)
    return n_waters

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.topology import is_ion
    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))
    group_names = get_group_name_from_group(item, indices=group_indices)
    n_ions=0
    for group_name in group_names:
        if is_ion(group_name): n_ions+=1
    del(group_indices, group_names)
    return n_ions

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.topology import group_name_to_molecule_type
    group_names = get_group_name_from_atom(item, indices=indices)
    molecule_types = [group_name_to_molecule_type(ii) for ii in group_names]
    del(group_names, group_name_to_molecule_type)
    return molecule_types

## Residue

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    return len(indices)

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    group=list(item.groups())
    group_names = [group[ii].name for ii in indices]
    del(group)
    return group_names

def get_group_index_from_group (item, indices='all', frame_indices='all'):

    return indices

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    group=list(item.groups())
    group_ids = [group[ii].id for ii in indices]
    del(group)
    result.append(group_ids)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    group=list(item.groups())
    chain_indices = [group[ii].chain.index for ii in indices]
    del(group)
    return chain_indices

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    group=list(item.groups())
    chain_ids = [group[ii].chain.id for ii in indices]
    del(group)
    return chain_ids

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.topology import group_name_to_molecule_type
    group=list(item.groups())
    group_names = [group[ii].name for ii in indices]
    molecule_types = [group_name_to_molecule_type(ii) for ii in group_names]
    del(group, group_names, group_name_to_molecule_type)
    return molecule_types

## Chain

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

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    return len(indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.topology import group_name_to_molecule_type
    chain=list(item.chains())
    molecule_types = []
    for ii in indices:
        group = list(chain[ii].groups())[0]
        molecule_types.append(group_name_to_molecule_type(group.name))
    del(chain, group)
    return molecule_types

## System

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.getNumAtoms()

def get_charge_from_system (item, indices='all', frame_indices='all'):

    return 'por hacer'

def get_net_charge_from_system (item, indices='all', frame_indices='all'):

    return 'por hacer'

def get_box_from_system (item, indices='all', frame_indices='all'):

    from numpy import array as _array

    box = item.getPeriodicBoxVectors()

    if box is not None:
        box = _array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box.unit

    return box


def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

