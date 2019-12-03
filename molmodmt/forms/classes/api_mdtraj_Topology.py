from molmodmt.utils.exceptions import *
from os.path import basename as _basename
from mdtraj.core.topology import Topology as _mdtraj_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

## To other form

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return ''.join([ r.name for r in tmp_item.groups ])

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molmodmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as aminoacids3_to_aminoacids1

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = to_aminoacids3_seq(tmp_item)
    tmp_item = aminoacids3_to_aminoacids1(tmp_item)
    return tmp_item

def to_molmodmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.io.dataframe import from_mdtraj_Topology as molmodmt_DataFrame_from_mdtraj_Topology
    tmp_item = molmodmt_DataFrame_from_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item.to_openmm()

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_yank_Topography as opennn_Topology_to_yank_Topography
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = opennn_Topology_to_yank_Topography(tmp_item)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_form)
    return tmp_item

def to_parmed_GromacsTopologyFile(item, atom_indices='all', frame_indices='all'):

    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile
    tmp_item = to_parmed_Structure(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return GromacsTopologyFile.from_structure(tmp_item)

def to_top(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from .api_parmed_GromacsTopologyFile import to_top as parmed_GromacsTopologyFile_to_top
    tmp_item = to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return parmed_GromacsTopologyFile_to_top(tmp_item, output_file_path=output_file_path)

def to_pandas_DataFrame(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

# Select

def select_with_MDTraj(item, selection):
    return item.select(selection)

def select_with_MolModMT(item, selection):

    from molmodmt.native.selector import dataframe_select
    tmp_item = to_pandas_DataFrame(item)
    atom_indices = dataframe_select(tmp_item, selection)
    del(tmp_item)
    return atom_indices

# Extract

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

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

def duplicate(item):

    return item.copy()

########################
### Get
########################

## from atom

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    return len(indices)

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return indices

def get_id_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    ids = [atom[ii].serial for ii in indices]
    del(atom)
    return ids

def get_name_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    names = [atom[ii].name for ii in indices]
    del(atom)
    return names

def get_element_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    elements = [atom[ii].element.symbol for ii in indices]
    del(atom)
    return elements

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    names = [atom[ii].group.name for ii in indices]
    del(atom)
    return names

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    values = [atom[ii].group.index for ii in indices]
    del(atom)
    return values

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    values = [atom[ii].group.resSeq for ii in indices]
    del(atom)
    return values

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    names = [None for ii in indices]
    return names

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    chains = list(item.chains)
    id_to_index={}
    for ii in range(len(chains)):
        id_to_index[chains[ii].index]=ii

    atom=list(item.atoms)
    values = [id_to_index[atom[ii].group.chain.index] for ii in indices]
    del(atom, chains)
    return values

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    values = [atom[ii].group.chain.index for ii in indices]
    del(atom)
    return values

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    group_indices = [atom[ii].group.index for ii in indices]
    group_indices = list(set(group_indices))
    del(atom)
    return len(group_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    atom=list(item.atoms)
    chain_indices = [atom[ii].group.chain.index for ii in indices]
    chain_indices = list(set(chain_indices))
    del(atom)
    return len(chain_indices)

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_aminoacid

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))

    group=list(item.groups)
    group_names = [group[ii].name for ii in group_indices]
    del(group)

    n_aminoacids=0
    for group_name in group_names:
        if is_aminoacid(group_name): n_aminoacids+=1
    del(group_indices, group_names)
    return n_aminoacids

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_nucleotide

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))

    group=list(item.groups)
    group_names = [group[ii].name for ii in group_indices]
    del(group)

    n_nucleotides=0
    for group_name in group_names:
        if is_nucleotide(group_name): n_nucleotides+=1
    del(group_indices, group_names)
    return n_nucleotides

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_water

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))

    group=list(item.groups)
    group_names = [group[ii].name for ii in group_indices]
    del(group)

    n_waters=0
    for group_name in group_names:
        if is_water(group_name): n_waters+=1
    del(group_indices, group_names)
    return n_waters

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_ion

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = list(set(group_indices))

    group=list(item.groups)
    group_names = [group[ii].name for ii in group_indices]
    del(group)

    n_ions=0
    for group_name in group_names:
        if is_ion(group_name): n_ions+=1
    del(group_indices, group_names)
    return n_ions

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    n_molecules = get_molecules_from_atom (item, indices=indices, frame_indices=frame_indices)
    return len(get(item, indices=indices, molecules=True))

def get_masses_from_atom (item, indices='all', frame_indices='all'):

    return [atom.element.mass for atom in item.atoms]

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    set_indices = set(indices)
    tmp_bonded = { ii:[] for ii in indices}
    for bond in item.bonds:
        if bond.atom1.index in set_indices:
            if bond.atom2.index in set_indices:
                tmp_bonded[bond.atom1.index].append(bond.atom2.index)
                tmp_bonded[bond.atom2.index].append(bond.atom1.index)
    return tmp_bonded

def get_bonds_from_atom (item, indices='all', frame_indices='all'):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.index,bond.atom2.index])
    return tmp_bonds

def get_graph_from_atom (item, indices='all', frame_indices='all'):

    return item.to_bondgraph()

def get_molecules_from_atom (item, indices='all', frame_indices='all'):

    set_indices = set(indices)
    tmp_molecules = []
    for mm in item.find_molecules():
        molecule = [ii.index for ii in mm if ii.index in set_indices]
        if len(molecule)>0:
            tmp_molecules.append(molecule)

    return tmp_molecules

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt.topology import group_name_to_molecule_type
    group_names = get_group_name_from_atom(item, indices=indices)
    molecule_types = [group_name_to_molecule_type(ii) for ii in group_names]
    del(group_names, group_name_to_molecule_type)
    return molecule_types

## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_groups_from_system (item, indices='all', frame_indices='all'):

    return item.n_groups

def get_n_chains_from_system (item, indices='all', frame_indices='all'):

    return item.n_chains

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_aminoacid

    n_aminoacids=0

    for group in item.groups:
        if is_aminoacid(group.name):
            n_aminoacids+=1

    return n_aminoacids

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_nucleotide

    n_nucleotides=0

    for group in item.groups:
        if is_nucleotide(group.name):
            n_nucleotides+=1

    return n_nucleotides

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_water

    n_waters=0

    for group in item.groups:
        if is_water(group.name):
            n_waters+=1

    return n_waters

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from molmodmt.topology import is_ion

    n_ions=0

    for group in item.groups:
        if is_ion(group.name):
            n_ions+=1

    return n_ions

def get_n_molecules_from_system (item, indices='all', frame_indices='all'):

    n_molecules = len(get_molecules_from_system(item))
    return n_molecules

def get_n_bonds_from_system (item, indices='all', frame_indices='all'):

    return item.n_bonds

def get_bonded_atoms_from_system (item, indices='all', frame_indices='all'):

    tmp_bonded = [[] for ii in range(item.n_atoms)]
    for bond in item.bonds:
        tmp_bonded[bond.atom1.index].append(bond.atom2.index)
        tmp_bonded[bond.atom2.index].append(bond.atom1.index)
    return tmp_bonded

def get_bonds_from_system (item, indices='all', frame_indices='all'):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.index,bond.atom2.index])
    return tmp_bonds

def get_graph_from_system (item, indices='all', frame_indices='all'):

    return item.to_bondgraph()

def get_molecules_from_system (item, indices='all', frame_indices='all'):

    tmp_molecules = []
    for mm in item.find_molecules():
        tmp_molecules.append([ii.index for ii in mm])
    return tmp_molecules

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

