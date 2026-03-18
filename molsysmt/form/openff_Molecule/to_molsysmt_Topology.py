from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openff.Molecule')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology

    n_atoms = item.n_atoms
    n_bonds = item.n_bonds

    tmp_item = Topology(n_atoms=n_atoms)

    atom_id = []
    atom_name = []
    atom_type = []

    for atom in item.atoms:
        idx = atom.molecule_atom_index
        symbol = atom.symbol
        name = atom.name if atom.name else symbol + str(idx)
        atom_id.append(str(idx))
        atom_name.append(name)
        atom_type.append(symbol)

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type

    if n_bonds > 0:
        bonded_atoms = [[b.atom1_index, b.atom2_index] for b in item.bonds]
        tmp_item.add_bonds(bonded_atoms, skip_digestion=True)

    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
