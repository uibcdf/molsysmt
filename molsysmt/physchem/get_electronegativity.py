import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError


@arg_digest()
def get_electronegativity(
    molecular_system,
    element="atom",
    selection="all",
    definition="pauling",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting Pauling electronegativity for a selected atom population.

    Returns a tabulated per-element electronegativity for every selected atom,
    looked up from the requested scale. The value is dimensionless.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='atom'
        Only 'atom' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : object, default='pauling'
        Published scale used for the selected population.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Electronegativity as a dimensionless PyUnitWizard quantity, shape
        ``(n_atoms,)``. Elements with no tabulated value (noble gases He/Ne/Ar,
        several f-block and super-heavy elements) and the neutral dummy elements
        ``Du``/``X`` return ``NaN``.


    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Selection strings are resolved with the requested syntax on the atom
    axis. Explicit atom indices retain order and repetitions; an empty atom
    selection returns a length-zero quantity. Other element levels are rejected,
    rather than silently interpreted as atom indices. No aggregate is inferred.

    The Pauling values can be regenerated from the ``mendeleev`` package, like
    the other physchem atom tables.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_electronegativity(molsys, element='atom', selection=[2, 0, 2])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_electronegativity` for selection, supported scope and reference definitions.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "atom":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["atom"],
            caller="molsysmt.physchem.get_electronegativity",
        )

    from molsysmt.physchem.atoms.electronegativity import units

    if definition == "pauling":
        from molsysmt.physchem.atoms.electronegativity import pauling as values
    else:
        raise NotImplementedMethodError()

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
        output.append(np.nan if var_aux is None else var_aux)

    output = puw.quantity(np.array(output, dtype=float), units)

    return output
