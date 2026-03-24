from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def get_atomic_radius(molecular_system, element='atom', selection='all', definition='vdw', syntax='MolSysMT',
                      skip_digestion=False):
    """
    Atomic radius for each selected atom.

    Returns a tabulated radius value for each atom based on its element type
    and the requested radius definition (e.g. van der Waals radius).  Values
    are returned as a PyUnitWizard quantity in nm.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'atom'}, default 'atom'
        Hierarchical element for which the radius is returned.  Currently
        only ``'atom'`` level is meaningful.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of atoms to include in the output.
    definition : {'vdw'}, default 'vdw'
        Radius definition to use.  ``'vdw'`` returns the van der Waals radius
        for each element.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    quantity
        Atomic radii as a PyUnitWizard quantity in nm.
        Shape: ``(n_atoms,)``.

    Raises
    ------
    NotImplementedError
        If an unsupported ``definition`` is requested.

    Notes
    -----
    Van der Waals radii are sourced from standard reference tables covering
    all elements of the periodic table.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get
    from molsysmt.physchem.atoms.radius import units

    if definition=='vdw':
        from molsysmt.physchem.atoms.radius import vdw as values
    else:
        raise NotImplementedError()


    atom_types = get(molecular_system, element='atom', selection=selection, atom_type=True)

    output = []

    for ii in atom_types:
        var_aux = values[ii.capitalize()]
        output.append(var_aux)

    output = puw.quantity(np.array(output), units)

    return output

