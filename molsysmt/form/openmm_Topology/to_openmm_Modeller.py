from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from openmm.Topology to openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    .. versionadded:: 1.0.0
    """

    from . import extract
    from molsysmt import pyunitwizard as puw
    from openmm.app import Modeller

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    positions = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    tmp_item = Modeller(tmp_item, positions)

    return tmp_item

