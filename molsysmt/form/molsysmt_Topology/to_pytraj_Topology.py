import numpy as np

from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


def _pytraj_residue_number(group_id, group_index):
    """Return a PyTraj-compatible integer residue number."""

    try:
        return int(group_id)
    except (TypeError, ValueError, OverflowError):
        return int(group_index) + 1


@arg_digest(form='molsysmt.Topology')
@dep_digest('pytraj')
def to_pytraj_Topology(item, atom_indices='all', skip_digestion=False):
    """Converting a native topology to PyTraj's reduced topology model."""

    from pytraj import Atom as PyTrajAtom
    from pytraj import Residue as PyTrajResidue
    from pytraj import Topology as PyTrajTopology

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.molsysmt_Topology.extract import extract
    from molsysmt.physchem import get_mass

    item = extract(
        item,
        atom_indices=atom_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    masses = puw.get_value(
        get_mass(item, element='atom', skip_digestion=True),
        to_unit='Da',
    )
    output = PyTrajTopology()

    residues = {}
    for group_index, group in enumerate(item.groups.itertuples(index=False)):
        residue_number = _pytraj_residue_number(group.group_id, group_index)
        atom_indices_in_group = item.atoms.index[
            item.atoms['group_index'] == group_index
        ]
        if len(atom_indices_in_group):
            chain_index = item.atoms.loc[atom_indices_in_group[0], 'chain_index']
            try:
                chain_index = int(chain_index)
            except (TypeError, ValueError, OverflowError):
                chain_index = 0
        else:
            chain_index = 0
        residues[group_index] = PyTrajResidue(
            str(group.group_name),
            resid=residue_number,
            icode=0,
            chainID=chain_index,
        )

    for atom_index, atom in enumerate(item.atoms.itertuples(index=False)):
        group_index = int(atom.group_index)
        pytraj_atom = PyTrajAtom(
            name=str(atom.atom_name),
            type='' if atom.atom_type is None else str(atom.atom_type),
            resid=group_index,
            mass=float(masses[atom_index]),
            charge=0.0,
        )
        output.add_atom(pytraj_atom, residues[group_index])

    bonds = item._get_chemical_state_bonds()
    if bonds.shape[0]:
        bonded_atom_pairs = np.ascontiguousarray(
            bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=np.int64)
        )
        output.add_bonds(bonded_atom_pairs)

    return output
