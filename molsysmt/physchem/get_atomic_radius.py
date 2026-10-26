import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError


@arg_digest()
def get_atomic_radius(
    molecular_system,
    element="atom",
    selection="all",
    definition="vdw",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting tabulated radii for a selected atom population.

    Returns a tabulated radius value for each atom based on its element type
    and the requested radius definition (e.g. van der Waals radius).  Values
    are returned as a PyUnitWizard quantity in nm.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='atom'
        Only 'atom' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : str, default='vdw'
        Reference dataset used to assign the requested physical property.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Atomic radii as a PyUnitWizard quantity in nm.
        Shape: ``(n_atoms,)``.


    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Selection strings are resolved with the requested syntax on the atom
    axis. Explicit atom indices retain order and repetitions; an empty atom
    selection returns a length-zero quantity. Other element levels are rejected,
    rather than silently interpreted as atom indices. No aggregate is inferred.

    Van der Waals radii are sourced from standard reference tables covering
    all elements of the periodic table. When using ``definition='protor'``, standard
    ProtOr radii are assigned to protein heavy atoms, falling back to element
    defaults where applicable.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_atomic_radius(molsys, element='atom', selection=[2, 0, 2])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_atomic_radius` for selection, supported scope and reference definitions.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "atom":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["atom"],
            caller="molsysmt.physchem.get_atomic_radius",
        )

    from molsysmt.physchem.atoms.radius import units

    if definition == "protor":
        from molsysmt.physchem.atoms.protor import get_protor_vdw_radius

        return get_protor_vdw_radius(
            molecular_system,
            selection=selection,
            syntax=syntax,
            skip_digestion=skip_digestion,
        )

    if definition == "vdw":
        from molsysmt.physchem.atoms.radius import vdw as values
    else:
        raise NotImplementedError()

    atom_types = get(
        molecular_system,
        element="atom",
        selection=selection,
        atom_type=True,
        syntax=syntax,
    )

    output = []

    for ii in atom_types:
        var_aux = values[ii.capitalize()]
        output.append(var_aux)

    output = puw.quantity(np.array(output), units)

    return output
