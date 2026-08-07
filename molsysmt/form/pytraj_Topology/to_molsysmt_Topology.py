from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.element.group import get_group_type_from_group_name


def _element_symbol(atom):
    """Return an elemental symbol without reusing a force-field atom type."""

    if atom.atomic_number <= 0:
        return None
    from pytraj.core.elements import atomic_number_element_dict

    symbol = atomic_number_element_dict.get(atom.atomic_number, '')
    if symbol in {'??', 'xp', ''}:
        return None
    return symbol.capitalize()


@arg_digest(form='pytraj.Topology')
@dep_digest('pytraj')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """Converting a PyTraj topology to the representable native subset."""

    from molsysmt.native import Topology

    n_atoms = item.n_atoms
    n_groups = item.n_residues
    output = Topology(n_atoms=n_atoms, n_groups=n_groups)

    atoms = list(item.atoms)
    residues = list(item.residues)

    output.atoms['atom_id'] = [str(atom.index) for atom in atoms]
    output.atoms['atom_name'] = [atom.name for atom in atoms]
    output.atoms['atom_type'] = [_element_symbol(atom) for atom in atoms]
    output.atoms['group_index'] = [atom.resid for atom in atoms]

    output.groups['group_id'] = [str(residue.original_resid) for residue in residues]
    output.groups['group_name'] = [residue.name for residue in residues]
    output.groups['group_type'] = [
        get_group_type_from_group_name(residue.name) for residue in residues
    ]

    bonded_atom_pairs = item.bond_indices
    if bonded_atom_pairs.shape[0]:
        output._append_chemical_state_bonds(bonded_atom_pairs)

    output.rebuild_components()
    output.rebuild_molecules()
    output.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract

        output = extract(
            output,
            atom_indices=atom_indices,
            skip_digestion=True,
        )

    return output
