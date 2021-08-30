from os.path import basename as _basename
from openmm.app import Topology as _openmm_app_Topology
from numpy import array as _array, unique as _unique, ndenumerate as _ndenumerate, concatenate as _concatenate
from numpy import arange as _arange, hstack as _hstack, empty as _empty

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'openmm.topology':form_name,
    'openmm.Topology':form_name,
    'openmm.app.topology.Topology':form_name,
    _openmm_app_Topology:form_name
}

info=["",""]
with_topology=True

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
    from openmm.app import Modeller

    positions = get(trajectory_item, target='atom', indices=atom_indices,
                    frame_indices=frame_indices, coordinates=True)
    tmp_item = Modeller(item, positions[0])
    return tmp_item

def to_pdb(item, output_filename=None, trajectory_item=None, atom_indices='all',
           frame_indices='all'):

    from molsysmt import get as _get
    from openmm.app import PDBFile
    from openmm.version import short_version
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

    if output_filename=='.pdb':
        return filedata
    else:
        with open(output_filename, 'w') as file:
            file.write(filedata)
        pass


def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from openmm.app import Topology
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

    if indices is 'all':
        n_atoms = get_n_atoms_from_system(item)
        output = _arange(n_atoms, dtype=int)
    else:
        output = indices

    return output

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output=[atom[ii].id for ii in tmp_indices]
    output=_array(output, dtype=int)
    del(atom)
    return output

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    output=_array(output)
    del(atom)
    return output

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    output=_array(output)
    del(atom)
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    output=_array(output)
    del(atom)
    return output

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.id for ii in tmp_indices]
    output=_array(output, dtype=int)
    del(atom)
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.name for ii in tmp_indices]
    output=_array(output)
    del(atom)
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import name_to_type as group_name_to_group_type

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [group_name_to_group_type(atom[ii].residue.name) for ii in tmp_indices]
    output=_array(output)
    del(atom)
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    output, _, _, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    _, output, _, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output


def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    _, _, output, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    _, _, _, output = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)
    output = _array(output)
    return output

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.id for ii in tmp_indices]
    del(atom)
    output = _array(output, dtype=object)
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [None for ii in tmp_indices]
    del(atom)
    output = _array(output, dtype=object)
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [None for ii in tmp_indices]
    del(atom)
    output = _array(output, dtype=object)
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    return get_component_index_from_atom (item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    return get_component_id_from_atom (item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    return get_component_name_from_atom (item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import component_type_to_molecule_type
    output = get_component_type_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = [component_type_to_molecule_type(ii) for ii in output]
    output = np.array(output)
    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_elements

    output, _, _, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_elements

    _, output, _, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_elements

    _, _, output, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_elements

    _, _, _, output = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system(item)
    else:
        return indices.shape[0]

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    output = get_group_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    output = get_component_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    output=[]

    if indices is 'all':

        for bond in item.bonds():
            output.append([bond.atom1.index, bond.atom2.index])

    else:

        set_indices = set(indices)

        for bond in item.bonds():
            if bond.atom1.index in set_indices:
                if bond.atom2.index in set_indices:
                    output.append([bond.atom1.index, bond.atom2.index])

    output = _array(output, dtype=int)

    return(output)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_atom(item, indices='all', frame_indices='all'):

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

    residue=list(item.residues())

    output = []
    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(residue[ii].atoms())
        output.append(_array([atom.index for atom in atoms]))
    output = _array(output)
    return output

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    residue=list(item.residues())

    output = []
    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(residue[ii].atoms())
        output.append(_array([atom.id for atom in atoms], dtype=int))
    output = _array(output)
    return output

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    residue=list(item.residues())

    output = []
    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(residue[ii].atoms())
        output.append(_array([atom.name for atom in atoms], dtype=object))
    output = _array(output)
    return output

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    residue=list(item.residues())

    output = []
    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(residue[ii].atoms())
        output.append(_array([atom.element.symbol for atom in atoms], dtype=object))
    output = _array(output)
    return output

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        output = _arange(n_indices, dtype=int)
    else:
        output = indices

    return output

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].id for ii in indices]
    del(group)
    output = _array(output, dtype=int)
    return output

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)
    output = _array(output, dtype=object)
    return output

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import name_to_type

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [name_to_type(group[ii].name) for ii in indices]
    del(group)
    output = _array(output, dtype=object)
    return output

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_index_from_atom = get_component_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_name_from_atom = get_component_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_id_from_atom = get_component_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_type_from_atom = get_component_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].chain.index for ii in indices]
    output = _array(output)
    del(group)
    return output

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].chain.id for ii in indices]
    output = _array(output)
    del(group)
    return output

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [None for ii in indices]
    del(group)
    return output

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [None for ii in indices]
    del(group)
    return output

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_index_from_atom = get_molecule_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_id_from_atom = get_molecule_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_name_from_atom = get_molecule_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_type_from_atom = get_molecule_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    output = get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    output = get_component_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_group(item, indices='all', frame_indices='all'):

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

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_indices = get_atom_index_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_indices[mask])

    output = _array(output)

    return output

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_id = get_atom_id_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_id[mask])

    output = _array(output)

    return output

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_name = get_atom_name_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_name[mask])

    output = _array(output)

    return output

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_type = get_atom_type_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_type[mask])

    output = _array(output)

    return output

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    group_index = get_group_index_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(_unique(group_index[mask]))

    output = _array(output)

    return output

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_component (item, indices='all', frame_indices='all'):

     if indices is 'all':
         output = _arange(get_n_components_from_system(item))
     else:
         output = indices
     return output

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    component_id_from_atom = get_component_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(component_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    component_name_from_atom = get_component_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(component_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    component_type_from_atom = get_component_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(component_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_index_from_atom = get_chain_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_id_from_atom = get_chain_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_name_from_atom = get_chain_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_type_from_atom = get_chain_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_index_from_atom = get_molecule_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_id_from_atom = get_molecule_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_name_from_atom = get_molecule_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_type_from_atom = get_molecule_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    output = get_group_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    output = get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_component(item, indices='all', frame_indices='all'):

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

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    atom_indices = get_atom_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(atom_indices[mask])

    output = _array(output)

    return output

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    group_index = get_group_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(group_index[mask]))

    output = _array(output)

    return output

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    component_index = get_component_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(component_index[mask]))

    output = _array(output)

    return output

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_id_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_name_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_type_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    chain_index = get_chain_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(chain_index[mask]))

    output = _array(output)

    return output

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

     if indices is 'all':
         output = _arange(get_n_molecules_from_system(item))
     else:
         output = indices
     return output

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    molecule_id_from_atom = get_molecule_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(molecule_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    molecule_name_from_atom = get_molecule_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(molecule_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    molecule_type_from_atom = get_molecule_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(molecule_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    output = get_group_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    output = get_component_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

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

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.index for atom in atoms]))
    del(chain)
    output = _array(output)
    return output

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.id for atom in atoms], dtype=int))
    del(chain)
    output = _array(output)
    return output

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.name for atom in atoms], dtype=object))
    del(chain)
    output = _array(output)
    return output

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.element.symbol for atom in atoms], dtype=object))
    del(chain)
    output = _array(output)
    return output


