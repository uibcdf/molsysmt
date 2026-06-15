from molsysmt._private.arg_digestion import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
from molsysmt._private.smonitor import NotImplementedMethodError
import numpy as np

@arg_digest()
def get_volume(molecular_system, selection='all', syntax='MolSysMT', definition='grantham'):
    """
    Side-chain volume per residue group from a reference scale.

    Returns a tabulated volume value for each selected residue group, looked
    up from one of the published amino-acid volume scales.  Volume provides a
    measure of steric bulk of the amino acid side chain and is used in
    evolutionary distance metrics.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of groups to include in the output.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    definition : {'grantham'}, default 'grantham'
        Volume scale to use.  Currently the only supported scale is
        ``'grantham'``, which tabulates side-chain volumes (in arbitrary
        units) for the 20 standard amino acids.

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
    The ``'grantham'`` scale reports side-chain volumes as part of the
    composite physicochemical distance between amino acids defined in:

        Grantham R. *Science* 185:862–864 (1974).

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'grantham':
        from .groups.volume import grantham as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, syntax='MolSysMT', name=True)

    output = []

    for ii in group_types:
        output.append(group_table_value(values, ii))

    output = np.array(output)

    return output

