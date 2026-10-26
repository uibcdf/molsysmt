import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_volume(
    molecular_system, selection="all", syntax="MolSysMT", definition="grantham"
):
    """
    Getting Grantham reference volume descriptors for selected groups.

    Returns a tabulated volume value for each selected residue group, looked
    up from one of the published amino-acid volume scales.  Volume provides a
    measure of steric bulk of the amino acid side chain and is used in
    evolutionary distance metrics.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    definition : str, default='grantham'
        Identifier of the published reference table to query.

    Returns
    -------
    numpy.ndarray
        1-D array of shape ``(n_groups,)`` with volume values for the
        selected residues (dimensionless relative units as defined by the
        scale).


    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Numeric group indices retain order and repetitions. Empty selections
    return the same container with length zero. The existing reference table
    and numerical values are unchanged; this query does not calculate a
    conformational geometric surface or volume, prepare chemistry or assign
    a chemical state. Unknown non-placeholder groups retain explicit errors.
    String selections use the requested syntax. Optional selection languages
    require their provider; the ordinary default remains MolSysMT.

    The ``'grantham'`` scale reports side-chain volumes as part of the
    composite physicochemical distance between amino acids defined in:

        Grantham R. *Science* 185:862–864 (1974).


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_volume(molsys, selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_volume` for reference values and selections.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == "grantham":
        from .groups.volume import grantham as values
    else:
        raise NotImplementedMethodError()

    group_types = get(
        molecular_system,
        element="group",
        selection=selection,
        syntax=syntax,
        name=True,
    )

    output = []

    for ii in group_types:
        output.append(
            group_table_value(
                values, ii, table="volume", caller="molsysmt.physchem.get_volume"
            )
        )

    output = np.array(output)

    return output
