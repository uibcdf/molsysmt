from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
import numpy as np

@arg_digest()
def get_area_buried(molecular_system, element='group', selection='all', definition='rose', skip_digestion=False):
    """
    Average area buried per residue group upon protein folding.

    Returns a tabulated value (in Å²) representing the average surface area
    buried when each residue transfers from a standard (extended chain) state
    to the folded protein interior.  Values are looked up from a static scale
    indexed by residue name.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'group'}, default 'group'
        Hierarchical element for which buried area is returned.  Currently
        only ``'group'`` (i.e. residue) is supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of groups to include in the output.
    definition : {'rose'}, default 'rose'
        Buried-area scale to use.  Currently the only supported scale is
        ``'rose'``, taken from Rose et al. (1985).
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    numpy.ndarray
        1-D array of shape ``(n_groups,)`` with buried area values in Å².

    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.

    Notes
    -----
    The ``'rose'`` scale reports the average area buried on transfer from a
    standard state to the folded protein, as tabulated for the 20 standard
    amino acids in:

        Rose G.D., Geselowitz A.R., Lesser G.J., Lee R.H., Zehfus M.H.
        *Science* 229:834–838 (1985).

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'rose':
        from .groups.area_buried import rose as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(group_table_value(values, ii))

    output = np.array(output)

    return output

