from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="mdtraj.Topology")
@dep_digest("mdtraj")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting atoms with preserved metadata and a compact MDTraj hierarchy.

    Parameters
    ----------
    item : mdtraj.Topology
        Source topology, which is left unchanged.
    atom_indices : int or array_like or str
        Atom indices to retain. The default is ``'all'``. Explicit subsets
        follow source atom order and coalesce repeated positions.
    structure_indices : int or array_like or str
        Unused compatibility argument: this form has no structure axis.
        The default is ``'all'``.
    copy_if_all : bool
        Whether ``'all'`` returns an independent copy. The default is True.
        Explicit atom subsets always return an independent topology.
    skip_digestion : bool
        Whether to skip argument digestion for a trusted internal call.
        The default is False.

    Returns
    -------
    mdtraj.Topology
        Selected topology with dense atom, group and chain indices, retained
        labels, atom serials and formal charges, and remapped bond metadata.

    Notes
    -----
    Unknown formal charges remain unknown. Explicit zero group sequence labels
    are preserved. Empty groups and chains are not copied into a subset.
    No chemical perception or coordinate calculation is performed.

    See Also
    --------
    molsysmt.basic.extract
        Extracting from any supported molecular-system form.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=2)
    >>> molsys.topology.atoms['atom_type'] = ['C', 'O']
    >>> topology = msm.convert(molsys, to_form='mdtraj.Topology')
    >>> extract(topology, atom_indices=[1]).n_atoms
    1

    .. admonition:: User guide

       See :ref:`Tutorial_Form_mdtraj_Topology` and :ref:`Tutorial_Extract`.

    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices):
        if copy_if_all:
            from mdtraj.core.topology import Topology

            if isinstance(item, Topology):
                from copy import deepcopy

                tmp_item = deepcopy(item)
            else:
                tmp_item = item
        else:
            tmp_item = item
    else:
        from mdtraj.core.topology import Topology

        atom_indices_to_be_kept = set(atom_indices)
        newTopology = Topology()
        old_atom_to_new_atom = {}

        for chain in item.chains:
            newChain = None
            for residue in chain.residues:
                newResidue = None
                for atom in residue.atoms:
                    if atom.index in atom_indices_to_be_kept:
                        if newChain is None:
                            newChain = newTopology.add_chain(chain_id=chain.chain_id)
                        if newResidue is None:
                            newResidue = newTopology.add_residue(
                                residue.name,
                                newChain,
                                resSeq=residue.resSeq,
                                segment_id=residue.segment_id,
                            )
                        newAtom = newTopology.add_atom(
                            atom.name,
                            atom.element,
                            newResidue,
                            serial=atom.serial,
                            formal_charge=atom.formal_charge,
                        )
                        old_atom_to_new_atom[atom] = newAtom

        bondsiter = item.bonds
        if not hasattr(bondsiter, "__iter__"):
            bondsiter = bondsiter()

        for bond in bondsiter:
            try:
                atom1, atom2 = bond
                newTopology.add_bond(
                    old_atom_to_new_atom[atom1],
                    old_atom_to_new_atom[atom2],
                    type=bond.type,
                    order=bond.order,
                )
            except KeyError:
                pass
                # we only put bonds into the new topology if both of their partners
                # were indexed and thus HAVE a new atom

        tmp_item = newTopology

    return tmp_item
