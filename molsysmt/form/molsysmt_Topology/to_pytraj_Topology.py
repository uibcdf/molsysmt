import numpy as np
import pandas as pd

from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


def _pytraj_residue_number(group_id, group_index):
    """Return a PyTraj-compatible integer residue number."""

    try:
        return int(group_id)
    except (TypeError, ValueError, OverflowError):
        return int(group_index) + 1


def _pytraj_chain_id(item, chain_index):
    """Return the textual chain identifier required by PyTraj."""

    if pd.isna(chain_index):
        return ''
    try:
        chain_index = int(chain_index)
    except (TypeError, ValueError, OverflowError):
        return ''
    if chain_index < 0 or chain_index >= item.n_chains:
        return ''
    chain_id = item.chains.iloc[chain_index]['chain_id']
    return '' if pd.isna(chain_id) else str(chain_id)


def _pytraj_chain_index(chain_index):
    """Return the integer chain value required by legacy PyTraj builds."""

    if pd.isna(chain_index):
        return 0
    try:
        return int(chain_index)
    except (TypeError, ValueError, OverflowError):
        return 0


def _pytraj_uses_text_chain_id(residue_type):
    """Detect which incompatible PyTraj 2.0.6 residue ABI is installed."""

    try:
        residue_type('UNK', resid=0, icode=0, chainID='')
    except (AttributeError, TypeError):
        return False
    return True


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
    uses_text_chain_id = _pytraj_uses_text_chain_id(PyTrajResidue)

    residues = {}
    for group_index, group in enumerate(item.groups.itertuples(index=False)):
        residue_number = _pytraj_residue_number(group.group_id, group_index)
        atom_indices_in_group = item.atoms.index[
            item.atoms['group_index'] == group_index
        ]
        if len(atom_indices_in_group):
            chain_index = item.atoms.loc[atom_indices_in_group[0], 'chain_index']
        else:
            chain_index = None
        residues[group_index] = PyTrajResidue(
            str(group.group_name),
            resid=residue_number,
            icode=0,
            chainID=(
                _pytraj_chain_id(item, chain_index)
                if uses_text_chain_id
                else _pytraj_chain_index(chain_index)
            ),
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
