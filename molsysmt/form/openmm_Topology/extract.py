from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="openmm.Topology")
@dep_digest("openmm")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting atoms with preserved OpenMM topology and chemical metadata.

    Parameters
    ----------
    item : openmm.Topology
        Source topology, which is left unchanged.
    atom_indices : int or array_like or str
        Atom indices to retain. The default is ``'all'``. Explicit subsets
        follow source atom order and coalesce repeated positions.
    structure_indices : int or array_like or str
        Unused compatibility argument: this form has no coordinate-structure
        axis. The default is ``'all'``.
    copy_if_all : bool
        Whether ``'all'`` returns an independent copy. The default is True.
        Explicit atom subsets always return an independent topology.
    skip_digestion : bool
        Whether to skip argument digestion for a trusted internal call.
        The default is False.

    Returns
    -------
    openmm.Topology
        Topology with dense retained atom, group and chain indices, original
        labels/insertion codes, formal charges, remapped bond type/order and
        independent periodic box vectors, stored by OpenMM in nanometers.

    Notes
    -----
    Unknown formal charges remain unknown. Full copies preserve empty groups
    and chains; explicit atom subsets omit parents with no retained atoms.
    No chemical perception or coordinate calculation is performed.

    See Also
    --------
    molsysmt.basic.extract
        Extracting from any supported molecular-system form.
    molsysmt.form.openmm_Topology.copy
        Copying all represented topology data through this builder.

    Examples
    --------
    >>> from openmm import app
    >>> source = app.Topology()
    >>> group = source.addResidue('LIG', source.addChain('A'))
    >>> nitrogen = source.addAtom('N', app.element.nitrogen, group, formalCharge=1)
    >>> oxygen = source.addAtom('O', app.element.oxygen, group)
    >>> result = extract(source, atom_indices=[1])
    >>> [(atom.index, atom.name, atom.formalCharge) for atom in result.atoms()]
    [(0, 'O', None)]

    .. admonition:: User guide

       See :ref:`Tutorial_Form_openmm_Topology` and :ref:`Tutorial_Extract`.

    .. versionadded:: 1.0.0
    """

    from openmm.app import Topology

    topology = item.topology if hasattr(item, "topology") else item
    all_atoms = is_all(atom_indices)
    if all_atoms and not copy_if_all:
        return item

    selected = None if all_atoms else set(atom_indices)
    new_item = Topology()
    new_atoms = {}
    for chain in topology.chains():
        new_chain = new_item.addChain(chain.id) if all_atoms else None
        for group in chain.residues():
            new_group = (
                new_item.addResidue(
                    group.name, new_chain, group.id, group.insertionCode
                )
                if all_atoms
                else None
            )
            for atom in group.atoms():
                if all_atoms or atom.index in selected:
                    if new_chain is None:
                        new_chain = new_item.addChain(chain.id)
                    if new_group is None:
                        new_group = new_item.addResidue(
                            group.name, new_chain, group.id, group.insertionCode
                        )
                    new_atoms[atom] = new_item.addAtom(
                        atom.name,
                        atom.element,
                        new_group,
                        atom.id,
                        formalCharge=atom.formalCharge,
                    )
    for bond in topology.bonds():
        if bond[0] in new_atoms and bond[1] in new_atoms:
            new_item.addBond(
                new_atoms[bond[0]], new_atoms[bond[1]], type=bond.type, order=bond.order
            )
    if hasattr(topology, "getPeriodicBoxVectors"):
        new_item.setPeriodicBoxVectors(topology.getPeriodicBoxVectors())
    elif hasattr(item, "getPeriodicBoxVectors"):
        new_item.setPeriodicBoxVectors(item.getPeriodicBoxVectors())
    return new_item