def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([residue.index for residue in residues]))
    del(chain)
    output = _array(output)
    return output

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([residue.id for residue in residues], dtype=int))
    del(chain)
    output = _array(output)
    return output

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([residue.name for residue in residues], dtype=object))
    del(chain)
    output = _array(output)
    return output

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import name_to_type

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([name_to_type(residue.name) for residue in residues], dtype=object))
    del(chain)
    output = _array(output)
    return output

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    component_index = get_component_index_from_atom(item, indices='all')
    chain_indices = get_chain_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (chain_indices==ii)
        output.append(_unique(component_index[mask]))

    output = _array(output)

    return output

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_id_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_name_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_type_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        output = _arange(n_indices, dtype=int)
    else:
        output = indices
    return output

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = _array(output)
    return output

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = _array(output)
    return output

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = _array(output)
    return output

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    molecule_index = get_molecule_index_from_atom(item, indices='all')
    chain_indices = get_chain_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (chain_indices==ii)
        output.append(_unique(molecule_index[mask]))

    output = _array(output)

    return output

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_molecule_id_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_molecule_name_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_molecule_type_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    output = get_group_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    output = get_component_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_chain(item, indices='all', frame_indices='all'):

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

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_indices = get_atom_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_indices[mask])

    output = _array(output)

    return output

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_ids = get_atom_id_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_ids[mask])

    output = _array(output)

    return output

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_names = get_atom_name_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_names[mask])

    output = _array(output)

    return output

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_types = get_atom_type_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_types[mask])

    output = _array(output)

    return output

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    group_index = get_group_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(group_index[mask]))

    output = _array(output)

    return output

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    component_index = get_component_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(component_index[mask]))

    output = _array(output)

    return output

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    chain_index = get_chain_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(chain_index[mask]))

    output = _array(output)

    return output

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    molecule_index = get_molecule_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(molecule_index[mask]))

    output = _array(output)

    return output

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_id_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output


def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_name_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_type_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

     if indices is 'all':
         output = _arange(get_n_entities_from_system(item))
     else:
         output = indices
     return output

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_entity:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_entity:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_entity:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    output = get_group_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    output = get_component_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.getNumAtoms()

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.getNumResidues()

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return get_n_components_from_atom(item, indices='all')

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.getNumChains()

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return get_n_molecules_from_atom(item, indices='all')

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return get_n_entities_from_atom(item, indices='all')

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return item.getNumBonds()

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    group_types = get_group_type_from_group(item, indices='all')
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    group_types = get_group_type_from_group(item, indices='all')
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='ion').sum()

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='small molecule').sum()

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='rna').sum()

def get_mass_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    box = item.getPeriodicBoxVectors()

    if box is not None:
        box_unit = box.unit
        box = _array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if frame_indices is 'all':
            output=box
        else:
            output=box[frame_indices,:,:]

    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

## bond

def get_index_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_index_from_bond(item, indices=indices)

def get_order_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_order_from_bond(item, indices=indices)

def get_type_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_type_from_bond(item, indices=indices)

def get_bond_index_from_bond(item, indices='all', frame_indices='all'):

    tmp_out = None

    if indices is 'all':

        n_bonds = get_n_bonds_from_system(item)
        tmp_out = _arange(n_bonds, dtype=int)

    else:
        tmp_out = indices

    return tmp_out

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=_array(output)
    del(bond)
    return output

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=_array(output)
    del(bond)
    return output

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in tmp_indices]
    output=_array(output)
    del(bond)
    return output

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    if indices is 'all':

        return get_n_bonds_from_system(item)

    else:

        return len(indices)

