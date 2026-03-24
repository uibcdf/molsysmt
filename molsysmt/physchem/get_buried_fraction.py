from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest()
def get_buried_fraction(molecular_system, element='group', selection='all', definition='janin', syntax='MolSysMT',
                        skip_digestion=False):
    """
    Fraction of residues observed in a buried environment.

    Returns a tabulated molar fraction value representing how frequently each
    residue type is found in a buried (solvent-inaccessible) environment in a
    reference dataset of folded proteins.  Values are looked up from a static
    scale indexed by residue name.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'group'}, default 'group'
        Hierarchical element for which the buried fraction is returned.
        Currently only ``'group'`` (i.e. residue) is supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of groups to include in the output.
    definition : {'janin'}, default 'janin'
        Buried-fraction scale to use.  Currently the only supported scale is
        ``'janin'``, which reports the molar fraction (%) of each residue
        type among 2001 buried residues.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    list of float
        Buried fraction values (in %) for each selected group, in the same
        order as the selection.  Length ``n_groups``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.

    Notes
    -----
    The ``'janin'`` scale reports the molar fraction (%) of each amino acid
    among 2001 buried residues from a structural database, as described in:

        Janin J. *Nature* 277:491–492 (1979).

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'janin':
        from .groups.buried_fraction import janin as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, group_name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    return output

