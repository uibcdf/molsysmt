from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
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
        Molecular system in any supported MolSysMT format.
    element : str, default='atom'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : object, default='vdw'
        Argument definition.
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
    NotImplementedError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Van der Waals radii are sourced from standard reference tables covering
    all elements of the periodic table. When using ``definition='protor'``, standard
    ProtOr radii are assigned to protein heavy atoms, falling back to element
    defaults where applicable.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get
    from molsysmt.physchem.atoms.radius import units

    if definition == 'protor':
        from molsysmt.physchem.atoms.protor import get_protor_vdw_radius
        return get_protor_vdw_radius(molecular_system, selection=selection, syntax=syntax,
                                     skip_digestion=skip_digestion)

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

