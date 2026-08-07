from molsysmt._private.argdigest import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np

@arg_digest(form='biopython.PDBStructure')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt._private.variables import is_all

    # BioPython hierarchy: Structure -> Model -> Chain -> Residue -> Atom
    # We will use the first model for topology by default
    model = list(item.get_models())[0]
    
    atoms = list(model.get_atoms())
    residues = list(model.get_residues())
    chains = list(model.get_chains())

    n_atoms = len(atoms)
    n_groups = len(residues)
    n_chains = len(chains)

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains)

    atom_id = []
    atom_name = []
    atom_type = []
    group_index_of_atoms = []

    res_to_index = {res: i for i, res in enumerate(residues)}
    chain_to_index = {ch: i for i, ch in enumerate(chains)}

    for atom in atoms:
        atom_id.append(str(atom.serial_number))
        atom_name.append(atom.name)
        atom_type.append(atom.element)
        group_index_of_atoms.append(res_to_index[atom.parent])

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type
    tmp_item.atoms['group_index'] = group_index_of_atoms

    group_id = []
    group_name = []
    group_type = []
    chain_index_of_groups = []

    for res in residues:
        group_id.append(str(res.id[1])) # resid is usually at index 1 of the id tuple
        group_name.append(res.resname)
        group_type.append(get_group_type_from_group_name(res.resname))
        chain_index_of_groups.append(chain_to_index[res.parent])

    tmp_item.groups['group_id'] = group_id
    tmp_item.groups['group_name'] = group_name
    tmp_item.groups['group_type'] = group_type
    # chain_index lives on atoms only
    _ci_grp = np.array(chain_index_of_groups, dtype=int)
    _gi_atom = np.array(group_index_of_atoms, dtype=int)
    tmp_item.atoms['chain_index'] = _ci_grp[_gi_atom]

    chain_id = []
    chain_name = []
    for ch in chains:
        chain_id.append(str(ch.id))
        chain_name.append(str(ch.id))

    tmp_item.chains['chain_id'] = chain_id
    tmp_item.chains['chain_name'] = chain_name

    # Rebuild hierarchy
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
