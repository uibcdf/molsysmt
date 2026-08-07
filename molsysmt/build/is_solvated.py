from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest()
def is_solvated(molecular_system, skip_digestion=False):
    """
    Check whether a molecular system is solvated with an explicit solvent box.

    A molecular system is considered solvated when it contains water molecules and
    has a periodic box, with a water number density above a physically meaningful
    threshold (> 15 molecules per nm³, consistent with liquid water at ambient
    conditions).

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    skip_digestion : bool, default False
        If True, argument digestion is skipped (intended for internal use).

    Returns
    -------
    bool
        True if the system contains water molecules inside a periodic box with
        a water number density greater than 15 molecules/nm³, False otherwise.

    Notes
    -----
    The number density threshold of 15 molecules/nm³ is well below the density of
    liquid water (approximately 33 molecules/nm³ at 300 K) but above values typical
    of gas-phase or vacuum simulations, making it a reliable discriminator for
    explicit solvation.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    output = False

    n_waters, volume = get(molecular_system, element='system', n_waters=True, box_volume=True, skip_digestion=True)

    if (n_waters>0) and (volume is not None):

        density_number = puw.get_value((n_waters/volume), to_unit='1/nm**3')

        if (density_number)>15:

            output = True

    return output

