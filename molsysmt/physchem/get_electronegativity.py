from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np


@arg_digest()
def get_electronegativity(molecular_system, element='atom', selection='all',
                          definition='pauling', syntax='MolSysMT', skip_digestion=False):
    """
    Electronegativity for each selected atom.

    Returns a tabulated per-element electronegativity for every selected atom,
    looked up from the requested scale. The value is dimensionless.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'atom'}, default 'atom'
        Hierarchical element for which electronegativity is returned. Only
        ``'atom'`` is supported, since electronegativity is a per-element
        property and is not meaningfully aggregated to coarser levels.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of atoms to include in the output.
    definition : {'pauling'}, default 'pauling'
        Electronegativity scale to use. ``'pauling'`` returns the Pauling-scale
        electronegativity for each element.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    quantity
        Electronegativity as a dimensionless PyUnitWizard quantity, shape
        ``(n_atoms,)``. Elements with no tabulated value (noble gases He/Ne/Ar,
        several f-block and super-heavy elements) and the neutral dummy elements
        ``Du``/``X`` return ``NaN``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.

    Notes
    -----
    The Pauling values can be regenerated from the ``mendeleev`` package, like
    the other physchem atom tables.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get
    from molsysmt.physchem.atoms.electronegativity import units

    if definition == 'pauling':
        from molsysmt.physchem.atoms.electronegativity import pauling as values
    else:
        raise NotImplementedMethodError()

    atom_types = get(molecular_system, element='atom', selection=selection, atom_type=True)

    output = []
    for ii in atom_types:
        var_aux = values[ii.capitalize()]
        output.append(np.nan if var_aux is None else var_aux)

    output = puw.quantity(np.array(output, dtype=float), units)

    return output
