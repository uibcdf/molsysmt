from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import make_coordinates_like
import numpy as np

def get_rank_3_XYZ(item):
    """
    Getting rank 3 XYZ from form XYZ.

    Parameters
    ----------
    item : XYZ
        Source item in XYZ form.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    try:
        return make_coordinates_like(item, standardized=False)
    except Exception:
        raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.form.XYZ.get_rank_3_XYZ")