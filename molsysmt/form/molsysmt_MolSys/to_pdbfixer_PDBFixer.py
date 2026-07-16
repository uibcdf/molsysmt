from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='molsysmt.MolSys')
@dep_digest('pdbfixer')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all',
                         pdb_chain_id='chain_name', skip_digestion=False):

    from pdbfixer.pdbfixer import PDBFixer

    from .to_string_pdb_text import to_string_pdb_text
    from io import StringIO

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  pdb_chain_id=pdb_chain_id, skip_digestion=True)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    bonds = item.topology._get_chemical_state_bonds()
    if bonds.shape[0] > 0:

        if is_all(atom_indices):
            selected_atom_indices = list(range(item.topology.n_atoms))
        else:
            selected_atom_indices = [int(ii) for ii in atom_indices]
        output_index = {source_index: target_index for target_index, source_index in enumerate(selected_atom_indices)}

        bonds_before = []
        for bond in bonds.itertuples(index=False):
            atom1_index = int(bond.atom1_index)
            atom2_index = int(bond.atom2_index)
            if atom1_index in output_index and atom2_index in output_index:
                bonds_before.append(sorted((output_index[atom1_index], output_index[atom2_index])))

        bonds_after = []
        for ii in tmp_item.topology.bonds():
            if ii.atom1.index<ii.atom2.index:
                bonds_after.append([ii.atom1.index, ii.atom2.index])
            else:
                bonds_after.append([ii.atom2.index, ii.atom1.index])

        missing_bonds = {tuple(ii) for ii in bonds_before} - {tuple(ii) for ii in bonds_after}

        if len(missing_bonds):

            atoms_list = list(tmp_item.topology.atoms())

            for atom1_index, atom2_index in missing_bonds:
                tmp_item.topology.addBond(atoms_list[atom1_index], atoms_list[atom2_index])

    return tmp_item
